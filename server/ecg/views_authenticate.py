from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor, Patient
from .serializers import DoctorSerializer, PatientSerializer
from typing import cast
from loguru import logger


class DoctorRegisterView(APIView):
    def post(self, request):
        full_name = request.data.get('full_name')
        phone_number = request.data.get('phone_number')
        # IF already someone exists
        if Doctor.objects.filter(
            full_name=full_name, phone_number=phone_number).exists():
            return Response(
                {'error': 'Doctor already exists'},
                status=status.HTTP_409_CONFLICT
            )
        # If None Exists
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            doctor = cast(Doctor, serializer.save())
            return Response(
                {'status': 'success', 'doctor_id': doctor.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientRegisterView(APIView):
    def post(self, request):
        full_name = request.data.get('full_name')
        phone_number = request.data.get('phone_number')
        # IF already someone exists
        if Patient.objects.filter(
            full_name=full_name, phone_number=phone_number).exists():
            return Response(
                {'error': 'Patient already exists'},
                status=status.HTTP_409_CONFLICT
            )
        # If None Exists
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            patient = cast(Patient,serializer.save())
            return Response(
                {'status': 'success', 'patient_id': patient.id},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorLoginView(APIView):
    def post(self, request):
        full_name = request.data.get('full_name')
        password = request.data.get('password')
        if not full_name or not password:
            return Response(
                {'error': 'Missing credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            doctor = Doctor.objects.get(full_name=full_name)
        except Doctor.DoesNotExist:
            return Response(
                {'error': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not doctor.check_password(password):
            return Response(
                {'error': 'Invalid password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response({
            'status': 'success',
            'id': doctor.id,
            'full_name': doctor.full_name
        })

class PatientLoginView(APIView):
    def post(self, request):
        full_name = request.data.get('full_name')
        password = request.data.get('password')

        if not full_name or not password:
            return Response(
                {'error': 'Missing credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            patient = Patient.objects.get(full_name=full_name)
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not patient.check_password(password):
            return Response(
                {'error': 'Invalid password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response({
            'status': 'success',
            'id': patient.id,
            'full_name': patient.full_name
        })

