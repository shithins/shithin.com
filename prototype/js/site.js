/**
 * shithin.com — minimal prototype
 * Small, dependency-free. Every module exits quietly if its markup is absent,
 * and the `.js` class is set by an inline script in <head> so that if this file
 * never loads, none of the reveal-on-scroll content stays hidden.
 */
(function () {
  'use strict';

  var reduce = false;
  try { reduce = matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

  function $(id) { return document.getElementById(id); }
  function $$(sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); }

  /* --- sticky header state ------------------------------------------------ */
  (function bar() {
    var el = $('bar');
    if (!el) return;
    var ticking = false;
    function update() {
      ticking = false;
      if (window.scrollY > 12) el.classList.add('stuck');
      else el.classList.remove('stuck');
    }
    update();
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
  })();

  /* --- reveal on scroll --------------------------------------------------- */
  (function reveal() {
    var items = $$('.rv');
    if (!items.length) return;
    if (reduce || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  })();

  /* --- live IST clock ----------------------------------------------------- */
  (function clock() {
    var el = $('clock');
    if (!el) return;
    function tick() {
      try {
        el.textContent = new Intl.DateTimeFormat('en-GB', {
          timeZone: 'Asia/Kolkata',
          hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
        }).format(new Date());
      } catch (e) { /* leave the placeholder */ }
    }
    tick();
    setInterval(tick, 1000);
  })();

  /* --- year --------------------------------------------------------------- */
  (function year() {
    var el = $('yr');
    if (el) el.textContent = new Date().getFullYear();
  })();

  /* --- footer subscribe (prototype: local confirmation only) -------------- */
  (function subscribe() {
    var form = document.querySelector('[data-subscribe]');
    if (!form) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = form.querySelector('input[type="email"]');
      var note = form.parentNode.querySelector('[data-subscribe-note]');
      if (!input || !input.value) return;
      if (note) {
        note.textContent = 'Thanks — this prototype does not store addresses yet.';
        note.style.color = 'var(--warm-2)';
      }
      input.value = '';
    });
  })();

  /* --- hero parallax (very subtle) ---------------------------------------- */
  (function parallax() {
    var el = document.querySelector('[data-parallax]');
    if (!el || reduce) return;
    var ticking = false;
    function update() {
      ticking = false;
      var y = Math.min(window.scrollY, window.innerHeight);
      el.style.transform = 'translate3d(0,' + (y * 0.12).toFixed(2) + 'px,0)';
    }
    update();
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
  })();
})();
