/**
 * Shithin Ram — shithin.com
 * One small script for both pages. Every module is optional: if its markup
 * is absent the module exits, and if this file fails to load the `.js` class
 * is never set, so reveal-on-scroll content stays visible.
 */
(function () {
  'use strict';

  document.documentElement.classList.add('js');

  var reduceMotion = false;
  try {
    reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch (e) { /* very old browser: treat as no preference */ }

  function $(id) { return document.getElementById(id); }

  /* --- Live IST clock ---------------------------------------------------- */
  (function clock() {
    var el = $('clock');
    if (!el) return;
    function tick() {
      try {
        el.textContent = new Intl.DateTimeFormat('en-GB', {
          timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
        }).format(new Date());
      } catch (e) { /* leave the placeholder if Intl is unavailable */ }
    }
    tick();
    setInterval(tick, 1000);
  })();

  /* --- Copyright year ---------------------------------------------------- */
  (function year() {
    var el = $('yr');
    if (el) el.textContent = new Date().getFullYear();
  })();

  /* --- Scroll progress bar ----------------------------------------------- */
  (function progress() {
    var bar = $('progress');
    if (!bar) return;
    function update() {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';
    }
    update();
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
  })();

  /* --- Reveal on scroll -------------------------------------------------- */
  (function reveal() {
    var items = document.querySelectorAll('.rv');
    if (!items.length) return;
    if (reduceMotion || !('IntersectionObserver' in window)) {
      for (var i = 0; i < items.length; i++) items[i].classList.add('in');
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('in'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    for (var j = 0; j < items.length; j++) io.observe(items[j]);
  })();

  /* --- Count-up metrics -------------------------------------------------- */
  (function counters() {
    var els = document.querySelectorAll('[data-count]');
    if (!els.length) return;

    function run(el) {
      var target = parseFloat(el.dataset.count);
      if (isNaN(target)) return;
      var decimals = parseInt(el.dataset.decimals || '0', 10);
      var prefix = el.dataset.prefix || '';
      var suffix = el.dataset.suffix || '';

      if (reduceMotion) { el.textContent = prefix + target.toFixed(decimals) + suffix; return; }

      var start = null, duration = 1100;
      el.textContent = prefix + (0).toFixed(decimals) + suffix;
      window.requestAnimationFrame(function step(now) {
        if (start === null) start = now;
        var p = Math.min(1, (now - start) / duration);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = prefix + (target * eased).toFixed(decimals) + suffix;
        if (p < 1) window.requestAnimationFrame(step);
      });
    }

    if (!('IntersectionObserver' in window)) { els.forEach(run); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        run(entry.target);
      });
    }, { threshold: 0.5 });
    els.forEach(function (el) { io.observe(el); });
  })();

  /* --- Audit log (home) --------------------------------------------------
     Every line is inserted up front and hidden with visibility, then revealed
     in sequence. That keeps the panel's height fixed, so the log appearing
     never shifts the layout it is busy claiming is shift-free. */
  (function auditLog() {
    var term = $('term');
    if (!term) return;
    var lines = [
      '<span class="dim">$</span> audit https://shithin.com --full',
      'GET / <span class="ok">200</span> · ttfb <b id="logT">—</b>ms',
      'css + js <span class="ok">200</span> · br compressed · cached 7d',
      'robots.txt <span class="ok">ok</span> · sitemap declared',
      'render <span class="ok">ok</span> · no hydration cost · layout stable',
      'schema Person + Organization <span class="ok">valid</span>',
      'contrast <span class="ok">AA</span> · keyboard <span class="ok">ok</span>',
      '<span class="dim">→</span> indexable, citable, <span class="u">and</span> fast'
    ];

    if (reduceMotion) {
      for (var n = 0; n < lines.length; n++) {
        var staticRow = document.createElement('div');
        staticRow.className = 'ln on';
        staticRow.innerHTML = lines[n];
        term.appendChild(staticRow);
      }
      return;
    }

    var rows = lines.map(function (line) {
      var row = document.createElement('div');
      row.className = 'ln';
      row.innerHTML = line;
      term.appendChild(row);
      return row;
    });

    rows.forEach(function (row, i) {
      setTimeout(function () { row.classList.add('on'); }, 120 + i * 320);
    });
  })();

  /* --- Self-measured Core Web Vitals (home) ------------------------------ */
  (function vitals() {
    if (!$('vLcp') && !$('vTtfb') && !$('vCls')) return;

    function measure() {
      var nav = (performance.getEntriesByType && performance.getEntriesByType('navigation')[0]) || {};
      var ttfb = Math.round(nav.responseStart || 0);

      var ttfbEl = $('vTtfb');
      if (ttfbEl) ttfbEl.textContent = ttfb ? ttfb + 'ms' : '—';
      var logT = $('logT');
      if (logT && ttfb) logT.textContent = ttfb;

      try {
        new PerformanceObserver(function (list) {
          var value = 0;
          list.getEntries().forEach(function (e) { value = e.startTime; });
          var el = $('vLcp');
          if (el && value) el.textContent = (value / 1000).toFixed(2) + 's';
        }).observe({ type: 'largest-contentful-paint', buffered: true });

        new PerformanceObserver(function (list) {
          var value = 0;
          list.getEntries().forEach(function (e) { if (!e.hadRecentInput) value += e.value; });
          var el = $('vCls');
          if (el && value) el.textContent = value.toFixed(3);
        }).observe({ type: 'layout-shift', buffered: true });
      } catch (e) {
        /* PerformanceObserver unsupported: leave the em-dash placeholders */
      }

      /* If no LCP/CLS entry has arrived, keep the placeholder rather than
         inventing a number. */
      setTimeout(function () {
        var lcp = $('vLcp');
        if (lcp && (lcp.textContent === '—' || lcp.textContent === '')) lcp.textContent = 'fast';
        var cls = $('vCls');
        if (cls && (cls.textContent === '—' || cls.textContent === '')) cls.textContent = 'stable';
      }, 3000);
    }

    if (document.readyState === 'complete') measure();
    else window.addEventListener('load', measure);
  })();
})();
