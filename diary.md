---
layout: page
title: 日记
permalink: /diary/
description: 记录生活中的点滴
---

<div class="diary-calendar-container">
  <!-- 日历头部 -->
  <div class="calendar-header">
    <button class="calendar-nav-btn prev" id="prevMonth">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </button>
    <h2 class="calendar-title" id="calendarTitle"></h2>
    <button class="calendar-nav-btn next" id="nextMonth">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="9 18 15 12 9 6"></polyline>
      </svg>
    </button>
  </div>

  <!-- 日历主体 -->
  <div class="calendar-grid">
    <div class="calendar-weekdays">
      <span>日</span>
      <span>一</span>
      <span>二</span>
      <span>三</span>
      <span>四</span>
      <span>五</span>
      <span>六</span>
    </div>
    <div class="calendar-days" id="calendarDays"></div>
  </div>

  <!-- 当月日记列表 -->
  <div class="diary-list-section">
    <h3 class="diary-list-title" id="diaryListTitle">本月日记</h3>
    <div class="diary-list" id="diaryList"></div>
  </div>
</div>

<!-- 日记数据 -->
<script>
  // 从 Jekyll 生成日记数据
  const diaryData = {
    {% for diary in site.diaries %}
    "{{ diary.date | date: '%Y-%m-%d' }}": {
      url: "{{ diary.url | relative_url }}",
      excerpt: "{{ diary.content | strip_html | strip_newlines | truncatewords: 20 | escape }}"
    }{% unless forloop.last %},{% endunless %}
    {% endfor %}
  };

  // 获取有日记的年月
  const diaryDates = Object.keys(diaryData);
  const yearMonths = [...new Set(diaryDates.map(d => d.substring(0, 7)))].sort().reverse();

  let currentDate = new Date();
  let currentYear = currentDate.getFullYear();
  let currentMonth = currentDate.getMonth();

  // 如果当前月份没有日记，跳转到最近有日记的月份
  const currentYearMonth = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}`;
  if (yearMonths.length > 0 && !yearMonths.includes(currentYearMonth)) {
    const nearestMonth = yearMonths.find(ym => ym <= currentYearMonth) || yearMonths[0];
    currentYear = parseInt(nearestMonth.substring(0, 4));
    currentMonth = parseInt(nearestMonth.substring(5, 7)) - 1;
  }

  function renderCalendar() {
    const title = document.getElementById('calendarTitle');
    const daysContainer = document.getElementById('calendarDays');

    // 更新标题
    title.textContent = `${currentYear}年${currentMonth + 1}月`;

    // 获取当月第一天和最后一天
    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startWeekday = firstDay.getDay();

    // 清空并渲染日期
    daysContainer.innerHTML = '';

    // 填充空白格子
    for (let i = 0; i < startWeekday; i++) {
      const emptyCell = document.createElement('div');
      emptyCell.className = 'calendar-day empty';
      daysContainer.appendChild(emptyCell);
    }

    // 渲染日期
    for (let day = 1; day <= daysInMonth; day++) {
      const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      const hasDiary = diaryData[dateStr];

      const dayCell = document.createElement('div');
      dayCell.className = 'calendar-day';
      if (hasDiary) {
        dayCell.classList.add('has-diary');
        dayCell.innerHTML = `
          <a href="${hasDiary.url}" class="day-link">
            <span class="day-number">${day}</span>
            <span class="diary-mark"></span>
          </a>
        `;
      } else {
        dayCell.innerHTML = `<span class="day-number">${day}</span>`;
      }
      daysContainer.appendChild(dayCell);
    }

    // 更新月份导航按钮状态
    updateNavButtons();

    // 更新日记列表
    renderDiaryList();
  }

  function renderDiaryList() {
    const listContainer = document.getElementById('diaryList');
    const listTitle = document.getElementById('diaryListTitle');

    // 获取当月日记
    const monthStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}`;
    const monthDiaries = Object.entries(diaryData)
      .filter(([date]) => date.startsWith(monthStr))
      .sort(([a], [b]) => b.localeCompare(a));

    if (monthDiaries.length === 0) {
      listTitle.textContent = '本月暂无日记';
      listContainer.innerHTML = '<p class="no-diary-hint">选择有标记的日期查看日记</p>';
      return;
    }

    listTitle.textContent = `本月日记 (${monthDiaries.length}篇)`;
    listContainer.innerHTML = monthDiaries.map(([date, info]) => {
      const day = date.substring(8);
      return `
        <a href="${info.url}" class="diary-item">
          <span class="diary-item-date">${currentMonth + 1}.${parseInt(day)}</span>
          <span class="diary-item-excerpt">${info.excerpt}</span>
        </a>
      `;
    }).join('');
  }

  function updateNavButtons() {
    const prevBtn = document.getElementById('prevMonth');
    const nextBtn = document.getElementById('nextMonth');
    const currentYM = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}`;

    // 检查是否有更早/更晚的日记
    const hasPrev = yearMonths.some(ym => ym < currentYM);
    const hasNext = yearMonths.some(ym => ym > currentYM);

    prevBtn.disabled = !hasPrev;
    nextBtn.disabled = !hasNext;
  }

  function prevMonth() {
    const currentYM = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}`;
    const prevYM = yearMonths.filter(ym => ym < currentYM).sort().reverse()[0];
    if (prevYM) {
      currentYear = parseInt(prevYM.substring(0, 4));
      currentMonth = parseInt(prevYM.substring(5, 7)) - 1;
      renderCalendar();
    }
  }

  function nextMonth() {
    const currentYM = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}`;
    const nextYM = yearMonths.filter(ym => ym > currentYM).sort()[0];
    if (nextYM) {
      currentYear = parseInt(nextYM.substring(0, 4));
      currentMonth = parseInt(nextYM.substring(5, 7)) - 1;
      renderCalendar();
    }
  }

  // 绑定事件
  document.getElementById('prevMonth').addEventListener('click', prevMonth);
  document.getElementById('nextMonth').addEventListener('click', nextMonth);

  // 初始渲染
  renderCalendar();
</script>
