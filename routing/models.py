import random

from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from datetime import timedelta

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

class UserOTP(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    email = models.EmailField()

    otp_code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False)

    purpose = models.CharField(
        max_length=20,
        choices=[
            ("signup","signup"),
            ("reset","reset"),
        ],
        default="signup"
    )

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=5)

    @classmethod
    def generate_signup(cls,email):

        cls.objects.filter(
            email=email,
            purpose="signup",
            is_verified=False
        ).delete()

        otp = f"{random.randint(100000,999999)}"

        return cls.objects.create(
            email=email,
            otp_code=otp,
            purpose="signup"
        )

    @classmethod
    def generate_reset(cls,user):

        cls.objects.filter(
            user=user,
            purpose="reset",
            is_verified=False
        ).delete()

        otp = f"{random.randint(100000,999999)}"

        return cls.objects.create(
            user=user,
            email=user.email,
            otp_code=otp,
            purpose="reset"
        )