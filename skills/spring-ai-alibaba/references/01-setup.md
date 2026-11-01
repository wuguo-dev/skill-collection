# 版本、依赖与模型

## 版本决策

2026-11-01 来源快照：

| 证据 | SAA | Spring AI | Extensions | Boot |
| --- | --- | --- | --- | --- |
| 官网版本表 | 1.1.2.0 | 1.1.2 | 1.1.2.1 或 1.1.2.0 | 3.5.x |
| 正式发布 POM | 1.1.2.2 | 1.1.2 | 1.1.2.2 | 3.5.8 |
| 预发行 POM | 2.0.0-M1.1 | 2.0.0-M1 | 2.0.0-M1.1 | 4.0.0 |

核对时 Latest 为 `v1.1.2.2`，`v1.1.2.1` 发布说明要求改用修正版。Quick-start 同页混有 `1.1.2.0` 和 `1.1.2.1`。以上依据：[版本表](https://java2ai.com/docs/versions/)、[发布记录](https://github.com/alibaba/spring-ai-alibaba/releases)、[正式 POM](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/pom.xml)、[预发行 POM](https://github.com/alibaba/spring-ai-alibaba/blob/v2.0.0-M1.1/pom.xml)。这不是永不过期的推荐版本。

[入门前置条件](https://java2ai.com/docs/quick-start/)为 JDK 17+、Maven 3.8+。保持既有工程 JDK；Boot 4.x 工程先做隔离兼容验证，不能据预发行用了 Boot 4.0.0 就保证 Boot 4.1.x 兼容，也不擅自降级业务工程。

## Maven 组合

以下是固定稳定线的依赖片段；沿用工程父 POM 与 Boot 管理，先检查已有 dependencyManagement。SAA BOM 不自动管理其余所有模块。[SAA BOM 源码](https://github.com/alibaba/spring-ai-alibaba/blob/v1.1.2.2/spring-ai-alibaba-bom/pom.xml)

```xml
<properties>
    <saa.version>1.1.2.2</saa.version>
    <spring-ai.version>1.1.2</spring-ai.version>
    <saa-extensions.version>1.1.2.2</saa-extensions.version>
</properties>
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.alibaba.cloud.ai</groupId>
            <artifactId>spring-ai-alibaba-bom</artifactId>
            <version>${saa.version}</version>
            <type>pom</type><scope>import</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.ai</groupId>
            <artifactId>spring-ai-bom</artifactId>
            <version>${spring-ai.version}</version>
            <type>pom</type><scope>import</scope>
        </dependency>
        <dependency>
            <groupId>com.alibaba.cloud.ai</groupId>
            <artifactId>spring-ai-alibaba-extensions-bom</artifactId>
            <version>${saa-extensions.version}</version>
            <type>pom</type><scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
<dependencies>
    <dependency>
        <groupId>com.alibaba.cloud.ai</groupId>
        <artifactId>spring-ai-alibaba-agent-framework</artifactId>
    </dependency>
    <dependency>
        <groupId>com.alibaba.cloud.ai</groupId>
        <artifactId>spring-ai-alibaba-starter-dashscope</artifactId>
    </dependency>
</dependencies>
```

使用工程 Maven wrapper 或现有 Maven 执行 `dependency:tree` 与 `help:effective-pom`，检查 SAA、Spring AI、Spring 与 Reactor 混版。输出只留本地，分享前脱敏。Graph 的非模型节点不需要模型 starter；其他提供商用对应 starter，处理多个 ChatModel Bean 的歧义。

## 模型与配置

```yaml
spring:
  ai:
    dashscope:
      api-key: ${AI_DASHSCOPE_API_KEY}
      chat:
        options:
          model: ${AI_DASHSCOPE_MODEL}
```

由运行环境提供 Key 和实际模型 ID，确认地域/端点、模型工具/流式/结构化能力。缺 Key 明确报告配置失败；参数范围以具体模型为准。依据：[Models](https://java2ai.com/docs/frameworks/agent-framework/tutorials/models/)。

优先注入 starter 的 ChatModel；多模型用具名 Bean/Qualifier。手工构造使用 `DashScopeApi.builder().apiKey(...).build()` → `DashScopeChatModel.builder().dashScopeApi(...).build()`。本基线的 `DashScopeChatOptions` 使用 `withModel`、`withTemperature`、`withMaxToken`，不要凭通用参数猜方法。

普通问答的方法体如下，builder 为已有的 `ChatClient.Builder`：

```java
import org.springframework.ai.chat.client.ChatClient;

ChatClient client = builder.build();
String answer = client.prompt().user(userText).call().content();
var textStream = client.prompt().user(userText).stream().content();
```

流返回 Flux，由 HTTP 层处理订阅和取消。ChatClient 的 Advisor 与 ReactAgent 的 Hook 是不同扩展 API。依据：[Spring AI 1.1 ChatClient](https://docs.spring.io/spring-ai/reference/1.1/api/chatclient.html)。
