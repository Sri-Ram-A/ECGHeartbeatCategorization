from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ecg.models import RecordingSession
from ecg.mqtt_client import mqtt_client
from typing import cast
from loguru import logger

COMMAND_TOPIC_FMT = "commands/{doctor_id}/{patient_id}"

class StartStreamingView(APIView):
    def post(self, request, doctor_id, patient_id):
        # Check for active session
        active_session = RecordingSession.objects.filter(
            doctor_id=doctor_id,
            patient_id=patient_id,
            stopped_at__isnull=True
        ).first()
        if active_session:
            return Response(
                {'error': 'Recording session already running',
                 'message': 'Recording session already running'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Create new session
        session = RecordingSession.objects.create(
            doctor_id=doctor_id,
            patient_id=patient_id,
            verdict='pending'
        )
        # Publish MQTT start command
        topic = COMMAND_TOPIC_FMT.format(doctor_id = doctor_id,patient_id = patient_id)
        mqtt_client.publish(topic, "start")
        logger.info(f"Sent START command to {topic}")

        return Response({
            'status': 'success',
            'session_id': session.id,
            'message': 'started'
        })


class StopStreamingView(APIView):
    def post(self, request, doctor_id, patient_id):
        # Find active session
        session = RecordingSession.objects.filter(
            doctor_id=doctor_id,
            patient_id=patient_id,
            stopped_at__isnull=True
        ).order_by('-started_at').first()
        if not session:
            return Response(
                {'error': 'No active recording session found',
                 'message': 'No active recording session found'},
                status=status.HTTP_404_NOT_FOUND
            )
        # Stop session
        session.stopped_at = timezone.now()
        session.save()
        # Publish MQTT stop command
        topic = f"commands/{doctor_id}/{patient_id}"
        mqtt_client.publish(topic, "stop")
        logger.warning(f"Sent STOP command to {topic}")
        return Response({
            'status': 'success',
            'session_id': session.id,
            'message': 'stopped'
        })


