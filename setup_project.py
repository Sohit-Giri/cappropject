#!/usr/bin/env python3
"""
RouteOptima v2 — Complete Project Setup
Run from inside your project folder:  python setup_project.py
Districts: Kathmandu · Bhaktapur · Lalitpur · Nuwakot · Dhading
"""
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(BASE, 'backend')

def w(rel, txt):
    p = os.path.join(B, rel) if not os.path.isabs(rel) else rel
    os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(txt.lstrip('\n'))
    print(f"  ✓  {rel}")

T  = os.path.join(B, 'routing', 'templates', 'routing')
S  = os.path.join(B, 'routing', 'static',    'routing')

# ─────────────────────────────────────────────── ROOT DEPLOYMENT FILES ───────
w(os.path.join(BASE, 'vercel.json'), """{
  "version": 2,
  "builds": [
    { "src": "backend/core/wsgi.py", "use": "@vercel/python" },
    { "src": "backend/staticfiles/**", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/static/(.*)", "dest": "/backend/staticfiles/$1" },
    { "src": "/(.*)",        "dest": "backend/core/wsgi.py"    }
  ]
}
""")

w(os.path.join(BASE, 'requirements.txt'), """
django>=4.2,<5.0
djangorestframework>=3.14
django-cors-headers>=4.3
psycopg2-binary>=2.9
osmnx>=1.9
networkx>=3.2
scipy>=1.11
python-dotenv>=1.0
gunicorn>=21.2
whitenoise>=6.6
""")

w(os.path.join(BASE, '.env.example'), """
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app
DB_NAME=fyp_n7gx
DB_USER=fyp_n7gx_user
DB_PASSWORD=F3bhOrPukM6SmdkauOWuuFstRSsUArBN
DB_HOST=dpg-d75pgdp4tr6s73cbra3g-a.ohio-postgres.render.com
DB_PORT=5432
EMAIL_HOST_USER=negativezero48@gmail.com
EMAIL_HOST_PASSWORD=ytsb nbhs znjs uiby
""")

w(os.path.join(BASE, 'build_files.sh'), """#!/usr/bin/env bash
set -e
pip install -r requirements.txt
cd backend
python manage.py collectstatic --no-input
python manage.py migrate --no-input
""")

w(os.path.join(BASE, '.gitignore'), """
__pycache__/
*.pyc
*.pyo
*.pyd
db.sqlite3
*.env
.env
graph_cache/
staticfiles/
media/
node_modules/
.DS_Store
*.log
""")

# ─────────────────────────────────────────────── DJANGO CORE ─────────────────
w('manage.py', """
#!/usr/bin/env python
import os, sys
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
if __name__ == '__main__':
    main()
""")

w('core/__init__.py', '')
w('routing/__init__.py', '')
w('routing/migrations/__init__.py', '')

w('core/wsgi.py', """
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_wsgi_application()
app = application
""")

w('core/settings.py', """
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-routeoptima-v2-dev-key-2026')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'routing.apps.RoutingConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.environ.get('DB_NAME',     'fyp_n7gx'),
        'USER':     os.environ.get('DB_USER',     'fyp_n7gx_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'F3bhOrPukM6SmdkauOWuuFstRSsUArBN'),
        'HOST':     os.environ.get('DB_HOST',     'dpg-d75pgdp4tr6s73cbra3g-a.ohio-postgres.render.com'),
        'PORT':     os.environ.get('DB_PORT',     '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True

GRAPH_DISTRICTS = [
    'Kathmandu, Bagmati Province, Nepal',
    'Bhaktapur, Bagmati Province, Nepal',
    'Lalitpur, Bagmati Province, Nepal',
    'Nuwakot, Bagmati Province, Nepal',
    'Dhading, Bagmati Province, Nepal',
]
GRAPH_CACHE_DIR = BASE_DIR / 'graph_cache'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.SessionAuthentication'],
}

# Email
EMAIL_BACKEND      = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST         = 'smtp.gmail.com'
EMAIL_PORT         = 587
EMAIL_USE_TLS      = True
EMAIL_HOST_USER    = os.environ.get('EMAIL_HOST_USER',    'negativezero48@gmail.com')
EMAIL_HOST_PASSWORD= os.environ.get('EMAIL_HOST_PASSWORD','ytsb nbhs znjs uiby')
DEFAULT_FROM_EMAIL = f'RouteOptima <{EMAIL_HOST_USER}>'
""")

w('core/urls.py', """
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',   include('routing.api_urls')),
    path('',       include('routing.urls')),
]
""")

# ─────────────────────────────────────────────── ROUTING APP ─────────────────
w('routing/apps.py', """
from django.apps import AppConfig
import threading, logging
logger = logging.getLogger(__name__)

class RoutingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'routing'

    def ready(self):
        import sys
        if 'runserver' not in sys.argv and 'gunicorn' not in sys.argv[0]:
            return
        def _load():
            try:
                from django.conf import settings
                from .graph_manager import GraphManager
                gm = GraphManager.get_instance()
                gm.load_districts(
                    districts=list(settings.GRAPH_DISTRICTS),
                    cache_dir=str(settings.GRAPH_CACHE_DIR)
                )
            except Exception as e:
                logger.error(f'Graph load error: {e}')
        threading.Thread(target=_load, daemon=True).start()
""")

w('routing/models.py', """
from django.db import models
from django.contrib.auth.models import User
import uuid

class RouteLog(models.Model):
    user             = models.ForeignKey(User, on_delete=models.CASCADE,
                                         related_name='routes', null=True, blank=True)
    src_name         = models.CharField(max_length=255, blank=True, default='')
    dst_name         = models.CharField(max_length=255, blank=True, default='')
    src_lat          = models.FloatField()
    src_lon          = models.FloatField()
    dst_lat          = models.FloatField()
    dst_lon          = models.FloatField()
    src_node         = models.BigIntegerField()
    dst_node         = models.BigIntegerField()
    path_distance_m  = models.FloatField()
    path_distance_km = models.FloatField()
    node_count       = models.IntegerField()
    computed_at      = models.DateTimeField(auto_now_add=True)
    share_token      = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        ordering = ['-computed_at']

    def __str__(self):
        return f'Route {self.id} | {self.path_distance_km} km'


class SavedRoute(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_routes')
    route_log  = models.ForeignKey(RouteLog, on_delete=models.CASCADE, related_name='saves')
    label      = models.CharField(max_length=100)
    saved_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-saved_at']

    def __str__(self):
        return f'{self.label} — {self.user.username}'


class UserPreference(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    theme = models.CharField(max_length=30, default='midnight')
    speed_mode = models.CharField(max_length=10, default='car',
                                  choices=[('walk','Walking'),('bike','Bicycle'),('car','Car')])

    def __str__(self):
        return f'{self.user.username} prefs'
""")

w('routing/admin.py', """
from django.contrib import admin
from .models import RouteLog, SavedRoute, UserPreference

@admin.register(RouteLog)
class RouteLogAdmin(admin.ModelAdmin):
    list_display  = ['id','user','src_name','dst_name','path_distance_km','computed_at']
    list_filter   = ['computed_at']
    search_fields = ['user__username','src_name','dst_name']

@admin.register(SavedRoute)
class SavedRouteAdmin(admin.ModelAdmin):
    list_display = ['label','user','saved_at']

@admin.register(UserPreference)
class UserPrefAdmin(admin.ModelAdmin):
    list_display = ['user','theme','speed_mode']
""")

w('routing/graph_manager.py', """
import os, logging
import networkx as nx
logger = logging.getLogger(__name__)

class GraphManager:
    _instance = None
    _graph    = None
    _districts = []
    _loaded_count = 0

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_districts(self, districts, cache_dir='graph_cache'):
        import osmnx as ox
        self._districts = districts
        os.makedirs(cache_dir, exist_ok=True)
        graphs = []
        for place in districts:
            safe = place.replace(',','').replace(' ','_').replace('/','_').lower()[:50]
            path = os.path.join(cache_dir, f'{safe}.graphml')
            try:
                if os.path.exists(path):
                    logger.info(f'Loading cached: {place}')
                    g = ox.load_graphml(path)
                else:
                    logger.info(f'Downloading: {place} ...')
                    g = ox.graph_from_place(place, network_type='drive')
                    ox.save_graphml(g, path)
                    logger.info(f'Cached: {place}')
                graphs.append(g)
                self._loaded_count += 1
                logger.info(f'Loaded {self._loaded_count}/{len(districts)} districts')
            except Exception as e:
                logger.warning(f'Skipping {place}: {e}')

        if graphs:
            self._graph = nx.compose_all(graphs) if len(graphs) > 1 else graphs[0]
            logger.info(f'Combined graph: {len(self._graph.nodes)} nodes, {len(self._graph.edges)} edges')
        else:
            logger.error('No district graphs could be loaded!')

    def get_nearest_node(self, lat, lon):
        import osmnx as ox
        if self._graph is None:
            raise RuntimeError('Graph not loaded yet')
        return ox.nearest_nodes(self._graph, X=lon, Y=lat)

    def get_graph(self):
        return self._graph

    def is_loaded(self):
        return self._graph is not None

    def get_info(self):
        if not self.is_loaded():
            loaded = self._loaded_count
            total  = len(self._districts)
            return {'loaded': False, 'message': f'Loading districts ({loaded}/{total})...',
                    'loaded_count': loaded, 'total': total}
        return {
            'loaded':    True,
            'districts': self._districts,
            'nodes':     len(self._graph.nodes),
            'edges':     len(self._graph.edges),
            'loaded_count': self._loaded_count,
            'total':     len(self._districts),
        }
""")

w('routing/route_engine.py', """
import networkx as nx
import logging
from .graph_manager import GraphManager
logger = logging.getLogger(__name__)

SPEED_KMH = {'walk': 5, 'bike': 15, 'car': 40}

class RouteEngine:
    def __init__(self):
        self.gm = GraphManager.get_instance()

    def compute_shortest_path(self, src, dst, mode='car'):
        g = self.gm.get_graph()
        if g is None:
            raise RuntimeError('Graph unavailable')
        try:
            path = nx.shortest_path(g, src, dst, weight='length', method='dijkstra')
            dist = nx.shortest_path_length(g, src, dst, weight='length', method='dijkstra')
        except nx.NetworkXNoPath:
            return None
        except nx.NodeNotFound as e:
            raise ValueError(str(e))

        coords = []
        for n in path:
            d = g.nodes[n]
            coords.append({'lat': round(d['y'], 6), 'lon': round(d['x'], 6), 'node_id': str(n)})

        dist_km   = round(dist / 1000, 3)
        speed_kmh = SPEED_KMH.get(mode, 40)
        eta_min   = round((dist_km / speed_kmh) * 60, 1)

        return {
            'path_coords':           coords,
            'total_distance_meters': round(dist, 2),
            'total_distance_km':     dist_km,
            'node_count':            len(path),
            'eta_minutes':           eta_min,
            'mode':                  mode,
            'speed_kmh':             speed_kmh,
        }
""")

w('routing/serializers.py', """
from rest_framework import serializers
from .models import RouteLog, SavedRoute

class RouteRequestSerializer(serializers.Serializer):
    src_lat  = serializers.FloatField()
    src_lon  = serializers.FloatField()
    dst_lat  = serializers.FloatField()
    dst_lon  = serializers.FloatField()
    src_name = serializers.CharField(required=False, allow_blank=True, default='')
    dst_name = serializers.CharField(required=False, allow_blank=True, default='')
    mode     = serializers.ChoiceField(choices=['walk','bike','car'], default='car')

class RouteLogSerializer(serializers.ModelSerializer):
    class Meta:
        model  = RouteLog
        fields = '__all__'

class SavedRouteSerializer(serializers.ModelSerializer):
    route_log = RouteLogSerializer(read_only=True)
    class Meta:
        model  = SavedRoute
        fields = '__all__'
""")

w('routing/urls.py', """
from django.urls import path
from . import views

urlpatterns = [
    path('',              views.landing,          name='landing'),
    path('login/',        views.login_view,        name='login'),
    path('register/',     views.register_view,     name='register'),
    path('logout/',       views.logout_view,       name='logout'),
    path('dashboard/',    views.dashboard,         name='dashboard'),
    path('map/',          views.map_view,          name='map'),
    path('history/',      views.history_view,      name='history'),
    path('analytics/',    views.analytics_view,    name='analytics'),
    path('algorithm/',    views.algorithm_view,    name='algorithm'),
    path('graph/',        views.graph_explorer,    name='graph'),
    path('compare/',      views.compare_view,      name='compare'),
    path('profile/',      views.profile_view,      name='profile'),
    path('settings/',     views.settings_view,     name='settings'),
    path('about/',        views.about_view,        name='about'),
    path('docs/',         views.docs_view,         name='docs'),
    path('benchmark/',    views.benchmark_view,    name='benchmark'),
    path('nodes/',        views.nodes_view,        name='nodes'),
    path('simulation/',   views.simulation_view,   name='simulation'),
    path('export/',       views.export_view,       name='export'),
    path('help/',         views.help_view,         name='help'),
    path('team/',         views.team_view,         name='team'),
    path('report/',       views.report_view,       name='report'),
    # Surprise features
    path('favorites/',    views.favorites_view,    name='favorites'),
    path('share/<uuid:token>/', views.share_view,  name='share'),
    path('eta/',          views.eta_view,          name='eta'),
    path('heatmap/',      views.heatmap_view,      name='heatmap'),
    path('leaderboard/',  views.leaderboard_view,  name='leaderboard'),
    path('replay/<int:pk>/', views.replay_view,    name='replay'),
]
""")

w('routing/api_urls.py', """
from django.urls import path
from . import views

urlpatterns = [
    path('route/',          views.RouteAPIView.as_view(),      name='api-route'),
    path('graph/',          views.GraphInfoAPIView.as_view(),   name='api-graph'),
    path('health/',         views.HealthAPIView.as_view(),      name='api-health'),
    path('history/',        views.HistoryAPIView.as_view(),     name='api-history'),
    path('analytics/',      views.AnalyticsAPIView.as_view(),   name='api-analytics'),
    path('save-route/',     views.SaveRouteAPIView.as_view(),   name='api-save-route'),
    path('saved-routes/',   views.SavedRoutesAPIView.as_view(), name='api-saved-routes'),
    path('delete-saved/<int:pk>/', views.DeleteSavedAPIView.as_view(), name='api-delete-saved'),
    path('heatmap-data/',   views.HeatmapDataAPIView.as_view(), name='api-heatmap'),
    path('leaderboard-data/', views.LeaderboardAPIView.as_view(), name='api-leaderboard'),
    path('set-theme/',      views.SetThemeAPIView.as_view(),    name='api-set-theme'),
]
""")

w('routing/views.py', """
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings as conf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import csv, json
from .models import RouteLog, SavedRoute, UserPreference
from .serializers import (RouteRequestSerializer, RouteLogSerializer,
                           SavedRouteSerializer)
from .graph_manager import GraphManager
from .route_engine import RouteEngine


def _get_pref(user):
    pref, _ = UserPreference.objects.get_or_create(user=user)
    return pref


def _send_welcome(user):
    try:
        send_mail(
            subject='Welcome to RouteOptima! 🗺️',
            message=(
                f'Hi {user.first_name or user.username},\n\n'
                'Welcome to RouteOptima — Nepal\'s smart route optimizer!\n\n'
                'You can now:\n'
                '  • Find shortest paths across Kathmandu Valley + Nuwakot & Dhading\n'
                '  • Search any place by name — tea shops, hospitals, schools\n'
                '  • Compare two routes side by side\n'
                '  • Save favourite routes and share them with friends\n\n'
                'Open the app: https://your-app.vercel.app/dashboard/\n\n'
                '— RouteOptima Team\n'
                '  IIMS College · Group 36 · 2026'
            ),
            from_email=conf.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email] if user.email else [],
            fail_silently=True,
        )
    except Exception:
        pass


# ── Public pages ──────────────────────────────────────────────────────────────
def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'routing/landing.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}! 👋')
            return redirect(request.GET.get('next', '/dashboard/'))
        messages.error(request, 'Invalid username or password.')
    return render(request, 'routing/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        u, e = request.POST.get('username','').strip(), request.POST.get('email','').strip()
        fn   = request.POST.get('first_name','').strip()
        p1, p2 = request.POST.get('password1',''), request.POST.get('password2','')
        if not u:
            messages.error(request, 'Username is required.')
        elif p1 != p2:
            messages.error(request, 'Passwords do not match.')
        elif len(p1) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        elif User.objects.filter(username=u).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=u, email=e, password=p1,
                                            first_name=fn)
            UserPreference.objects.create(user=user)
            login(request, user)
            _send_welcome(user)
            messages.success(request, f'Account created! Welcome, {fn or u}! 🎉')
            return redirect('dashboard')
    return render(request, 'routing/register.html')


def logout_view(request):
    logout(request)
    return redirect('landing')


def about_view(request):   return render(request, 'routing/about.html')
def docs_view(request):    return render(request, 'routing/docs.html')
def help_view(request):    return render(request, 'routing/help.html')
def team_view(request):    return render(request, 'routing/team.html')


def share_view(request, token):
    route = get_object_or_404(RouteLog, share_token=token)
    return render(request, 'routing/share.html', {'route': route})


# ── Protected pages ───────────────────────────────────────────────────────────
@login_required
def dashboard(request):
    qs       = RouteLog.objects.filter(user=request.user)
    total    = qs.count()
    total_km = round(sum(r.path_distance_km for r in qs), 2)
    avg_km   = round(total_km / total, 2) if total else 0
    saved    = SavedRoute.objects.filter(user=request.user).count()
    gm       = GraphManager.get_instance()
    return render(request, 'routing/dashboard.html', {
        'total_routes': total, 'total_km': total_km,
        'avg_km': avg_km, 'saved_count': saved,
        'recent_routes': qs[:6],
        'graph_info': gm.get_info(),
    })


@login_required
def map_view(request):
    pref = _get_pref(request.user)
    return render(request, 'routing/map.html', {'mode': pref.speed_mode})


@login_required
def history_view(request):
    routes = RouteLog.objects.filter(user=request.user)
    return render(request, 'routing/history.html', {'routes': routes})


@login_required
def analytics_view(request):
    return render(request, 'routing/analytics.html')


@login_required
def algorithm_view(request):
    return render(request, 'routing/algorithm.html')


@login_required
def graph_explorer(request):
    return render(request, 'routing/graph_explorer.html',
                  {'graph_info': GraphManager.get_instance().get_info()})


@login_required
def compare_view(request):
    return render(request, 'routing/compare.html')


@login_required
def profile_view(request):
    if request.method == 'POST':
        u = request.user
        u.email      = request.POST.get('email',      u.email)
        u.first_name = request.POST.get('first_name', u.first_name)
        u.last_name  = request.POST.get('last_name',  u.last_name)
        u.save()
        messages.success(request, 'Profile updated.')
    total = RouteLog.objects.filter(user=request.user).count()
    return render(request, 'routing/profile.html', {'total_routes': total})


@login_required
def settings_view(request):
    pref = _get_pref(request.user)
    if request.method == 'POST':
        pref.theme      = request.POST.get('theme', pref.theme)
        pref.speed_mode = request.POST.get('speed_mode', pref.speed_mode)
        pref.save()
        messages.success(request, 'Settings saved.')
    return render(request, 'routing/settings.html', {'pref': pref})


@login_required
def benchmark_view(request):
    return render(request, 'routing/benchmark.html')


@login_required
def nodes_view(request):
    return render(request, 'routing/nodes.html',
                  {'graph_info': GraphManager.get_instance().get_info()})


@login_required
def simulation_view(request):
    return render(request, 'routing/simulation.html')


@login_required
def report_view(request):
    qs       = RouteLog.objects.filter(user=request.user)
    total    = qs.count()
    total_km = round(sum(r.path_distance_km for r in qs), 2)
    avg_km   = round(total_km / total, 2) if total else 0
    max_r    = qs.order_by('-path_distance_km').first()
    return render(request, 'routing/report.html', {
        'total': total, 'total_km': total_km,
        'avg_km': avg_km, 'max_route': max_r,
        'routes': qs[:20],
    })


@login_required
def export_view(request):
    fmt    = request.GET.get('format', '')
    routes = RouteLog.objects.filter(user=request.user)
    if fmt == 'csv':
        resp = HttpResponse(content_type='text/csv')
        resp['Content-Disposition'] = 'attachment; filename="routes.csv"'
        w2 = csv.writer(resp)
        w2.writerow(['ID','From','To','Distance (km)','Nodes','Date'])
        for r in routes:
            w2.writerow([r.id, r.src_name or f'{r.src_lat:.4f},{r.src_lon:.4f}',
                         r.dst_name or f'{r.dst_lat:.4f},{r.dst_lon:.4f}',
                         r.path_distance_km, r.node_count, r.computed_at])
        return resp
    if fmt == 'json':
        data = list(routes.values())
        resp = HttpResponse(json.dumps(data, default=str), content_type='application/json')
        resp['Content-Disposition'] = 'attachment; filename="routes.json"'
        return resp
    return render(request, 'routing/export.html', {'routes': routes})


# ── Surprise Feature Views ────────────────────────────────────────────────────
@login_required
def favorites_view(request):
    saved = SavedRoute.objects.filter(user=request.user).select_related('route_log')
    return render(request, 'routing/favorites.html', {'saved': saved})


@login_required
def eta_view(request):
    return render(request, 'routing/eta.html')


@login_required
def heatmap_view(request):
    return render(request, 'routing/heatmap.html')


@login_required
def leaderboard_view(request):
    return render(request, 'routing/leaderboard.html')


@login_required
def replay_view(request, pk):
    route = get_object_or_404(RouteLog, pk=pk, user=request.user)
    return render(request, 'routing/replay.html', {'route': route})


# ── REST API ──────────────────────────────────────────────────────────────────
class RouteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = RouteRequestSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'status': 'error', 'errors': ser.errors}, status=400)
        gm = GraphManager.get_instance()
        if not gm.is_loaded():
            return Response({'status': 'error',
                             'message': 'Graph loading. Retry shortly.'}, status=503)
        d = ser.validated_data
        try:
            sn = gm.get_nearest_node(d['src_lat'], d['src_lon'])
            dn = gm.get_nearest_node(d['dst_lat'], d['dst_lon'])
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)
        if sn == dn:
            return Response({'status': 'error',
                             'message': 'Source and destination are too close.'}, status=400)
        engine = RouteEngine()
        try:
            result = engine.compute_shortest_path(sn, dn, mode=d.get('mode','car'))
        except (ValueError, RuntimeError) as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)
        if result is None:
            return Response({'status': 'error',
                             'message': 'No drivable path found between these points.'}, status=404)
        log = RouteLog.objects.create(
            user=request.user,
            src_name=d.get('src_name',''), dst_name=d.get('dst_name',''),
            src_lat=d['src_lat'],  src_lon=d['src_lon'],
            dst_lat=d['dst_lat'],  dst_lon=d['dst_lon'],
            src_node=sn, dst_node=dn,
            path_distance_m=result['total_distance_meters'],
            path_distance_km=result['total_distance_km'],
            node_count=result['node_count'],
        )
        result['route_id']    = log.id
        result['share_token'] = str(log.share_token)
        return Response({'status': 'success', 'data': result})


class GraphInfoAPIView(APIView):
    def get(self, request):
        return Response(GraphManager.get_instance().get_info())


class HealthAPIView(APIView):
    def get(self, request):
        gm = GraphManager.get_instance()
        return Response({
            'status': 'ready' if gm.is_loaded() else 'loading',
            'graph':  gm.get_info(),
        })


class HistoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logs = RouteLog.objects.filter(user=request.user)[:20]
        return Response(RouteLogSerializer(logs, many=True).data)


class AnalyticsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.db.models import Avg, Count, Sum
        from datetime import date, timedelta
        routes = RouteLog.objects.filter(user=request.user)
        stats  = routes.aggregate(
            total=Count('id'), avg_dist=Avg('path_distance_km'),
            total_dist=Sum('path_distance_km'), avg_nodes=Avg('node_count'),
        )
        today = date.today()
        daily = []
        for i in range(13, -1, -1):
            dd  = today - timedelta(days=i)
            cnt = routes.filter(computed_at__date=dd).count()
            daily.append({'date': str(dd), 'count': cnt})
        return Response({'stats': stats, 'daily': daily})


class SaveRouteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        route_id = request.data.get('route_id')
        label    = request.data.get('label', 'My Route')
        try:
            log = RouteLog.objects.get(pk=route_id, user=request.user)
        except RouteLog.DoesNotExist:
            return Response({'status': 'error', 'message': 'Route not found'}, status=404)
        sr = SavedRoute.objects.create(user=request.user, route_log=log, label=label)
        return Response({'status': 'ok', 'saved_id': sr.id})


class SavedRoutesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        saved = SavedRoute.objects.filter(user=request.user).select_related('route_log')[:30]
        return Response(SavedRouteSerializer(saved, many=True).data)


class DeleteSavedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        SavedRoute.objects.filter(pk=pk, user=request.user).delete()
        return Response({'status': 'ok'})


class HeatmapDataAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.db.models import Count
        logs = RouteLog.objects.all()[:500]
        pts  = [[r.src_lat, r.src_lon, 0.5] for r in logs] + \
               [[r.dst_lat, r.dst_lon, 0.5] for r in logs]
        return Response({'points': pts})


class LeaderboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.db.models import Sum, Count
        users = (RouteLog.objects
                 .values('user__username')
                 .annotate(total_km=Sum('path_distance_km'), routes=Count('id'))
                 .order_by('-total_km')[:10])
        return Response({'leaderboard': list(users)})


class SetThemeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pref = _get_pref(request.user)
        pref.theme = request.data.get('theme', pref.theme)
        pref.save()
        return Response({'status': 'ok', 'theme': pref.theme})
""")

# ═══════════════════════════════════════════════ CSS ═════════════════════════
os.makedirs(os.path.join(S, 'css'), exist_ok=True)
w(os.path.join(S, 'css', 'style.css'), """
/* ═══ RESET & THEMES ════════════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Midnight (default dark blue) ── */
:root, [data-theme="midnight"] {
  --bg0:#060d1a; --bg1:#0c1830; --bg2:#102040; --bg3:#162d56; --bg4:#1e3f78;
  --accent:#3b82f6; --accent2:#60a5fa; --accent3:#1d4ed8;
  --text1:#e8f0fe; --text2:#94a8c7; --text3:#5a7aaa;
  --green:#34d399; --red:#f87171; --yellow:#fbbf24; --purple:#a78bfa;
  --border:rgba(59,130,246,.22); --card-glow:rgba(59,130,246,.08);
  --sidebar-bg:rgba(12,24,48,.95);
}
[data-theme="obsidian"] {
  --bg0:#0a0812; --bg1:#130d20; --bg2:#1a1030; --bg3:#221445; --bg4:#2d1a60;
  --accent:#8b5cf6; --accent2:#a78bfa; --accent3:#6d28d9;
  --text1:#ede9fe; --text2:#a08cc0; --text3:#6b56a0;
  --green:#34d399; --red:#f87171; --yellow:#fbbf24; --purple:#c4b5fd;
  --border:rgba(139,92,246,.22); --card-glow:rgba(139,92,246,.08);
  --sidebar-bg:rgba(19,13,32,.95);
}
[data-theme="emerald"] {
  --bg0:#050f0a; --bg1:#081a10; --bg2:#0c2418; --bg3:#103020; --bg4:#15422c;
  --accent:#10b981; --accent2:#34d399; --accent3:#059669;
  --text1:#d1fae5; --text2:#6ee7b7; --text3:#34a874;
  --green:#a7f3d0; --red:#fca5a5; --yellow:#fde68a; --purple:#c4b5fd;
  --border:rgba(16,185,129,.22); --card-glow:rgba(16,185,129,.08);
  --sidebar-bg:rgba(8,26,16,.95);
}
[data-theme="crimson"] {
  --bg0:#0f0508; --bg1:#1a0810; --bg2:#250b18; --bg3:#320e20; --bg4:#48122e;
  --accent:#e11d48; --accent2:#fb7185; --accent3:#be123c;
  --text1:#ffe4e6; --text2:#fda4af; --text3:#f43f5e;
  --green:#34d399; --red:#fca5a5; --yellow:#fbbf24; --purple:#c4b5fd;
  --border:rgba(225,29,72,.22); --card-glow:rgba(225,29,72,.08);
  --sidebar-bg:rgba(26,8,16,.95);
}
[data-theme="arctic"] {
  --bg0:#030d12; --bg1:#05161e; --bg2:#071f2c; --bg3:#082b3e; --bg4:#0a3d58;
  --accent:#06b6d4; --accent2:#22d3ee; --accent3:#0891b2;
  --text1:#cffafe; --text2:#67e8f9; --text3:#06bbd0;
  --green:#34d399; --red:#f87171; --yellow:#fbbf24; --purple:#a78bfa;
  --border:rgba(6,182,212,.22); --card-glow:rgba(6,182,212,.08);
  --sidebar-bg:rgba(5,22,30,.95);
}
[data-theme="parchment"] {
  --bg0:#f8f6f0; --bg1:#ffffff; --bg2:#f3f0e8; --bg3:#e8e4d8; --bg4:#dbd6c8;
  --accent:#2563eb; --accent2:#3b82f6; --accent3:#1d4ed8;
  --text1:#1e293b; --text2:#475569; --text3:#94a3b8;
  --green:#059669; --red:#dc2626; --yellow:#d97706; --purple:#7c3aed;
  --border:rgba(37,99,235,.15); --card-glow:rgba(37,99,235,.04);
  --sidebar-bg:rgba(255,255,255,.97);
}

html, body {
  height: 100%;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg0);
  color: var(--text1);
  transition: background .3s, color .3s;
}

/* ═══ LANDING ════════════════════════════════════════════════════════════════ */
.landing-nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 999;
  display: flex; align-items: center; justify-content: space-between;
  padding: .9rem 2rem;
  background: rgba(6,13,26,.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}
.landing-logo { display: flex; align-items: center; gap: .7rem; text-decoration: none; }
.landing-logo .icon { width: 36px; height: 36px; background: var(--accent); border-radius: 9px;
  display: flex; align-items: center; justify-content: center; font-size: 18px; color: #fff; }
.landing-logo .name { font-size: 17px; font-weight: 800; color: var(--text1); letter-spacing: -.3px; }
.landing-logo .sub  { font-size: 10px; color: var(--text3); }
.nav-links { display: flex; align-items: center; gap: 1.5rem; }
.nav-links a { font-size: 14px; color: var(--text2); text-decoration: none; transition: color .2s; }
.nav-links a:hover { color: var(--text1); }
.nav-actions { display: flex; align-items: center; gap: .75rem; }

.hero {
  min-height: 100vh; display: flex; flex-direction: column;
  align-items: center; justify-content: center; text-align: center;
  padding: 6rem 2rem 4rem;
  background: radial-gradient(ellipse at 60% 40%, rgba(59,130,246,.12) 0%, transparent 60%),
              radial-gradient(ellipse at 20% 80%, rgba(139,92,246,.08) 0%, transparent 50%);
}
.hero-badge { display: inline-flex; align-items: center; gap: .4rem; background: rgba(59,130,246,.15);
  border: 1px solid rgba(59,130,246,.3); border-radius: 20px; padding: .3rem .9rem;
  font-size: 12px; color: var(--accent2); font-weight: 600; margin-bottom: 1.5rem; }
.hero h1 { font-size: clamp(2.4rem, 5vw, 4rem); font-weight: 900; letter-spacing: -1.5px;
  line-height: 1.1; margin-bottom: 1.25rem; }
.hero h1 span { color: var(--accent2); }
.hero p { font-size: 1.1rem; color: var(--text2); max-width: 560px; line-height: 1.65; margin-bottom: 2.5rem; }
.hero-actions { display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center; }

.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.25rem; padding: 4rem 2rem; max-width: 1100px; margin: 0 auto; }
.feature-card { background: var(--bg1); border: 1px solid var(--border); border-radius: 14px;
  padding: 1.5rem; transition: border-color .2s, box-shadow .2s; }
.feature-card:hover { border-color: var(--accent); box-shadow: 0 0 24px var(--card-glow); }
.feature-icon { font-size: 2rem; margin-bottom: .9rem; }
.feature-card h3 { font-size: 15px; font-weight: 700; margin-bottom: .4rem; }
.feature-card p { font-size: 13px; color: var(--text2); line-height: 1.55; }

.districts-section { background: var(--bg1); border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border); padding: 3rem 2rem; text-align: center; }
.districts-section h2 { font-size: 1.5rem; font-weight: 800; margin-bottom: .6rem; }
.districts-section p  { color: var(--text2); margin-bottom: 2rem; font-size: 14px; }
.district-chips { display: flex; flex-wrap: wrap; gap: .75rem; justify-content: center; }
.district-chip  { background: var(--bg2); border: 1px solid var(--border); border-radius: 30px;
  padding: .45rem 1.1rem; font-size: 13px; font-weight: 600; color: var(--accent2); }

.stats-section { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1px; background: var(--border); margin: 0; }
.stats-section .s { background: var(--bg0); padding: 2rem; text-align: center; }
.stats-section .s .val { font-size: 2rem; font-weight: 800; color: var(--accent2); }
.stats-section .s .lbl { font-size: 12px; color: var(--text3); margin-top: .3rem; }

.landing-footer { text-align: center; padding: 2rem; border-top: 1px solid var(--border);
  font-size: 12px; color: var(--text3); }

/* ═══ AUTH ═══════════════════════════════════════════════════════════════════ */
.auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center;
  background: radial-gradient(ellipse at top left, var(--bg3) 0%, var(--bg0) 65%); }
.auth-card { width: 440px; background: var(--bg1); border: 1px solid var(--border);
  border-radius: 18px; padding: 2.5rem; box-shadow: 0 24px 64px rgba(0,0,0,.4); }
.auth-logo { display: flex; align-items: center; gap: .75rem; margin-bottom: 2rem; }
.auth-logo-icon { width: 44px; height: 44px; background: var(--accent); border-radius: 11px;
  display: flex; align-items: center; justify-content: center; font-size: 20px; color: #fff; }
.auth-logo-text .t1 { font-size: 17px; font-weight: 800; color: var(--text1); }
.auth-logo-text .t2 { font-size: 11px; color: var(--text3); }
.auth-card h2 { font-size: 22px; font-weight: 800; margin-bottom: .4rem; }
.auth-card .sub { font-size: 13px; color: var(--text2); margin-bottom: 1.75rem; }
.auth-back { display: inline-flex; align-items: center; gap: .4rem; font-size: 12px;
  color: var(--text3); text-decoration: none; margin-bottom: 1.5rem; transition: color .2s; }
.auth-back:hover { color: var(--accent2); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: .75rem; }
.form-group { margin-bottom: 1.1rem; }
.form-group label { display: block; font-size: 11px; font-weight: 700; color: var(--text3);
  margin-bottom: .4rem; letter-spacing: .6px; text-transform: uppercase; }
.form-group input, .form-group select {
  width: 100%; padding: .7rem 1rem; background: var(--bg2); border: 1px solid var(--border);
  border-radius: 8px; color: var(--text1); font-size: 14px; transition: border-color .2s; }
.form-group input:focus, .form-group select:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(59,130,246,.15); }
.auth-footer { text-align: center; margin-top: 1.25rem; font-size: 13px; color: var(--text3); }
.auth-footer a { color: var(--accent2); text-decoration: none; }

/* ═══ BUTTONS ════════════════════════════════════════════════════════════════ */
.btn { display: inline-flex; align-items: center; justify-content: center; gap: .45rem;
  padding: .7rem 1.3rem; border-radius: 8px; font-size: 14px; font-weight: 600;
  border: none; cursor: pointer; transition: all .2s; text-decoration: none; white-space: nowrap; }
.btn-primary { background: var(--accent); color: #fff; }
.btn-primary:hover { background: var(--accent2); transform: translateY(-1px); box-shadow: 0 4px 16px rgba(59,130,246,.35); }
.btn-secondary { background: var(--bg3); color: var(--text1); border: 1px solid var(--border); }
.btn-secondary:hover { background: var(--bg4); }
.btn-outline { background: transparent; color: var(--accent); border: 1px solid var(--accent); }
.btn-outline:hover { background: var(--accent); color: #fff; }
.btn-ghost { background: transparent; color: var(--text2); border: 1px solid var(--border); }
.btn-ghost:hover { background: var(--bg2); color: var(--text1); }
.btn-sm { padding: .38rem .85rem; font-size: 12px; border-radius: 6px; }
.btn-lg { padding: .9rem 2rem; font-size: 16px; border-radius: 10px; }
.btn-full { width: 100%; margin-top: .5rem; }
.btn-danger { background: rgba(239,68,68,.15); color: var(--red); border: 1px solid rgba(239,68,68,.3); }
.btn-danger:hover { background: rgba(239,68,68,.25); }

/* ═══ MESSAGES ═══════════════════════════════════════════════════════════════ */
.msg-list { margin-bottom: 1rem; }
.msg { padding: .65rem 1rem; border-radius: 8px; font-size: 13px; margin-bottom: .4rem; }
.msg-error   { background: rgba(239,68,68,.1);  border: 1px solid rgba(239,68,68,.3);  color: var(--red); }
.msg-success { background: rgba(52,211,153,.1);  border: 1px solid rgba(52,211,153,.3); color: var(--green); }
.msg-info    { background: rgba(59,130,246,.1);  border: 1px solid rgba(59,130,246,.3); color: var(--accent2); }
.messages { padding: .75rem 1.75rem 0; }
.message { padding: .65rem 1rem; border-radius: 8px; font-size: 13px; margin-bottom: .4rem; }
.message.error   { background: rgba(239,68,68,.1);  border: 1px solid rgba(239,68,68,.3);  color: var(--red); }
.message.success { background: rgba(52,211,153,.1);  border: 1px solid rgba(52,211,153,.3); color: var(--green); }

/* ═══ APP LAYOUT ═════════════════════════════════════════════════════════════ */
.app-layout { display: flex; height: 100vh; overflow: hidden; }

/* ═══ SIDEBAR ════════════════════════════════════════════════════════════════ */
.sidebar { width: 228px; background: var(--sidebar-bg); border-right: 1px solid var(--border);
  display: flex; flex-direction: column; flex-shrink: 0; overflow-y: auto; backdrop-filter: blur(12px); }
.sidebar-brand { padding: 1.1rem 1rem; display: flex; align-items: center; gap: .65rem;
  border-bottom: 1px solid var(--border); flex-shrink: 0; }
.brand-icon { width: 34px; height: 34px; background: var(--accent); border-radius: 9px;
  display: flex; align-items: center; justify-content: center; color: #fff; font-size: 16px; }
.brand-title { font-size: 14px; font-weight: 800; color: var(--text1); letter-spacing: -.3px; }
.brand-sub { font-size: 10px; color: var(--text3); }
.nav-section { padding: .65rem 0 0; }
.nav-label { font-size: 9px; font-weight: 800; letter-spacing: 1.6px; color: var(--text3);
  padding: 0 1rem .35rem; text-transform: uppercase; }
.nav-link { display: flex; align-items: center; gap: .55rem; padding: .48rem 1rem;
  font-size: 13px; color: var(--text2); text-decoration: none;
  border-left: 3px solid transparent; transition: all .15s; border-radius: 0 6px 6px 0; margin: 1px 4px 1px 0; }
.nav-link:hover { background: var(--bg2); color: var(--text1); }
.nav-link.active { background: rgba(59,130,246,.12); color: var(--accent2); border-left-color: var(--accent); }
.nav-icon { font-size: 14px; width: 18px; text-align: center; flex-shrink: 0; }
.sidebar-footer { margin-top: auto; padding: .75rem; border-top: 1px solid var(--border);
  display: flex; align-items: center; gap: .5rem; }
.user-card { display: flex; align-items: center; gap: .6rem; flex: 1; text-decoration: none; }
.user-avatar { width: 32px; height: 32px; background: var(--accent3); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 800; color: #fff; flex-shrink: 0; }
.user-name { font-size: 13px; font-weight: 600; color: var(--text1); }
.user-role { font-size: 10px; color: var(--text3); }
.logout-btn { color: var(--text3); text-decoration: none; font-size: 17px; padding: .25rem .4rem;
  border-radius: 4px; transition: color .2s; }
.logout-btn:hover { color: var(--red); }

/* ═══ MAIN CONTENT ═══════════════════════════════════════════════════════════ */
.main-content { flex: 1; overflow-y: auto; overflow-x: hidden; display: flex; flex-direction: column; }
.page-header { padding: 1.5rem 1.75rem 0; }
.page-header h1 { font-size: 21px; font-weight: 800; margin-bottom: .25rem; letter-spacing: -.3px; }
.page-header .desc { font-size: 13px; color: var(--text2); }
.page-body { padding: 1.25rem 1.75rem 2rem; flex: 1; }
.content-wrap { max-width: 820px; }

/* ═══ CARDS ══════════════════════════════════════════════════════════════════ */
.card { background: var(--bg1); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem; }
.card:hover { box-shadow: 0 4px 20px var(--card-glow); }
.card-title { font-size: 12px; font-weight: 700; color: var(--text3); margin-bottom: .75rem;
  text-transform: uppercase; letter-spacing: .7px; }

/* Stat cards */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.25rem; }
@media (max-width: 900px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } }
.stat-card { background: var(--bg1); border: 1px solid var(--border); border-radius: 12px;
  padding: 1.1rem 1.25rem; transition: border-color .2s, box-shadow .2s; }
.stat-card:hover { border-color: var(--accent); box-shadow: 0 4px 20px var(--card-glow); }
.stat-icon { font-size: 1.5rem; margin-bottom: .5rem; }
.stat-val { font-size: 28px; font-weight: 800; color: var(--text1); margin-bottom: .15rem; letter-spacing: -1px; }
.stat-lbl { font-size: 12px; color: var(--text3); font-weight: 600; text-transform: uppercase; letter-spacing: .4px; }
.stat-card.blue   .stat-val { color: var(--accent2); }
.stat-card.green  .stat-val { color: var(--green); }
.stat-card.yellow .stat-val { color: var(--yellow); }
.stat-card.purple .stat-val { color: var(--purple); }

/* ═══ TABLES ═════════════════════════════════════════════════════════════════ */
.table-wrap { overflow-x: auto; border-radius: 10px; border: 1px solid var(--border); }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
thead th { padding: .65rem 1rem; text-align: left; font-size: 11px; font-weight: 700;
  letter-spacing: .6px; text-transform: uppercase; color: var(--text3);
  background: var(--bg2); border-bottom: 1px solid var(--border); }
tbody td { padding: .72rem 1rem; border-bottom: 1px solid rgba(59,130,246,.07); color: var(--text2); }
tbody tr:last-child td { border-bottom: none; }
tbody tr:hover td { background: var(--bg2); color: var(--text1); }
.badge { display: inline-flex; align-items: center; gap: .25rem; padding: .2rem .6rem;
  border-radius: 20px; font-size: 11px; font-weight: 700; }
.badge-green  { background: rgba(52,211,153,.12); color: var(--green); }
.badge-blue   { background: rgba(59,130,246,.15);  color: var(--accent2); }
.badge-red    { background: rgba(248,113,113,.12); color: var(--red); }
.badge-yellow { background: rgba(251,191,36,.12);  color: var(--yellow); }

/* ═══ SEARCH BOX ═════════════════════════════════════════════════════════════ */
.place-search-wrap { position: relative; }
.place-search-input { width: 100%; padding: .65rem .9rem .65rem 2.2rem; background: var(--bg2);
  border: 1px solid var(--border); border-radius: 8px; color: var(--text1); font-size: 13px;
  transition: border-color .2s; }
.place-search-input:focus { outline: none; border-color: var(--accent); }
.place-search-icon { position: absolute; left: .7rem; top: 50%; transform: translateY(-50%);
  color: var(--text3); font-size: 13px; pointer-events: none; }
.place-results { position: absolute; top: calc(100% + 4px); left: 0; right: 0;
  background: var(--bg2); border: 1px solid var(--border); border-radius: 8px;
  z-index: 3000; max-height: 200px; overflow-y: auto; box-shadow: 0 8px 24px rgba(0,0,0,.4); }
.place-result-item { padding: .6rem .9rem; font-size: 12px; color: var(--text2); cursor: pointer;
  border-bottom: 1px solid var(--border); transition: background .15s; }
.place-result-item:last-child { border-bottom: none; }
.place-result-item:hover { background: var(--bg3); color: var(--text1); }
.place-result-item .place-name { font-weight: 600; color: var(--text1); }
.place-result-item .place-addr { font-size: 11px; color: var(--text3); margin-top: 1px; }

/* ═══ MAP ════════════════════════════════════════════════════════════════════ */
.map-layout { display: flex; height: 100%; overflow: hidden; }
.map-panel { width: 272px; background: var(--bg1); border-right: 1px solid var(--border);
  overflow-y: auto; padding: 1rem; flex-shrink: 0; display: flex; flex-direction: column; gap: .85rem; }
.map-container { flex: 1; position: relative; }
#map { width: 100%; height: 100%; }
.map-hint { position: absolute; bottom: 1rem; left: 50%; transform: translateX(-50%);
  background: rgba(6,13,26,.92); border: 1px solid var(--border); color: var(--text2);
  padding: .5rem 1.1rem; border-radius: 20px; font-size: 12px;
  pointer-events: none; z-index: 1000; white-space: nowrap; backdrop-filter: blur(8px); }
.map-loading { position: absolute; inset: 0; background: rgba(6,13,26,.85);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: .75rem; z-index: 2000; font-size: 13px; color: var(--text2); }
.spinner { width: 28px; height: 28px; border: 2px solid var(--bg3);
  border-top-color: var(--accent); border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: .4rem; flex-shrink: 0; }
.dot-green  { background: var(--green); box-shadow: 0 0 8px var(--green); }
.dot-red    { background: var(--red); }
.dot-yellow { background: var(--yellow); animation: pulse 1.5s ease-in-out infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: .4; } }

.coord-row { display: flex; align-items: center; gap: .5rem; padding: .5rem .7rem;
  background: var(--bg2); border-radius: 8px; border: 1px solid var(--border); font-size: 12px; }
.coord-row .lbl { font-size: 10px; font-weight: 700; color: var(--text3); text-transform: uppercase; width: 28px; flex-shrink: 0; }
.coord-row .coord-text { color: var(--text2); flex: 1; font-family: monospace; }
.coord-row .place-nm { color: var(--text1); font-weight: 600; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.route-result { background: var(--bg2); border: 1px solid var(--border); border-radius: 10px;
  padding: .9rem; display: flex; flex-direction: column; gap: .5rem; }
.route-result .row { display: flex; justify-content: space-between; align-items: baseline; }
.route-result .label { font-size: 11px; color: var(--text3); font-weight: 600; text-transform: uppercase; }
.route-result .value { font-size: 15px; font-weight: 800; color: var(--accent2); }
.route-result .sub { font-size: 11px; color: var(--text3); }

.mode-select { display: flex; gap: .4rem; margin-bottom: .25rem; }
.mode-btn { flex: 1; padding: .45rem .5rem; border-radius: 7px; font-size: 12px; font-weight: 600;
  border: 1px solid var(--border); background: var(--bg2); color: var(--text3); cursor: pointer; transition: all .15s; text-align: center; }
.mode-btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }

/* ═══ THEME SWITCHER ═════════════════════════════════════════════════════════ */
.theme-switcher { display: flex; gap: .5rem; flex-wrap: wrap; margin: .75rem 0; }
.theme-dot { width: 28px; height: 28px; border-radius: 50%; cursor: pointer; border: 2px solid transparent;
  transition: border-color .2s, transform .15s; }
.theme-dot:hover { transform: scale(1.15); }
.theme-dot.selected { border-color: var(--text1); }
.theme-dot[data-t="midnight"] { background: linear-gradient(135deg,#060d1a,#3b82f6); }
.theme-dot[data-t="obsidian"] { background: linear-gradient(135deg,#0a0812,#8b5cf6); }
.theme-dot[data-t="emerald"]  { background: linear-gradient(135deg,#050f0a,#10b981); }
.theme-dot[data-t="crimson"]  { background: linear-gradient(135deg,#0f0508,#e11d48); }
.theme-dot[data-t="arctic"]   { background: linear-gradient(135deg,#030d12,#06b6d4); }
.theme-dot[data-t="parchment"]{ background: linear-gradient(135deg,#f8f6f0,#2563eb); }

/* ═══ COMPARE ════════════════════════════════════════════════════════════════ */
.compare-wrap { display: flex; flex-direction: column; height: 100%; }
.compare-inputs { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; padding: 1rem 1.75rem; }
.compare-maps { display: grid; grid-template-columns: 1fr 1fr; gap: .75rem;
  flex: 1; padding: 0 1.75rem 1rem; min-height: 0; }
.compare-map-box { position: relative; border-radius: 12px; overflow: hidden;
  border: 1px solid var(--border); min-height: 350px; }
.compare-map-box .map-label { position: absolute; top: .7rem; left: .7rem;
  background: rgba(6,13,26,.92); border: 1px solid var(--border); padding: .3rem .75rem;
  border-radius: 20px; font-size: 12px; color: var(--text1); z-index: 1000; backdrop-filter: blur(8px); }
.compare-panel { padding: .75rem 1.25rem; background: var(--bg1); border-top: 1px solid var(--border);
  display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.compare-stat { display: flex; flex-direction: column; align-items: center; }
.compare-stat .val { font-size: 1.4rem; font-weight: 800; }
.compare-stat .lbl { font-size: 11px; color: var(--text3); font-weight: 600; }

/* ═══ MISC ═══════════════════════════════════════════════════════════════════ */
.progress-bar { height: 6px; background: var(--bg2); border-radius: 3px; overflow: hidden; margin-top: .4rem; }
.progress-fill { height: 100%; background: var(--accent); border-radius: 3px; transition: width .5s; }
.faq-item { border-bottom: 1px solid var(--border); padding: 1rem 0; }
.faq-q { font-weight: 700; font-size: 14px; margin-bottom: .5rem; color: var(--text1); cursor: pointer; }
.faq-a { font-size: 13px; color: var(--text2); line-height: 1.6; }
.api-endpoint { background: var(--bg2); border: 1px solid var(--border); border-radius: 10px;
  padding: 1rem 1.25rem; margin-bottom: 1rem; }
.endpoint-method { display: inline-block; padding: .2rem .55rem; border-radius: 5px;
  font-size: 11px; font-weight: 700; font-family: monospace; margin-right: .5rem; }
.method-get  { background: rgba(52,211,153,.15);  color: var(--green); }
.method-post { background: rgba(59,130,246,.15);  color: var(--accent2); }
.endpoint-url { font-family: monospace; font-size: 13px; color: var(--accent2); }
.code-block { background: var(--bg0); border: 1px solid var(--border); border-radius: 7px;
  padding: .75rem 1rem; font-family: monospace; font-size: 12px; color: var(--text2);
  overflow-x: auto; margin-top: .65rem; }
.team-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 1rem; }
.team-card { background: var(--bg1); border: 1px solid var(--border); border-radius: 14px;
  padding: 1.5rem; text-align: center; transition: all .2s; }
.team-card:hover { border-color: var(--accent); transform: translateY(-3px); box-shadow: 0 8px 24px var(--card-glow); }
.team-avatar { width: 56px; height: 56px; background: var(--accent3); border-radius: 50%;
  display: flex; align-items: center; justify-content: center; font-size: 18px;
  font-weight: 800; color: #fff; margin: 0 auto 1rem; }
.team-card h3 { font-size: 15px; font-weight: 700; margin-bottom: .3rem; }
.team-card .role { font-size: 12px; color: var(--text2); margin-bottom: .5rem; }
.team-card .email { font-size: 11px; color: var(--text3); word-break: break-all; }
.bench-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: .75rem; margin-top: 1rem; }
.bench-card { background: var(--bg2); border-radius: 10px; padding: .9rem; text-align: center; border: 1px solid var(--border); }
.bench-val { font-size: 22px; font-weight: 800; color: var(--accent2); }
.bench-lbl { font-size: 11px; color: var(--text3); margin-top: .2rem; }
.leaderboard-row { display: flex; align-items: center; gap: 1rem; padding: .85rem 1rem;
  border-radius: 10px; background: var(--bg2); margin-bottom: .5rem; border: 1px solid var(--border); }
.leaderboard-rank { font-size: 18px; font-weight: 900; width: 32px; text-align: center; }
.leaderboard-name { flex: 1; font-weight: 600; }
.leaderboard-km { font-size: 13px; color: var(--accent2); font-weight: 700; }
.leaderboard-routes { font-size: 12px; color: var(--text3); }
.saved-card { background: var(--bg1); border: 1px solid var(--border); border-radius: 10px;
  padding: 1rem; margin-bottom: .75rem; display: flex; align-items: center; gap: 1rem; transition: all .2s; }
.saved-card:hover { border-color: var(--accent); }
.saved-icon { font-size: 1.5rem; }
.saved-label { font-weight: 700; font-size: 14px; margin-bottom: .2rem; }
.saved-meta { font-size: 12px; color: var(--text3); }
.report-header { background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 1px solid var(--border); border-radius: 14px; padding: 1.75rem; margin-bottom: 1.25rem; }
.eta-card { background: var(--bg2); border: 1px solid var(--border); border-radius: 12px;
  padding: 1.25rem; text-align: center; transition: all .2s; }
.eta-card:hover { border-color: var(--accent); }
.eta-icon { font-size: 2rem; margin-bottom: .6rem; }
.eta-val  { font-size: 2rem; font-weight: 900; color: var(--accent2); }
.eta-lbl  { font-size: 12px; color: var(--text3); margin-top: .25rem; }
""")

# ─────────────────────────────────────────────────────────── JS ───────────────
os.makedirs(os.path.join(S, 'js'), exist_ok=True)
w(os.path.join(S, 'js', 'theme.js'), r"""
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
""")

w(os.path.join(S, 'js', 'app.js'), r"""
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
""")

w(os.path.join(S, 'js', 'map.js'), r"""
// map.js — route optimizer map page

function getCsrf() {
  return document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] || '';
}

const map = L.map('map', { zoomControl: false }).setView([27.7103, 85.3222], 12);
L.control.zoom({ position: 'bottomright' }).addTo(map);

// Tile layer switcher — dark default
let tileUrl = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
const tileLayer = L.tileLayer(tileUrl, {
  attribution: '&copy; CartoDB &copy; OpenStreetMap',
  subdomains: 'abcd', maxZoom: 19,
}).addTo(map);

// Theme → tile auto-switch
(function () {
  const t = localStorage.getItem('ro_theme') || 'midnight';
  if (t === 'parchment') {
    tileLayer.setUrl('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
  }
})();

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
""")

# ═══════════════════════════════════════════════════ BASE TEMPLATE ══════════
w(os.path.join(T, 'base.html'), """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}RouteOptima{% endblock %}</title>
  {% load static %}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{% static 'routing/css/style.css' %}">
  <script src="{% static 'routing/js/theme.js' %}"></script>
  {% block head %}{% endblock %}
</head>
<body>
{% block public %}
{% if user.is_authenticated %}
<div class="app-layout">
  <aside class="sidebar">
    <div class="sidebar-brand">
      <div class="brand-icon">&#9672;</div>
      <div><div class="brand-title">RouteOptima</div><div class="brand-sub">Dijkstra SPF</div></div>
    </div>
    <nav>
      <div class="nav-section">
        <div class="nav-label">Main</div>
        <a href="{% url 'dashboard' %}"  class="nav-link {% if request.resolver_match.url_name == 'dashboard' %}active{% endif %}"><span class="nav-icon">⬡</span> Dashboard</a>
        <a href="{% url 'map' %}"        class="nav-link {% if request.resolver_match.url_name == 'map' %}active{% endif %}"><span class="nav-icon">🗺</span> Route Map</a>
        <a href="{% url 'compare' %}"    class="nav-link {% if request.resolver_match.url_name == 'compare' %}active{% endif %}"><span class="nav-icon">⇆</span> Compare</a>
        <a href="{% url 'simulation' %}" class="nav-link {% if request.resolver_match.url_name == 'simulation' %}active{% endif %}"><span class="nav-icon">▶</span> Simulation</a>
      </div>
      <div class="nav-section">
        <div class="nav-label">Data</div>
        <a href="{% url 'history' %}"    class="nav-link {% if request.resolver_match.url_name == 'history' %}active{% endif %}"><span class="nav-icon">⏱</span> History</a>
        <a href="{% url 'analytics' %}"  class="nav-link {% if request.resolver_match.url_name == 'analytics' %}active{% endif %}"><span class="nav-icon">📊</span> Analytics</a>
        <a href="{% url 'favorites' %}"  class="nav-link {% if request.resolver_match.url_name == 'favorites' %}active{% endif %}"><span class="nav-icon">⭐</span> Favourites</a>
        <a href="{% url 'export' %}"     class="nav-link {% if request.resolver_match.url_name == 'export' %}active{% endif %}"><span class="nav-icon">⬇</span> Export</a>
        <a href="{% url 'report' %}"     class="nav-link {% if request.resolver_match.url_name == 'report' %}active{% endif %}"><span class="nav-icon">📄</span> Report</a>
      </div>
      <div class="nav-section">
        <div class="nav-label">Tools</div>
        <a href="{% url 'heatmap' %}"     class="nav-link {% if request.resolver_match.url_name == 'heatmap' %}active{% endif %}"><span class="nav-icon">🔥</span> Heatmap</a>
        <a href="{% url 'eta' %}"         class="nav-link {% if request.resolver_match.url_name == 'eta' %}active{% endif %}"><span class="nav-icon">⏩</span> ETA Calc</a>
        <a href="{% url 'leaderboard' %}" class="nav-link {% if request.resolver_match.url_name == 'leaderboard' %}active{% endif %}"><span class="nav-icon">🏆</span> Leaderboard</a>
        <a href="{% url 'benchmark' %}"   class="nav-link {% if request.resolver_match.url_name == 'benchmark' %}active{% endif %}"><span class="nav-icon">⚡</span> Benchmark</a>
      </div>
      <div class="nav-section">
        <div class="nav-label">System</div>
        <a href="{% url 'algorithm' %}"    class="nav-link {% if request.resolver_match.url_name == 'algorithm' %}active{% endif %}"><span class="nav-icon">⚙</span> Algorithm</a>
        <a href="{% url 'graph' %}"        class="nav-link {% if request.resolver_match.url_name == 'graph' %}active{% endif %}"><span class="nav-icon">◉</span> Graph Info</a>
        <a href="{% url 'nodes' %}"        class="nav-link {% if request.resolver_match.url_name == 'nodes' %}active{% endif %}"><span class="nav-icon">◦</span> Nodes</a>
        <a href="{% url 'settings' %}"     class="nav-link {% if request.resolver_match.url_name == 'settings' %}active{% endif %}"><span class="nav-icon">⚙</span> Settings</a>
      </div>
      <div class="nav-section">
        <div class="nav-label">Info</div>
        <a href="{% url 'about' %}"  class="nav-link {% if request.resolver_match.url_name == 'about' %}active{% endif %}"><span class="nav-icon">ℹ</span> About</a>
        <a href="{% url 'team' %}"   class="nav-link {% if request.resolver_match.url_name == 'team' %}active{% endif %}"><span class="nav-icon">👥</span> Team</a>
        <a href="{% url 'docs' %}"   class="nav-link {% if request.resolver_match.url_name == 'docs' %}active{% endif %}"><span class="nav-icon">📚</span> Docs</a>
        <a href="{% url 'help' %}"   class="nav-link {% if request.resolver_match.url_name == 'help' %}active{% endif %}"><span class="nav-icon">?</span> Help</a>
      </div>
    </nav>
    <div class="sidebar-footer">
      <a href="{% url 'profile' %}" class="user-card">
        <div class="user-avatar">{{ user.username|slice:":2"|upper }}</div>
        <div><div class="user-name">{{ user.get_short_name|default:user.username }}</div><div class="user-role">{{ user.email|default:"User" }}</div></div>
      </a>
      <a href="{% url 'logout' %}" class="logout-btn" title="Logout">⏻</a>
    </div>
  </aside>
  <div class="main-content">
    {% if messages %}
    <div class="messages">
      {% for m in messages %}<div class="message {{ m.tags }}">{{ m }}</div>{% endfor %}
    </div>
    {% endif %}
    {% block content %}{% endblock %}
  </div>
</div>
{% else %}
{% block public_content %}{% endblock %}
{% endif %}
{% endblock %}
<script src="{% static 'routing/js/app.js' %}"></script>
{% block scripts %}{% endblock %}
</body>
</html>
""")

# ═══════════════════════════════════════════════════ LANDING ════════════════
w(os.path.join(T, 'landing.html'), """
{% extends 'routing/base.html' %}
{% load static %}
{% block title %}RouteOptima — Shortest Path Optimizer for Nepal{% endblock %}
{% block public %}
<nav class="landing-nav">
  <a href="{% url 'landing' %}" class="landing-logo">
    <div class="icon">&#9672;</div>
    <div><div class="name">RouteOptima</div><div class="sub">Dijkstra SPF</div></div>
  </a>
  <div class="nav-links">
    <a href="{% url 'about' %}">About</a>
    <a href="{% url 'docs' %}">Docs</a>
    <a href="{% url 'team' %}">Team</a>
    <a href="{% url 'help' %}">Help</a>
  </div>
  <div class="nav-actions">
    <!-- Theme switcher in nav -->
    <div style="display:flex;gap:.35rem;align-items:center;">
      <div class="theme-dot" data-t="midnight" title="Midnight"></div>
      <div class="theme-dot" data-t="obsidian" title="Obsidian"></div>
      <div class="theme-dot" data-t="emerald"  title="Emerald"></div>
      <div class="theme-dot" data-t="crimson"  title="Crimson"></div>
      <div class="theme-dot" data-t="arctic"   title="Arctic"></div>
      <div class="theme-dot" data-t="parchment" title="Light"></div>
    </div>
    <a href="{% url 'login' %}"    class="btn btn-ghost btn-sm">Log In</a>
    <a href="{% url 'register' %}" class="btn btn-primary btn-sm">Get Started</a>
  </div>
</nav>

<section class="hero">
  <div class="hero-badge">🗺 Nepal Road Network · Dijkstra SPF · 5 Districts</div>
  <h1>Find the <span>Shortest Route</span><br>Across the Valley</h1>
  <p>RouteOptima uses Dijkstra's shortest-path algorithm on real OpenStreetMap data covering Kathmandu, Bhaktapur, Lalitpur, Nuwakot, and Dhading districts.</p>
  <div class="hero-actions">
    <a href="{% url 'register' %}" class="btn btn-primary btn-lg">Start Routing Free</a>
    <a href="{% url 'about' %}"    class="btn btn-ghost btn-lg">Learn More</a>
  </div>
</section>

<div class="districts-section">
  <h2>Coverage Districts</h2>
  <p>Real road network data from OpenStreetMap — updated live.</p>
  <div class="district-chips">
    <span class="district-chip">📍 Kathmandu</span>
    <span class="district-chip">📍 Bhaktapur</span>
    <span class="district-chip">📍 Lalitpur</span>
    <span class="district-chip">📍 Nuwakot</span>
    <span class="district-chip">📍 Dhading</span>
  </div>
</div>

<div class="stats-section">
  <div class="s"><div class="val">5</div><div class="lbl">Districts Covered</div></div>
  <div class="s"><div class="val">50K+</div><div class="lbl">Road Nodes</div></div>
  <div class="s"><div class="val">Dijkstra</div><div class="lbl">Core Algorithm</div></div>
  <div class="s"><div class="val">Free</div><div class="lbl">OSM Data</div></div>
</div>

<div class="features-grid">
  <div class="feature-card"><div class="feature-icon">🔍</div><h3>Place Search</h3><p>Search any location by name — from a small tea shop to a large hospital. No need to know coordinates.</p></div>
  <div class="feature-card"><div class="feature-icon">⚡</div><h3>Instant Routes</h3><p>Dijkstra's algorithm computes the optimal path in milliseconds across the entire graph.</p></div>
  <div class="feature-card"><div class="feature-icon">⇆</div><h3>Route Comparison</h3><p>Run two different routes side-by-side and compare distance, ETA, and node count.</p></div>
  <div class="feature-card"><div class="feature-icon">🚶 🚲 🚗</div><h3>Travel Modes</h3><p>Get estimated travel time for walking, cycling, or driving — automatically calculated.</p></div>
  <div class="feature-card"><div class="feature-icon">⭐</div><h3>Saved Favourites</h3><p>Bookmark your most-used routes with custom labels and replay them anytime.</p></div>
  <div class="feature-card"><div class="feature-icon">🔥</div><h3>Route Heatmap</h3><p>Visualise the busiest route endpoints across all users on an interactive heat map.</p></div>
  <div class="feature-card"><div class="feature-icon">🔗</div><h3>Route Sharing</h3><p>Generate a unique shareable link for any computed route — no login needed to view.</p></div>
  <div class="feature-card"><div class="feature-icon">🏆</div><h3>Leaderboard</h3><p>See which users have covered the most distance. Compete with your team members!</p></div>
</div>

<footer class="landing-footer">
  <p>RouteOptima &copy; 2026 — IIMS College · Group 36 · Supervised by Nabeen Kumar Aryal</p>
</footer>
{% endblock %}
""")

# ═════════════════════════════════════════════ LOGIN / REGISTER ═════════════
w(os.path.join(T, 'login.html'), """
{% extends 'routing/base.html' %}
{% block title %}Log In — RouteOptima{% endblock %}
{% block public %}
<div class="auth-page">
  <div class="auth-card">
    <div class="auth-logo">
      <div class="auth-logo-icon">&#9672;</div>
      <div class="auth-logo-text"><div class="t1">RouteOptima</div><div class="t2">Dijkstra SPF · Nepal</div></div>
    </div>
    <a href="{% url 'landing' %}" class="auth-back">← Back to Home</a>
    <h2>Welcome back</h2>
    <p class="sub">Log in to access your routes and analytics.</p>
    {% if messages %}
    <div class="msg-list">{% for m in messages %}<div class="msg {% if m.tags == 'error' %}msg-error{% else %}msg-success{% endif %}">{{ m }}</div>{% endfor %}</div>
    {% endif %}
    <form method="POST">
      {% csrf_token %}
      <div class="form-group"><label>Username</label><input type="text" name="username" required autofocus placeholder="your username"></div>
      <div class="form-group"><label>Password</label><input type="password" name="password" required placeholder="••••••••"></div>
      <button type="submit" class="btn btn-primary btn-full">Log In →</button>
    </form>
    <div class="auth-footer">Don't have an account? <a href="{% url 'register' %}">Sign up free</a></div>
    <div style="margin-top:.75rem;text-align:center;">
      <div style="font-size:11px;color:var(--text3);margin-bottom:.5rem;">Choose theme</div>
      <div style="display:flex;gap:.4rem;justify-content:center;">
        <div class="theme-dot" data-t="midnight" title="Midnight"></div>
        <div class="theme-dot" data-t="obsidian" title="Obsidian"></div>
        <div class="theme-dot" data-t="emerald"  title="Emerald"></div>
        <div class="theme-dot" data-t="crimson"  title="Crimson"></div>
        <div class="theme-dot" data-t="arctic"   title="Arctic"></div>
        <div class="theme-dot" data-t="parchment" title="Light"></div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
""")

w(os.path.join(T, 'register.html'), """
{% extends 'routing/base.html' %}
{% block title %}Register — RouteOptima{% endblock %}
{% block public %}
<div class="auth-page">
  <div class="auth-card">
    <div class="auth-logo">
      <div class="auth-logo-icon">&#9672;</div>
      <div class="auth-logo-text"><div class="t1">RouteOptima</div><div class="t2">Dijkstra SPF · Nepal</div></div>
    </div>
    <a href="{% url 'landing' %}" class="auth-back">← Back to Home</a>
    <h2>Create account</h2>
    <p class="sub">Join RouteOptima and start optimising routes.</p>
    {% if messages %}
    <div class="msg-list">{% for m in messages %}<div class="msg {% if m.tags == 'error' %}msg-error{% else %}msg-success{% endif %}">{{ m }}</div>{% endfor %}</div>
    {% endif %}
    <form method="POST">
      {% csrf_token %}
      <div class="form-group"><label>First Name</label><input type="text" name="first_name" placeholder="Your first name"></div>
      <div class="form-group"><label>Username</label><input type="text" name="username" required autofocus placeholder="choose a username"></div>
      <div class="form-group"><label>Email</label><input type="email" name="email" placeholder="for welcome email"></div>
      <div class="form-row">
        <div class="form-group"><label>Password</label><input type="password" name="password1" required placeholder="min 6 chars"></div>
        <div class="form-group"><label>Confirm</label><input type="password" name="password2" required placeholder="repeat"></div>
      </div>
      <button type="submit" class="btn btn-primary btn-full">Create Account →</button>
    </form>
    <div class="auth-footer">Already have an account? <a href="{% url 'login' %}">Log in</a></div>
  </div>
</div>
{% endblock %}
""")

# ═════════════════════════════════════════════ DASHBOARD ═══════════════════
w(os.path.join(T, 'dashboard.html'), """
{% extends 'routing/base.html' %}
{% block title %}Dashboard — RouteOptima{% endblock %}
{% block content %}
<div class="page-header">
  <h1>👋 Welcome{% if user.first_name %}, {{ user.first_name }}{% endif %}!</h1>
  <div class="desc">Here's your route activity at a glance.</div>
</div>
<div class="page-body">
  <div class="stats-grid">
    <div class="stat-card blue"><div class="stat-icon">🗺</div><div class="stat-val">{{ total_routes }}</div><div class="stat-lbl">Total Routes</div></div>
    <div class="stat-card green"><div class="stat-icon">📏</div><div class="stat-val">{{ total_km }}</div><div class="stat-lbl">km Travelled</div></div>
    <div class="stat-card yellow"><div class="stat-icon">⚡</div><div class="stat-val">{{ avg_km }}</div><div class="stat-lbl">Avg km / Route</div></div>
    <div class="stat-card purple"><div class="stat-icon">⭐</div><div class="stat-val">{{ saved_count }}</div><div class="stat-lbl">Saved Routes</div></div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 320px;gap:1rem;margin-bottom:1rem">
    <!-- Graph status -->
    <div class="card">
      <div class="card-title">Graph Status</div>
      {% if graph_info.loaded %}
      <div style="display:flex;gap:.5rem;align-items:center;margin-bottom:.75rem">
        <span class="status-dot dot-green"></span>
        <span style="font-weight:700;color:var(--green)">All districts loaded</span>
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem">
        <div style="text-align:center;padding:.75rem;background:var(--bg2);border-radius:8px;border:1px solid var(--border)">
          <div style="font-size:1.4rem;font-weight:800;color:var(--accent2)">{{ graph_info.nodes|default:"—" }}</div>
          <div style="font-size:11px;color:var(--text3)">Nodes</div>
        </div>
        <div style="text-align:center;padding:.75rem;background:var(--bg2);border-radius:8px;border:1px solid var(--border)">
          <div style="font-size:1.4rem;font-weight:800;color:var(--accent2)">{{ graph_info.edges|default:"—" }}</div>
          <div style="font-size:11px;color:var(--text3)">Edges</div>
        </div>
        <div style="text-align:center;padding:.75rem;background:var(--bg2);border-radius:8px;border:1px solid var(--border)">
          <div style="font-size:1.4rem;font-weight:800;color:var(--green)">{{ graph_info.loaded_count }}/{{ graph_info.total }}</div>
          <div style="font-size:11px;color:var(--text3)">Districts</div>
        </div>
      </div>
      {% else %}
      <div style="display:flex;gap:.5rem;align-items:center;margin-bottom:.5rem">
        <span class="status-dot dot-yellow"></span>
        <span style="color:var(--yellow)">{{ graph_info.message }}</span>
      </div>
      <div class="progress-bar"><div class="progress-fill" style="width:{{ graph_info.loaded_count|default:0 }}0%"></div></div>
      {% endif %}
    </div>
    <!-- Quick nav -->
    <div class="card">
      <div class="card-title">Quick Access</div>
      <div style="display:flex;flex-direction:column;gap:.5rem">
        <a href="{% url 'map' %}"        class="btn btn-primary btn-sm">🗺 Open Route Map</a>
        <a href="{% url 'compare' %}"    class="btn btn-secondary btn-sm">⇆ Compare Routes</a>
        <a href="{% url 'favorites' %}"  class="btn btn-secondary btn-sm">⭐ My Favourites</a>
        <a href="{% url 'heatmap' %}"    class="btn btn-secondary btn-sm">🔥 Route Heatmap</a>
        <a href="{% url 'leaderboard' %}" class="btn btn-secondary btn-sm">🏆 Leaderboard</a>
      </div>
    </div>
  </div>

  {% if recent_routes %}
  <div class="card">
    <div class="card-title">Recent Routes</div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>#</th><th>From</th><th>To</th><th>Distance</th><th>Date</th><th></th></tr></thead>
        <tbody>
          {% for r in recent_routes %}
          <tr>
            <td style="color:var(--text3)">{{ r.id }}</td>
            <td>{{ r.src_name|default:"—" }}</td>
            <td>{{ r.dst_name|default:"—" }}</td>
            <td><span class="badge badge-blue">{{ r.path_distance_km }} km</span></td>
            <td style="color:var(--text3)">{{ r.computed_at|date:"M j, H:i" }}</td>
            <td><a href="{% url 'replay' r.id %}" class="btn btn-ghost btn-sm">▶ Replay</a></td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
  {% else %}
  <div class="card" style="text-align:center;padding:2.5rem">
    <div style="font-size:3rem;margin-bottom:.75rem">🗺</div>
    <div style="font-weight:700;margin-bottom:.4rem">No routes yet</div>
    <div style="color:var(--text2);font-size:13px;margin-bottom:1rem">Open the Route Map and compute your first route!</div>
    <a href="{% url 'map' %}" class="btn btn-primary">Open Route Map</a>
  </div>
  {% endif %}
</div>
{% endblock %}
""")

# ═════════════════════════════════════════════ MAP ══════════════════════════
w(os.path.join(T, 'map.html'), """
{% extends 'routing/base.html' %}
{% load static %}
{% block title %}Route Map — RouteOptima{% endblock %}
{% block head %}
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
{% endblock %}
{% block content %}
<div class="map-layout" style="height:calc(100vh - 0px)">
  <!-- Side panel -->
  <div class="map-panel">
    <div style="font-size:12px;font-weight:800;color:var(--text3);text-transform:uppercase;letter-spacing:.7px">Start Point</div>
    <div class="place-search-wrap">
      <span class="place-search-icon">🔍</span>
      <input id="srcInput" class="place-search-input" type="text" placeholder="Search start (e.g. Pashupatinath)" autocomplete="off">
      <div id="srcResults" class="place-results" style="display:none"></div>
    </div>
    <div id="srcCoord" class="coord-row" style="display:none">
      <span class="lbl" style="color:var(--green)">A</span>
      <span class="coord-text"></span>
    </div>
    <button class="btn btn-ghost btn-sm" style="margin-top:-.25rem" onclick="clicking='src';setHint('Click on the map to set start point')">📌 Click on map</button>

    <div style="font-size:12px;font-weight:800;color:var(--text3);text-transform:uppercase;letter-spacing:.7px;margin-top:.5rem">End Point</div>
    <div class="place-search-wrap">
      <span class="place-search-icon">🔍</span>
      <input id="dstInput" class="place-search-input" type="text" placeholder="Search destination (e.g. Boudha)" autocomplete="off">
      <div id="dstResults" class="place-results" style="display:none"></div>
    </div>
    <div id="dstCoord" class="coord-row" style="display:none">
      <span class="lbl" style="color:var(--red)">B</span>
      <span class="coord-text"></span>
    </div>
    <button class="btn btn-ghost btn-sm" style="margin-top:-.25rem" onclick="clicking='dst';setHint('Click on the map to set end point')">📌 Click on map</button>

    <div style="font-size:12px;font-weight:800;color:var(--text3);text-transform:uppercase;letter-spacing:.7px;margin-top:.5rem">Travel Mode</div>
    <div class="mode-select">
      <div class="mode-btn {% if mode == 'walk' %}active{% endif %}" data-mode="walk">🚶 Walk</div>
      <div class="mode-btn {% if mode == 'bike' %}active{% endif %}" data-mode="bike">🚲 Bike</div>
      <div class="mode-btn {% if mode == 'car' %}active{% else %}{% endif %}" data-mode="car" {% if mode != 'walk' and mode != 'bike' %}style="background:var(--accent);border-color:var(--accent);color:#fff"{% endif %}>🚗 Car</div>
    </div>
    <input type="hidden" id="selectedMode" value="{{ mode }}">

    <div id="routeResult" style="display:none">
      <div class="route-result">
        <div class="card-title" style="margin-bottom:.5rem">Route Found</div>
        <div class="row"><span class="label">Distance</span><span class="value" id="routeKm">—</span></div>
        <div class="row"><span class="label">ETA</span><span class="value" id="routeEta">—</span></div>
        <div class="row"><span class="label">Nodes</span><span id="routeNodes" style="font-size:13px;color:var(--text2)">—</span></div>
      </div>
      <div style="display:flex;gap:.5rem;margin-top:.5rem">
        <button class="btn btn-secondary btn-sm" onclick="saveRoute()" style="flex:1">⭐ Save</button>
        <button class="btn btn-secondary btn-sm" onclick="shareRoute()" style="flex:1">🔗 Share</button>
        <a id="replayBtn" href="#" class="btn btn-secondary btn-sm" style="flex:1">▶</a>
      </div>
    </div>

    <button class="btn btn-ghost btn-sm" onclick="clearRoute()" style="margin-top:auto">✕ Clear</button>

    <div style="display:flex;align-items:center;gap:.4rem;font-size:12px;padding:.5rem 0;border-top:1px solid var(--border);margin-top:.25rem">
      <span id="statusDot" class="status-dot dot-yellow"></span>
      <span id="statusLbl" style="color:var(--text2)">Checking…</span>
    </div>
  </div>

  <!-- Map -->
  <div class="map-container">
    <div id="mapLoading" class="map-loading" style="display:none">
      <div class="spinner"></div>
      <span>Computing route…</span>
    </div>
    <div id="map"></div>
    <div id="mapHint" class="map-hint">Search or click map to set start point</div>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script src="{% static 'routing/js/map.js' %}"></script>
<script>
document.getElementById('routeResult').querySelectorAll('#routeNodes').forEach(()=>{});
document.getElementById('replayBtn').addEventListener('click', e=>{
  if(window._lastRouteId){ e.currentTarget.href='/replay/'+window._lastRouteId+'/'; }
});
</script>
{% endblock %}
""")

# ═════════════════════════════════════════════ COMPARE ══════════════════════
w(os.path.join(T, 'compare.html'), """
{% extends 'routing/base.html' %}
{% load static %}
{% block title %}Compare Routes — RouteOptima{% endblock %}
{% block head %}
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
{% endblock %}
{% block content %}
<div class="page-header">
  <h1>⇆ Compare Routes</h1>
  <div class="desc">Search two routes side-by-side — Dijkstra vs a different endpoint.</div>
</div>
<div class="compare-wrap" style="height:calc(100vh - 130px)">
  <div class="compare-inputs">
    <!-- Route A -->
    <div class="card" style="padding:.85rem">
      <div class="card-title" style="color:var(--accent2)">Route A</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:.6rem">
        <div>
          <div style="font-size:11px;color:var(--text3);margin-bottom:.3rem;font-weight:700;text-transform:uppercase">Start A</div>
          <div class="place-search-wrap"><span class="place-search-icon">🔍</span>
            <input id="aSrcInput" class="place-search-input" type="text" placeholder="Start point A" autocomplete="off">
            <div id="aSrcResults" class="place-results" style="display:none"></div></div>
        </div>
        <div>
          <div style="font-size:11px;color:var(--text3);margin-bottom:.3rem;font-weight:700;text-transform:uppercase">End A</div>
          <div class="place-search-wrap"><span class="place-search-icon">🔍</span>
            <input id="aDstInput" class="place-search-input" type="text" placeholder="End point A" autocomplete="off">
            <div id="aDstResults" class="place-results" style="display:none"></div></div>
        </div>
      </div>
      <div id="aResult" style="margin-top:.5rem;font-size:12px;color:var(--text3)">Not computed</div>
    </div>
    <!-- Route B -->
    <div class="card" style="padding:.85rem">
      <div class="card-title" style="color:var(--green)">Route B</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:.6rem">
        <div>
          <div style="font-size:11px;color:var(--text3);margin-bottom:.3rem;font-weight:700;text-transform:uppercase">Start B</div>
          <div class="place-search-wrap"><span class="place-search-icon">🔍</span>
            <input id="bSrcInput" class="place-search-input" type="text" placeholder="Start point B" autocomplete="off">
            <div id="bSrcResults" class="place-results" style="display:none"></div></div>
        </div>
        <div>
          <div style="font-size:11px;color:var(--text3);margin-bottom:.3rem;font-weight:700;text-transform:uppercase">End B</div>
          <div class="place-search-wrap"><span class="place-search-icon">🔍</span>
            <input id="bDstInput" class="place-search-input" type="text" placeholder="End point B" autocomplete="off">
            <div id="bDstResults" class="place-results" style="display:none"></div></div>
        </div>
      </div>
      <div id="bResult" style="margin-top:.5rem;font-size:12px;color:var(--text3)">Not computed</div>
    </div>
  </div>
  <div class="compare-maps">
    <div class="compare-map-box"><div class="map-label" style="border-color:var(--accent)">🔵 Route A</div><div id="mapA" style="width:100%;height:100%"></div></div>
    <div class="compare-map-box"><div class="map-label" style="border-color:var(--green)">🟢 Route B</div><div id="mapB" style="width:100%;height:100%"></div></div>
  </div>
  <div class="compare-panel" id="comparePanel" style="display:none">
    <div><div class="compare-stat"><div class="val" id="cAkm" style="color:var(--accent2)">—</div><div class="lbl">Route A km</div></div></div>
    <div><div class="compare-stat"><div class="val" id="cBkm" style="color:var(--green)">—</div><div class="lbl">Route B km</div></div></div>
    <div><div class="compare-stat"><div class="val" id="cAeta">—</div><div class="lbl">Route A ETA</div></div></div>
    <div><div class="compare-stat"><div class="val" id="cBeta">—</div><div class="lbl">Route B ETA</div></div></div>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script>
const mapA = L.map('mapA').setView([27.7103, 85.3222], 12);
const mapB = L.map('mapB').setView([27.7103, 85.3222], 12);
const turl = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
const attr = '&copy; CartoDB &copy; OpenStreetMap';
L.tileLayer(turl,{attribution:attr,subdomains:'abcd',maxZoom:19}).addTo(mapA);
L.tileLayer(turl,{attribution:attr,subdomains:'abcd',maxZoom:19}).addTo(mapB);

const csrf = ()=>document.cookie.split('; ').find(r=>r.startsWith('csrftoken='))?.split('=')[1]||'';
let stateA={src:null,dst:null}, stateB={src:null,dst:null};
let routeLA=null, routeLB=null;

async function computeCmp(state, map, routeLayerRef, color, resultEl, prefix) {
  if (!state.src || !state.dst) return;
  resultEl.textContent = 'Computing…';
  const r = await fetch('/api/route/', {
    method:'POST', credentials:'same-origin',
    headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},
    body: JSON.stringify({src_lat:state.src.lat,src_lon:state.src.lon,
      dst_lat:state.dst.lat,dst_lon:state.dst.lon,mode:'car',
      src_name:state.src.name||'',dst_name:state.dst.name||''})
  });
  const j = await r.json();
  if (j.status === 'success') {
    if (routeLayerRef.current) map.removeLayer(routeLayerRef.current);
    const lls = j.data.path_coords.map(c=>[c.lat,c.lon]);
    routeLayerRef.current = L.polyline(lls,{color,weight:5,opacity:.85}).addTo(map);
    map.fitBounds(routeLayerRef.current.getBounds(),{padding:[30,30]});
    resultEl.innerHTML = `<span style="color:var(--accent2);font-weight:700">${j.data.total_distance_km} km</span> · ${j.data.eta_minutes} min · ${j.data.node_count} nodes`;
    document.getElementById('c'+prefix+'km').textContent  = j.data.total_distance_km + ' km';
    document.getElementById('c'+prefix+'eta').textContent = j.data.eta_minutes + ' min';
    document.getElementById('comparePanel').style.display = 'grid';
  } else {
    resultEl.textContent = j.message || 'Error';
  }
}

const refA = {current:null}, refB = {current:null};

function setupSearch(inId, resId, state, key, map, ref, color, resEl, prefix) {
  const input   = document.getElementById(inId);
  const results = document.getElementById(resId);
  buildSearchUI(input, results, p => {
    state[key] = {lat:p.lat, lon:p.lon, name:p.name};
    L.marker([p.lat,p.lon]).addTo(map).bindPopup(p.name);
    map.setView([p.lat,p.lon],14);
    if (state.src && state.dst) computeCmp(state,map,ref,color,resEl,prefix);
  });
}

const aRes = document.getElementById('aResult');
const bRes = document.getElementById('bResult');

setupSearch('aSrcInput','aSrcResults',stateA,'src',mapA,refA,'#60a5fa',aRes,'A');
setupSearch('aDstInput','aDstResults',stateA,'dst',mapA,refA,'#60a5fa',aRes,'A');
setupSearch('bSrcInput','bSrcResults',stateB,'src',mapB,refB,'#34d399',bRes,'B');
setupSearch('bDstInput','bDstResults',stateB,'dst',mapB,refB,'#34d399',bRes,'B');
</script>
{% endblock %}
""")

# ═════════════════════════════════════════════ FAVOURITES ═══════════════════
w(os.path.join(T, 'favorites.html'), """
{% extends 'routing/base.html' %}
{% block title %}Favourites — RouteOptima{% endblock %}
{% block content %}
<div class="page-header"><h1>⭐ Saved Favourites</h1><div class="desc">Your bookmarked routes.</div></div>
<div class="page-body">
{% if saved %}
  {% for s in saved %}
  <div class="saved-card" id="saved-{{ s.id }}">
    <div class="saved-icon">⭐</div>
    <div style="flex:1">
      <div class="saved-label">{{ s.label }}</div>
      <div class="saved-meta">{{ s.route_log.src_name|default:"—" }} → {{ s.route_log.dst_name|default:"—" }} · {{ s.route_log.path_distance_km }} km · {{ s.saved_at|date:"M j, Y" }}</div>
    </div>
    <a href="{% url 'replay' s.route_log.id %}" class="btn btn-secondary btn-sm">▶ Replay</a>
    <a href="/share/{{ s.route_log.share_token }}/" class="btn btn-ghost btn-sm">🔗 Share</a>
    <button class="btn btn-danger btn-sm" onclick="deleteSaved({{ s.id }})">✕</button>
  </div>
  {% endfor %}
{% else %}
  <div class="card" style="text-align:center;padding:3rem">
    <div style="font-size:3rem;margin-bottom:.75rem">⭐</div>
    <div style="font-weight:700;margin-bottom:.4rem">No saved routes yet</div>
    <div style="color:var(--text2);font-size:13px;margin-bottom:1rem">Compute a route and click "Save" to bookmark it.</div>
    <a href="{% url 'map' %}" class="btn btn-primary">Open Route Map</a>
  </div>
{% endif %}
</div>
{% endblock %}
{% block scripts %}
<script>
async function deleteSaved(id) {
  if (!confirm('Remove this saved route?')) return;
  const r = await fetch(`/api/delete-saved/${id}/`, {
    method:'DELETE', credentials:'same-origin',
    headers:{'X-CSRFToken': document.cookie.split('; ').find(r=>r.startsWith('csrftoken='))?.split('=')[1]||''}
  });
  const j = await r.json();
  if (j.status === 'ok') document.getElementById('saved-'+id)?.remove();
}
</script>
{% endblock %}
""")

# ═════════════════════════════════════════════ SHARE (public) ════════════════
w(os.path.join(T, 'share.html'), """
{% extends 'routing/base.html' %}
{% load static %}
{% block title %}Shared Route — RouteOptima{% endblock %}
{% block head %}
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
{% endblock %}
{% block public %}
<nav class="landing-nav">
  <a href="{% url 'landing' %}" class="landing-logo"><div class="icon">&#9672;</div><div><div class="name">RouteOptima</div></div></a>
  <div class="nav-actions">
    <a href="{% url 'login' %}" class="btn btn-ghost btn-sm">Log In</a>
    <a href="{% url 'register' %}" class="btn btn-primary btn-sm">Sign Up Free</a>
  </div>
</nav>
<div style="padding:5rem 2rem 2rem;max-width:900px;margin:0 auto">
  <div class="card" style="margin-bottom:1rem">
    <div style="font-size:18px;font-weight:800;margin-bottom:.5rem">🔗 Shared Route</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:.75rem">
      <div><div style="font-size:11px;color:var(--text3);text-transform:uppercase;font-weight:700">From</div><div style="font-weight:600">{{ route.src_name|default:"Point A" }}</div></div>
      <div><div style="font-size:11px;color:var(--text3);text-transform:uppercase;font-weight:700">To</div><div style="font-weight:600">{{ route.dst_name|default:"Point B" }}</div></div>
      <div><div style="font-size:11px;color:var(--text3);text-transform:uppercase;font-weight:700">Distance</div><div style="font-weight:800;color:var(--accent2)">{{ route.path_distance_km }} km</div></div>
    </div>
  </div>
  <div style="height:450px;border-radius:12px;overflow:hidden;border:1px solid var(--border)">
    <div id="shareMap" style="width:100%;height:100%"></div>
  </div>
  <div style="text-align:center;margin-top:1.5rem">
    <a href="{% url 'register' %}" class="btn btn-primary btn-lg">Create Your Own Routes →</a>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script>
const m = L.map('shareMap').setView([{{ route.src_lat }}, {{ route.src_lon }}], 13);
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{subdomains:'abcd',maxZoom:19}).addTo(m);
L.marker([{{ route.src_lat }}, {{ route.src_lon }}]).addTo(m).bindPopup('Start').openPopup();
L.marker([{{ route.dst_lat }}, {{ route.dst_lon }}]).addTo(m).bindPopup('End');
L.polyline([[{{ route.src_lat }},{{ route.src_lon }}],[{{ route.dst_lat }},{{ route.dst_lon }}]],{color:'#3b82f6',weight:4,opacity:.8,dashArray:'8 4'}).addTo(m);
</script>
{% endblock %}
""")

# ═════════════════════════════════════════════ HEATMAP ══════════════════════
w(os.path.join(T, 'heatmap.html'), """
{% extends 'routing/base.html' %}
{% load static %}
{% block title %}Route Heatmap — RouteOptima{% endblock %}
{% block head %}
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>
{% endblock %}
{% block content %}
<div class="page-header"><h1>🔥 Route Heatmap</h1><div class="desc">Visualise the busiest origin and destination points across all routes.</div></div>
<div style="height:calc(100vh - 130px);padding:0 1.75rem 1rem">
  <div style="height:100%;border-radius:12px;overflow:hidden;border:1px solid var(--border);position:relative">
    <div id="heatmap" style="width:100%;height:100%"></div>
    <div style="position:absolute;top:.75rem;right:.75rem;z-index:1000;background:rgba(6,13,26,.9);border:1px solid var(--border);padding:.75rem 1rem;border-radius:10px;font-size:12px;color:var(--text2);backdrop-filter:blur(8px)">
      <div style="font-weight:700;color:var(--text1);margin-bottom:.4rem">Legend</div>
      <div style="display:flex;align-items:center;gap:.5rem"><div style="width:12px;height:12px;background:#f87171;border-radius:50%"></div> High activity</div>
      <div style="display:flex;align-items:center;gap:.5rem;margin-top:.25rem"><div style="width:12px;height:12px;background:#3b82f6;border-radius:50%"></div> Low activity</div>
    </div>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script>
const m = L.map('heatmap').setView([27.7103, 85.3222], 12);
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{subdomains:'abcd',maxZoom:19}).addTo(m);
fetch('/api/heatmap-data/', {credentials:'same-origin'})
  .then(r=>r.json()).then(d=>{
    if (d.points && d.points.length) {
      L.heatLayer(d.points, {radius:20, blur:18, maxZoom:17, gradient:{0.2:'#3b82f6',0.5:'#f59e0b',1:'#ef4444'}}).addTo(m);
    } else {
      // demo points around KTM
      const pts = [[27.7103,85.3222,1],[27.7200,85.3400,1],[27.6945,85.3420,0.8],[27.7350,85.3380,0.9],[27.7000,85.3300,0.6]];
      L.heatLayer(pts, {radius:25, blur:20}).addTo(m);
    }
  });
</script>
{% endblock %}
""")

# ═════════════════════════════════════════════ LEADERBOARD ══════════════════
w(os.path.join(T, 'leaderboard.html'), """
{% extends 'routing/base.html' %}
{% block title %}Leaderboard — RouteOptima{% endblock %}
{% block content %}
<div class="page-header"><h1>🏆 Leaderboard</h1><div class="desc">Top users by total distance computed.</div></div>
<div class="page-body">
  <div id="board" style="max-width:600px">
    <div style="text-align:center;color:var(--text3);padding:2rem">Loading…</div>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script>
const medals = ['🥇','🥈','🥉'];
fetch('/api/leaderboard-data/', {credentials:'same-origin'})
  .then(r=>r.json()).then(d=>{
    const board = document.getElementById('board');
    if (!d.leaderboard || !d.leaderboard.length) {
      board.innerHTML = '<div class="card" style="text-align:center;padding:2rem;color:var(--text2)">No data yet — be the first!</div>';
      return;
    }
    board.innerHTML = '';
    d.leaderboard.forEach((u, i) => {
      board.innerHTML += `
        <div class="leaderboard-row">
          <div class="leaderboard-rank">${medals[i] || (i+1)}</div>
          <div class="leaderboard-name">${u.user__username}</div>
          <div class="leaderboard-km">${(u.total_km||0).toFixed(2)} km</div>
          <div class="leaderboard-routes">${u.routes} routes</div>
        </div>`;
    });
  });
</script>
{% endblock %}
""")

# ═════════════════════════════════════════════ ETA CALCULATOR ═══════════════
w(os.path.join(T, 'eta.html'), """
{% extends 'routing/base.html' %}
{% block title %}ETA Calculator — RouteOptima{% endblock %}
{% block content %}
<div class="page-header"><h1>⏩ ETA Calculator</h1><div class="desc">Estimate travel time from a distance and travel mode.</div></div>
<div class="page-body">
  <div style="max-width:480px">
    <div class="card" style="margin-bottom:1rem">
      <div class="card-title">Distance</div>
      <div class="form-group">
        <label>Distance (km)</label>
        <input type="number" id="distInput" class="place-search-input" value="5" min="0.1" step="0.1" style="padding:.65rem .9rem">
      </div>
      <div class="card-title" style="margin-top:.75rem">Mode</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem;margin-bottom:1rem">
        <label style="cursor:pointer">
          <input type="radio" name="mode" value="walk" style="display:none">
          <div class="eta-card" id="mWalk" style="cursor:pointer">
            <div class="eta-icon">🚶</div>
            <div style="font-size:13px;font-weight:700">Walk</div>
            <div style="font-size:11px;color:var(--text3)">5 km/h</div>
          </div>
        </label>
        <label style="cursor:pointer">
          <input type="radio" name="mode" value="bike" style="display:none">
          <div class="eta-card" id="mBike">
            <div class="eta-icon">🚲</div>
            <div style="font-size:13px;font-weight:700">Bicycle</div>
            <div style="font-size:11px;color:var(--text3)">15 km/h</div>
          </div>
        </label>
        <label style="cursor:pointer">
          <input type="radio" name="mode" value="car" style="display:none" checked>
          <div class="eta-card" id="mCar" style="border-color:var(--accent)">
            <div class="eta-icon">🚗</div>
            <div style="font-size:13px;font-weight:700">Car</div>
            <div style="font-size:11px;color:var(--text3)">40 km/h</div>
          </div>
        </label>
      </div>
      <button class="btn btn-primary btn-full" onclick="calc()">Calculate ETA</button>
    </div>
    <div id="etaResult" style="display:none" class="card" style="text-align:center">
      <div class="card-title">Estimated Time</div>
      <div style="text-align:center;padding:.5rem 0">
        <div style="font-size:3.5rem;font-weight:900;color:var(--accent2)" id="etaMinVal">—</div>
        <div style="color:var(--text3);font-size:13px">minutes</div>
        <div style="margin-top:.75rem;color:var(--text2);font-size:13px" id="etaSubtext"></div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script>
const speeds = {walk:5, bike:15, car:40};
let selMode = 'car';
document.querySelectorAll('input[name="mode"]').forEach(r => {
  r.addEventListener('change', () => {
    selMode = r.value;
    document.querySelectorAll('.eta-card').forEach(c => c.style.borderColor='var(--border)');
    document.getElementById('m'+selMode.charAt(0).toUpperCase()+selMode.slice(1)).style.borderColor='var(--accent)';
  });
});
document.querySelectorAll('.eta-card').forEach(card => {
  card.addEventListener('click', () => {
    const inp = card.previousElementSibling;
    if (inp) { inp.checked = true; inp.dispatchEvent(new Event('change')); }
  });
});
function calc() {
  const dist = parseFloat(document.getElementById('distInput').value) || 0;
  const spd  = speeds[selMode] || 40;
  const mins = (dist / spd * 60);
  const h    = Math.floor(mins / 60);
  const m    = Math.round(mins % 60);
  document.getElementById('etaMinVal').textContent = Math.round(mins);
  document.getElementById('etaSubtext').textContent = h > 0 ? `${h}h ${m}min at ${spd} km/h` : `${m} min at ${spd} km/h`;
  document.getElementById('etaResult').style.display = 'block';
}
</script>
{% endblock %}
""")

# ═════════════════════════════════════════════ REPLAY ═══════════════════════
w(os.path.join(T, 'replay.html'), """
{% extends 'routing/base.html' %}
{% load static %}
{% block title %}Replay Route — RouteOptima{% endblock %}
{% block head %}
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
{% endblock %}
{% block content %}
<div class="page-header">
  <h1>▶ Route Replay</h1>
  <div class="desc">{{ route.src_name|default:"Start" }} → {{ route.dst_name|default:"End" }} · {{ route.path_distance_km }} km · {{ route.computed_at|date:"M j, Y H:i" }}</div>
</div>
<div style="padding:.5rem 1.75rem 1rem;height:calc(100vh - 130px)">
  <div style="height:100%;border-radius:12px;overflow:hidden;border:1px solid var(--border);position:relative">
    <div id="replayMap" style="width:100%;height:100%"></div>
    <div style="position:absolute;bottom:1rem;left:50%;transform:translateX(-50%);z-index:1000;display:flex;gap:.5rem">
      <button class="btn btn-primary btn-sm" onclick="startReplay()">▶ Play</button>
      <button class="btn btn-ghost btn-sm" onclick="resetReplay()">↺ Reset</button>
    </div>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script>
const m = L.map('replayMap').setView([{{ route.src_lat }},{{ route.src_lon }}], 14);
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{subdomains:'abcd',maxZoom:19}).addTo(m);
// Simple A→B line (real path requires storing coords, this is a placeholder)
const src = [{{ route.src_lat }},{{ route.src_lon }}];
const dst = [{{ route.dst_lat }},{{ route.dst_lon }}];
const fullLine = L.polyline([src,dst],{color:'#3b82f6',weight:4,opacity:.4,dashArray:'8 4'}).addTo(m);
m.fitBounds(fullLine.getBounds(),{padding:[60,60]});
const marker = L.marker(src).addTo(m).bindPopup('{{ route.src_name|default:"Start" }}').openPopup();
let animLine = null, frame = null;

function startReplay() {
  if (animLine) m.removeLayer(animLine);
  animLine = L.polyline([src],{color:'#34d399',weight:5}).addTo(m);
  let t = 0;
  function step() {
    t = Math.min(t + 0.015, 1);
    const lat = src[0] + (dst[0]-src[0])*t;
    const lon = src[1] + (dst[1]-src[1])*t;
    marker.setLatLng([lat,lon]);
    animLine.addLatLng([lat,lon]);
    if (t < 1) frame = requestAnimationFrame(step);
    else { marker.setLatLng(dst); marker.bindPopup('{{ route.dst_name|default:"End" }}').openPopup(); }
  }
  cancelAnimationFrame(frame);
  step();
}

function resetReplay() {
  cancelAnimationFrame(frame);
  marker.setLatLng(src);
  if (animLine) { m.removeLayer(animLine); animLine = null; }
}
</script>
{% endblock %}
""")

# ═════════════════════════════════════════════ HISTORY ══════════════════════
w(os.path.join(T, 'history.html'), """
{% extends 'routing/base.html' %}
{% block title %}History — RouteOptima{% endblock %}
{% block content %}
<div class="page-header"><h1>⏱ Route History</h1><div class="desc">All {{ routes.count }} routes computed by your account.</div></div>
<div class="page-body">
  <div class="table-wrap">
    <table>
      <thead><tr><th>ID</th><th>From</th><th>To</th><th>Distance</th><th>Nodes</th><th>Date</th><th></th></tr></thead>
      <tbody>
        {% for r in routes %}
        <tr>
          <td style="color:var(--text3)">{{ r.id }}</td>
          <td>{{ r.src_name|default:"—" }}</td>
          <td>{{ r.dst_name|default:"—" }}</td>
          <td><span class="badge badge-blue">{{ r.path_distance_km }} km</span></td>
          <td style="color:var(--text3)">{{ r.node_count }}</td>
          <td style="color:var(--text3)">{{ r.computed_at|date:"M j, Y H:i" }}</td>
          <td style="display:flex;gap:.4rem">
            <a href="{% url 'replay' r.id %}" class="btn btn-ghost btn-sm">▶</a>
            <a href="/share/{{ r.share_token }}/" class="btn btn-ghost btn-sm">🔗</a>
          </td>
        </tr>
        {% empty %}
        <tr><td colspan="7" style="text-align:center;padding:2rem;color:var(--text3)">No routes yet — <a href="{% url 'map' %}" style="color:var(--accent2)">compute your first!</a></td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}
""")

# ═════════════════════════════════════════════ ANALYTICS ════════════════════
w(os.path.join(T, 'analytics.html'), """
{% extends 'routing/base.html' %}
{% block title %}Analytics — RouteOptima{% endblock %}
{% block head %}<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>{% endblock %}
{% block content %}
<div class="page-header"><h1>📊 Analytics</h1><div class="desc">Your personal route statistics.</div></div>
<div class="page-body">
  <div class="stats-grid" id="statCards" style="margin-bottom:1.5rem">
    <div class="stat-card blue"><div class="stat-icon">🗺</div><div class="stat-val" id="sTotal">—</div><div class="stat-lbl">Total Routes</div></div>
    <div class="stat-card green"><div class="stat-icon">📏</div><div class="stat-val" id="sTotalKm">—</div><div class="stat-lbl">Total km</div></div>
    <div class="stat-card yellow"><div class="stat-icon">⚡</div><div class="stat-val" id="sAvg">—</div><div class="stat-lbl">Avg km</div></div>
    <div class="stat-card purple"><div class="stat-icon">◦</div><div class="stat-val" id="sNodes">—</div><div class="stat-lbl">Avg Nodes</div></div>
  </div>
  <div style="display:grid;grid-template-columns:2fr 1fr;gap:1rem">
    <div class="card"><div class="card-title">Routes Per Day (last 14 days)</div><canvas id="dailyChart" height="120"></canvas></div>
    <div class="card"><div class="card-title">Distance Breakdown</div><canvas id="distChart" height="160"></canvas></div>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script>
fetch('/api/analytics/', {credentials:'same-origin'}).then(r=>r.json()).then(d=>{
  const s = d.stats;
  document.getElementById('sTotal').textContent   = s.total || 0;
  document.getElementById('sTotalKm').textContent = (s.total_dist||0).toFixed(1);
  document.getElementById('sAvg').textContent     = (s.avg_dist||0).toFixed(2);
  document.getElementById('sNodes').textContent   = Math.round(s.avg_nodes||0);

  const accent = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#3b82f6';
  const accent2= getComputedStyle(document.documentElement).getPropertyValue('--accent2').trim()|| '#60a5fa';
  const text3  = getComputedStyle(document.documentElement).getPropertyValue('--text3').trim()  || '#5a7aaa';

  new Chart(document.getElementById('dailyChart'), {
    type:'bar',
    data:{labels:d.daily.map(x=>x.date.slice(5)),datasets:[{data:d.daily.map(x=>x.count),backgroundColor:accent+'44',borderColor:accent,borderWidth:2,borderRadius:4}]},
    options:{plugins:{legend:{display:false}},scales:{x:{ticks:{color:text3}},y:{ticks:{color:text3,stepSize:1},beginAtZero:true}}}
  });

  const km = s.total_dist || 1;
  new Chart(document.getElementById('distChart'), {
    type:'doughnut',
    data:{labels:['Computed','Goal 100km'],datasets:[{data:[Math.min(km,100),(100-Math.min(km,100))],backgroundColor:[accent,accent+'22'],borderWidth:0}]},
    options:{plugins:{legend:{labels:{color:text3,font:{size:11}}}},cutout:'70%'}
  });
});
</script>
{% endblock %}
""")

# ═════════════════════════════════════════════ SETTINGS ═════════════════════
w(os.path.join(T, 'settings.html'), """
{% extends 'routing/base.html' %}
{% block title %}Settings — RouteOptima{% endblock %}
{% block content %}
<div class="page-header"><h1>⚙ Settings</h1><div class="desc">Customise your RouteOptima experience.</div></div>
<div class="page-body">
  <div style="max-width:560px">
    {% if messages %}{% for m in messages %}<div class="message {{ m.tags }}">{{ m }}</div>{% endfor %}{% endif %}
    <form method="POST">
      {% csrf_token %}
      <div class="card" style="margin-bottom:1rem">
        <div class="card-title">Appearance Theme</div>
        <p style="font-size:13px;color:var(--text2);margin-bottom:1rem">Choose your preferred colour scheme. This is saved to your account and synced across devices.</p>
        <div class="theme-switcher">
          <div class="theme-dot {% if pref.theme == 'midnight' %}selected{% endif %}" data-t="midnight" title="Midnight"></div>
          <div class="theme-dot {% if pref.theme == 'obsidian' %}selected{% endif %}" data-t="obsidian" title="Obsidian"></div>
          <div class="theme-dot {% if pref.theme == 'emerald'  %}selected{% endif %}" data-t="emerald"  title="Emerald"></div>
          <div class="theme-dot {% if pref.theme == 'crimson'  %}selected{% endif %}" data-t="crimson"  title="Crimson"></div>
          <div class="theme-dot {% if pref.theme == 'arctic'   %}selected{% endif %}" data-t="arctic"   title="Arctic"></div>
          <div class="theme-dot {% if pref.theme == 'parchment' %}selected{% endif %}" data-t="parchment" title="Light"></div>
        </div>
        <div style="margin-top:.75rem;font-size:12px;color:var(--text3)">
          Midnight · Obsidian · Emerald · Crimson · Arctic · Parchment (light)
        </div>
        <input type="hidden" name="theme" id="themeInput" value="{{ pref.theme }}">
      </div>

      <div class="card" style="margin-bottom:1rem">
        <div class="card-title">Default Travel Mode</div>
        <div class="form-group">
          <label>Mode used when computing routes</label>
          <select name="speed_mode">
            <option value="walk" {% if pref.speed_mode == 'walk' %}selected{% endif %}>🚶 Walking (5 km/h)</option>
            <option value="bike" {% if pref.speed_mode == 'bike' %}selected{% endif %}>🚲 Bicycle (15 km/h)</option>
            <option value="car"  {% if pref.speed_mode == 'car'  %}selected{% endif %}>🚗 Car (40 km/h)</option>
          </select>
        </div>
      </div>

      <button type="submit" class="btn btn-primary">Save Settings</button>
    </form>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script>
document.querySelectorAll('.theme-dot').forEach(d=>{
  d.addEventListener('click',()=>{
    document.getElementById('themeInput').value = d.dataset.t;
  });
});
</script>
{% endblock %}
""")

# ═════════════════════════════════════════════ ABOUT ═════════════════════════
w(os.path.join(T, 'about.html'), """
{% extends 'routing/base.html' %}
{% block title %}About — RouteOptima{% endblock %}
{% block public %}
<nav class="landing-nav">
  <a href="{% url 'landing' %}" class="landing-logo"><div class="icon">&#9672;</div><div><div class="name">RouteOptima</div></div></a>
  <div class="nav-links">
    <a href="{% url 'landing' %}">Home</a>
    <a href="{% url 'docs' %}">Docs</a>
    <a href="{% url 'team' %}">Team</a>
    <a href="{% url 'help' %}">Help</a>
  </div>
  <div class="nav-actions">
    {% if user.is_authenticated %}
    <a href="{% url 'dashboard' %}" class="btn btn-primary btn-sm">Go to Dashboard</a>
    {% else %}
    <a href="{% url 'login' %}"    class="btn btn-ghost btn-sm">Log In</a>
    <a href="{% url 'register' %}" class="btn btn-primary btn-sm">Get Started</a>
    {% endif %}
  </div>
</nav>
{% block content %}
<div class="page-header" style="padding-top:5rem">
  <h1>About RouteOptima</h1>
  <div class="desc">Nepal's shortest-path route optimizer — built with Dijkstra's algorithm and OpenStreetMap.</div>
</div>
<div class="page-body">
  <div style="display:grid;grid-template-columns:1fr 300px;gap:1.5rem;max-width:960px">
    <div>
      <div class="card" style="margin-bottom:1rem">
        <div class="card-title">What is RouteOptima?</div>
        <p style="color:var(--text2);line-height:1.7;margin-bottom:.75rem">RouteOptima is a Final Year Project (FYP) built by Group 36 at IIMS College. It provides a web-based interface to compute the shortest drivable route between any two points across five districts of Nepal's Bagmati Province: <strong style="color:var(--text1)">Kathmandu, Bhaktapur, Lalitpur, Nuwakot, and Dhading</strong>.</p>
        <p style="color:var(--text2);line-height:1.7;margin-bottom:.75rem">Real road network data is pulled from <strong style="color:var(--text1)">OpenStreetMap</strong> using the <code style="color:var(--accent2);font-family:monospace">osmnx</code> library and stored locally as a GraphML file. The graph is loaded into memory once, and subsequent route queries run in milliseconds.</p>
        <p style="color:var(--text2);line-height:1.7">The core algorithm is <strong style="color:var(--accent2)">Dijkstra's Shortest Path First (SPF)</strong>, implemented via NetworkX. Users can search any place — a tea shop, a school, a bank — by name and instantly compute the shortest route.</p>
      </div>
      <div class="card" style="margin-bottom:1rem">
        <div class="card-title">Technology Stack</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:.65rem">
          <div style="padding:.65rem;background:var(--bg2);border-radius:8px;border:1px solid var(--border)"><div style="font-weight:700;margin-bottom:.2rem">Backend</div><div style="font-size:12px;color:var(--text2)">Python 3.11 · Django 4.x · Django REST Framework</div></div>
          <div style="padding:.65rem;background:var(--bg2);border-radius:8px;border:1px solid var(--border)"><div style="font-weight:700;margin-bottom:.2rem">Algorithm</div><div style="font-size:12px;color:var(--text2)">Dijkstra SPF · NetworkX · OSMnx</div></div>
          <div style="padding:.65rem;background:var(--bg2);border-radius:8px;border:1px solid var(--border)"><div style="font-weight:700;margin-bottom:.2rem">Database</div><div style="font-size:12px;color:var(--text2)">PostgreSQL (Render) — route logs, users, favourites</div></div>
          <div style="padding:.65px;background:var(--bg2);border-radius:8px;border:1px solid var(--border)"><div style="font-weight:700;margin-bottom:.2rem">Frontend</div><div style="font-size:12px;color:var(--text2)">HTML5 · CSS3 · Leaflet.js · Chart.js · Nominatim</div></div>
          <div style="padding:.65rem;background:var(--bg2);border-radius:8px;border:1px solid var(--border)"><div style="font-weight:700;margin-bottom:.2rem">Map Data</div><div style="font-size:12px;color:var(--text2)">OpenStreetMap (free, open-source)</div></div>
          <div style="padding:.65rem;background:var(--bg2);border-radius:8px;border:1px solid var(--border)"><div style="font-weight:700;margin-bottom:.2rem">Deployment</div><div style="font-size:12px;color:var(--text2)">Vercel (web) · Render (PostgreSQL)</div></div>
        </div>
      </div>
    </div>
    <div>
      <div class="card" style="margin-bottom:1rem">
        <div class="card-title">Project Details</div>
        <div style="display:flex;flex-direction:column;gap:.5rem;font-size:13px">
          <div style="display:flex;justify-content:space-between"><span style="color:var(--text3)">Group</span><span>Group 36</span></div>
          <div style="display:flex;justify-content:space-between"><span style="color:var(--text3)">Institute</span><span>IIMS College</span></div>
          <div style="display:flex;justify-content:space-between"><span style="color:var(--text3)">Partner</span><span>Taylor's University</span></div>
          <div style="display:flex;justify-content:space-between"><span style="color:var(--text3)">Year</span><span>2026</span></div>
          <div style="display:flex;justify-content:space-between"><span style="color:var(--text3)">Supervisor</span><span>Nabeen Kumar Aryal</span></div>
          <div style="display:flex;justify-content:space-between"><span style="color:var(--text3)">Algorithm</span><span style="color:var(--accent2)">Dijkstra SPF</span></div>
          <div style="display:flex;justify-content:space-between"><span style="color:var(--text3)">Districts</span><span>5</span></div>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Quick Links</div>
        <div style="display:flex;flex-direction:column;gap:.5rem">
          <a href="{% url 'docs' %}"  class="btn btn-secondary btn-sm" style="text-align:left">📚 API Documentation</a>
          <a href="{% url 'team' %}"  class="btn btn-secondary btn-sm" style="text-align:left">👥 Meet the Team</a>
          <a href="{% url 'help' %}"  class="btn btn-secondary btn-sm" style="text-align:left">❓ Help & FAQ</a>
          {% if user.is_authenticated %}
          <a href="{% url 'map' %}"   class="btn btn-primary btn-sm"   style="text-align:left">🗺 Open Route Map</a>
          {% else %}
          <a href="{% url 'register' %}" class="btn btn-primary btn-sm" style="text-align:left">🚀 Get Started Free</a>
          {% endif %}
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
{% endblock %}
""")

# ═════════════════════════════════════════════ TEAM ═════════════════════════
w(os.path.join(T, 'team.html'), """
{% extends 'routing/base.html' %}
{% block title %}Team — RouteOptima{% endblock %}
{% block public %}
<nav class="landing-nav">
  <a href="{% url 'landing' %}" class="landing-logo"><div class="icon">&#9672;</div><div><div class="name">RouteOptima</div></div></a>
  <div class="nav-links"><a href="{% url 'landing' %}">Home</a><a href="{% url 'about' %}">About</a><a href="{% url 'docs' %}">Docs</a></div>
  <div class="nav-actions">
    {% if user.is_authenticated %}<a href="{% url 'dashboard' %}" class="btn btn-primary btn-sm">Dashboard</a>
    {% else %}<a href="{% url 'login' %}" class="btn btn-ghost btn-sm">Log In</a><a href="{% url 'register' %}" class="btn btn-primary btn-sm">Sign Up</a>{% endif %}
  </div>
</nav>
{% block content %}
<div class="page-header" style="padding-top:5rem"><h1>👥 The Team</h1><div class="desc">Group 36 — IIMS College / Taylor's University · Capstone Project 2026</div></div>
<div class="page-body">
  <div class="card" style="max-width:820px;margin-bottom:1.5rem;padding:1.25rem 1.5rem">
    <p style="color:var(--text2);line-height:1.7">RouteOptima was designed and built by a five-person team under the supervision of <strong style="color:var(--text1)">Nabeen Kumar Aryal</strong> as part of the Bachelor of Computer Science (Honours) degree programme at IIMS College in partnership with Taylor's University, Malaysia.</p>
  </div>
  <div class="team-grid" style="max-width:900px">
    <div class="team-card" style="border-color:var(--accent)">
      <div class="team-avatar" style="background:var(--accent)">SK</div>
      <h3>Sudip KC</h3><div class="role">🏅 Project Leader<br>System Integration</div>
      <div class="email">sudip23012002@iimscollege.edu.np</div>
    </div>
    <div class="team-card">
      <div class="team-avatar">SG</div>
      <h3>Sohit Giri</h3><div class="role">⚙ Backend Architect<br>API & Database</div>
      <div class="email">sohit23012005@iimscollege.edu.np</div>
    </div>
    <div class="team-card">
      <div class="team-avatar">MK</div>
      <h3>Muskan Khadka</h3><div class="role">🗺 Map & Network<br>GIS Modelling</div>
      <div class="email">muskan23012027@iimscollege.edu.np</div>
    </div>
    <div class="team-card">
      <div class="team-avatar">MP</div>
      <h3>Mahima Parajuli</h3><div class="role">⚡ Algorithm Engineer<br>Dijkstra SPF</div>
      <div class="email">mahima23012049@iimscollege.edu.np</div>
    </div>
    <div class="team-card">
      <div class="team-avatar">AB</div>
      <h3>Apekshya Basnyat</h3><div class="role">🎨 Frontend Dev<br>UI / Simulation</div>
      <div class="email">apekshya23012030@iimscollege.edu.np</div>
    </div>
  </div>
</div>
{% endblock %}
{% endblock %}
""")

# ═════════════════════════════════════════════ DOCS ═════════════════════════
w(os.path.join(T, 'docs.html'), """
{% extends 'routing/base.html' %}
{% block title %}Documentation — RouteOptima{% endblock %}
{% block public %}
<nav class="landing-nav">
  <a href="{% url 'landing' %}" class="landing-logo"><div class="icon">&#9672;</div><div><div class="name">RouteOptima</div></div></a>
  <div class="nav-links"><a href="{% url 'landing' %}">Home</a><a href="{% url 'about' %}">About</a><a href="{% url 'team' %}">Team</a></div>
  <div class="nav-actions">
    {% if user.is_authenticated %}<a href="{% url 'dashboard' %}" class="btn btn-primary btn-sm">Dashboard</a>
    {% else %}<a href="{% url 'login' %}" class="btn btn-ghost btn-sm">Log In</a><a href="{% url 'register' %}" class="btn btn-primary btn-sm">Sign Up</a>{% endif %}
  </div>
</nav>
{% block content %}
<div class="page-header" style="padding-top:5rem"><h1>📚 API Documentation</h1><div class="desc">REST API reference for the RouteOptima backend</div></div>
<div class="page-body">
  <div class="content-wrap">
    <div class="card" style="margin-bottom:1rem">
      <div class="card-title">Authentication</div>
      <p style="font-size:13px;color:var(--text2);line-height:1.6">All protected endpoints require session authentication. Log in via the web UI at <code style="color:var(--accent2)">/login/</code>. The session cookie is automatically included. Public endpoints (<code style="color:var(--accent2)">/api/health/</code>, <code style="color:var(--accent2)">/api/graph/</code>) require no login.</p>
    </div>
    <div class="api-endpoint">
      <div><span class="endpoint-method method-post">POST</span><span class="endpoint-url">/api/route/</span></div>
      <p style="font-size:13px;color:var(--text2);margin:.4rem 0">Compute the shortest route using Dijkstra's algorithm.</p>
      <div class="code-block">Request: {"src_lat":27.7103,"src_lon":85.3222,"dst_lat":27.7350,"dst_lon":85.3400,"src_name":"Pashupatinath","dst_name":"Boudha","mode":"car"}
Response: {"status":"success","data":{"path_coords":[...],"total_distance_km":4.251,"eta_minutes":6.4,"node_count":47,"route_id":12,"share_token":"uuid..."}}</div>
    </div>
    <div class="api-endpoint">
      <div><span class="endpoint-method method-get">GET</span><span class="endpoint-url">/api/health/</span></div>
      <p style="font-size:13px;color:var(--text2);margin:.4rem 0">Check backend and graph status.</p>
      <div class="code-block">{"status":"ready","graph":{"loaded":true,"nodes":52300,"edges":119800,"loaded_count":5,"total":5}}</div>
    </div>
    <div class="api-endpoint">
      <div><span class="endpoint-method method-get">GET</span><span class="endpoint-url">/api/analytics/</span></div>
      <p style="font-size:13px;color:var(--text2);margin:.4rem 0">Get personal route statistics and daily counts.</p>
    </div>
    <div class="api-endpoint">
      <div><span class="endpoint-method method-post">POST</span><span class="endpoint-url">/api/save-route/</span></div>
      <p style="font-size:13px;color:var(--text2);margin:.4rem 0">Save a route to favourites.</p>
      <div class="code-block">{"route_id": 12, "label": "Office commute"}</div>
    </div>
    <div class="api-endpoint">
      <div><span class="endpoint-method method-get">GET</span><span class="endpoint-url">/api/heatmap-data/</span></div>
      <p style="font-size:13px;color:var(--text2);margin:.4rem 0">Returns lat/lon intensity points for heatmap overlay.</p>
    </div>
    <div class="api-endpoint">
      <div><span class="endpoint-method method-get">GET</span><span class="endpoint-url">/api/leaderboard-data/</span></div>
      <p style="font-size:13px;color:var(--text2);margin:.4rem 0">Top 10 users by total distance computed.</p>
    </div>
    <div class="api-endpoint">
      <div><span class="endpoint-method method-post">POST</span><span class="endpoint-url">/api/set-theme/</span></div>
      <p style="font-size:13px;color:var(--text2);margin:.4rem 0">Save the user's theme preference.</p>
      <div class="code-block">{"theme": "emerald"}</div>
    </div>
  </div>
</div>
{% endblock %}
{% endblock %}
""")

# ═════════════════════════════════════════════ HELP ══════════════════════════
w(os.path.join(T, 'help.html'), """
{% extends 'routing/base.html' %}
{% block title %}Help — RouteOptima{% endblock %}
{% block public %}
<nav class="landing-nav">
  <a href="{% url 'landing' %}" class="landing-logo"><div class="icon">&#9672;</div><div><div class="name">RouteOptima</div></div></a>
  <div class="nav-links"><a href="{% url 'landing' %}">Home</a><a href="{% url 'about' %}">About</a><a href="{% url 'docs' %}">Docs</a><a href="{% url 'team' %}">Team</a></div>
  <div class="nav-actions">
    {% if user.is_authenticated %}<a href="{% url 'dashboard' %}" class="btn btn-primary btn-sm">Dashboard</a>
    {% else %}<a href="{% url 'login' %}" class="btn btn-ghost btn-sm">Log In</a><a href="{% url 'register' %}" class="btn btn-primary btn-sm">Sign Up</a>{% endif %}
  </div>
</nav>
{% block content %}
<div class="page-header" style="padding-top:5rem"><h1>❓ Help & FAQ</h1><div class="desc">Common questions and troubleshooting tips.</div></div>
<div class="page-body">
  <div style="max-width:720px">
    <div class="faq-item"><div class="faq-q">Why is the map blank or stuck on "Loading districts"?</div><div class="faq-a">The backend is downloading road data for all 5 districts from OpenStreetMap on first run. This can take 2–5 minutes. The status indicator turns green when ready. Cached runs start instantly.</div></div>
    <div class="faq-item"><div class="faq-q">How does place search work?</div><div class="faq-a">We use the Nominatim (OpenStreetMap) geocoding API. Type any place name — a tea shop, school, temple, bank — and results will appear as a dropdown. Select one to place the marker.</div></div>
    <div class="faq-item"><div class="faq-q">Can I also click on the map instead of searching?</div><div class="faq-a">Yes! Click the "📌 Click on map" button to enter click mode. Your next click on the map places either the start or end marker. The map auto-reverses coordinates to a place name.</div></div>
    <div class="faq-item"><div class="faq-q">What districts are covered?</div><div class="faq-a">Kathmandu, Bhaktapur, Lalitpur, Nuwakot, and Dhading — all within Bagmati Province. The combined graph contains over 50,000 road nodes and 100,000+ edges.</div></div>
    <div class="faq-item"><div class="faq-q">How do I share a route?</div><div class="faq-a">After computing a route, click the "🔗 Share" button. A unique URL is copied to your clipboard. Anyone can open this link without needing to log in.</div></div>
    <div class="faq-item"><div class="faq-q">What is the Heatmap page?</div><div class="faq-a">It shows a visual heat map of the most popular start and end points across all users. Brighter areas mean more activity.</div></div>
    <div class="faq-item"><div class="faq-q">How does the Leaderboard work?</div><div class="faq-a">It ranks all registered users by their total computed distance (km). The more routes you calculate, the higher your ranking.</div></div>
    <div class="faq-item"><div class="faq-q">Can I change the colour theme?</div><div class="faq-a">Yes! Go to Settings or click the coloured dots in the top navigation bar. There are 6 themes: Midnight, Obsidian, Emerald, Crimson, Arctic, and Parchment (light).</div></div>
  </div>
</div>
{% endblock %}
{% endblock %}
""")

# ═════════════════════════════════════════════ REMAINING PAGES ══════════════
w(os.path.join(T, 'algorithm.html'), """
{% extends 'routing/base.html' %}
{% block title %}Algorithm — RouteOptima{% endblock %}
{% block head %}<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>{% endblock %}
{% block content %}
<div class="page-header"><h1>⚙ Dijkstra's Algorithm</h1><div class="desc">Step-by-step interactive explainer of the shortest path algorithm.</div></div>
<div class="page-body">
  <div style="display:grid;grid-template-columns:1fr 280px;gap:1rem;max-width:900px">
    <div class="card">
      <div class="card-title">How Dijkstra Works</div>
      <ol id="steps" style="padding-left:1.25rem;color:var(--text2);font-size:13px;line-height:2">
        <li>Start at the source node — assign distance 0. All others get ∞.</li>
        <li>Add source to a min-priority queue.</li>
        <li>Pop the node with smallest known distance.</li>
        <li>For each neighbour: calculate distance through current node.</li>
        <li>If shorter than known distance → update and re-queue.</li>
        <li>Repeat until the destination is popped from the queue.</li>
        <li>Trace back via predecessor pointers to build the path.</li>
      </ol>
      <div style="margin-top:1rem">
        <div class="card-title">Complexity</div>
        <div style="font-family:monospace;font-size:13px;color:var(--accent2)">O((V + E) log V) — with a min-heap priority queue</div>
        <div style="font-size:12px;color:var(--text3);margin-top:.25rem">V = vertices (nodes), E = edges. For Nepal 5-district graph: ~50K nodes, ~120K edges.</div>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Sample Graph Demo</div>
      <canvas id="algDemo" height="220"></canvas>
      <button class="btn btn-primary btn-sm" style="width:100%;margin-top:.75rem" onclick="runDemo()">▶ Animate</button>
      <div id="demoLog" style="font-size:11px;color:var(--text3);margin-top:.5rem;font-family:monospace;min-height:60px"></div>
    </div>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script>
const nodes = [{x:60,y:50},{x:200,y:30},{x:340,y:70},{x:100,y:160},{x:280,y:170},{x:380,y:200}];
const edges = [[0,1,4],[0,3,2],[1,2,5],[1,3,1],[1,4,3],[2,4,2],[3,4,4],[4,5,6],[2,5,3]];
const accent = ()=>getComputedStyle(document.documentElement).getPropertyValue('--accent').trim()||'#3b82f6';
const canvas = document.getElementById('algDemo');
const ctx = canvas.getContext('2d');
canvas.width = 420; canvas.height = 220;

function draw(visited=[],current=-1,path=[]) {
  ctx.clearRect(0,0,420,220);
  const sc = 1.05;
  edges.forEach(([a,b,w])=>{
    ctx.strokeStyle = path.includes(a) && path.includes(b) ? '#34d399' : '#334466';
    ctx.lineWidth = path.includes(a)&&path.includes(b) ? 2.5 : 1;
    ctx.beginPath(); ctx.moveTo(nodes[a].x*sc,nodes[a].y*sc+10); ctx.lineTo(nodes[b].x*sc,nodes[b].y*sc+10); ctx.stroke();
    const mx=(nodes[a].x+nodes[b].x)/2*sc, my=(nodes[a].y+nodes[b].y)/2*sc+10;
    ctx.fillStyle='#667'; ctx.font='10px monospace'; ctx.fillText(w,mx,my);
  });
  nodes.forEach((n,i)=>{
    ctx.beginPath(); ctx.arc(n.x*sc,n.y*sc+10,10,0,2*Math.PI);
    ctx.fillStyle = i===current?accent():visited.includes(i)?'#1d4ed8':'#1e3f78';
    ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=1.5; ctx.stroke();
    ctx.fillStyle='#fff'; ctx.font='bold 10px sans-serif'; ctx.textAlign='center'; ctx.fillText(i,n.x*sc,n.y*sc+14);
  });
}
draw();

async function runDemo() {
  const log = document.getElementById('demoLog');
  const dist=[Infinity,Infinity,Infinity,Infinity,Infinity,Infinity]; dist[0]=0;
  const visited=[], prev=[-1,-1,-1,-1,-1,-1];
  const queue=[0];
  log.textContent='Start → Node 0, dist=0';
  draw([],0,[]);
  await sleep(700);
  while(queue.length){
    queue.sort((a,b)=>dist[a]-dist[b]);
    const u=queue.shift(); visited.push(u);
    draw(visited,u,[]);
    log.textContent=`Visiting Node ${u} (dist=${dist[u]})`;
    await sleep(800);
    if(u===5) break;
    for(const [a,b,w] of edges){
      const nb = a===u?b:b===u?a:-1;
      if(nb<0||visited.includes(nb)) continue;
      if(dist[u]+w<dist[nb]){ dist[nb]=dist[u]+w; prev[nb]=u; queue.push(nb); }
    }
  }
  const path=[]; let c=5;
  while(c!==-1){path.unshift(c);c=prev[c];}
  draw(visited,-1,path);
  log.textContent=`Shortest: ${path.join('→')} (dist=${dist[5]})`;
}
function sleep(ms){return new Promise(r=>setTimeout(r,ms));}
</script>
{% endblock %}
""")

w(os.path.join(T, 'graph_explorer.html'), """
{% extends 'routing/base.html' %}
{% block title %}Graph Explorer — RouteOptima{% endblock %}
{% block content %}
<div class="page-header"><h1>◉ Graph Explorer</h1><div class="desc">Road network metadata for all loaded districts.</div></div>
<div class="page-body">
  <div class="stats-grid" style="margin-bottom:1.5rem">
    <div class="stat-card blue"><div class="stat-icon">◦</div><div class="stat-val">{{ graph_info.nodes|default:"—" }}</div><div class="stat-lbl">Total Nodes</div></div>
    <div class="stat-card green"><div class="stat-icon">↔</div><div class="stat-val">{{ graph_info.edges|default:"—" }}</div><div class="stat-lbl">Total Edges</div></div>
    <div class="stat-card yellow"><div class="stat-icon">📍</div><div class="stat-val">{{ graph_info.loaded_count|default:"0" }}</div><div class="stat-lbl">Districts Loaded</div></div>
    <div class="stat-card purple"><div class="stat-icon">✓</div><div class="stat-val">{% if graph_info.loaded %}Ready{% else %}Loading{% endif %}</div><div class="stat-lbl">Status</div></div>
  </div>
  {% if graph_info.loaded %}
  <div class="card">
    <div class="card-title">Loaded Districts</div>
    {% for d in graph_info.districts %}
    <div class="district-chip" style="display:inline-flex;margin:.25rem">📍 {{ d }}</div>
    {% endfor %}
  </div>
  {% else %}
  <div class="card"><div style="color:var(--yellow)">⏳ {{ graph_info.message }}</div></div>
  {% endif %}
</div>
{% endblock %}
""")

w(os.path.join(T, 'profile.html'), """
{% extends 'routing/base.html' %}
{% block title %}Profile — RouteOptima{% endblock %}
{% block content %}
<div class="page-header"><h1>👤 Profile</h1><div class="desc">Manage your account details.</div></div>
<div class="page-body">
  <div style="max-width:480px">
    {% if messages %}{% for m in messages %}<div class="message {{ m.tags }}">{{ m }}</div>{% endfor %}{% endif %}
    <div class="card" style="margin-bottom:1rem">
      <div class="card-title">Account Stats</div>
      <div style="display:flex;gap:1.5rem">
        <div><div style="font-size:24px;font-weight:800;color:var(--accent2)">{{ total_routes }}</div><div style="font-size:12px;color:var(--text3)">Total Routes</div></div>
        <div><div style="font-size:24px;font-weight:800;color:var(--green)">{{ user.date_joined|date:"M Y" }}</div><div style="font-size:12px;color:var(--text3)">Member Since</div></div>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Edit Profile</div>
      <form method="POST">
        {% csrf_token %}
        <div class="form-row">
          <div class="form-group"><label>First Name</label><input type="text" name="first_name" value="{{ user.first_name }}"></div>
          <div class="form-group"><label>Last Name</label><input type="text" name="last_name" value="{{ user.last_name }}"></div>
        </div>
        <div class="form-group"><label>Email</label><input type="email" name="email" value="{{ user.email }}"></div>
        <div class="form-group"><label>Username</label><input type="text" value="{{ user.username }}" disabled style="opacity:.6"></div>
        <button type="submit" class="btn btn-primary">Save Changes</button>
      </form>
    </div>
  </div>
</div>
{% endblock %}
""")

w(os.path.join(T, 'benchmark.html'), """
{% extends 'routing/base.html' %}
{% block title %}Benchmark — RouteOptima{% endblock %}
{% block content %}
<div class="page-header"><h1>⚡ Benchmark</h1><div class="desc">Test API response time for route computation.</div></div>
<div class="page-body">
  <div style="max-width:600px">
    <div class="card" style="margin-bottom:1rem">
      <div class="card-title">Run Benchmark</div>
      <div class="form-group"><label>Number of requests</label>
        <select id="nReq"><option>5</option><option selected>10</option><option>20</option></select></div>
      <button class="btn btn-primary" onclick="runBench()">▶ Start Benchmark</button>
      <div id="bProgress" style="display:none;margin-top:.75rem">
        <div style="font-size:12px;color:var(--text2);margin-bottom:.3rem" id="bStatus">Running…</div>
        <div class="progress-bar"><div class="progress-fill" id="bFill" style="width:0%"></div></div>
      </div>
    </div>
    <div id="bResults" style="display:none" class="bench-grid">
      <div class="bench-card"><div class="bench-val" id="bAvg">—</div><div class="bench-lbl">Avg ms</div></div>
      <div class="bench-card"><div class="bench-val" id="bMin">—</div><div class="bench-lbl">Min ms</div></div>
      <div class="bench-card"><div class="bench-val" id="bMax">—</div><div class="bench-lbl">Max ms</div></div>
      <div class="bench-card"><div class="bench-val" id="bOk">—</div><div class="bench-lbl">Success %</div></div>
    </div>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script>
const testRoutes=[
  {src_lat:27.7103,src_lon:85.3222,dst_lat:27.7350,dst_lon:85.3400,mode:'car'},
  {src_lat:27.6900,src_lon:85.3420,dst_lat:27.7200,dst_lon:85.3100,mode:'car'},
  {src_lat:27.7200,src_lon:85.3500,dst_lat:27.6750,dst_lon:85.3280,mode:'car'},
];
async function runBench(){
  const n=parseInt(document.getElementById('nReq').value);
  document.getElementById('bProgress').style.display='block';
  document.getElementById('bResults').style.display='none';
  const times=[]; let ok=0;
  for(let i=0;i<n;i++){
    const route=testRoutes[i%testRoutes.length];
    const t0=performance.now();
    try{
      const r=await fetch('/api/route/',{method:'POST',credentials:'same-origin',
        headers:{'Content-Type':'application/json','X-CSRFToken':document.cookie.split('; ').find(r=>r.startsWith('csrftoken='))?.split('=')[1]||''},
        body:JSON.stringify(route)});
      const j=await r.json();
      if(j.status==='success')ok++;
    }catch{}
    times.push(Math.round(performance.now()-t0));
    document.getElementById('bFill').style.width=((i+1)/n*100)+'%';
    document.getElementById('bStatus').textContent=`${i+1}/${n} requests done`;
  }
  const avg=Math.round(times.reduce((a,b)=>a+b,0)/times.length);
  document.getElementById('bAvg').textContent=avg;
  document.getElementById('bMin').textContent=Math.min(...times);
  document.getElementById('bMax').textContent=Math.max(...times);
  document.getElementById('bOk').textContent=Math.round(ok/n*100)+'%';
  document.getElementById('bResults').style.display='grid';
}
</script>
{% endblock %}
""")

w(os.path.join(T, 'nodes.html'), """
{% extends 'routing/base.html' %}
{% block title %}Nodes — RouteOptima{% endblock %}
{% block content %}
<div class="page-header"><h1>◦ Node Browser</h1><div class="desc">Road network node information.</div></div>
<div class="page-body">
  <div class="stats-grid" style="max-width:600px;margin-bottom:1.5rem">
    <div class="stat-card blue"><div class="stat-val">{{ graph_info.nodes|default:"—" }}</div><div class="stat-lbl">Nodes</div></div>
    <div class="stat-card green"><div class="stat-val">{{ graph_info.edges|default:"—" }}</div><div class="stat-lbl">Edges</div></div>
  </div>
  {% if not graph_info.loaded %}
  <div class="card" style="color:var(--yellow)">⏳ Graph loading — {{ graph_info.message }}</div>
  {% else %}
  <div class="card"><div class="card-title">About the Graph</div>
  <p style="color:var(--text2);font-size:13px;line-height:1.65">Each node represents a road intersection or endpoint in the OpenStreetMap data. Edges represent road segments with their length (in metres) as the weight used by Dijkstra's algorithm. The combined graph merges all {{ graph_info.loaded_count }} districts.</p></div>
  {% endif %}
</div>
{% endblock %}
""")

w(os.path.join(T, 'simulation.html'), """
{% extends 'routing/base.html' %}
{% load static %}
{% block title %}Simulation — RouteOptima{% endblock %}
{% block head %}
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
{% endblock %}
{% block content %}
<div class="page-header"><h1>▶ Route Simulation</h1><div class="desc">Animate a vehicle travelling a computed route.</div></div>
<div style="display:flex;height:calc(100vh - 130px);padding:0 1.75rem 1rem;gap:1rem">
  <div class="map-panel" style="border-radius:12px;border:1px solid var(--border)">
    <div class="card-title">Compute Route First</div>
    <p style="font-size:12px;color:var(--text2);margin-bottom:.75rem">Search or click map to pick start and end, then simulate.</p>
    <div class="place-search-wrap"><span class="place-search-icon">🔍</span>
      <input id="simSrc" class="place-search-input" type="text" placeholder="Start" autocomplete="off">
      <div id="simSrcRes" class="place-results" style="display:none"></div></div>
    <div class="place-search-wrap" style="margin-top:.5rem"><span class="place-search-icon">🔍</span>
      <input id="simDst" class="place-search-input" type="text" placeholder="Destination" autocomplete="off">
      <div id="simDstRes" class="place-results" style="display:none"></div></div>
    <button class="btn btn-primary btn-sm" style="width:100%;margin-top:.75rem" onclick="simRoute()">Compute</button>
    <div id="simStatus" style="font-size:12px;color:var(--text3);margin-top:.5rem"></div>
    <button id="simPlay" class="btn btn-secondary btn-sm" style="width:100%;margin-top:.5rem;display:none" onclick="playSimulation()">▶ Start Simulation</button>
    <div style="margin-top:.75rem" id="speedRow" style="display:none">
      <label style="font-size:11px;color:var(--text3)">Speed</label>
      <input type="range" id="simSpeed" min="1" max="10" value="5" style="width:100%;accent-color:var(--accent)">
    </div>
  </div>
  <div style="flex:1;border-radius:12px;overflow:hidden;border:1px solid var(--border)">
    <div id="simMap" style="width:100%;height:100%"></div>
  </div>
</div>
{% endblock %}
{% block scripts %}
<script>
const smap = L.map('simMap').setView([27.7103,85.3222],12);
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{subdomains:'abcd',maxZoom:19}).addTo(smap);
let simPath=[], simLine=null, simMarker=null, animFrame=null;
let simSrc=null, simDst=null;

buildSearchUI(document.getElementById('simSrc'),document.getElementById('simSrcRes'),p=>{simSrc=p;});
buildSearchUI(document.getElementById('simDst'),document.getElementById('simDstRes'),p=>{simDst=p;});

async function simRoute(){
  if(!simSrc||!simDst){document.getElementById('simStatus').textContent='Please select both points.';return;}
  document.getElementById('simStatus').textContent='Computing…';
  const csrf=document.cookie.split('; ').find(r=>r.startsWith('csrftoken='))?.split('=')[1]||'';
  const r=await fetch('/api/route/',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json','X-CSRFToken':csrf},
    body:JSON.stringify({src_lat:simSrc.lat,src_lon:simSrc.lon,dst_lat:simDst.lat,dst_lon:simDst.lon,mode:'car',src_name:simSrc.name,dst_name:simDst.name})});
  const j=await r.json();
  if(j.status!=='success'){document.getElementById('simStatus').textContent=j.message;return;}
  simPath=j.data.path_coords.map(c=>[c.lat,c.lon]);
  if(simLine)smap.removeLayer(simLine);
  simLine=L.polyline(simPath,{color:'#3b82f6',weight:4,opacity:.5}).addTo(smap);
  smap.fitBounds(simLine.getBounds(),{padding:[40,40]});
  document.getElementById('simStatus').textContent=`Route ready — ${j.data.total_distance_km} km`;
  document.getElementById('simPlay').style.display='block';
  document.getElementById('speedRow').style.display='block';
}

function playSimulation(){
  if(!simPath.length)return;
  cancelAnimationFrame(animFrame);
  if(simMarker)smap.removeLayer(simMarker);
  simMarker=L.marker(simPath[0]).addTo(smap);
  let idx=0;
  const speed=()=>parseInt(document.getElementById('simSpeed').value);
  function step(){
    idx=Math.min(idx+speed(),simPath.length-1);
    simMarker.setLatLng(simPath[idx]);
    if(idx<simPath.length-1)animFrame=requestAnimationFrame(step);
  }
  step();
}
</script>
{% endblock %}
""")

w(os.path.join(T, 'export.html'), """
{% extends 'routing/base.html' %}
{% block title %}Export — RouteOptima{% endblock %}
{% block content %}
<div class="page-header"><h1>⬇ Export Data</h1><div class="desc">Download your route history in various formats.</div></div>
<div class="page-body">
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;max-width:700px;margin-bottom:1.5rem">
    <a href="?format=csv" class="card" style="text-align:center;cursor:pointer;text-decoration:none">
      <div style="font-size:2.5rem;margin-bottom:.75rem">📄</div>
      <h3 style="margin-bottom:.3rem">CSV</h3><p style="font-size:12px;color:var(--text2)">Excel-compatible spreadsheet of all routes</p>
    </a>
    <a href="?format=json" class="card" style="text-align:center;cursor:pointer;text-decoration:none">
      <div style="font-size:2.5rem;margin-bottom:.75rem">📋</div>
      <h3 style="margin-bottom:.3rem">JSON</h3><p style="font-size:12px;color:var(--text2)">Full JSON export for developers</p>
    </a>
    <div class="card" style="text-align:center;opacity:.5">
      <div style="font-size:2.5rem;margin-bottom:.75rem">🗺</div>
      <h3 style="margin-bottom:.3rem">GeoJSON</h3><p style="font-size:12px;color:var(--text2)">Coming soon</p>
    </div>
  </div>
  <div class="card"><div class="card-title">{{ routes.count }} Routes Available</div>
    <p style="font-size:13px;color:var(--text2)">Export includes route ID, place names, coordinates, distance, node count, and timestamp.</p>
  </div>
</div>
{% endblock %}
""")

w(os.path.join(T, 'report.html'), """
{% extends 'routing/base.html' %}
{% block title %}Report — RouteOptima{% endblock %}
{% block content %}
<div class="page-header"><h1>📄 Report</h1><div class="desc">Auto-generated summary for your route activity.</div></div>
<div class="page-body">
  <div class="report-header">
    <div style="font-size:1.5rem;font-weight:900;margin-bottom:.4rem">RouteOptima User Report</div>
    <div style="font-size:13px;color:var(--text2)">{{ user.get_full_name|default:user.username }} · Generated {{ "now"|date:"M j, Y" }}</div>
  </div>
  <div class="stats-grid" style="margin-bottom:1.25rem">
    <div class="stat-card blue"><div class="stat-val">{{ total }}</div><div class="stat-lbl">Total Routes</div></div>
    <div class="stat-card green"><div class="stat-val">{{ total_km }}</div><div class="stat-lbl">Total km</div></div>
    <div class="stat-card yellow"><div class="stat-val">{{ avg_km }}</div><div class="stat-lbl">Avg km/Route</div></div>
    <div class="stat-card purple"><div class="stat-val">{% if max_route %}{{ max_route.path_distance_km }}{% else %}—{% endif %}</div><div class="stat-lbl">Longest Route km</div></div>
  </div>
  {% if routes %}
  <div class="table-wrap card" style="padding:0">
    <table>
      <thead><tr><th>#</th><th>From</th><th>To</th><th>Distance</th><th>Date</th></tr></thead>
      <tbody>
        {% for r in routes %}
        <tr>
          <td style="color:var(--text3)">{{ r.id }}</td>
          <td>{{ r.src_name|default:"—" }}</td>
          <td>{{ r.dst_name|default:"—" }}</td>
          <td><span class="badge badge-blue">{{ r.path_distance_km }} km</span></td>
          <td style="color:var(--text3)">{{ r.computed_at|date:"M j, Y" }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% endif %}
</div>
{% endblock %}
""")

print("\n" + "═"*64)
print("  RouteOptima v2 — All files created! ✓")
print("═"*64)
print("""
═══════════════════════════════════════════════════════════════
  STEP 1 — Install dependencies
═══════════════════════════════════════════════════════════════

  cd backend
  pip install -r ../requirements.txt

═══════════════════════════════════════════════════════════════
  STEP 2 — Database migrations (PostgreSQL on Render)
═══════════════════════════════════════════════════════════════

  python manage.py makemigrations routing
  python manage.py migrate
  python manage.py createsuperuser

═══════════════════════════════════════════════════════════════
  STEP 3 — Run locally
═══════════════════════════════════════════════════════════════

  python manage.py runserver
  → Open http://127.0.0.1:8000/

  The graph downloads all 5 districts on first run (~2-5 min).
  Watch logs for: "Combined graph: XXXXX nodes, XXXXX edges"

═══════════════════════════════════════════════════════════════
  STEP 4 — Deploy to GitHub + Vercel
═══════════════════════════════════════════════════════════════

  1.  Create a NEW GitHub repo (e.g. route-optimizer)

  2.  In your project root (where setup_project.py is):
      git init
      git add .
      git commit -m "Initial RouteOptima v2"
      git remote add origin https://github.com/YOUR_USER/route-optimizer.git
      git push -u origin main

  3.  Go to https://vercel.com → New Project → Import from GitHub
      → Select your repo → Framework: Other
      → Root Directory: leave blank (vercel.json is at root)

  4.  In Vercel → Settings → Environment Variables, add:
      SECRET_KEY        = any-long-random-string
      DEBUG             = False
      DB_NAME           = fyp_n7gx
      DB_USER           = fyp_n7gx_user
      DB_PASSWORD       = F3bhOrPukM6SmdkauOWuuFstRSsUArBN
      DB_HOST           = dpg-d75pgdp4tr6s73cbra3g-a.ohio-postgres.render.com
      DB_PORT           = 5432
      EMAIL_HOST_USER   = negativezero48@gmail.com
      EMAIL_HOST_PASSWORD = ytsb nbhs znjs uiby

  5.  Click Deploy! Vercel auto-runs build_files.sh

═══════════════════════════════════════════════════════════════
  IMPORTANT NOTE about the graph on Vercel
═══════════════════════════════════════════════════════════════

  Vercel's serverless functions have a 50 MB limit and short
  cold-start time — the OSM graph (~200 MB) can't run there.

  RECOMMENDED: Deploy the Django backend on Render (free tier)
  and use Vercel only for static assets, OR run everything on
  Render as a Web Service:

  Render Web Service command:
    cd backend && gunicorn core.wsgi:application

  Then your vercel.json becomes just a redirect to Render URL.

═══════════════════════════════════════════════════════════════
  6 SURPRISE FEATURES added ✓
═══════════════════════════════════════════════════════════════

  ⭐  Saved Favourites   — /favorites/ — bookmark routes
  🔗  Route Sharing      — /share/<token>/ — public share link
  ⏩  ETA Calculator     — /eta/ — walk/bike/car time estimator
  🔥  Route Heatmap      — /heatmap/ — popular point visualiser
  🏆  Leaderboard        — /leaderboard/ — top users by km
  ▶   Route Replay       — /replay/<id>/ — animate past routes

  Plus: 6 colour themes (Midnight/Obsidian/Emerald/Crimson/Arctic/Light)
        Place search with Nominatim (any shop, school, temple)
        Welcome email on registration
        Back-to-Home on login/register pages
""")