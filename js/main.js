/**
 * Shithin Ram — Personal Portfolio & Authority Site
 * Interactive components: Live Kerala IST clock, clipboard copy toast, nav highlights.
 */

document.addEventListener('DOMContentLoaded', () => {
  initClock();
  initCopyButtons();
  highlightActiveNav();
});

/* --------------------------------------------------------------------------
   Live Kerala (IST / Asia/Kolkata) Clock
   -------------------------------------------------------------------------- */
function initClock() {
  const clockEl = document.getElementById('kerala-clock');
  if (!clockEl) return;

  function update() {
    try {
      const now = new Date();
      // Format to Indian Standard Time (UTC+5:30)
      const options = {
        timeZone: 'Asia/Kolkata',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      };
      const timeString = new Intl.DateTimeFormat('en-US', options).format(now);
      clockEl.textContent = `${timeString} IST`;
    } catch (e) {
      // Fallback
      const d = new Date();
      const utc = d.getTime() + (d.getTimezoneOffset() * 60000);
      const ist = new Date(utc + (3600000 * 5.5));
      clockEl.textContent = ist.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' IST';
    }
  }

  update();
  setInterval(update, 1000);
}

/* --------------------------------------------------------------------------
   Clipboard Copy & Toast Notification
   -------------------------------------------------------------------------- */
function initCopyButtons() {
  const copyButtons = document.querySelectorAll('[data-copy]');
  const toast = document.getElementById('toast');

  copyButtons.forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const text = btn.getAttribute('data-copy');
      const label = btn.getAttribute('data-label') || text;

      try {
        await navigator.clipboard.writeText(text);
        showToast(`Copied ${label} to clipboard`);
      } catch (err) {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
          document.execCommand('copy');
          showToast(`Copied ${label} to clipboard`);
        } catch (fallbackErr) {
          showToast(`Contact: ${text}`);
        }
        document.body.removeChild(textarea);
      }
    });
  });

  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(window._toastTimeout);
    window._toastTimeout = setTimeout(() => {
      toast.classList.remove('show');
    }, 2400);
  }
}

/* --------------------------------------------------------------------------
   Highlight Active Nav
   -------------------------------------------------------------------------- */
function highlightActiveNav() {
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = document.querySelectorAll('.nav-link');

  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });
}
