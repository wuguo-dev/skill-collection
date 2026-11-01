# RAG、多智能体与 Skills

## RAG

| 需求 | 方式 |
| --- | --- |
| 每次先检索再回答 | 两步 RAG |
| Agent 自行决定何时/多次检索 | 检索工具 + Agentic RAG |
| 检索质量判定与回退 | Graph/业务流程实现混合模式 |

已有 SQL、CRM、文档检索先复用。新向量链路才选择 Reader/Parser → splitter → embedding → VectorStore → retriever，核对维度、元数据与重建成本。QuestionAnswerAdvisor/RetrievalAugmentationAdvisor 面向 ChatClient；ReactAgent 用相应检索工具或消息 Hook，不能混用注册方式。依据：[RAG](https://java2ai.com/docs/frameworks/agent-framework/advanced/rag/)。

先授权过滤再检索限量取回。答案带来源、时间和口径；空结果明确缺证据。分别评估召回与引用正确性。检索文本不能改变系统权限。

## 多智能体

| 模式 | API | 场景 |
| --- | --- | --- |
| 固定串行 | SequentialAgent | 先写，再审 |
| 独立并行 | ParallelAgent | 显式合并互不依赖任务 |
| 按需专家路由 | LlmRoutingAgent | 一次决策选择一个或多个专家，必要时并行后合并 |
| 循环协调 | ReactAgent + AgentTool（Supervisor 模式） | 主 Agent 根据专家结果继续调度或结束 |
| 子 Agent 是工具 | AgentTool.getFunctionToolCallback(child) | 主 Agent 按需调用专家 |

SequentialAgent、ParallelAgent、LlmRoutingAgent 在 `com.alibaba.cloud.ai.graph.agent.flow.agent`，AgentTool 在 `com.alibaba.cloud.ai.graph.agent`。各子 Agent 配模型、职责和描述，用 outputKey 命名输出，后续 instruction 以 `{key}` 引用，原输入可用 `{input}`。缺失占位符不能当有效结果。

上下文传播选项的命名以目标 Builder 为准，查 includeContents 与推理内容返回选项的实际签名。只传后续需要的内容；并行明确键冲突和结果合并，Supervisor 有停止预算。依据：[Multi-agent](https://java2ai.com/docs/frameworks/agent-framework/advanced/multi-agent/)、[Agent Tool](https://java2ai.com/docs/frameworks/agent-framework/advanced/agent-tool/)。

**基线与官网差异**：官网的“只路由一个专家”和 `SupervisorAgent` 类示例不能直接当作 v1.1.2.2 的 API。该标签路由实现一次决策可选多个专家，并行执行后合并；官方 Supervisor 模式示例使用 ReactAgent 包裹专家 AgentTool，在主 ReAct 循环中继续决策。不要生成该基线不存在的 SupervisorAgent import。依据：[路由构建策略](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/flow/strategy/RoutingGraphBuildingStrategy.java)、[RoutingNode](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/flow/node/RoutingNode.java)、[SupervisorConfig 示例](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/examples/multiagent-patterns/supervisor/src/main/java/com/alibaba/cloud/ai/examples/multiagents/supervisor/SupervisorConfig.java)。

## SAA 运行时 Skills

这里是应用内 Agent 可读的技能；本技能本身则服务开发助手，安装目录与运行环境分别配置。每个运行时技能子目录至少有带 name/description 的 SKILL.md。装配片段：

```java
import com.alibaba.cloud.ai.graph.agent.ReactAgent;
import com.alibaba.cloud.ai.graph.agent.hook.skills.SkillsAgentHook;
import com.alibaba.cloud.ai.graph.skills.registry.SkillRegistry;
import com.alibaba.cloud.ai.graph.skills.registry.filesystem.FileSystemSkillRegistry;

SkillRegistry registry = FileSystemSkillRegistry.builder()
    .projectSkillsDirectory(trustedSkillsPath)
    .build();
SkillsAgentHook hook = SkillsAgentHook.builder().skillRegistry(registry).build();
ReactAgent agent = ReactAgent.builder()
    .name("knowledge_assistant")
    .model(chatModel)
    .hooks(hook)
    .build();
```

Hook 注入技能列表并注册 read_skill，groupedTools 按技能名绑定工具，按需披露。打包使用 ClasspathSkillRegistry，核对资源解包路径和权限；文件系统同名技能项目级覆盖用户级，避免无意加载未审核目录。

ChatClient/Graph 的 SkillPromptAugmentAdvisor 只注入发现提示，不自动注册 read_skill，需提供读取工具或已配置 Hook 的 Agent 节点。加载技能不等于获得 Shell/Python 权限。依据：[Skills](https://java2ai.com/docs/frameworks/agent-framework/tutorials/skills/)。

## A2A 与 Chat UI

跨进程独立部署/发现才引入 A2aRemoteAgent、AgentCardProvider 和版本匹配的 Nacos/starter；发现不替代认证与资源授权。不要照抄演示密码。MCP 是工具接入，A2A 是远程 Agent 协作，不能只换 URL 互用。[A2A](https://java2ai.com/docs/frameworks/agent-framework/advanced/a2a/)

Chat UI 核对示例的事件协议、后端入口与启动脚本；演示端口不是既有部署要求，不把 Graph toString 直接接 UI。[Agent Chat UI](https://java2ai.com/docs/frameworks/studio/quick-start/)
