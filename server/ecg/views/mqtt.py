from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ecg.mqtt_client import mqtt_client
from ecg.serializers.mqtt import StartStreamingSerializer,StopStreamingSerializer
from loguru import logger
COMMAND_TOPIC_FMT = "commands/{doctor_id}/{patient_id}"

class StartStreamingView(APIView):
    serializer_class = StartStreamingSerializer

    def post(self, request, doctor_id, patient_id):
        serializer = self.serializer_class(data={"doctor_id": doctor_id,"patient_id": patient_id})
        serializer.is_valid(raise_exception=True)
        session = serializer.save()

        topic = COMMAND_TOPIC_FMT.format(doctor_id=doctor_id,patient_id=patient_id)
        mqtt_client.publish(topic, "start")
        logger.info(f"Sent START command to {topic}")
        return Response({"status": "success","session_id": session.id,"message": "started"},status=status.HTTP_201_CREATED)

class StopStreamingView(APIView):
    serializer_class = StopStreamingSerializer

    def post(self, request, doctor_id, patient_id):
        serializer = self.serializer_class(data={"doctor_id": doctor_id,"patient_id": patient_id})
        serializer.is_valid(raise_exception=True)
        session = serializer.save()

        topic = COMMAND_TOPIC_FMT.format(doctor_id=doctor_id,patient_id=patient_id)
        mqtt_client.publish(topic, "stop")
        logger.warning(f"Sent STOP command to {topic}")

        return Response({"status": "success","session_id": session.id,"message": "stopped"},status=status.HTTP_200_OK)


