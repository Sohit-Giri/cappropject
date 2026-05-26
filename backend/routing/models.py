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
    path_coords      = models.TextField(null=True, blank=True)
    node_count       = models.IntegerField()
    computed_at      = models.DateTimeField(auto_now_add=True)
    share_token      = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, null=True)

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
