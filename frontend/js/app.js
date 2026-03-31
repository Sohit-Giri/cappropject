// frontend/js/app.js

// This automatically uses whatever address you typed in the browser (localhost or 127.0.0.1)
const API = window.location.origin + '/api';
// ── Map initialisation ────────────────────────────────────────────────
const map = L.map('map', { zoomControl: true }).setView([27.7103, 85.3222], 13);

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  attribution: '© CartoDB © OpenStreetMap',
  subdomains: 'abcd', maxZoom: 19
}).addTo(map);

setTimeout(() => { map.invalidateSize(); }, 100);
// ── State ─────────────────────────────────────────────────────────────
let srcLatLng = null, dstLatLng = null;
let srcMarker = null, dstMarker = null, routeLayer = null;
let clickState = 'src';  // 'src' or 'dst'

// ── Custom icons ──────────────────────────────────────────────────────
// ── Custom icons ──────────────────────────────────────────────────────
const iconSrc = L.divIcon({ 
  className: '', 
  html: `<div style="background:#56d364;width:12px;height:12px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 8px rgba(86,211,100,0.5)"></div>`,
  iconSize: [16, 16], 
  iconAnchor: [8, 8] 
});

const iconDst = L.divIcon({ 
  className: '', 
  html: `<div style="background:#ff6b6b;width:12px;height:12px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 8px rgba(255,107,107,0.5)"></div>`,
  iconSize: [16, 16], 
  iconAnchor: [8, 8] 
});

// ── Map click handler ─────────────────────────────────────────────────
map.on('click', (e) => {
  const { lat, lng } = e.latlng;

  if (clickState === 'src') {
    if (srcMarker) map.removeLayer(srcMarker);
    srcLatLng = { lat, lng };
    srcMarker = L.marker([lat, lng], { icon: iconSrc })
      .bindPopup('Start').addTo(map);
    document.getElementById('srcCoord').querySelector('.coord-text').textContent =
      `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
    document.getElementById('coordsPanel').style.display = 'block';
    updateHint('Now click to set your destination');
    clickState = 'dst';

  } else {
    if (dstMarker) map.removeLayer(dstMarker);
    dstLatLng = { lat, lng };
    dstMarker = L.marker([lat, lng], { icon: iconDst })
      .bindPopup('End').addTo(map);
    document.getElementById('dstCoord').querySelector('.coord-text').textContent =
      `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
    computeRoute();
    clickState = 'src';
  }
});

// ── Route computation ─────────────────────────────────────────────────
async function computeRoute() {
  if (!srcLatLng || !dstLatLng) return;
  showLoading(true);
  updateHint('Computing shortest path...');

  try {
    const res = await fetch(`${API}/route/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        src_lat: srcLatLng.lat, src_lon: srcLatLng.lng,
        dst_lat: dstLatLng.lat, dst_lon: dstLatLng.lng,
      })
    });

    const json = await res.json();

    if (!res.ok || json.status === 'error') {
      updateHint(json.message || 'Error computing route');
      showLoading(false);
      return;
    }

    const { path_coords, total_distance_km, node_count } = json.data;

    // Draw polyline
    if (routeLayer) map.removeLayer(routeLayer);
    const latlngs = path_coords.map(p => [p.lat, p.lon]);
    routeLayer = L.polyline(latlngs, {
      color: '#2E75B6', weight: 4, opacity: .9,
      dashArray: null
    }).addTo(map);

    // Fit map to route
    map.fitBounds(routeLayer.getBounds(), { padding: [40, 40] });

    // Update sidebar
    document.getElementById('metricDist').textContent = total_distance_km;
    document.getElementById('metricNodes').textContent = node_count;
    document.getElementById('resultPanel').style.display = 'block';
    updateHint(`Route found: ${total_distance_km} km through ${node_count} nodes`);
    loadHistory();

  } catch (err) {
    updateHint('Connection error — is the backend running?');
  } finally {
    showLoading(false);
  }
}

// ── UI helpers ────────────────────────────────────────────────────────
function resetMap() {
  if (srcMarker) map.removeLayer(srcMarker);
  if (dstMarker) map.removeLayer(dstMarker);
  if (routeLayer) map.removeLayer(routeLayer);
  srcLatLng = dstLatLng = srcMarker = dstMarker = routeLayer = null;
  clickState = 'src';
  document.getElementById('resultPanel').style.display = 'none';
  document.getElementById('coordsPanel').style.display = 'none';
  updateHint('Click anywhere on the map to set your starting point');
}

function updateHint(msg) {
  document.getElementById('mapHint').textContent = msg;
}
function showLoading(v) {
  document.getElementById('loadingOverlay').style.display = v ? 'flex' : 'none';
}

// ── History ───────────────────────────────────────────────────────────
async function loadHistory() {
  try {
    const res = await fetch(`${API}/history/`);
    const logs = await res.json();
    const list = document.getElementById('historyList');
    list.innerHTML = logs.slice(0, 8).map(l =>
      `
${l.path_distance_km} km  |  ${l.node_count} nodes
`
    ).join('');
  } catch(_) {}
}

// ── Health check / graph info ─────────────────────────────────────────
async function checkHealth() {
  const pill = document.getElementById('statusPill');
  try {
    const res = await fetch(`${API}/health/`);
    const json = await res.json();
    if (json.status === 'ready') {
      pill.textContent = 'Ready';
      pill.className = 'status-pill';
      document.getElementById('infoPlace').textContent  = json.graph.place || '—';
      document.getElementById('infoNodes').textContent  = json.graph.nodes?.toLocaleString() || '—';
      document.getElementById('infoEdges').textContent  = json.graph.edges?.toLocaleString() || '—';
      loadHistory();
    } else {
      pill.textContent = 'Loading graph...';
      pill.className = 'status-pill loading';
      setTimeout(checkHealth, 5000);
    }
  } catch(_) {
    pill.textContent = 'Backend offline';
    pill.className = 'status-pill error';
    setTimeout(checkHealth, 8000);
  }
}

checkHealth();