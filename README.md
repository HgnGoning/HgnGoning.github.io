# TTDB 博客

一个极简但有创意的个人博客，基于 Jekyll 构建，托管于 GitHub Pages。

## 本地预览

### 前置要求

- Ruby 2.7 或更高版本
- RubyGems
- Bundler

### 安装步骤

```bash
# 安装依赖
bundle install

# 启动本地服务器
bundle exec jekyll serve

# 在浏览器访问
# http://localhost:4000
```

## GitHub Pages 部署

### 方法一：创建仓库

1. 在 GitHub 上创建新仓库：
   - 仓库名可以是 `blog` 或任意名称
   - 如果想使用 `https://hgngoning.github.io` 作为域名，仓库名应为 `hgngoning.github.io`

2. 推送代码到 GitHub：
   ```bash
   git init
   git add .
   git commit -m "Initial commit: TTDB blog setup"
   git branch -M main
   git remote add origin https://github.com/HgnGoning/<仓库名>.git
   git push -u origin main
   ```

3. 启用 GitHub Pages：
   - 进入仓库 Settings → Pages
   - Source 选择 `Deploy from a branch`
   - Branch 选择 `main`，目录选择 `/ (root)`
   - 点击 Save

4. 等待几分钟后访问：
   - `https://hgngoning.github.io/blog`（如果仓库名是 blog）
   - 或 `https://hgngoning.github.io`（如果仓库名是 hgngoning.github.io）

### 方法二：GitHub Actions 自动部署

如果需要更多自定义，可以创建 `.github/workflows/jekyll.yml`：

```yaml
name: Build and deploy Jekyll site

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true

      - run: bundle exec jekyll build

      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./_site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    steps:
      - uses: actions/deploy-pages@v4
```

## 写作指南

### 创建新文章

在 `_posts` 目录下创建文件，命名格式为 `YYYY-MM-DD-title.md`：

```markdown
---
layout: post
title: "文章标题"
date: 2026-03-20
categories: [技术]
tags: [Jekyll, 博客]
---

文章内容...
```

### 文章分类

- `技术` - 技术相关文章
- `生活` - 生活随笔
- `其他` - 其他内容

### Markdown 语法

支持标准 Markdown 语法，以及：
- 代码高亮
- 表格
- 任务列表
- 数学公式（需要额外配置）

## 自定义

### 修改站点信息

编辑 `_config.yml` 文件：

```yaml
title: TTDB
description: 一个极简但有创意的个人博客
author: HgnGoning
```

### 修改样式

样式文件位于 `_sass` 目录：
- `_variables.scss` - 颜色、字体变量
- `_base.scss` - 基础样式
- `_layout.scss` - 布局样式
- `_components.scss` - 组件样式
- `_syntax.scss` - 代码高亮
- `_animations.scss` - 动画效果

## 许可证

MIT License
