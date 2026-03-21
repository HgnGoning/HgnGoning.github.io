# TTDB 博客写作指南

## 推荐工作流

### 1. 写文章

在 `_drafts/` 目录下创建 `.md` 文件，直接写内容即可。

**不需要手动添加 front matter**，我会自动处理。

```
F:/paper/Blog/_drafts/我的新文章.md
```

### 2. 告诉我处理

写完后告诉我：

| 命令 | 说明 |
|------|------|
| `处理待办区` | 自动分析所有文章并发布 |
| `处理 xxx.md` | 处理指定文章 |
| `处理 xxx.md，分类为数据库` | 指定分类 |
| `处理 xxx.md，标签为 Redis,缓存` | 指定标签 |
| `处理并推送` | 处理完后自动推送到 GitHub |

### 3. 图片处理

- 图片放在 `assets/images/` 目录
- 命名格式：`YYYY-MM-DD-文章名-序号.png`
- 文章中引用：`![描述](../assets/images/图片名.png)`

---

## 手动方式

如果你想自己处理，可以手动创建文章：

### 文章格式

在 `_posts/` 目录创建文件，命名格式：`YYYY-MM-DD-标题.md`

```markdown
---
layout: post
title: "文章标题"
date: 2026-03-21
categories: [数据库]
tags: [Redis, 缓存]
---

正文内容...
```

### Front Matter 说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `layout` | 是 | 固定填 `post` |
| `title` | 是 | 文章标题 |
| `date` | 是 | 发布日期 `YYYY-MM-DD` |
| `categories` | 否 | 分类 |
| `tags` | 否 | 标签 |

---

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

---

## Markdown 语法

```markdown
# 一级标题
## 二级标题
### 三级标题

**加粗** *斜体*

- 无序列表
- 无序列表

1. 有序列表
2. 有序列表

> 引用

[链接](https://example.com)

![图片](../assets/images/xxx.png)

`行内代码`

```java
// 代码块
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```
```

---

## 本地预览

```bash
cd F:/paper/Blog
bundle exec jekyll serve
```

访问 http://localhost:4000

---

## 目录结构

```
Blog/
├── _drafts/          # 待办区（写文章放这里）
├── _posts/           # 已发布的文章
├── assets/images/    # 图片目录
├── _config.yml       # 博客配置
└── ...
```

---

## 常见问题

### Q: 推送后网站没有更新？

等待 1-2 分钟，GitHub Pages 需要构建时间。

### Q: 文章没有显示？

检查文件名格式：`YYYY-MM-DD-标题.md`

### Q: 图片不显示？

确保路径正确：`../assets/images/图片名.png`
