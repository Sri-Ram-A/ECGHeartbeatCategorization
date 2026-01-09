from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ecg.models import Doctor, Patient
from ecg.serializers import DoctorSerializer, PatientSerializer

class PatientListView(APIView):
    serializer_class = PatientSerializer
    def get(self, request):
        patients = Patient.objects.all()
        serializer = self.serializer_class(patients, many=True)
        return Response(
            {'patients': serializer.data},
            status=status.HTTP_200_OK
        )

class DoctorListView(APIView):
    serializer_class = DoctorSerializer

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = self.serializer_class(doctors, many=True)
        return Response(
            {'doctors': serializer.data},
            status=status.HTTP_200_OK
        )
