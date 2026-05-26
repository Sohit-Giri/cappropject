// map.js — route optimizer map page

function getCsrf() {
  return document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] || '';
}

const map = L.map('map', { zoomControl: false }).setView([27.7103, 85.3222], 12);
L.control.zoom({ position: 'bottomright' }).addTo(map);

// Tile layer switcher — dark default
// --- UPDATED TILE LOGIC ---
// Use Voyager: It works perfectly for both Light and Dark themes
let tileUrl = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png';

const tileLayer = L.tileLayer(tileUrl, {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
  subdomains: 'abcd', 
  maxZoom: 20,
}).addTo(map);

// Theme → tile auto-switch fix
(function () {
  const t = localStorage.getItem('ro_theme') || 'midnight';
  // If the theme is arctic (white), we keep the clean Voyager look.
  // If midnight, we use the Dark Matter tiles.
  if (t === 'midnight') {
    tileLayer.setUrl('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png');
  } else {
    tileLayer.setUrl('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png');
  }
})();
// ---------------------------

let src = null, dst = null, srcM = null, dstM = null, routeL = null;
let clicking = null; // null = not in click mode; 'src' or 'dst'
let selectedMode = document.getElementById('selectedMode')?.value || 'car';

const mkIcon = (color, glow) => L.divIcon({
  className: '',
  html: `<div style="width:14px;height:14px;background:${color};border-radius:50%;border:2.5px solid #fff;box-shadow:0 0 10px ${glow}"></div>`,
  iconSize: [14, 14], iconAnchor: [7, 7]
});
const srcIcon = mkIcon('#34d399','#34d399');
const dstIcon = mkIcon('#f87171','#f87171');

function setHint(msg) {
  const h = document.getElementById('mapHint');
  if (h) h.textContent = msg;
}

function showLoad(v) {
  const l = document.getElementById('mapLoading');
  if (l) l.style.display = v ? 'flex' : 'none';
}

function placeMarker(type, lat, lon, name) {
  if (type === 'src') {
    if (srcM) map.removeLayer(srcM);
    src = { lat, lon };
    srcM = L.marker([lat, lon], { icon: srcIcon }).addTo(map)
             .bindPopup(`<b style="color:#34d399">🟢 Start</b><br><small>${name||''}</small>`);
    const el = document.getElementById('srcCoord');
    if (el) { el.querySelector('.coord-text').textContent = name || `${lat.toFixed(5)}, ${lon.toFixed(5)}`; el.style.display = 'flex'; }
  } else {
    if (dstM) map.removeLayer(dstM);
    dst = { lat, lon };
    dstM = L.marker([lat, lon], { icon: dstIcon }).addTo(map)
             .bindPopup(`<b style="color:#f87171">🔴 End</b><br><small>${name||''}</small>`);
    const el = document.getElementById('dstCoord');
    if (el) { el.querySelector('.coord-text').textContent = name || `${lat.toFixed(5)}, ${lon.toFixed(5)}`; el.style.display = 'flex'; }
  }
}

// Map click handler
map.on('click', e => {
  if (!clicking) return;
  const { lat, lng } = e.latlng;
  reverseGeocode(lat, lng).then(name => {
    placeMarker(clicking, lat, lng, name);
    if (clicking === 'src') {
      clicking = 'dst';
      setHint('Now click the map or search for destination');
    } else {
      clicking = null;
      computeRoute();
    }
  });
});

async function reverseGeocode(lat, lon) {
  try {
    const r = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json&accept-language=en`);
    const d = await r.json();
    return d.name || d.display_name?.split(',')[0] || '';
  } catch { return ''; }
}

async function computeRoute() {
  if (!src || !dst) return;
  showLoad(true);
  setHint('Running Dijkstra\'s algorithm…');
  try {
    const resp = await fetch('/api/route/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
      credentials: 'same-origin',
      body: JSON.stringify({
        src_lat: src.lat, src_lon: src.lon,
        dst_lat: dst.lat, dst_lon: dst.lon,
        src_name: document.getElementById('srcInput')?.value || '',
        dst_name: document.getElementById('dstInput')?.value || '',
        mode: selectedMode,
      }),
    });
    const j = await resp.json();
    showLoad(false);
    if (j.status === 'success') {
      drawRoute(j.data);
    } else {
      setHint(j.message || 'Error computing route');
    }
  } catch (e) {
    showLoad(false);
    setHint('Network error — is the server running?');
  }
}

function drawRoute(data) {
  if (routeL) map.removeLayer(routeL);
  const latlngs = data.path_coords.map(c => [c.lat, c.lon]);
  routeL = L.polyline(latlngs, { color: getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#3b82f6',
    weight: 5, opacity: .85, lineJoin: 'round', lineCap: 'round' }).addTo(map);
  map.fitBounds(routeL.getBounds(), { padding: [40, 40] });

  const km = data.total_distance_km;
  const eta = data.eta_minutes;
  document.getElementById('routeKm')?.textContent    && (document.getElementById('routeKm').textContent    = km + ' km');
  document.getElementById('routeNodes')?.textContent  && (document.getElementById('routeNodes').textContent  = data.node_count);
  document.getElementById('routeEta')?.textContent    && (document.getElementById('routeEta').textContent    = eta + ' min');
  document.getElementById('routeResult')?.style       && (document.getElementById('routeResult').style.display = 'block');

  // store for save
  window._lastRouteId    = data.route_id;
  window._lastShareToken = data.share_token;
  setHint('Route found! Click "Save" to bookmark it.');
}

function clearRoute() {
  if (srcM) map.removeLayer(srcM);
  if (dstM) map.removeLayer(dstM);
  if (routeL) map.removeLayer(routeL);
  src = dst = srcM = dstM = routeL = null;
  document.getElementById('routeResult').style.display = 'none';
  document.getElementById('srcCoord').style.display    = 'none';
  document.getElementById('dstCoord').style.display    = 'none';
  document.getElementById('srcInput').value = '';
  document.getElementById('dstInput').value = '';
  clicking = null;
  setHint('Search or click map to set start point');
}

function saveRoute() {
  if (!window._lastRouteId) return;
  const label = prompt('Name this route:', 'My Route') || 'My Route';
  fetch('/api/save-route/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    credentials: 'same-origin',
    body: JSON.stringify({ route_id: window._lastRouteId, label }),
  }).then(r => r.json()).then(d => {
    if (d.status === 'ok') setHint('Route saved to favourites! ⭐');
  });
}

function shareRoute() {
  if (!window._lastShareToken) return;
  const url = `${location.origin}/share/${window._lastShareToken}/`;
  navigator.clipboard.writeText(url).then(() => setHint('Share link copied to clipboard!'));
}

// Mode buttons
document.querySelectorAll('.mode-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    selectedMode = btn.dataset.mode;
    if (src && dst) computeRoute(); // recompute with new mode
  });
});

// Health check
async function checkHealth() {
  const dot  = document.getElementById('statusDot');
  const lbl  = document.getElementById('statusLbl');
  try {
    const r = await fetch('/api/health/', { credentials: 'same-origin' });
    const d = await r.json();
    if (d.status === 'ready') {
      dot.className = 'status-dot dot-green';
      lbl.textContent = `Graph Ready — ${(d.graph.nodes||0).toLocaleString()} nodes`;
    } else {
      dot.className = 'status-dot dot-yellow';
      const lc = d.graph.loaded_count || 0;
      const tot = d.graph.total || 5;
      lbl.textContent = `Loading districts (${lc}/${tot})…`;
      setTimeout(checkHealth, 4000);
    }
  } catch {
    dot.className = 'status-dot dot-red';
    lbl.textContent = 'Backend Offline';
    setTimeout(checkHealth, 5000);
  }
}
checkHealth();

// Build search UIs after DOM ready
document.addEventListener('DOMContentLoaded', () => {
  const srcInput   = document.getElementById('srcInput');
  const srcResults = document.getElementById('srcResults');
  const dstInput   = document.getElementById('dstInput');
  const dstResults = document.getElementById('dstResults');

  if (srcInput && srcResults) {
    buildSearchUI(srcInput, srcResults, p => {
      placeMarker('src', p.lat, p.lon, p.name);
      map.setView([p.lat, p.lon], 15);
      if (dst) computeRoute();
    });
  }
  if (dstInput && dstResults) {
    buildSearchUI(dstInput, dstResults, p => {
      placeMarker('dst', p.lat, p.lon, p.name);
      map.setView([p.lat, p.lon], 15);
      if (src) computeRoute();
    });
  }
});

setHint('Search for a place or click on the map to start');