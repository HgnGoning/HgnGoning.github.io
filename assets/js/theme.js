/**
 * TTDB 博客交互脚本
 */

(function() {
  'use strict';

  // ============================================
  // 主题切换
  // ============================================
  const themeToggle = document.getElementById('theme-toggle');

  if (themeToggle) {
    themeToggle.addEventListener('click', function() {
      const html = document.documentElement;
      const currentTheme = html.getAttribute('data-theme');
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';

      html.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
    });
  }

  // ============================================
  // 返回顶部按钮
  // ============================================
  const backToTop = document.getElementById('back-to-top');

  if (backToTop) {
    // 显示/隐藏按钮
    function toggleBackToTop() {
      if (window.scrollY > 300) {
        backToTop.classList.add('visible');
      } else {
        backToTop.classList.remove('visible');
      }
    }

    window.addEventListener('scroll', toggleBackToTop, { passive: true });

    // 点击返回顶部
    backToTop.addEventListener('click', function() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // ============================================
  // 导航栏滚动效果
  // ============================================
  const header = document.querySelector('.site-header');

  if (header) {
    let lastScrollY = 0;

    function handleHeaderScroll() {
      const currentScrollY = window.scrollY;

      if (currentScrollY > 50) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }

      lastScrollY = currentScrollY;
    }

    window.addEventListener('scroll', handleHeaderScroll, { passive: true });
  }

  // ============================================
  // 文章目录 - 右侧悬浮
  // ============================================
  const tocSidebar = document.getElementById('toc-sidebar');
  const tocToggleBtn = document.getElementById('toc-toggle-btn');
  const tocCloseBtn = document.getElementById('toc-close-btn');
  const tocPanel = document.getElementById('toc-panel');
  const tocPanelContent = document.getElementById('toc-panel-content');
  const postContent = document.querySelector('.post-content');

  // 生成目录
  if (tocPanelContent && postContent) {
    const headings = postContent.querySelectorAll('h2, h3, h4');

    if (headings.length > 0) {
      const tocList = document.createElement('ul');

      headings.forEach(function(heading, index) {
        // 为标题添加 id
        const id = 'heading-' + index;
        heading.id = id;

        const level = parseInt(heading.tagName.charAt(1));
        const li = document.createElement('li');
        const link = document.createElement('a');

        link.href = '#' + id;
        link.textContent = heading.textContent;
        link.setAttribute('data-target', id);
        li.appendChild(link);

        // 根据层级添加缩进类
        if (level === 3) {
          li.style.paddingLeft = '12px';
        } else if (level === 4) {
          li.style.paddingLeft = '24px';
        }

        tocList.appendChild(li);
      });

      tocPanelContent.appendChild(tocList);

      // 点击目录链接平滑滚动
      tocList.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', function(e) {
          e.preventDefault();
          const targetId = this.getAttribute('data-target');
          const target = document.getElementById(targetId);
          if (target) {
            const headerHeight = document.querySelector('.site-header')?.offsetHeight || 64;
            const targetPosition = target.offsetTop - headerHeight - 20;
            window.scrollTo({
              top: targetPosition,
              behavior: 'smooth'
            });
            // 更新活动状态
            tocList.querySelectorAll('a').forEach(function(a) {
              a.classList.remove('active');
            });
            this.classList.add('active');
          }
        });
      });

      // 滚动时高亮当前目录项
      let ticking = false;
      window.addEventListener('scroll', function() {
        if (!ticking) {
          window.requestAnimationFrame(function() {
            const headerHeight = document.querySelector('.site-header')?.offsetHeight || 64;
            const scrollPosition = window.scrollY + headerHeight + 100;

            let currentHeading = null;
            headings.forEach(function(heading) {
              if (heading.offsetTop <= scrollPosition) {
                currentHeading = heading;
              }
            });

            if (currentHeading) {
              tocList.querySelectorAll('a').forEach(function(link) {
                link.classList.remove('active');
                if (link.getAttribute('data-target') === currentHeading.id) {
                  link.classList.add('active');
                }
              });
            }
            ticking = false;
          });
          ticking = true;
        }
      }, { passive: true });

    } else {
      // 没有标题时隐藏整个目录侧边栏
      if (tocSidebar) {
        tocSidebar.style.display = 'none';
      }
    }
  }

  // 目录展开/收起
  if (tocToggleBtn && tocPanel) {
    tocToggleBtn.addEventListener('click', function() {
      tocPanel.classList.add('open');
      tocToggleBtn.classList.add('hidden');
    });
  }

  if (tocCloseBtn && tocPanel && tocToggleBtn) {
    tocCloseBtn.addEventListener('click', function() {
      tocPanel.classList.remove('open');
      tocToggleBtn.classList.remove('hidden');
    });
  }

  // 点击目录外部关闭
  document.addEventListener('click', function(e) {
    if (tocPanel && tocPanel.classList.contains('open')) {
      if (!tocPanel.contains(e.target) && !tocToggleBtn.contains(e.target)) {
        tocPanel.classList.remove('open');
        if (tocToggleBtn) {
          tocToggleBtn.classList.remove('hidden');
        }
      }
    }
  });

  // ============================================
  // 文章列表淡入动画（已禁用，极简风格不需要）
  // ============================================

  // ============================================
  // 图片懒加载（如果需要）
  // ============================================
  const lazyImages = document.querySelectorAll('img[data-src]');

  if (lazyImages.length > 0 && 'IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          imageObserver.unobserve(img);
        }
      });
    });

    lazyImages.forEach(function(img) {
      imageObserver.observe(img);
    });
  }

  // ============================================
  // 外部链接新窗口打开
  // ============================================
  const links = document.querySelectorAll('a[href^="http"]');

  links.forEach(function(link) {
    if (link.hostname !== window.location.hostname) {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    }
  });

  // ============================================
  // 复制代码按钮（可选）
  // ============================================
  const codeBlocks = document.querySelectorAll('pre code');

  codeBlocks.forEach(function(codeBlock) {
    const pre = codeBlock.parentElement;

    // 创建复制按钮
    const copyButton = document.createElement('button');
    copyButton.className = 'copy-button';
    copyButton.textContent = '复制';
    copyButton.style.cssText = `
      position: absolute;
      top: 8px;
      right: 8px;
      padding: 4px 8px;
      font-size: 12px;
      background: var(--color-bg-secondary);
      border: 1px solid var(--color-border);
      border-radius: 4px;
      cursor: pointer;
      opacity: 0;
      transition: opacity 0.2s;
    `;

    pre.style.position = 'relative';
    pre.appendChild(copyButton);

    // 鼠标悬停显示按钮
    pre.addEventListener('mouseenter', function() {
      copyButton.style.opacity = '1';
    });

    pre.addEventListener('mouseleave', function() {
      copyButton.style.opacity = '0';
    });

    // 复制功能
    copyButton.addEventListener('click', function() {
      navigator.clipboard.writeText(codeBlock.textContent).then(function() {
        copyButton.textContent = '已复制!';
        setTimeout(function() {
          copyButton.textContent = '复制';
        }, 2000);
      });
    });
  });

})();
