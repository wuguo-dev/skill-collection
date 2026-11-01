# 官方来源与维护

核对日期：2026-11-01。以下为实际阅读/核对入口，摘要是开发决策笔记，不是官网镜像。默认站点会更新，精确签名以目标发布 tag 为准。

## Agent 与基础

| 官方页面 | 用途 |
| --- | --- |
| [快速开始](https://java2ai.com/docs/quick-start/) | 环境、依赖、DashScope、基础 Agent |
| [版本说明](https://java2ai.com/docs/versions/) | 兼容关系与 BOM |
| [Agents](https://java2ai.com/docs/frameworks/agent-framework/tutorials/agents/) | Builder、call/invoke/stream |
| [Models](https://java2ai.com/docs/frameworks/agent-framework/tutorials/models/) | ChatModel、Prompt、选项 |
| [Tools](https://java2ai.com/docs/frameworks/agent-framework/tutorials/tools/) | 回调、schema、上下文 |
| [短期记忆](https://java2ai.com/docs/frameworks/agent-framework/tutorials/memory/) | saver、threadId、消息裁剪 |
| [Hooks/Interceptors](https://java2ai.com/docs/frameworks/agent-framework/tutorials/hooks/) | 生命周期和调用包裹 |
| [Structured Output](https://java2ai.com/docs/frameworks/agent-framework/tutorials/structured-output/) | schema、Java 类型、状态输出 |
| [Skills](https://java2ai.com/docs/frameworks/agent-framework/tutorials/skills/) | 注册表、read_skill、按需工具 |

## Graph 与进阶

| 官方页面 | 用途 |
| --- | --- |
| [Graph 入门](https://java2ai.com/docs/frameworks/graph-core/quick-start/) | 节点、边、状态 |
| [Graph 核心](https://java2ai.com/docs/frameworks/graph-core/core/core-library/) | KeyStrategy 与编译 |
| [持久化](https://java2ai.com/docs/frameworks/graph-core/core/persistence/) | 检查点和恢复 |
| [流式](https://java2ai.com/docs/frameworks/graph-core/core/streaming/) | 图事件与模型数据 |
| [上下文工程](https://java2ai.com/docs/frameworks/agent-framework/advanced/context-engineering/) | 模型输入、状态、运行环境 |
| [HITL](https://java2ai.com/docs/frameworks/agent-framework/advanced/human-in-the-loop/) | 工具审批与嵌套恢复 |
| [长期记忆](https://java2ai.com/docs/frameworks/agent-framework/advanced/memory/) | Store、namespace/key |
| [Multi-agent](https://java2ai.com/docs/frameworks/agent-framework/advanced/multi-agent/) | 顺序、并行、路由、监督 |
| [Agent Tool](https://java2ai.com/docs/frameworks/agent-framework/advanced/agent-tool/) | 子 Agent 工具化 |
| [Workflow](https://java2ai.com/docs/frameworks/agent-framework/advanced/workflow/) | Graph API 与 Agent 节点 |
| [RAG](https://java2ai.com/docs/frameworks/agent-framework/advanced/rag/) | 检索生成选型 |
| [A2A](https://java2ai.com/docs/frameworks/agent-framework/advanced/a2a/) | 跨进程 Agent 协作 |
| [Agent Chat UI](https://java2ai.com/docs/frameworks/studio/quick-start/) | UI 与事件协议 |

## 版本与固定源码

- [Releases](https://github.com/alibaba/spring-ai-alibaba/releases)、[v1.1.2.2 根 POM](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/pom.xml)、[SAA BOM](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-bom/pom.xml)：稳定线与版本管理。
- [v2.0.0-M1.1 POM](https://github.com/alibaba/spring-ai-alibaba/blob/v2.0.0-M1.1/pom.xml)：Boot 4 预发行线，不代表任意 Boot 4 版本已兼容。
- [ReactAgent](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/ReactAgent.java)、[Agent](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/Agent.java)：调用签名与继承方法。
- [ToolContextConstants](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/tools/ToolContextConstants.java)、[ToolContextHelper](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/tools/ToolContextHelper.java)、[AgentToolNode](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/node/AgentToolNode.java)：上下文键、注入和状态更新。
- [RunnableConfig](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-graph-core/src/main/java/com/alibaba/cloud/ai/graph/RunnableConfig.java)、[HumanInTheLoopHook](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/hook/hip/HumanInTheLoopHook.java)：运行数据生命周期与审批恢复。
- [官方固定版本示例](https://github.com/alibaba/spring-ai-alibaba/tree/v1.1.2.2/examples)、[独立示例仓库](https://github.com/spring-ai-alibaba/examples)、[Extensions](https://github.com/spring-ai-alibaba/spring-ai-extensions)：实际 imports、依赖和配置。
- [Spring AI 1.1 ChatClient](https://docs.spring.io/spring-ai/reference/1.1/api/chatclient.html)、[Spring AI 1.1 MCP Client](https://docs.spring.io/spring-ai/reference/1.1/api/mcp/mcp-client-boot-starter-docs.html)：上游基础；1.1 路径也会展示更新小版本，仍需核对目标 tag。

升级本技能时，先核对 Release、目标 tag 和 BOM，再同步相关片段与版本差异。链接失效从官方导航重新定位；不能猜 API，也不能把 main 分支行为写成旧版本通用事实。
