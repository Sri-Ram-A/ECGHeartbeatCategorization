import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import json
from loguru import logger
from django.conf import settings
from django.utils import timezone

class MQTTClient:
    def __init__(self):
        self.client = None
        self.connected = False

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            logger.info("Connected to MQTT broker")
            self.connected = True
            # Subscribe to all stream topics
            client.subscribe("stream/+/+")
            client.subscribe("devices/register")
            logger.info("Subscribed to stream and device topics")
        else:
            logger.error(f"Failed to connect to MQTT broker. RC={rc}")

    def on_disconnect(self, client, packet, exc=None):
        logger.warning("Disconnected from MQTT broker")
        self.connected = False

    def on_message(self, client, userdata, msg):
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())

            if topic.startswith("stream/"):
                self.handle_ecg_stream(topic, payload)
            elif topic == "devices/register":
                self.handle_device_registration(payload)

        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}")

    def handle_ecg_stream(self, topic, payload):
        """Process incoming ECG data"""
        parts = topic.split("/")
        if len(parts) == 3:
            _, doctor_id, patient_id = parts
            timestamp = payload.get('timestamp')
            values = payload.get('values')
            device_id = payload.get('device_id')
            
            logger.info(f"ECG Stream - Doctor:{doctor_id} Patient:{patient_id} Device:{device_id}")
            
            # TODO: Add your processing logic:
            # - Store in database
            # - Run ML inference
            # - Detect anomalies
            # - Broadcast to frontend via WebSocket/Channels

    def handle_device_registration(self, payload):
        """Handle device registration"""
        from .models import Device
        
        device_id = payload.get('device_id')
        if device_id:
            device, created = Device.objects.get_or_create(device_id=device_id)
            device.last_seen = timezone.now()
            device.save()
            
            if created:
                logger.info(f"New device registered: {device_id}")
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