# RouteOptima

**Simulation of Vehicle Transport and Route Optimization Using Dijkstra's Shortest Path First Algorithm**

RouteOptima is a web-based vehicle routing platform built for the Kathmandu Valley road network. It computes shortest paths for driving, cycling, and walking on real OpenStreetMap data using Dijkstra's algorithm, and serves the result through a Django REST API to a Leaflet.js map front end.

Built as a Final Year Capstone Project by **Group 36**, IIMS College (Taylor's University), supervised by **Nabeen Kumar Aryal**.

🔗 **Live app:** [g36capproject.up.railway.app](https://g36capproject.up.railway.app/)
🔗 Mirror: [g36capproject.vercel.app](https://g36capproject.vercel.app/)

---

## What it does

- Computes the shortest path between two locations using **Dijkstra's Shortest Path First algorithm**
- Builds a weighted road graph from real **OpenStreetMap** data via **OSMnx**
- Geocodes location names via the **Nominatim** API
- Renders the route on an interactive **Leaflet.js** map
- Persists every computed route, saved favourites, user preferences, and OTP-based account verification in **PostgreSQL**
- Exposes route history, analytics, heatmap, and leaderboard views over a REST API

## Tech stack

| Layer | Technology |
|---|---|
| Backend framework | Django 4.2 + Django REST Framework |
| Database | PostgreSQL (Supabase, production) / SQLite (local dev) |
| Graph & routing | OSMnx, NetworkX, SciPy |
| Geocoding | Nominatim (OpenStreetMap) |
| Frontend map | Leaflet.js |
| Auth | Django session authentication |
| Static files | WhiteNoise |
| App server | Gunicorn (WSGI) |
| Hosting | Railway (primary) + Vercel (mirrored domain) |

## Architecture

Three-tier design:

```
Browser (Leaflet.js UI)
        │
        ▼
Django REST API  ──►  RouteComputationService ──► NetworkX (Dijkstra) on cached OSMnx graph
        │
        ▼
PostgreSQL (Supabase)  +  Nominatim (geocoding)  +  OpenStreetMap (road data)
```

The road graph is downloaded and built once via OSMnx, then cached in memory (Singleton `GraphManager`) so subsequent route requests don't re-download or rebuild it.

## API endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/route/` | POST | Compute shortest route (car/bike/walk) between two coordinates |
| `/api/health/` | GET | Backend + graph readiness check |
| `/api/history/` | GET | Authenticated user's recent route logs |
| `/api/analytics/` | GET | Aggregated personal route statistics |
| `/api/save-route/` | POST | Save a computed route as a named favourite |
| `/api/saved-routes/` | GET | List the authenticated user's saved routes |
| `/api/delete-saved/<id>/` | DELETE | Remove a saved route |
| `/api/heatmap-data/` | GET | Coordinate density data for heatmap overlay |
| `/api/leaderboard-data/` | GET | Top users by total distance computed |
| `/api/set-theme/` | POST | Update the authenticated user's UI preference |

Full request/response examples: see `/docs/` on the [live site](https://g36capproject.up.railway.app/docs/).

## Project structure

```
route_optimizer/
├── backend/
│   ├── core/            # Django project settings, URLs, WSGI/ASGI
│   ├── routing/         # Main app — models, views, serializers, graph engine
│   │   ├── models.py         # RouteLog, SavedRoute, UserPreference, UserOTP
│   │   ├── views.py          # API views
│   │   ├── graph_manager.py  # Singleton OSMnx graph cache
│   │   ├── route_engine.py   # Dijkstra route computation service
│   │   └── serializers.py
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example       # Environment variable template (placeholders only)
├── build.sh                # Railway/Render build: install, collectstatic, migrate
├── railway.json             # Railway deploy config (Gunicorn start command)
└── vercel.json               # Vercel mirror deploy config
```

## Local setup

```bash
# 1. Clone
git clone https://github.com/Sohit-Giri/cappropject.git
cd cappropject/backend

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# then fill in .env with your own values — never commit real secrets:
#   SECRET_KEY=
#   DEBUG=True
#   ALLOWED_HOSTS=localhost,127.0.0.1
#   DB_NAME= / DB_USER= / DB_PASSWORD= / DB_HOST= / DB_PORT=
#   EMAIL_HOST_USER= / EMAIL_HOST_PASSWORD=

# 5. Run migrations
python manage.py migrate

# 6. Start the dev server
python manage.py runserver
```

Without a configured `DB_*` connection, the app falls back to local SQLite.

## Deployment

- **Railway** (primary): persistent Gunicorn WSGI container. Deploy config in `railway.json`; `build.sh` runs `pip install`, `collectstatic`, and `migrate` before the app starts.
- **Vercel** (mirror): same codebase, mirrored domain, configured via `vercel.json`.
- **Database**: PostgreSQL hosted on Supabase in production. Connection string and all secrets are read from environment variables (12-factor config) — never hardcoded.

## Team — Group 36

| Name | Role |
|---|---|
| Sudip KC | Project Manager & Backend Engineering Lead |
| Sohit Giri | Database Developer & Server Deployment Manager |
| Muskan Khadka | Full-Stack Developer (Core Backend Engineer) |
| Mahima Parajuli | Frontend Engineer, GIS & Map Modeler |
| Apekshya Basnyat | Frontend Developer, Algorithm Implementation & QA Software Tester |

Supervised by **Nabeen Kumar Aryal**.

## Scope & limitations

This is an academic simulation tool. It intentionally does **not** include real-time traffic, live GPS navigation, or commercialization features — the goal is a deterministic, reproducible, and transparent routing algorithm for research and teaching, as an alternative to black-box commercial routers.

## License

Academic capstone project — IIMS College / Taylor's University, 2026.
