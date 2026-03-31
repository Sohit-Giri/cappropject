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
