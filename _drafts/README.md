# 待办区使用说明

这是博客文章的待处理区域。把你的 Markdown 文档放在这里，然后告诉我处理它们。

## 使用方式

### 1. 写文章

在这个目录下创建 `.md` 文件，直接写内容即可。

### 2. 告诉我处理

写完后告诉我：
- `处理待办区的文章` - 我会自动分析并发布
- `处理 xxx.md，分类为数据库` - 指定分类
- `处理 xxx.md，标签为 Redis,缓存` - 指定标签
- `处理所有文章并推送` - 处理完自动推送到 GitHub

### 3. 文档格式

你可以只写纯内容，不需要 front matter：

```markdown
# 这是标题

正文内容...

## 二级标题

更多内容...
```

或者自己指定 front matter：

```markdown
---
title: 这是标题
date: 2026-03-21
categories: [数据库]
tags: [Redis, 缓存]
---

正文内容...
```

### 4. 图片处理

如果文章中有图片：
- 本地图片：放在 `assets/images/` 目录
- 文章中用相对路径引用：`![描述](../assets/images/图片名.png)`
- 或者直接告诉我图片文件，我帮你处理

## 分类参考

| 分类 | 适用内容 |
|------|----------|
| java基础 | Java 语法、集合、IO、反射、注解 |
| java后端开发 | Spring、MyBatis、微服务 |
| 数据库 | MySQL、Redis、MongoDB |
| 中间件 | RabbitMQ、Kafka、Elasticsearch |
| 大模型 | AI、LangChain4j、Spring AI |
| 项目 | 项目实战、经验总结 |
| 工具 | Git、IDE、效率工具 |
| 生活 | 随笔、感想 |

## 当前待处理文件

（在此目录下的 .md 文件都会被处理）
