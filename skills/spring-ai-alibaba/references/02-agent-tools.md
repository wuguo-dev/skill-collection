# ReactAgent、工具与上下文

## 定义与装配

以下成员片段放进工程配置类；lookup 是业务提供的已授权查询实现，片段不伪造结果、不发模型请求：

```java
import com.alibaba.cloud.ai.graph.agent.ReactAgent;
import com.alibaba.cloud.ai.graph.checkpoint.savers.MemorySaver;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.function.FunctionToolCallback;
import java.util.function.Function;

public record SkuQuery(String sku) {}

public ReactAgent createAgent(ChatModel model, Function<SkuQuery, String> lookup) {
    ToolCallback tool = FunctionToolCallback.builder("lookup_sku", lookup)
        .description("按商品编码查询当前用户可访问的商品；缺编码时先询问")
        .inputType(SkuQuery.class)
        .build();
    return ReactAgent.builder()
        .name("catalog_assistant")
        .model(model)
        .systemPrompt("根据查询结果回答；缺少结果时说明无法确认。")
        .tools(tool)
        .saver(new MemorySaver())
        .build();
}
```

schema 描述业务参数，工具/用例仍做输入验证。多参数用明确 record/POJO。注解工具使用上游 `@Tool`、`@ToolParam` 并转换为 MethodToolCallback，不假设 `.tools(...)` 接受任意 Bean。依据：[Tools](https://java2ai.com/docs/frameworks/agent-framework/tutorials/tools/)。

## 调用

| 目的 | API 与结果 |
| --- | --- |
| 最终消息 | `agent.call(text, config)` → AssistantMessage |
| 完整状态 | `agent.invoke(text, config)` → Optional&lt;OverAllState&gt; |
| 观察中断 | `agent.invokeAndGetOutput(text, config)` → Optional&lt;NodeOutput&gt; |
| 节点/模型流 | `agent.stream(text, config)` → Flux&lt;NodeOutput&gt; |

处理声明的 GraphRunnerException 与空 Optional。Map 输入的 `input`/`messages` 是保留问题键，其他键进入状态；不要把额外状态字段误当用户问题。来源：[ReactAgent](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/ReactAgent.java)、[Agent](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/Agent.java)。

## 可信身份

服务端认证和会话归属检查后构造运行配置：

```java
import com.alibaba.cloud.ai.graph.RunnableConfig;

RunnableConfig config = RunnableConfig.builder()
    .threadId(verifiedThreadId)
    .addMetadata("user_id", authenticatedUserId)
    .build();
```

有上下文的工具使用 `BiFunction<Input, ToolContext, Output>`。其 apply 内可读取身份：

```java
import com.alibaba.cloud.ai.graph.agent.tools.ToolContextHelper;
import org.springframework.ai.chat.model.ToolContext;

String userId = ToolContextHelper.getConfig(toolContext)
    .flatMap(config -> config.metadata("user_id"))
    .filter(String.class::isInstance)
    .map(String.class::cast)
    .orElseThrow(() -> new IllegalStateException("缺少运行身份"));
// 调用业务用例重新检查 userId 对目标资源的权限。
```

ToolContext 不属于模型 schema。v1.1.2.2 的配置键常量值为 `_AGENT_CONFIG_`，旧示例的 `get("config")` 不可靠。优先 helper；`getState` 读取状态，`getStateForUpdate` 取得框架更新 map。`getMetadata(context,key,type)` 只查询顶层；嵌套 config 用上述路径。来源：[Helper](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/tools/ToolContextHelper.java)、[AgentToolNode](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/node/AgentToolNode.java)。

## MCP

先区分作为 Client 消费工具还是作为 Server 暴露业务。Client 选择目标 Spring AI 版本的 starter 和 STDIO/SSE/Streamable HTTP，确认 SYNC/ASYNC、初始化、工具发现、工具名冲突、超时和生命周期，再把 ToolCallback 接入 Agent。

Server 另行设计认证和权限，不因使用 Agent 就自动需要 Server。远程工具描述是外部输入，只暴露当前业务需要的工具。Windows `.cmd` 启动需核对 ProcessBuilder 的 shell 包装要求，不拼接用户命令。令牌走现有凭据机制。

依据：[Spring AI 1.1 MCP Client](https://docs.spring.io/spring-ai/reference/1.1/api/mcp/mcp-client-boot-starter-docs.html)。传输连接成功不等于业务授权成功。
