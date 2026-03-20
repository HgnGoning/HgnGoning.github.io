# TTDB 博客写作指南

## 快速开始

### 写一篇新文章

1. 在 `_posts/` 目录下创建新文件
2. 文件命名格式：`YYYY-MM-DD-标题.md`（如 `2026-03-20-my-first-post.md`）
3. 在文件开头添加 Front Matter：

```markdown
---
layout: post
title: "文章标题"
date: 2026-03-20
categories: [分类名]
tags: [标签1, 标签2]
---

这里写文章正文...
```

### 更新网站

```bash
# 1. 进入博客目录
cd F:/paper/Blog

# 2. 提交更改
git add .
git commit -m "添加新文章：xxx"

# 3. 推送到 GitHub
git push
```

推送后等待 1-2 分钟，访问 https://hgngoning.github.io 查看更新。

---

## 文章格式

### Front Matter 说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `layout` | 是 | 固定填 `post` |
| `title` | 是 | 文章标题 |
| `date` | 是 | 发布日期，格式 `YYYY-MM-DD` |
| `categories` | 否 | 分类，如 `[技术]` 或 `[技术, Java]` |
| `tags` | 否 | 标签，如 `[Redis, 数据库]` |

### Markdown 基础语法

```markdown
# 一级标题
## 二级标题
### 三级标题

**加粗文本**
*斜体文本*

- 无序列表项 1
- 无序列表项 2

1. 有序列表项 1
2. 有序列表项 2

> 引用文本

[链接文字](https://example.com)

![图片描述](图片路径)
```

### 代码块

```markdown
行内代码：`code`

代码块：
```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
\```
（去掉反引号前的反斜杠）
```

支持的语言标记：`java`, `python`, `javascript`, `sql`, `bash`, `json`, `xml`, `yaml` 等

---

## 分类建议

| 分类名 | 适用内容 |
|--------|----------|
| `java基础` | Java 语法、集合、IO、反射等 |
| `java后端开发` | Spring、MyBatis、微服务等 |
| `数据库` | MySQL、Redis、MongoDB 等 |
| `中间件` | RabbitMQ、Kafka、Elasticsearch 等 |
| `项目` | 项目实战、经验总结 |
| `工具` | Git、IDE、效率工具 |
| `生活` | 随笔、感想 |

---

## 本地预览

如果已安装 Ruby 和 Jekyll：

```bash
cd F:/paper/Blog
bundle exec jekyll serve
```

然后访问 http://localhost:4000

---

## 图片处理

### 方法一：放在 assets/images/ 目录

1. 将图片放入 `assets/images/` 目录
2. 在文章中引用：

```markdown
![图片描述]({{ "/assets/images/图片名.png" | relative_url }})
```

### 方法二：使用图床

上传到图床（如 GitHub、阿里云 OSS、七牛云等），直接使用外链：

```markdown
![图片描述](https://图床地址/图片.png)
```

---

## 常见问题

### Q: 推送后网站没有更新？

等待 1-2 分钟，GitHub Pages 需要时间构建。可以在 GitHub 仓库的 **Actions** 页面查看构建状态。

### Q: 文章没有显示？

检查：
1. 文件名格式是否正确（`YYYY-MM-DD-title.md`）
2. Front Matter 格式是否正确
3. `layout: post` 是否填写

### Q: 中文显示乱码？

确保文件保存为 **UTF-8 编码**。

### Q: 如何修改博客配置？

编辑 `_config.yml` 文件，修改后需要推送才能生效。

---

## 快捷命令

```bash
# 查看本地更改状态
git status

# 查看提交历史
git log --oneline -5

# 撤销未提交的更改
git checkout -- 文件名

# 查看远程仓库地址
git remote -v
```

---

## 参考资源

- [Markdown 语法指南](https://markdown.com.cn/basic-syntax/)
- [Jekyll 官方文档](https://jekyllrb.com/docs/)
- [GitHub Pages 文档](https://docs.github.com/zh/pages)
