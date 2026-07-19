// map.js — route optimizer map page

function getCsrf() {
  return document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] || '';
}

const map = L.map('map', { zoomControl: false }).setView([27.7103, 85.3222], 12);
L.control.zoom({ position: 'bottomright' }).addTo(map);

// Tile layer switcher
// Tile layer switcher — UPDATED SUBDOMAINS CONFIGURATION TO PREVENT BLANK BOXES
let tileUrl = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png';
const tileLayer = L.tileLayer(tileUrl, {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
  subdomains: 'abcd', // Default for Carto
  maxZoom: 20,
}).addTo(map);

(function () {
  const t = localStorage.getItem('ro_theme');

    // CRITICAL FIX: Explicitly drops the 'd' subdomain because OpenStreetMap only accepts a, b, or c
    tileLayer.options.subdomains = 'abc';
    tileLayer.setUrl('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');

})();

// ONE CENTRAL CORE DATA STRUCTURE FOR COGNITIVE RETENTION
let src = null, dst = null;
let srcM = null, dstM = null;
let userLocM = null, userLocCircle = null; 
let clicking = null; 
let selectedMode = 'all'; 

let activeRoutes = {
  car: { polyline: null, pulseMarker: null, color: '#3b82f6', dash: null, name: 'Driving', badgeId: 'Car' },
  bike: { polyline: null, pulseMarker: null, color: '#f59e0b', dash: '10, 10', name: 'Cycling', badgeId: 'Bike' },
  walk: { polyline: null, pulseMarker: null, color: '#10b981', dash: '3, 6', name: 'Walking', badgeId: 'Walk' }
};

const mkIcon = (color, glow) => L.divIcon({
  className: '',
  html: `<div style="width:14px;height:14px;background:${color};border-radius:50%;border:2.5px solid #fff;box-shadow:0 0 10px ${glow}"></div>`,
  iconSize: [14, 14], iconAnchor: [7, 7]
});
const srcIcon = mkIcon('#34d399','#34d399');
const dstIcon = mkIcon('#f87171','#f87171');

const mkAnimIcon = (color) => L.divIcon({
  className: 'route-pulse-marker',
  html: `<div style="width:12px;height:12px;background:${color};border-radius:50%;border:2px solid #fff;box-shadow:0 0 8px ${color}"></div>`,
  iconSize: [12, 12], iconAnchor: [6, 6]
});

const mkUserLocIcon = () => L.divIcon({
  className: 'user-location-marker-container',
  html: `<div class="gps-pulse-ring"></div><div class="gps-core-dot"></div>`,
  iconSize: [24, 24], iconAnchor: [12, 12]
});

function setHint(msg) {
  const h = document.getElementById('mapHint');
  if (h) h.textContent = msg;
}

function showLoad(v) {
  const l = document.getElementById('mapLoading');
  if (l) l.style.display = v ? 'flex' : 'none';
}

// MODIFIED TO UPDATE BOTH DATA STATE FIELDS INDEPENDENTLY WITHOUT CLEARING THE COMPANION
function placeMarker(type, lat, lon, name) {
  const cleanStr = `${lat.toFixed(6)}, ${lon.toFixed(6)}`;
  
  if (type === 'src') {
    if (srcM) map.removeLayer(srcM);
    src = { lat, lon }; // Keeps core routing system in sync
    
    srcM = L.marker([lat, lon], { icon: srcIcon }).addTo(map)
             .bindPopup(`<b style="color:#34d399">🟢 Start</b><br><small>${name||cleanStr}</small>`);
    
    const el = document.getElementById('srcCoord');
    if (el) { 
      el.querySelector('.coord-text').textContent = name || cleanStr; 
      el.style.display = 'flex'; 
    }
    const input = document.getElementById('srcInput');
    if (input) input.value = name || cleanStr;
  } else {
    if (dstM) map.removeLayer(dstM);
    dst = { lat, lon }; // Keeps core routing system in sync
    
    dstM = L.marker([lat, lon], { icon: dstIcon }).addTo(map)
             .bindPopup(`<b style="color:#f87171">🔴 End</b><br><small>${name||cleanStr}</small>`);
    
    const el = document.getElementById('dstCoord');
    if (el) { 
      el.querySelector('.coord-text').textContent = name || cleanStr; 
      el.style.display = 'flex'; 
    }
    const input = document.getElementById('dstInput');
    if (input) input.value = name || cleanStr;
  }

  // Auto-trigger calculation smoothly if BOTH variables exist
  if (src && dst) {
    computeRoute();
  }
}

// FIXED CORE CLICK EVENT HANDLER
map.on('click', e => {
  if (!clicking) return;
  const { lat, lng } = e.latlng;
  
  reverseGeocode(lat, lng).then(name => {
    placeMarker(clicking, lat, lng, name);
    releaseButtonLocks();
    clicking = null; // Instantly breaks loop so it won't force target switches
  });
});

async function reverseGeocode(lat, lon) {
  try {
    const r = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json&accept-language=en`);
    const d = await r.json();
    return d.name || d.display_name?.split(',')[0] || `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
  } catch { return `${lat.toFixed(4)}, ${lon.toFixed(4)}`; }
}

// SYSTEM INITIALIZATION LOCATOR (Plotting only tracking points, NOT overwriting selection logic)
function requestUserLocation() {
  if (!navigator.geolocation) {
    setHint("Geolocation services not supported by your browser framework.");
    return;
  }
  
navigator.geolocation.getCurrentPosition(
  async (position) => {
    const { latitude, longitude, accuracy } = position.coords;
    
    // FIX: Cap the radius at 1000 meters (1km) so it doesn't cover the whole city
    // If accuracy is missing, default to 50 meters
    const displayRadius = Math.min(accuracy || 50, 1000);
    
    if (userLocM) map.removeLayer(userLocM);
    if (userLocCircle) map.removeLayer(userLocCircle);
    
    userLocCircle = L.circle([latitude, longitude], {
      radius: displayRadius, // Use the capped radius here
      color: '#3b82f6',
      fillColor: '#3b82f6',
      fillOpacity: 0.15,
      weight: 1
    }).addTo(map);
      
      userLocM = L.marker([latitude, longitude], { icon: mkUserLocIcon() }).addTo(map)
                  .bindPopup("<b>Your Current Real-time Location</b>");
      
      map.setView([latitude, longitude], 13);
    },
    (error) => { console.warn(`Position setup skipped: ${error.message}`); },
    { enableHighAccuracy: true, timeout: 10000 }
  );
}

async function computeRoute() {
  if (!src || !dst) return;
  showLoad(true);
  setHint('Running Multi-Modal Dijkstra engine…');
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
      }),
    });
    const j = await resp.json();
    showLoad(false);
    if (j.status === 'success') {
      drawMultiRoutes(j.routes);
      window._lastRouteId    = j.route_id;
      window._lastShareToken = j.share_token;
    } else {
      setHint(j.message || 'Error computing multi-modal routes');
    }
  } catch (e) {
    showLoad(false);
    setHint('Network error — is the server running?');
  }
}

function drawMultiRoutes(routesData) {
  clearRouteLayers();
  let bounds = L.latLngBounds();
  let infoHtml = "";

  Object.keys(activeRoutes).forEach(mode => {
    const route = routesData[mode];
    if (!route || !route.path_coords || route.path_coords.length === 0) return;

    const latlngs = route.path_coords.map(c => [c.lat, c.lon]);
    const prefix = activeRoutes[mode].badgeId; 
    
    const cardEl = document.getElementById(`route${prefix}Km`)?.closest('.mode-btn') || document.querySelector(`[data-mode="${mode}"]`);
    if (cardEl) {
      cardEl.innerHTML = `<div style="text-align:center; font-size:12px; color:#fff;">
        <div>${mode === 'walk' ? '🚶 Walk' : mode === 'bike' ? '🚲 Bike' : '🚗 Car'}</div>
        <strong style="color:${activeRoutes[mode].color}; font-size:14px;">${route.eta_minutes} min</strong>
        <div style="font-size:10px; color:#9ca3af;">${route.total_distance_km} km</div>
      </div>`;
    }

// 2. Draw Polyline tracks (UPDATED FOR TRANSPARENCY & LEGIBILITY)
activeRoutes[mode].polyline = L.polyline(latlngs, { 
  color: activeRoutes[mode].color,
  weight: mode === 'car' ? 6 : 4, // Slightly adjusted width
  opacity: 0.45,                 // CRITICAL: Lowered from 0.85 to 0.45 so roads show through perfectly
  dashArray: activeRoutes[mode].dash,
  lineJoin: 'round', 
  lineCap: 'round',
  interactive: false             // Prevents the line from stealing mouse clicks from the map/roads underneath
}).addTo(map);

    bounds.extend(activeRoutes[mode].polyline.getBounds());

    if (latlngs.length > 1) {
      const pulseM = L.marker(latlngs[0], { icon: mkAnimIcon(activeRoutes[mode].color) }).addTo(map);
      activeRoutes[mode].pulseMarker = pulseM;
      animateMarkerAlongPath(pulseM, latlngs, route.speed_kmh);
    }

    infoHtml += `
      <div class="mode-summary-card">
        <div class="mode-summary-header">
          <span class="mode-title-wrapper">
            <span class="mode-indicator-dot" style="background: ${activeRoutes[mode].color};"></span>
            <strong>${activeRoutes[mode].name}</strong>
          </span>
          <span class="mode-eta-badge" style="color: ${activeRoutes[mode].color};">${route.eta_minutes} mins</span>
        </div>
        <div class="mode-metrics-row">
          <span><span class="metric-icon">📏</span> ${route.total_distance_km} km</span>
          <span><span class="metric-icon">📍</span> ${route.node_count} nodes</span>
          <span><span class="metric-icon">⚡</span> ${route.speed_kmh} km/h</span>
        </div>
      </div>
    `;
  });

  if (bounds.isValid()) {
    map.fitBounds(bounds, { padding: [40, 40] });
  }

  const container = document.getElementById('routeResult');
  if (container) {
    container.innerHTML = `
      <div class="comparison-hub-wrapper">
        <h4 class="comparison-hub-title">Multi-Modal System Pipeline</h4>
        <div class="comparison-cards-container">${infoHtml}</div>
        <div class="comparison-actions-row">
          <button onclick="saveRoute()" class="btn-action btn-save">⭐ Save</button>
          <button onclick="shareRoute()" class="btn-action btn-share">🔗 Share</button>
          <button onclick="clearRoute()" class="btn-action btn-reset">Reset</button>
        </div>
      </div>
    `;
    container.style.display = 'block';
  }

  setHint('Multi-Modal route tracks loaded completely!');
}

function animateMarkerAlongPath(marker, coords, speedKmh) {
  let currentIndex = 0;
  const baseInterval = 45; 
  const velocityModifier = Math.max(1, speedKmh / 8); 
  const durationStep = baseInterval / velocityModifier;

  function move() {
    if (!map.hasLayer(marker)) return; 
    if (currentIndex >= coords.length - 1) currentIndex = 0;

    const startPoint = coords[currentIndex];
    const endPoint = coords[currentIndex + 1];
    let step = 0;
    const totalSteps = Math.max(3, Math.round(15 / velocityModifier)); 

    function animateStep() {
      if (!map.hasLayer(marker)) return;
      step++;
      const progress = step / totalSteps;
      const currentLat = startPoint[0] + (endPoint[0] - startPoint[0]) * progress;
      const currentLon = startPoint[1] + (endPoint[1] - startPoint[1]) * progress;
      marker.setLatLng([currentLat, currentLon]);

      if (step < totalSteps) {
        setTimeout(animateStep, durationStep);
      } else {
        currentIndex++;
        setTimeout(move, durationStep * 2);
      }
    }
    animateStep();
  }
  move();
}

function clearRouteLayers() {
  Object.keys(activeRoutes).forEach(mode => {
    if (activeRoutes[mode].polyline) {
      map.removeLayer(activeRoutes[mode].polyline);
      activeRoutes[mode].polyline = null;
    }
    if (activeRoutes[mode].pulseMarker) {
      map.removeLayer(activeRoutes[mode].pulseMarker);
      activeRoutes[mode].pulseMarker = null;
    }
  });
}

function clearRoute() {
    document.getElementById('srcInput').value = '';
    document.getElementById('dstInput').value = '';
    
    const srcCoord = document.getElementById('srcCoord');
    const dstCoord = document.getElementById('dstCoord');
    if (srcCoord) srcCoord.style.display = 'none';
    if (dstCoord) dstCoord.style.display = 'none';
    
    const routeResult = document.getElementById('routeResult');
    if (routeResult) routeResult.style.display = 'none';

    if (srcM) { map.removeLayer(srcM); srcM = null; }
    if (dstM) { map.removeLayer(dstM); dstM = null; }
    
    clearRouteLayers();

    src = null;
    dst = null;
    
    setHint("Search or click map to set start point");
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

document.querySelectorAll('.mode-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    if (src && dst) computeRoute(); 
  });
});

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


// UI AUTOCOMPLETE LINK INTEGRATION (UPDATED WITH DROPDOWN OVERRIDE FIX)
document.addEventListener('DOMContentLoaded', () => {
  const srcInput   = document.getElementById('srcInput');
  const srcResults = document.getElementById('srcResults');
  const dstInput   = document.getElementById('dstInput');
  const dstResults = document.getElementById('dstResults');

  if (srcInput && srcResults) {
    buildSearchUI(srcInput, srcResults, p => {
      // CRITICAL FIX: If a map selection mode was active, cancel it immediately
      releaseButtonLocks();
      clicking = null;

      placeMarker('src', p.lat, p.lon, p.name);
      map.setView([p.lat, p.lon], 15);
    });
  }
  if (dstInput && dstResults) {
    buildSearchUI(dstInput, dstResults, p => {
      // CRITICAL FIX: If a map selection mode was active, cancel it immediately
      releaseButtonLocks();
      clicking = null;

      placeMarker('dst', p.lat, p.lon, p.name);
      map.setView([p.lat, p.lon], 15);
    });
  }

  // Draw real-time alignment dot, but don't hijack input targets!
  setTimeout(requestUserLocation, 1200);
});

// --- INTERACTIVE DEFENSE STATE MACHINES (FIXED) ---
let dynamicClickingState = {
    isAwaiting: false,
    activeButton: null,
    originalText: ""
};

function handleMapClickToggle(mode, buttonId, message) {
    // If user clicks a different map selector button, release the old button lock first
    if (dynamicClickingState.activeButton && dynamicClickingState.activeButton.id !== buttonId) {
        releaseButtonLocks();
    }

    const targetBtn = document.getElementById(buttonId);
    clicking = mode; 
    setHint(message);
    
    dynamicClickingState.isAwaiting = true;
    dynamicClickingState.activeButton = targetBtn;
    dynamicClickingState.originalText = "📌 Click on map";
    
    targetBtn.disabled = true;
    targetBtn.innerHTML = `<span>⏳ Selecting...</span>`;
    document.getElementById('map').style.cursor = 'crosshair';
}

function releaseButtonLocks() {
    if (dynamicClickingState.activeButton) {
        dynamicClickingState.activeButton.disabled = false;
        dynamicClickingState.activeButton.innerHTML = dynamicClickingState.originalText;
    }
    document.getElementById('map').style.cursor = '';
    dynamicClickingState.isAwaiting = false;
    dynamicClickingState.activeButton = null;
}

// LIVE GEOLOCATION TRIGGER ASSIGNMENT PIPELINE (NOW UNLOCKED)
function useCurrentLocation(targetField) {
    const btnId = targetField === 'src' ? 'btn-start-current' : 'btn-dest-current';
    const targetBtn = document.getElementById(btnId);
    const originalText = "📍 Current Loc";

    if (!navigator.geolocation) {
        alert("Geolocation not supported by this browser.");
        return;
    }

    // Cancel map picking mode if geolocation is chosen instead
    releaseButtonLocks();
    clicking = null;

    targetBtn.disabled = true;
    targetBtn.innerHTML = `<span>⏳ Fetching...</span>`;
    setHint("Fetching your live device coordinates...");

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            map.setView([lat, lon], 16);
            const locationName = await reverseGeocode(lat, lon);
            
            placeMarker(targetField, lat, lon, locationName || "My Location");

            targetBtn.disabled = false;
            targetBtn.innerHTML = originalText;
        },
        (error) => {
            setHint("Location capture blocked or unavailable.");
            targetBtn.disabled = false;
            targetBtn.innerHTML = originalText;
            console.error(error);
        },
        { enableHighAccuracy: true, timeout: 8000 }
    );
}

// --- NEW CONTROL: LEAFLET SHOW LOCATION BUTTON (ABOVE ZOOM) ---
const LocationControl = L.Control.extend({
    options: { position: 'bottomright' },
    onAdd: function (map) {
        const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-user-location-ctrl');
        container.style.backgroundColor = 'white';
        container.style.width = '30px';
        container.style.height = '30px';
        container.style.cursor = 'pointer';
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.justifyContent = 'center';
        container.style.fontSize = '16px';
        container.style.marginBottom = '2px'; // Leaves a gap right above the zoom control
        container.title = "Show My Location";
        container.innerHTML = "⟟";

        // Handle dark theme styling dynamically
        const t = localStorage.getItem('ro_theme') || 'midnight';
        if (t === 'midnight') {
            container.style.backgroundColor = '#1f2937';
            container.style.border = '1px solid #374151';
            container.style.color = '#fff';
        }

        L.DomEvent.on(container, 'click', function (e) {
            L.DomEvent.stopPropagation(e);
            if (userLocM) {
                map.setView(userLocM.getLatLng(), 16);
            } else {
                requestUserLocation();
            }
        });

        return container;
    }
});

// Register and inject the new location tracker control onto the map view canvas
map.addControl(new LocationControl());