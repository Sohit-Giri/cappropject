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
