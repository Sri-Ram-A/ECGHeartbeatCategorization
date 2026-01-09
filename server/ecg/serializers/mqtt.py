from rest_framework import serializers
from ecg.models import RecordingSession
from django.utils import timezone
from rest_framework import serializers

class StartStreamingSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField()
    patient_id = serializers.IntegerField()

    def validate(self, attrs):
        doctor_id = attrs["doctor_id"]
        patient_id = attrs["patient_id"]
        active_session = RecordingSession.objects.filter(
            doctor_id=doctor_id,
            patient_id=patient_id,
            stopped_at__isnull=True
        ).first()
        if active_session:
            raise serializers.ValidationError("Recording session already running")
        return attrs

    def create(self, validated_data):
        return RecordingSession.objects.create(
            doctor_id=validated_data["doctor_id"],
            patient_id=validated_data["patient_id"],
            verdict="pending"
        )


class StopStreamingSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField()
    patient_id = serializers.IntegerField()

    def validate(self, attrs):
        session = RecordingSession.objects.filter(
            doctor_id=attrs["doctor_id"],
            patient_id=attrs["patient_id"],
            stopped_at__isnull=True
        ).order_by("-started_at").first()
        if not session:
            raise serializers.ValidationError("No active recording session found")
        attrs["session"] = session
        return attrs
    
    # No create() here — stopping is not creation
    def save(self):
        session = self.validated_data["session"]
        session.stopped_at = timezone.now()
        session.save()
        return session
