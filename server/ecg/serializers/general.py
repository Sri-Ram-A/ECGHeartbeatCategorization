from rest_framework import serializers
from ecg.models import RecordingSession, Device
from rest_framework import serializers

class RecordingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordingSession
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
