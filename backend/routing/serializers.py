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
