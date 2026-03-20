---
layout: page
title: 归档
permalink: /archive/
description: 文章归档
---

这里收录了所有的博客文章，按时间倒序排列。

{% assign postsByYear = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}

{% for year in postsByYear %}
<section class="archive-group">
  <h2 class="archive-year">{{ year.name }}</h2>
  <ul class="archive-list">
    {% for post in year.items %}
    <li>
      <span class="date">{{ post.date | date: "%m月%d日" }}</span>
      <span class="title">
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      </span>
    </li>
    {% endfor %}
  </ul>
</section>
{% endfor %}

{% if site.posts.size == 0 %}
<div class="empty-state">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
    <path d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
  </svg>
  <p>暂无文章归档</p>
</div>
{% endif %}
