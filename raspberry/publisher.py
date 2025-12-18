import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from datetime import datetime
from dotenv import load_dotenv
from getmac import get_mac_address
from pathlib import Path
import json
import socket
import os
import time
from loguru import logger

# Load .env configuration
BASE_DIR = Path().resolve().parent
load_dotenv(dotenv_path=str(BASE_DIR / ".env"))
logger.success(f"Loaded env from : {BASE_DIR / ".env"}")
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
KEEP_ALIVE = 60

streaming = False   # flag controlled by MQTT commands
PATIENT_ID = "4"
DOCTOR_ID = "9"

DEVICE = f"{socket.gethostname()}_{get_mac_address()}"
TOPIC = f"stream/{DOCTOR_ID}/{PATIENT_ID}"
COMMAND_TOPIC = f"commands/{DOCTOR_ID}/{PATIENT_ID}"
# MQTT Callback Handlers
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logger.success("Connected to MQTT broker successfully")
        client.subscribe(COMMAND_TOPIC)
        logger.info(f"Subscribed to: {COMMAND_TOPIC}")
    else:
        logger.error(f"Failed to connect. RC={rc}")

def on_message(client, userdata, msg):
    global streaming
    command = msg.payload.decode().strip().lower()
    logger.info(f"Received command: {command}")
    if command == "start":
        streaming = True
        logger.success("Streaming enabled by Jetson")
    elif command == "stop":
        streaming = False
        logger.warning("Streaming disabled by Jetson")

# Replace with actual ECG read
def read_ecg():
    # right now send dummy. Replace with real sensor value
    return {
        "lead1": 0.12,
        "lead2": 0.18,
        "lead3": -0.02
    }

# Configure MQTT Client
client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
client.tls_set() # TLS encryption
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD) # Authentication
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, KEEP_ALIVE)
client.loop_start()
logger.info("Raspberry Pi MQTT client started. Waiting for commands...")

# MAIN STREAM LOOP
try:
    while True:
        if streaming:
            payload = {
                "timestamp": str(datetime.now()),
                "values": read_ecg()
            }
            client.publish(TOPIC, json.dumps(payload))
            logger.info(f"ECG sent → {TOPIC} → {payload}")
        time.sleep(0.25)  # Adjust streaming rate
        
except KeyboardInterrupt:
    logger.warning("Stopping RPi client...")

finally:
    client.loop_stop()
    client.disconnect()
    logger.success("Disconnected from MQTT broker")
