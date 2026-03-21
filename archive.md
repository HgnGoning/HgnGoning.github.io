---
layout: page
title: 归档
permalink: /archive/
description: 文章归档
---

<!-- 分类导航 -->
<nav class="archive-nav">
  <a href="#java基础" class="archive-nav-item">Java基础</a>
  <a href="#java后端开发" class="archive-nav-item">后端开发</a>
  <a href="#数据库" class="archive-nav-item">数据库</a>
  <a href="#中间件" class="archive-nav-item">中间件</a>
  <a href="#大模型" class="archive-nav-item">大模型</a>
  <a href="#算法" class="archive-nav-item">算法</a>
  <a href="#项目" class="archive-nav-item">项目</a>
  <a href="#其他" class="archive-nav-item">其他</a>
</nav>

{% assign all_posts = site.posts | sort: "date" | reverse %}

<!-- Java基础 -->
<section class="archive-section" id="java基础">
  <h2 class="archive-category-title">Java基础</h2>
  <p class="archive-category-desc">Java 语法、集合、IO、反射、注解等基础知识</p>
  <ul class="archive-list">
    {% for post in all_posts %}
      {% if post.categories contains "java基础" %}
      <li class="archive-item">
        <span class="archive-date">{{ post.date | date: "%Y-%m-%d" }}</span>
        <a href="{{ post.url | relative_url }}" class="archive-title">{{ post.title }}</a>
        <div class="archive-tags">
          {% for tag in post.tags limit:3 %}
          <span class="archive-tag">{{ tag }}</span>
          {% endfor %}
        </div>
      </li>
      {% endif %}
    {% endfor %}
  </ul>
</section>

<!-- Java后端开发 -->
<section class="archive-section" id="java后端开发">
  <h2 class="archive-category-title">Java后端开发</h2>
  <p class="archive-category-desc">Spring、MyBatis、微服务等后端技术</p>
  <ul class="archive-list">
    {% for post in all_posts %}
      {% if post.categories contains "java后端开发" %}
      <li class="archive-item">
        <span class="archive-date">{{ post.date | date: "%Y-%m-%d" }}</span>
        <a href="{{ post.url | relative_url }}" class="archive-title">{{ post.title }}</a>
        <div class="archive-tags">
          {% for tag in post.tags limit:3 %}
          <span class="archive-tag">{{ tag }}</span>
          {% endfor %}
        </div>
      </li>
      {% endif %}
    {% endfor %}
  </ul>
</section>

<!-- 数据库 -->
<section class="archive-section" id="数据库">
  <h2 class="archive-category-title">数据库</h2>
  <p class="archive-category-desc">MySQL、Redis、MongoDB 等数据库技术</p>
  <ul class="archive-list">
    {% for post in all_posts %}
      {% if post.categories contains "数据库" %}
      <li class="archive-item">
        <span class="archive-date">{{ post.date | date: "%Y-%m-%d" }}</span>
        <a href="{{ post.url | relative_url }}" class="archive-title">{{ post.title }}</a>
        <div class="archive-tags">
          {% for tag in post.tags limit:3 %}
          <span class="archive-tag">{{ tag }}</span>
          {% endfor %}
        </div>
      </li>
      {% endif %}
    {% endfor %}
  </ul>
</section>

<!-- 中间件 -->
<section class="archive-section" id="中间件">
  <h2 class="archive-category-title">中间件</h2>
  <p class="archive-category-desc">RabbitMQ、Kafka、Elasticsearch 等中间件</p>
  <ul class="archive-list">
    {% for post in all_posts %}
      {% if post.categories contains "中间件" %}
      <li class="archive-item">
        <span class="archive-date">{{ post.date | date: "%Y-%m-%d" }}</span>
        <a href="{{ post.url | relative_url }}" class="archive-title">{{ post.title }}</a>
        <div class="archive-tags">
          {% for tag in post.tags limit:3 %}
          <span class="archive-tag">{{ tag }}</span>
          {% endfor %}
        </div>
      </li>
      {% endif %}
    {% endfor %}
  </ul>
</section>

<!-- 大模型 -->
<section class="archive-section" id="大模型">
  <h2 class="archive-category-title">大模型</h2>
  <p class="archive-category-desc">AI、LangChain4j、Spring AI 等大模型相关</p>
  <ul class="archive-list">
    {% for post in all_posts %}
      {% if post.categories contains "大模型" %}
      <li class="archive-item">
        <span class="archive-date">{{ post.date | date: "%Y-%m-%d" }}</span>
        <a href="{{ post.url | relative_url }}" class="archive-title">{{ post.title }}</a>
        <div class="archive-tags">
          {% for tag in post.tags limit:3 %}
          <span class="archive-tag">{{ tag }}</span>
          {% endfor %}
        </div>
      </li>
      {% endif %}
    {% endfor %}
  </ul>
</section>

<!-- 算法 -->
<section class="archive-section" id="算法">
  <h2 class="archive-category-title">算法</h2>
  <p class="archive-category-desc">LeetCode、数据结构、算法刷题记录</p>
  <ul class="archive-list">
    {% for post in all_posts %}
      {% if post.categories contains "算法" %}
      <li class="archive-item">
        <span class="archive-date">{{ post.date | date: "%Y-%m-%d" }}</span>
        <a href="{{ post.url | relative_url }}" class="archive-title">{{ post.title }}</a>
        <div class="archive-tags">
          {% for tag in post.tags limit:3 %}
          <span class="archive-tag">{{ tag }}</span>
          {% endfor %}
        </div>
      </li>
      {% endif %}
    {% endfor %}
  </ul>
</section>

<!-- 项目 -->
<section class="archive-section" id="项目">
  <h2 class="archive-category-title">项目</h2>
  <p class="archive-category-desc">项目实战、经验总结</p>
  <ul class="archive-list">
    {% for post in all_posts %}
      {% if post.categories contains "项目" %}
      <li class="archive-item">
        <span class="archive-date">{{ post.date | date: "%Y-%m-%d" }}</span>
        <a href="{{ post.url | relative_url }}" class="archive-title">{{ post.title }}</a>
        <div class="archive-tags">
          {% for tag in post.tags limit:3 %}
          <span class="archive-tag">{{ tag }}</span>
          {% endfor %}
        </div>
      </li>
      {% endif %}
    {% endfor %}
  </ul>
</section>

<!-- 其他（未分类的文章） -->
<section class="archive-section" id="其他">
  <h2 class="archive-category-title">其他</h2>
  <p class="archive-category-desc">工具、随笔、其他内容</p>
  <ul class="archive-list">
    {% for post in all_posts %}
      {% assign has_category = false %}
      {% for cat in post.categories %}
        {% if cat == "java基础" or cat == "java后端开发" or cat == "数据库" or cat == "中间件" or cat == "大模型" or cat == "算法" or cat == "项目" %}
          {% assign has_category = true %}
        {% endif %}
      {% endfor %}
      {% unless has_category %}
      <li class="archive-item">
        <span class="archive-date">{{ post.date | date: "%Y-%m-%d" }}</span>
        <a href="{{ post.url | relative_url }}" class="archive-title">{{ post.title }}</a>
        {% if post.categories.size > 0 %}
        <div class="archive-tags">
          {% for tag in post.tags limit:3 %}
          <span class="archive-tag">{{ tag }}</span>
          {% endfor %}
        </div>
        {% endif %}
      </li>
      {% endunless %}
    {% endfor %}
  </ul>
</section>

{% if site.posts.size == 0 %}
<div class="empty-state">
  <p>暂无文章归档</p>
</div>
{% endif %}
