from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ecg.models import Doctor, Patient
from ecg.serializers.authenticate import DoctorSerializer, PatientSerializer,DoctorLoginSerializer,PatientLoginSerializer
from typing import cast
# from loguru import logger
# from pprint import pformat

class DoctorRegisterView(APIView):
    serializer_class = DoctorSerializer

    def post(self, request):
        # logger.debug(f"Request details:\n{pformat(request.__dict__)}")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            doctor = cast(Doctor, serializer.save())
            return Response(
                {'status': 'success', 'doctor_id': doctor.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientRegisterView(APIView):
    serializer_class = PatientSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            patient = cast(Patient,serializer.save())
            return Response(
                {'status': 'success', 'patient_id': patient.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorLoginView(APIView):
    serializer_class = DoctorLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor = serializer.validated_data.get("doctor")
        return Response(
            {
                "status": "success",
                "id": doctor.id,
                "full_name": doctor.full_name,
            },
            status=status.HTTP_200_OK,
        )

class PatientLoginView(APIView):
    serializer_class = PatientLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.validated_data.get("patient")
        return Response(
            {
                "status": "success",
                "id": patient.id,
                "full_name": patient.full_name,
            },
            status=status.HTTP_200_OK,
        )
