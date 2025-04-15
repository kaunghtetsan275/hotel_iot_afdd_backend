from rest_framework import serializers
from .models import Hotel, Floor, Room, Device, FaultStatus, FaultThreshold

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class FaultStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultStatus
        fields = '__all__'

class FaultThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultThreshold
        fields = '__all__'