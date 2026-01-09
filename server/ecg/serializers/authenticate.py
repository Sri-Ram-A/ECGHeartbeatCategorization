from rest_framework import serializers
from ecg.models import Doctor, Patient
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



