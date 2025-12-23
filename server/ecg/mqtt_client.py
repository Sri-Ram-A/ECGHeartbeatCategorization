import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import json
from loguru import logger
from django.conf import settings
from django.utils import timezone

DEVICE_REGISTER_TOPIC = "devices/register"
ECG_STREAM_TOPIC = "stream/+/+"
PREDICTION_TOPIC = "prediction/+/+"

class MQTTClient:

    def __init__(self):
        self.client = None
        self.connected = False

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.connected = True
            client.subscribe([
                (ECG_STREAM_TOPIC, 1),
                (PREDICTION_TOPIC, 1),
                (DEVICE_REGISTER_TOPIC, 1)
            ])
            logger.success("MQTT connected & subscribed")

    def on_disconnect(self, client, userdata, rc, properties=None):
        logger.warning(f"Disconnected from MQTT broker (rc={rc})")
        self.connected = False

    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode())
        topic = msg.topic

        if topic == DEVICE_REGISTER_TOPIC:
            self.handle_device_registration(payload)
        
        elif topic.startswith("stream"):
            self.handle_ecg_stream(topic, payload)

        elif topic.startswith("prediction"):
            self.handle_prediction(topic, payload)

    def handle_ecg_stream(self, topic, payload):
        _, doctor_id, patient_id = topic.split("/")
        values = payload["values"]
        logger.info(f"ECG RX | D:{doctor_id} P:{patient_id}")
        # Store / forward via WebSocket later

    def handle_prediction(self, topic, payload):
        _, doctor_id, patient_id = topic.split("/")
        prediction = payload["prediction"]
        confidence = payload.get("confidence")
        logger.success(f"PREDICTION | D:{doctor_id} P:{patient_id} → {prediction}")

        # Save verdict to RecordingSession

    def handle_device_registration(self, payload):
        """Handle device registration"""
        from .models import Device
        device_id = payload.get('device_id')
        if device_id:
            device, created = Device.objects.get_or_create(device_id=device_id)
            device.last_seen = timezone.now()
            device.save()
            if created:
                logger.success(f"New device registered: {device_id}")
            else:
                logger.info(f"Device updated: {device_id}")

    def connect(self):
        """Initialize and connect to MQTT broker"""
        try:
            self.client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
            # Set callbacks
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            # Configure TLS and authentication
            self.client.tls_set()
            self.client.username_pw_set(
                settings.MQTT_USERNAME,
                settings.MQTT_PASSWORD
            )

            # Connect to broker
            self.client.connect(
                settings.MQTT_HOST,
                settings.MQTT_PORT,
                keepalive=60
            )

            # Start loop in background
            self.client.loop_start()
            logger.info("MQTT client started")

        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")

    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("MQTT client disconnected")

    def publish(self, topic, message):
        """Publish message to MQTT broker"""
        if self.client and self.connected:
            self.client.publish(topic, message)
        else:
            logger.warning("Cannot publish - MQTT client not connected")


# Global MQTT client instance
mqtt_client = MQTTClient()