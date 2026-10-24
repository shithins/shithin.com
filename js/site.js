/**
 * shithin.com — "Field Notes"
 * Dependency-free.
 *
 * The site sits in one forest. Its hour and weather follow the visitor:
 *
 *   day   → butterflies and small birds crossing the canopy
 *   night → fireflies drifting through the trees
 *   rain  → rain over the whole place, slightly desaturated
 *
 * Detection is deliberately shy: an instant guess from local clock time paints
 * the page immediately, then — only if the network allows — the guess is
 * refined with the visitor's coarse location and current weather. Nothing here
 * is required for the page to work, and every module exits quietly when its
 * markup is absent. The visitor can pin any climate from the footer.
 */
(function () {
  'use strict';

  var reduce = false;
  try { reduce = matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  var CHAPTER_LABELS = {
    '00': '00 / Overture',
    '01': '01 / The Frame',
    '02': '02 / The Lab',
    '03': '03 / The Field',
    '04': '04 / The Person',
    '05': '05 / Coda'
  };

  /* ======================================================================
     CLIMATE
     ====================================================================== */
  var Climate = (function () {
    var root = document.documentElement;
    var PREF_KEY = 'shithin-ambience';
    var CACHE_KEY = 'shithin-climate';
    var pref = 'auto';
    var mode = 'night';

    try { pref = localStorage.getItem(PREF_KEY) || 'auto'; } catch (e) {}

    function announce(next) {
      if (next === mode) return;
      mode = next;
      root.setAttribute('data-climate', mode);
      try {
        document.dispatchEvent(new CustomEvent('ambiencechange', { detail: { mode: mode } }));
      } catch (e) {}
    }

    function byClock() {
      var h = new Date().getHours();
      return (h >= 6 && h < 19) ? 'day' : 'night';
    }

    function mapWeather(code, isDay) {
      var rain = (code >= 51 && code <= 67) || (code >= 80 && code <= 82) || (code >= 95 && code <= 99);
      if (rain) return 'rain';
      return isDay ? 'day' : 'night';
    }

    function cached() {
      try {
        var c = JSON.parse(sessionStorage.getItem(CACHE_KEY) || 'null');
        if (c && Date.now() - c.t < 30 * 60 * 1000) return c.mode;
      } catch (e) {}
      return null;
    }

    function refine() {
      if (pref !== 'auto') return;
      var hit = cached();
      if (hit) { announce(hit); return; }
      if (!('fetch' in window)) return;

      // Coarse location by IP, then current weather. Both are CORS-friendly and
      // keyless; both fail silently after a short timeout.
      var ctrl = 'AbortController' in window ? new AbortController() : null;
      var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 3200);

      fetch('https://ipapi.co/json/', ctrl ? { signal: ctrl.signal } : {})
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (loc) {
          if (!loc || typeof loc.latitude !== 'number') throw new Error('no location');
          return fetch(
            'https://api.open-meteo.com/v1/forecast?latitude=' + loc.latitude +
            '&longitude=' + loc.longitude + '&current=weather_code,is_day',
            ctrl ? { signal: ctrl.signal } : {}
          );
        })
        .then(function (r) { return r && r.ok ? r.json() : null; })
        .then(function (j) {
          clearTimeout(timer);
          if (!j || !j.current) return;
          var next = mapWeather(j.current.weather_code, j.current.is_day === 1);
          try { sessionStorage.setItem(CACHE_KEY, JSON.stringify({ t: Date.now(), mode: next })); } catch (e) {}
          if (pref === 'auto') announce(next);
        })
        .catch(function () { clearTimeout(timer); });
    }

    function sync() {
      $$('[data-ambience]').forEach(function (b) {
        b.setAttribute('aria-pressed', b.getAttribute('data-ambience') === pref ? 'true' : 'false');
      });
    }

    function set(next) {
      pref = next;
      try { localStorage.setItem(PREF_KEY, pref); } catch (e) {}
      sync();
      if (pref === 'auto') { announce(byClock()); refine(); }
      else announce(pref);
    }

    function current() { return mode; }

    function init() {
      // A pinned climate from a previous visit wins over the clock.
      mode = (pref === 'auto') ? byClock() : pref;
      root.setAttribute('data-climate', mode);
      $$('[data-ambience]').forEach(function (b) {
        b.addEventListener('click', function () { set(b.getAttribute('data-ambience')); });
      });
      sync();
      if (pref === 'auto') refine();
    }

    return { init: init, current: current, set: set };
  })();

  /* ======================================================================
     FAUNA — one canvas per forest scene, driven by the climate
     ====================================================================== */
  var Fauna = (function () {
    var fields = [];
    var raf = 0;
    var last = 0;

    function rand(a, b) { return a + Math.random() * (b - a); }

    function make(mode, w, h) {
      var area = Math.max(1, w * h);
      var parts = [];
      var i;

      if (mode === 'night') {
        var n = Math.max(9, Math.min(30, Math.round(area / 26000)));
        for (i = 0; i < n; i++) {
          parts.push({
            t: 'firefly',
            x: rand(0.03, 0.97) * w,
            y: rand(0.10, 0.95) * h,
            r: rand(1.1, 2.6),
            vx: rand(-6, 6), vy: rand(-5, 5),
            phase: rand(0, Math.PI * 2),
            pulse: rand(0.5, 1.35),
            hue: Math.random() < 0.35 ? 'warm' : 'green'
          });
        }
      } else if (mode === 'rain') {
        var drops = Math.max(36, Math.min(150, Math.round(area / 8200)));
        for (i = 0; i < drops; i++) {
          parts.push({
            t: 'drop',
            x: rand(-0.1, 1.1) * w,
            y: rand(0, 1) * h,
            len: rand(9, 26),
            vy: rand(520, 950),
            a: rand(0.10, 0.30)
          });
        }
      } else {
        var b = Math.max(2, Math.min(8, Math.round(area / 70000)));
        for (i = 0; i < b; i++) {
          parts.push({
            t: 'butterfly',
            x: rand(0.05, 0.95) * w,
            y: rand(0.15, 0.9) * h,
            s: rand(3.4, 6.4),
            vx: rand(-11, 11), vy: rand(-7, 7),
            phase: rand(0, Math.PI * 2),
            flap: rand(7, 11),
            warm: Math.random() < 0.6
          });
        }
        var nb = Math.max(1, Math.min(4, Math.round(area / 160000)));
        for (i = 0; i < nb; i++) {
          parts.push({
            t: 'bird',
            x: rand(0, 1) * w,
            y: rand(0.08, 0.45) * h,
            s: rand(4, 8),
            vx: rand(16, 34) * (Math.random() < 0.5 ? 1 : -1),
            vy: rand(-3, 3),
            phase: rand(0, Math.PI * 2)
          });
        }
      }
      return parts;
    }

    function size(f) {
      var r = f.el.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      f.w = Math.max(1, Math.round(r.width));
      f.h = Math.max(1, Math.round(r.height));
      f.canvas.width = Math.round(f.w * dpr);
      f.canvas.height = Math.round(f.h * dpr);
      f.canvas.style.width = f.w + 'px';
      f.canvas.style.height = f.h + 'px';
      f.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      f.parts = make(f.mode, f.w, f.h);
    }

    function drawFirefly(ctx, p, t) {
      var pulse = 0.35 + 0.65 * (0.5 + 0.5 * Math.sin(t * p.pulse + p.phase));
      var col = p.hue === 'green' ? '198, 232, 150' : '236, 206, 126';
      var g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 7);
      g.addColorStop(0, 'rgba(' + col + ',' + (0.95 * pulse).toFixed(3) + ')');
      g.addColorStop(0.35, 'rgba(' + col + ',' + (0.30 * pulse).toFixed(3) + ')');
      g.addColorStop(1, 'rgba(' + col + ',0)');
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r * 7, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(255, 248, 220,' + (0.85 * pulse).toFixed(3) + ')';
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r * 0.75, 0, Math.PI * 2);
      ctx.fill();
    }

    function drawButterfly(ctx, p, t) {
      var flap = Math.sin(t * p.flap + p.phase);
      var spread = 0.35 + 0.65 * Math.abs(flap);
      var col = p.warm ? '233, 208, 152' : '206, 222, 198';
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(Math.sin(t * 0.7 + p.phase) * 0.25);
      ctx.fillStyle = 'rgba(' + col + ',0.72)';
      ctx.beginPath();
      ctx.ellipse(-p.s * spread, -p.s * 0.35, p.s * spread, p.s * 0.55, -0.35, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.ellipse(p.s * spread, -p.s * 0.35, p.s * spread, p.s * 0.55, 0.35, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(' + col + ',0.55)';
      ctx.beginPath();
      ctx.ellipse(-p.s * spread * 0.8, p.s * 0.45, p.s * spread * 0.72, p.s * 0.42, 0.3, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.ellipse(p.s * spread * 0.8, p.s * 0.45, p.s * spread * 0.72, p.s * 0.42, -0.3, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    function drawBird(ctx, p, t) {
      var flap = Math.sin(t * 6 + p.phase);
      var w = p.s * (0.6 + 0.4 * Math.abs(flap));
      var lift = p.s * flap * 0.35;
      ctx.strokeStyle = 'rgba(226, 232, 216, 0.5)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(p.x - w, p.y + lift);
      ctx.quadraticCurveTo(p.x - w * 0.4, p.y - p.s * 0.35, p.x, p.y);
      ctx.quadraticCurveTo(p.x + w * 0.4, p.y - p.s * 0.35, p.x + w, p.y + lift);
      ctx.stroke();
    }

    function step(f, dt, t) {
      var ctx = f.ctx;
      ctx.clearRect(0, 0, f.w, f.h);
      for (var i = 0; i < f.parts.length; i++) {
        var p = f.parts[i];
        if (p.t === 'firefly') {
          p.x += p.vx * dt; p.y += p.vy * dt;
          p.vx += Math.sin(t * 0.6 + p.phase) * 2.4 * dt;
          p.vy += Math.cos(t * 0.5 + p.phase * 1.7) * 2.0 * dt;
          p.vx = Math.max(-14, Math.min(14, p.vx));
          p.vy = Math.max(-12, Math.min(12, p.vy));
          if (p.x < -20) p.x = f.w + 20;
          if (p.x > f.w + 20) p.x = -20;
          if (p.y < -20) p.y = f.h + 20;
          if (p.y > f.h + 20) p.y = -20;
          drawFirefly(ctx, p, t);
        } else if (p.t === 'drop') {
          p.y += p.vy * dt;
          if (p.y > f.h + 30) { p.y = -30; p.x = rand(-0.1, 1.1) * f.w; }
          ctx.strokeStyle = 'rgba(196, 216, 220,' + p.a.toFixed(3) + ')';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p.x - p.len * 0.18, p.y - p.len);
          ctx.stroke();
        } else if (p.t === 'butterfly') {
          p.x += p.vx * dt; p.y += p.vy * dt;
          p.vx += Math.sin(t * 1.1 + p.phase) * 9 * dt;
          p.vy += Math.cos(t * 0.9 + p.phase) * 7 * dt;
          p.vx = Math.max(-22, Math.min(22, p.vx));
          p.vy = Math.max(-16, Math.min(16, p.vy));
          if (p.x < 10) { p.x = 10; p.vx = Math.abs(p.vx); }
          if (p.x > f.w - 10) { p.x = f.w - 10; p.vx = -Math.abs(p.vx); }
          if (p.y < 10) { p.y = 10; p.vy = Math.abs(p.vy); }
          if (p.y > f.h - 10) { p.y = f.h - 10; p.vy = -Math.abs(p.vy); }
          drawButterfly(ctx, p, t);
        } else if (p.t === 'bird') {
          p.x += p.vx * dt; p.y += p.vy * dt;
          if (p.x < -40) p.x = f.w + 40;
          if (p.x > f.w + 40) p.x = -40;
          drawBird(ctx, p, t);
        }
      }
    }

    function loop(now) {
      raf = requestAnimationFrame(loop);
      if (document.hidden) return;
      if (!last) last = now;
      var dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      var t = now / 1000;
      var vh = window.innerHeight;
      for (var i = 0; i < fields.length; i++) {
        var f = fields[i];
        var r = f.el.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) continue;   // entirely offscreen: skip
        step(f, dt, t);
      }
    }

    function rebuild(mode) {
      fields.forEach(function (f) {
        f.mode = mode;
        f.parts = make(mode, f.w, f.h);
        f.ctx.clearRect(0, 0, f.w, f.h);
      });
    }

    function init() {
      if (reduce) return;                       // no ambient motion at all
      fields = $$('[data-fauna]').map(function (el) {
        var canvas = document.createElement('canvas');
        el.appendChild(canvas);
        var f = { el: el, canvas: canvas, ctx: canvas.getContext('2d'), mode: Climate.current() };
        size(f);
        return f;
      });
      if (!fields.length) return;

      if ('ResizeObserver' in window) {
        var ro = new ResizeObserver(function () { fields.forEach(size); });
        fields.forEach(function (f) { ro.observe(f.el); });
      } else {
        window.addEventListener('resize', function () { fields.forEach(size); }, { passive: true });
      }

      document.addEventListener('ambiencechange', function (e) { rebuild(e.detail.mode); });
      raf = requestAnimationFrame(loop);
    }

    return { init: init };
  })();

  /* ======================================================================
     PAGE CHROME
     ====================================================================== */

  /* --- top bar: hairline appears once the overture is behind us ---------- */
  (function topbar() {
    var el = $('#bar');
    if (!el) return;
    var ticking = false;
    function update() {
      ticking = false;
      el.classList.toggle('is-stuck', window.scrollY > 40);
    }
    update();
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
  })();

  /* --- reading progress: one hairline, the bookmark edge ------------------ */
  (function progress() {
    var el = $('#progress');
    if (!el) return;
    var ticking = false;
    function update() {
      ticking = false;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      el.style.transform = 'scaleX(' + p.toFixed(4) + ')';
    }
    update();
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener('resize', update, { passive: true });
  })();

  /* --- reveal on scroll -------------------------------------------------- */
  (function reveal() {
    var items = $$('[data-reveal], [data-line]').filter(function (el) {
      return !el.closest('.overture');
    });
    if (!items.length) return;

    if (reduce || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-seen'); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var group = el.parentElement ? $$('[data-reveal],[data-line]', el.parentElement) : [el];
        var i = group.indexOf(el);
        var delay = i > 0 ? Math.min(i * 70, 280) : 0;
        setTimeout(function () { el.classList.add('is-seen'); }, delay);
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    items.forEach(function (el) { io.observe(el); });
  })();

  /* --- overture entrance ------------------------------------------------- */
  (function overture() {
    var el = $('.overture');
    if (!el) return;
    requestAnimationFrame(function () {
      setTimeout(function () { el.classList.add('is-in'); }, reduce ? 0 : 120);
    });
  })();

  /* --- chapter rail ------------------------------------------------------ */
  (function rail() {
    var sections = $$('[data-chapter]');
    var now = $('#rail-now');
    if (!sections.length || !now) return;

    if (sections.length < 3) {
      var ticks = $('.rail__ticks');
      if (ticks) ticks.style.display = 'none';
      return;
    }

    var tickEls = $$('[data-rail-tick]');

    function mark(num) {
      now.textContent = CHAPTER_LABELS[num] || (num + ' /');
      var n = parseInt(num, 10);
      tickEls.forEach(function (t) {
        t.classList.toggle('is-on', t.getAttribute('data-rail-tick') === String(n));
      });
    }

    if (reduce || !('IntersectionObserver' in window)) { mark('00'); return; }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) mark(entry.target.getAttribute('data-chapter'));
      });
    }, { rootMargin: '-45% 0px -45% 0px', threshold: 0 });

    sections.forEach(function (s) { io.observe(s); });
    mark('00');
  })();

  /* --- parallax ---------------------------------------------------------- */
  (function parallax() {
    var layers = $$('[data-parallax]');
    if (!layers.length || reduce) return;

    var ticking = false;
    function update() {
      ticking = false;
      var vh = window.innerHeight;
      layers.forEach(function (layer) {
        var r = layer.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var progress = (r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2);
        var shift = progress * -26;
        layer.style.transform = 'translate3d(0,' + shift.toFixed(2) + 'px,0)';
      });
    }
    update();
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener('resize', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
  })();

  /* --- live IST clock ---------------------------------------------------- */
  (function clock() {
    var el = $('#clock');
    if (!el) return;
    function tick() {
      try {
        el.textContent = new Intl.DateTimeFormat('en-GB', {
          timeZone: 'Asia/Kolkata',
          hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
        }).format(new Date());
      } catch (e) {}
    }
    tick();
    setInterval(tick, 1000);
  })();

  /* --- year -------------------------------------------------------------- */
  (function year() {
    var el = $('#yr');
    if (el) el.textContent = new Date().getFullYear();
  })();

  /* --- boot -------------------------------------------------------------- */
  Climate.init();
  Fauna.init();
})();
