# Graph、流式与人工审批

## Graph 最小闭环

节点返回状态增量，边决定下一节点，KeyStrategy 决定同键合并。先确定 Replace/Append/专用策略，不能依赖并行的最后写入作汇总。以下方法不调用模型或外部服务：

```java
import com.alibaba.cloud.ai.graph.CompiledGraph;
import com.alibaba.cloud.ai.graph.KeyStrategyFactory;
import com.alibaba.cloud.ai.graph.StateGraph;
import com.alibaba.cloud.ai.graph.state.strategy.ReplaceStrategy;
import java.util.Map;
import static com.alibaba.cloud.ai.graph.StateGraph.START;
import static com.alibaba.cloud.ai.graph.StateGraph.END;
import static com.alibaba.cloud.ai.graph.action.AsyncNodeAction.node_async;

public CompiledGraph createGraph() throws Exception {
    KeyStrategyFactory strategies = () -> Map.of("answer", new ReplaceStrategy());
    return new StateGraph(strategies)
        .addNode("prepare", node_async(state -> Map.of("answer", "准备完成")))
        .addEdge(START, "prepare")
        .addEdge("prepare", END)
        .compile();
}
```

使用 `graph.invoke(Map.of(), config)` 并检查 Optional。实际节点实现 NodeAction/NodeActionWithConfig，调用既有业务用例。条件边映射覆盖所有返回值；节点只返回更新键，避免把旧列表全部返回导致 Append 重复。compile 检查结构，不等于业务验证。依据：[Graph 核心](https://java2ai.com/docs/frameworks/graph-core/core/core-library/)、[Workflow](https://java2ai.com/docs/frameworks/agent-framework/advanced/workflow/)。

持久化使用 CompileConfig 的 saver 配置，查目标版本依赖/API。测试同线程恢复、不同线程隔离及重启；不删除真实 checkpoint 掩盖序列化失败。依据：[持久化](https://java2ai.com/docs/frameworks/graph-core/core/persistence/)。

## 流式协议

Agent stream 返回 Flux<NodeOutput>，可能包含节点、Hook、工具、中断与模型事件。先识别 StreamingOutput 与 OutputType，再转换为前端协议：

- `OutputType.AGENT_MODEL_STREAMING` 文本作为增量；`OutputType.AGENT_MODEL_FINISHED` 可能带完整结果，不能重复追加。不要省略枚举名称中的 `AGENT_` 前缀。
- 工具完成、审批中断和错误单独发事件，定义运行 ID 与终止语义；不把所有 toString 当正文。
- thinking/reasoning 单独处理，不默认当答案或全量记录。
- HTTP 层保留取消和错误传播；断开释放下游资源。业务 Service 不自行 subscribe 后立即报告完成。

模型流、Graph 事件流与 SSE 是不同层次。验证首段、顺序、最终全文不重复、断开取消与失败；便捷 streamMessages 等 API 以目标版本为准。依据：[Agents](https://java2ai.com/docs/frameworks/agent-framework/tutorials/agents/)、[Graph 流式](https://java2ai.com/docs/frameworks/graph-core/core/streaming/)。

枚举位于 `com.alibaba.cloud.ai.graph.streaming.OutputType`，工具/Hook 事件分别有 `AGENT_TOOL_FINISHED`、`AGENT_HOOK_FINISHED`。签名依据：[OutputType v1.1.2.2](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-graph-core/src/main/java/com/alibaba/cloud/ai/graph/streaming/OutputType.java)。

## HITL 恢复

配置 `com.alibaba.cloud.ai.graph.agent.hook.hip.HumanInTheLoopHook` 与 ToolConfig：`.approvalOn(真实工具名, ToolConfig.builder().description(...).build())`，注册 hook、saver，调用带受控 threadId。

1. invokeAndGetOutput 返回 InterruptionMetadata 时保存服务端中断记录，向审批者展示脱敏后的操作与参数。
2. 校验审批人权限、会话归属和记录仍待处理。逐项收集批准、编辑或拒绝，不能自动批准。
3. 基于原 node/state 构造新 InterruptionMetadata；复制原 ToolFeedback 保留 ID/name，填写 FeedbackResult。编辑参数重新做 schema/业务权限验证。
4. 同线程使用 `RunnableConfig.builder().threadId(threadId).addHumanFeedback(feedback).build()`；独立 Agent 示例以空字符串恢复，原始 Graph 示例按 API 使用空 Map。
5. 再检查返回值，可能再次中断或失败；业务工具实际成功后才记成功。

v1.1.2.2 按 name+id 匹配每个待审反馈，result 不能为空；缺项可再次中断。通用 resume()/withResume() 填入字符串占位，不能代替 HITL 的 InterruptionMetadata。

嵌套 Agent 在父图层恢复，父图 CompileConfig 与子 Agent 使用相应共享 saver 配置。恢复时重新附带经过核验的运行身份，不信任客户端整份 state；副作用工具设计幂等，防止反馈重放/恢复重试重复执行。

依据：[HITL 教程](https://java2ai.com/docs/frameworks/agent-framework/advanced/human-in-the-loop/)、[Hook 校验实现](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/hook/hip/HumanInTheLoopHook.java)、[RunnableConfig](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-graph-core/src/main/java/com/alibaba/cloud/ai/graph/RunnableConfig.java)。
