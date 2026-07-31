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
