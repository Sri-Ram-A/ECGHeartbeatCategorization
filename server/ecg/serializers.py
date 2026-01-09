from rest_framework import serializers
from .models import Doctor, Patient, RecordingSession, Device
from django.utils import timezone
from rest_framework import serializers

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
    
    def validate(self, attrs):
        full_name = attrs.get('full_name')
        phone_number = attrs.get('phone_number')
        if Doctor.objects.filter(full_name=full_name,phone_number=phone_number).exists():
            raise serializers.ValidationError("Doctor with this full name and phone number already exists.")
        return attrs
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        doctor = Doctor(**validated_data)
        doctor.set_password(password)
        doctor.save()
        return doctor

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def validate(self, attrs):
        full_name = attrs.get('full_name')
        phone_number = attrs.get('phone_number')
        if Patient.objects.filter(full_name=full_name,phone_number=phone_number).exists():
            raise serializers.ValidationError("Patient with this full name and phone number already exists.")
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        patient = Patient(**validated_data)
        patient.set_password(password)
        patient.save()
        return patient

class DoctorLoginSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        full_name = attrs.get("full_name")
        password = attrs.get("password")
        try:
            doctor = Doctor.objects.get(full_name=full_name)
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Doctor not found")
        if not doctor.check_password(password):
            raise serializers.ValidationError("Invalid password")
        # attach the authenticated object for later use
        attrs["doctor"] = doctor
        return attrs

class PatientLoginSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        full_name = attrs.get("full_name")
        password = attrs.get("password")
        try:
            patient = Patient.objects.get(full_name=full_name)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient not found")
        if not patient.check_password(password):
            raise serializers.ValidationError("Invalid password")
        attrs["patient"] = patient
        return attrs
class RecordingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordingSession
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'



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
