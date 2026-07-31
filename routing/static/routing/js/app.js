// app.js — shared utilities
function getCsrf() {
  return document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] || '';
}

async function apiFetch(url, opts = {}) {
  const defaults = {
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    credentials: 'same-origin',
  };
  return fetch(url, { ...defaults, ...opts, headers: { ...defaults.headers, ...opts.headers } });
}

function fmtDate(s) {
  return new Date(s).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function fmtNum(n) {
  return (n || 0).toLocaleString('en-US', { maximumFractionDigits: 2 });
}

// Nominatim place search for the 5 districts
// bbox: minlon, minlat, maxlon, maxlat
const DISTRICTS_BBOX = '84.65,27.61,85.52,28.20';

async function searchPlaces(query) {
  if (!query || query.length < 2) return [];
  const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query + ' Nepal')}&format=json&limit=7&viewbox=${DISTRICTS_BBOX}&bounded=0&countrycodes=np&addressdetails=1&accept-language=en`;
  try {
    const r = await fetch(url, { headers: { 'Accept-Language': 'en' } });
    return await r.json();
  } catch { return []; }
}

function buildSearchUI(inputEl, resultsEl, onSelect) {
  let timer;
  inputEl.addEventListener('input', () => {
    clearTimeout(timer);
    const q = inputEl.value.trim();
    if (q.length < 2) { resultsEl.style.display = 'none'; return; }
    timer = setTimeout(async () => {
      const places = await searchPlaces(q);
      if (!places.length) { resultsEl.style.display = 'none'; return; }
      resultsEl.innerHTML = '';
      places.slice(0, 6).forEach(p => {
        const div = document.createElement('div');
        div.className = 'place-result-item';
        const nm = p.name || p.display_name.split(',')[0];
        const addr = p.display_name;
        div.innerHTML = `<div class="place-name">${nm}</div><div class="place-addr">${addr}</div>`;
        div.addEventListener('click', () => {
          inputEl.value = nm;
          resultsEl.style.display = 'none';
          onSelect({ name: nm, lat: parseFloat(p.lat), lon: parseFloat(p.lon), display: addr });
        });
        resultsEl.appendChild(div);
      });
      resultsEl.style.display = 'block';
    }, 300);
  });
  document.addEventListener('click', e => {
    if (!inputEl.contains(e.target) && !resultsEl.contains(e.target))
      resultsEl.style.display = 'none';
  });
}
