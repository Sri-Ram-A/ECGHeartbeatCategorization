from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor, Patient
from .serializers import DoctorSerializer, PatientSerializer
from loguru import logger

class PatientListView(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(
            {'patients': serializer.data},
            status=status.HTTP_200_OK
        )

class DoctorListView(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(
            {'doctors': serializer.data},
            status=status.HTTP_200_OK
        )
