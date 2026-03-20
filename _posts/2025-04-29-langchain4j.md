---
layout: post
title: LangChain4j
date: 2025-04-29
categories: [java后端开发]
tags: [大模型]
---

## 一、入门

LangChain4j 的目标是简化将大语言模型（LLM - Large Language Model）集成到 Java 应用程序中的过程。

### 1、主要功能

- 与大型语言模型和向量数据库的便捷交互 通过统一的应用程序编程接口（API），可以轻松访问所有主要的商业和开源大型语言模型以及向量数据库，使你能够构建聊天机器人、智能助手等应用。
- 专为 Java 打造 借助Spring Boot 集成，能够将大模型集成到Java应用程序中。
- 大型语言模型与 Java 之间实现了双向集成：你可以从 Java 中调用大型语言模型，同时也允许大型语言模型反过来调用你的 Java 代码 智能代理、工具、检索增强生成（RAG） 为常见的大语言模型操作提供了广泛的工具，涵盖从底层的提示词模板创建、聊天记忆管理和输出解析，到智能代理和检索增强生成等高级模式。

### 2、创建SpringBoot测试环境

#### 2.1 新建一个Maven项目

添加如下依赖

```xml
<properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <spring-boot.version>3.2.6</spring-boot.version>
    <knife4j.version>4.3.0</knife4j.version>
    <langchain4j.version>1.0.0-beta3</langchain4j.version>
    <mybatis-plus.version>3.5.11</mybatis-plus.version>
</properties>
<dependencies>
    <!-- web应用程序核心依赖 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <!-- 编写和运行测试用例 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <!-- 前后端分离中的后端接口测试工具 -->
    <dependency>
        <groupId>com.github.xiaoymin</groupId>
        <artifactId>knife4j-openapi3-jakarta-spring-boot-starter</artifactId>
        <version>${knife4j.version}</version>
    </dependency>
</dependencies>
<dependencyManagement>
    <dependencies>
        <!--引入SpringBoot依赖管理清单-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>${spring-boot.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### 3、大语言模型

#### 3.1 语言模型分类

- 按照输入输出分类
  - 文本续写模型（类似输入法联想，一个字一个字的生成）
  - 对话模型（chat多轮会话）
- 按照是否联网分类
  - 离线模型
  - 在线模型

#### 3.2 常用大模型

- OpenAI（ChatGPT）
- Azure OpenAI
- Google Gemini
- Anthropic Claude
- 阿里云通义千问
- 百度文心一言
- 智谱清言

#### 3.3 大模型API标准

- OpenAI API标准：事实上的行业标准
- OneAPI：将各种大模型转为OpenAI标准

### 4、大模型接入LangChain4j

LangChain4j支持多种大模型接入方式：

- OpenAI
- Azure OpenAI
- 阿里云通义千问
- 本地模型（Ollama）

#### 4.1 接入阿里云通义千问

1. 申请API Key
2. 添加依赖

```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-dashscope</artifactId>
    <version>${langchain4j.version}</version>
</dependency>
```

3. 配置模型

```java
@Configuration
public class LLMConfig {

    @Bean
    public ChatLanguageModel chatLanguageModel() {
        return QwenChatModel.builder()
                .apiKey("your-api-key")
                .modelName("qwen-plus")
                .build();
    }
}
```

## 二、AI服务

### 1、AiServices

AiServices 是 LangChain4j 提供的高级 API，用于简化与大语言模型的交互。

```java
interface Assistant {
    String chat(String message);
}

@Test
public void testAiServices() {
    Assistant assistant = AiServices.create(Assistant.class, qwenChatModel);
    String answer = assistant.chat("你好");
    System.out.println(answer);
}
```

### 2、使用ChatMemory实现聊天记忆

使用AIService可以封装多轮对话的复杂性，使聊天记忆功能的实现变得简单

```java
@Test
public void testChatMemory3() {
    //创建chatMemory
    MessageWindowChatMemory chatMemory = MessageWindowChatMemory.withMaxMessages(10);
    //创建AIService
    Assistant assistant = AiServices
        .builder(Assistant.class)
        .chatLanguageModel(qwenChatModel)
        .chatMemory(chatMemory)
        .build();
    //调用service的接口
    String answer1 = assistant.chat("我是环环");
    System.out.println(answer1);
    String answer2 = assistant.chat("我是谁");
    System.out.println(answer2);
}
```

### 3、系统消息

通过系统消息可以设定AI的角色和行为。

```java
interface Assistant {
    @SystemMessage("你是一个专业的Java开发工程师，请用专业的角度回答问题")
    String chat(@UserMessage String message);
}
```

## 三、提示词工程

### 1、提示词模板

使用提示词模板可以动态生成提示词。

```java
interface Assistant {
    @UserMessage("请根据以下要求生成代码：{{requirement}}")
    String generateCode(@V("requirement") String requirement);
}
```

### 2、输出解析

LangChain4j 支持将 AI 输出解析为结构化数据。

```java
interface Assistant {
    @UserMessage("请生成一个用户信息，包含姓名、年龄、邮箱")
    UserInfo generateUserInfo();
}

record UserInfo(String name, int age, String email) {}
```

## 四、RAG（检索增强生成）

### 1、RAG概述

RAG（Retrieval-Augmented Generation）是一种将检索和生成相结合的技术：
1. 将文档进行向量化存储
2. 根据用户问题检索相关文档
3. 将检索结果作为上下文传递给大模型

### 2、向量数据库

常用的向量数据库：
- Milvus
- Pinecone
- Elasticsearch
- Redis

### 3、文档嵌入

```java
EmbeddingModel embeddingModel = new AllMiniLmL6V2EmbeddingModel();

Embedding embedding = embeddingModel.embed("Hello World").content();
```

### 4、文档存储与检索

```java
EmbeddingStore<TextSegment> embeddingStore = new InMemoryEmbeddingStore<>();

// 存储文档
embeddingStore.add(embedding, textSegment);

// 检索文档
List<EmbeddingMatch<TextSegment>> relevant = embeddingStore.findRelevant(embedding, 10);
```

## 五、工具调用

### 1、定义工具

```java
class Tools {
    @Tool("查询当前天气")
    public String getWeather(String city) {
        return city + "今天天气晴朗";
    }
}
```

### 2、注册工具

```java
Assistant assistant = AiServices.builder(Assistant.class)
    .chatLanguageModel(qwenChatModel)
    .tools(new Tools())
    .build();
```

## 六、最佳实践

### 1、错误处理

```java
interface Assistant {
    Result<String> chat(String message);
}

@Test
public void testWithErrorHandling() {
    Result<String> result = assistant.chat("你好");
    if (result.hasError()) {
        System.out.println("Error: " + result.error().getMessage());
    } else {
        System.out.println(result.content());
    }
}
```

### 2、流式输出

```java
interface Assistant {
    TokenStream chatStream(String message);
}

@Test
public void testStreaming() {
    assistant.chatStream("写一首诗")
        .onNext(token -> System.out.print(token))
        .onComplete(response -> System.out.println("\n完成"))
        .onError(Throwable::printStackTrace)
        .start();
}
```

### 3、日志记录

配置日志级别查看详细的请求和响应信息。

```yaml
logging:
  level:
    dev.langchain4j: DEBUG
```
