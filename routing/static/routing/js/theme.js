// theme.js — runs on every page
(function () {
  const saved = localStorage.getItem('ro_theme') || 'midnight';
  document.documentElement.setAttribute('data-theme', saved);

  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('ro_theme', t);
    document.querySelectorAll('.theme-dot').forEach(d => {
      d.classList.toggle('selected', d.dataset.t === t);
    });
    // Persist to server if logged in
    const csrf = document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] || '';
    if (csrf) {
      fetch('/api/set-theme/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
        body: JSON.stringify({ theme: t }),
        credentials: 'same-origin',
      }).catch(() => {});
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.theme-dot').forEach(d => {
      if (d.dataset.t === saved) d.classList.add('selected');
      d.addEventListener('click', () => applyTheme(d.dataset.t));
    });
  });
})();
