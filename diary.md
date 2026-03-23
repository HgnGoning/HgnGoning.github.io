---
layout: page
title: 日记
permalink: /diary/
description: 记录生活中的点滴
---

{% assign diaries = site.diaries | sort: "date" | reverse %}

{% if diaries.size > 0 %}
<div class="diary-timeline">
  {% assign current_year = nil %}
  {% for diary in diaries %}
    {% assign year = diary.date | date: "%Y" %}
    {% if year != current_year %}
      {% assign current_year = year %}
      <div class="diary-year-divider">{{ year }}</div>
    {% endif %}
    <article class="diary-entry">
      <a href="{{ diary.url | relative_url }}" class="diary-entry-link">
        <time class="diary-entry-date">{{ diary.date | date: "%m.%d" }}</time>
        <div class="diary-entry-content">
          {{ diary.content | strip_html | truncatewords: 30 }}
        </div>
      </a>
    </article>
  {% endfor %}
</div>
{% else %}
<div class="empty-state">
  <p>还没有日记</p>
  <p class="empty-hint">生活点滴，值得记录</p>
</div>
{% endif %}
