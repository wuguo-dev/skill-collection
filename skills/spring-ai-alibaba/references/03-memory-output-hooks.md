# 记忆、输出与扩展

## 数据生命周期

| 数据 | 机制 | 边界 |
| --- | --- | --- |
| 一次执行上下文 | RunnableConfig.context() | 不随 checkpoint 自动恢复 |
| 运行身份/环境 | RunnableConfig metadata | 不当永久授权快照，恢复重新确认 |
| 会话消息和图状态 | OverAllState + saver + threadId | 换线程不自动共享 |
| 跨会话偏好/知识 | Store 的 namespace/key | 不等同于持久化 checkpoint |

依据：[RunnableConfig](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-graph-core/src/main/java/com/alibaba/cloud/ai/graph/RunnableConfig.java)、[长期记忆](https://java2ai.com/docs/frameworks/agent-framework/advanced/memory/)。

MemorySaver 与 MemoryStore 都是进程内实现。跨重启需要实际版本支持的持久化实现，并核对依赖、序列化、初始化和隔离；不能仅换数据库 saver 就声称跨会话长期记忆完成。

同一会话多次调用使用相同 threadId 和一致 Agent/saver 语义；新会话先核验归属。裁剪/摘要遵守 token 预算和消息有效顺序，尤其保留 tool call 与结果配对；摘要不是无损备份。依据：[短期记忆](https://java2ai.com/docs/frameworks/agent-framework/tutorials/memory/)。

## 结构化输出

固定输出类型用 `.outputType(ResultDto.class)`；动态 schema 用 `.outputSchema(...)`。ResultDto 必须可被实际 Jackson 配置处理。已配置 outputType 的 Agent 调用方法体：

```java
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.converter.BeanOutputConverter;

AssistantMessage message = agent.call(userText, config);
BeanOutputConverter<ResultDto> converter = new BeanOutputConverter<>(ResultDto.class);
ResultDto result = converter.convert(message.getText());
// 校验必填字段、范围、枚举和业务规则后再使用。
```

`outputType` 不把 call 返回类型改成 DTO。官网同时描述最终消息 JSON 与状态 `structured_output`；要用后者时查目标实现/运行结果，确认键和类型再读取。`outputKey` 是流程状态输出键，不是 schema。

模型原生约束与工具格式化策略随提供商/版本变化。限制解析失败后的修复次数；合法 JSON 不代表数据真实或满足业务条件。依据：[Structured Output](https://java2ai.com/docs/frameworks/agent-framework/tutorials/structured-output/)。

## 扩展点

| 目的 | API |
| --- | --- |
| 整次 Agent 开始/结束 | AgentHook，BEFORE_AGENT/AFTER_AGENT |
| 每轮模型前后更新状态 | ModelHook，返回状态增量 map |
| 裁剪/替换消息 | MessagesModelHook、AgentCommand、UpdatePolicy |
| 包裹模型调用、动态提示/模型 | ModelInterceptor，调用 handler |
| 包裹工具执行、受控错误处理 | ToolInterceptor，调用 handler |
| ChatClient 调用链 | 上游 Advisor |

按实际 API 指定 HookPositions 并通过 `.hooks(...)`/`.interceptors(...)` 注册，不能只定义 Bean 就假设生效。Hook 的持久状态更新与 Interceptor 的单次请求修改要区分。依据：[Hooks](https://java2ai.com/docs/frameworks/agent-framework/tutorials/hooks/)、[上下文工程](https://java2ai.com/docs/frameworks/agent-framework/advanced/context-engineering/)。

可用 `ModelCallLimitHook.builder().runLimit(5).exitBehavior(ModelCallLimitHook.ExitBehavior.ERROR).build()` 限制循环，包为 `com.alibaba.cloud.ai.graph.agent.hook.modelcalllimit`。次数按业务预算设定，另设工具超时。依据：[Quick-start 调用限制](https://java2ai.com/docs/quick-start/)。

日志仅记录运行编号、模型、耗时、次数和安全错误分类；不打印全部 messages/state/工具参数或 Key。可恢复业务错误给受控反馈；未知错误保留服务端原因，不能全部变成成功工具结果。
