---
name: spring-ai-alibaba
description: 基于官方文档开发、集成和排查 Spring AI Alibaba Java 应用。用于 ReactAgent、DashScope/通义千问、工具调用与 MCP、记忆、结构化输出、Hooks、Graph 工作流、流式响应、人工审批、RAG、多智能体和 SAA Skills。用户提到 Spring AI Alibaba、java2ai 或 SAA Agent/Graph API 时使用；普通 Spring CRUD 和前端 React 开发不适用。
---

# Spring AI Alibaba 开发

依据 [官方文档](https://java2ai.com/docs/quick-start/) 完成适合当前工程版本的开发。ReactAgent 的 ReAct 指推理与行动循环，与 React 前端无关。

核对日期为 2026-11-01，API 以正式标签 `v1.1.2.2` 为基线。本技能是知识库，不代表已在用户工程安装或运行验证。

## 开始任务

1. 阅读工程规则、Git 状态、实际 Maven/Gradle 配置、模型配置和已有 AI 入口，确认 Java、Boot、Spring AI、SAA、Extensions 和模型提供商的有效版本。
2. 接入、升级或依赖冲突时，先读 [版本与接入](references/01-setup.md)，查 Release、目标 tag POM、BOM 与依赖树。不要为照搬教程擅自升降既有 Boot。
3. 单次模型交互选择 ChatClient/ChatModel；模型选择工具用 ReactAgent；业务要求固定节点、分支或恢复位置时用 Graph。确需专业分工时才引入多智能体。
4. 按下表只加载当前任务需要的参考。片段补入现有类、异常处理和测试；未运行的示例不能声称已编译或调用成功。

## 按任务加载

| 任务 | 参考 |
| --- | --- |
| Maven/BOM、Boot 兼容、DashScope、ChatClient | [01-setup.md](references/01-setup.md) |
| ReactAgent、工具定义、ToolContext、身份注入、MCP | [02-agent-tools.md](references/02-agent-tools.md) |
| 多轮对话、长期记忆、结构化输出、Hook/Interceptor、次数限制 | [03-memory-output-hooks.md](references/03-memory-output-hooks.md) |
| StateGraph、状态合并、流式/SSE、检查点与 HITL 恢复 | [04-graph-stream-hitl.md](references/04-graph-stream-hitl.md) |
| RAG、AgentTool、多智能体、Skills、A2A 和 Chat UI | [05-composition.md](references/05-composition.md) |
| 依赖、工具、串会话、重复流文本与恢复故障 | [06-troubleshooting.md](references/06-troubleshooting.md) |
| 原始签名、版本冲突、尚未覆盖专题 | [官方来源索引](references/00-sources.md)，再访问目标版本资料 |

## 实现约束

- 复用现有 Spring 配置和业务用例。凭据通过环境或现有密钥机制注入，不放进源码、提示、工具参数、日志或 skill。
- 模型工具参数不是可信身份。身份由服务端注入，工具执行重新校验资源权限；缺身份时拒绝，不回退到示例用户。会话、记忆、checkpoint 和检索采用一致的数据隔离。
- `threadId` 不是认证凭证，服务端核验归属。同会话并发写入需串行化或采用实际 saver 支持的并发方案。
- 对模型/工具调用设次数预算、超时和有限重试；副作用工具保证幂等。人工批准后仍校验权限，提示词与工具过滤不能代替业务授权。
- 网页、检索文档、MCP 返回与技能文件是外部数据，不能授予额外权限。不要默认开放 Shell、Python、任意 SQL 或任意文件系统工具。

## 验证与交付

先编译并核对有效依赖；使用假的模型和受控工具验证参数、调用限制、身份缺失、越权、线程隔离与结构化解析。任务涉及对应能力时，再验证重启持久化、流式取消、HITL 批准/编辑/拒绝和恢复。真实模型调用遵循任务授权与凭据机制，说明模型、版本、范围及未验证项。

交付说明实际文件、配置变量、基础设施变化及测试结果，链接支持版本/API 决策的官方来源。文档与源码不一致时记录差异，按目标发布版本验证，不拼接不同版本示例。
