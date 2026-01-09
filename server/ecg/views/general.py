from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ecg.models import Doctor, Patient,RecordingSession,Device
from ecg.serializers.authenticate import DoctorSerializer, PatientSerializer
from ecg.serializers.general import RecordingSessionSerializer,DeviceSerializer
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
class RecordingListView(APIView):
    serializer_class = RecordingSessionSerializer

    def get(self, request):
        recordings = RecordingSession.objects.all()
        serializer = self.serializer_class(recordings, many=True)
        return Response(
            {'recordings': serializer.data},
            status=status.HTTP_200_OK
        )
class DeviceListView(APIView):
    serializer_class = DeviceSerializer

    def get(self, request):
        devices = Device.objects.all()
        serializer = self.serializer_class(devices, many=True)
        return Response(
            {'devices': serializer.data},
            status=status.HTTP_200_OK
        )
