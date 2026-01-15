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
import numpy as np

# Configuration
BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

# Connect to Broker
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# Global vars
DATASET_PATH = BASE_DIR / "mitbih_test.csv"
DOCTOR_ID = "1"
PATIENT_ID = "1"
DEVICE_ID = f"{socket.gethostname()}_{get_mac_address()}"

DEVICE_REGISTER_TOPIC = "devices/register"
STREAM_TOPIC = f"stream/{DOCTOR_ID}/{PATIENT_ID}"
COMMANDS_TOPIC = f"commands/{DOCTOR_ID}/{PATIENT_ID}"

# Global state
streaming = False

def load_ecg_data():
    """Load ECG dataset from CSV"""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")
    data = np.genfromtxt(str(DATASET_PATH),delimiter=',',skip_header=1,max_rows=100)
    data = data[:, :-1]  # Remove last column (label)
    logger.info(f"Loaded {data.shape[0]} ECG signals with {data.shape[1]} values each")
    return data

def on_connect(client, userdata, flags, rc,properties=None):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        logger.success("Connected to MQTT broker")
        client.subscribe(COMMANDS_TOPIC)
        logger.info(f"Subscribed to {COMMANDS_TOPIC}")
    else:
        logger.error(f"Connection failed. Error code: {rc}")

def on_message(client, userdata, msg):
    """Callback when receiving MQTT messages"""
    global streaming
    command = msg.payload.decode().strip().lower()
    if command == "start":
        streaming = True
        logger.success("▶ Streaming STARTED")
    elif command == "stop":
        streaming = False
        logger.warning("⏸ Streaming STOPPED")
    else:
        logger.warning(f"Unknown command: {command}")

def register_device(client):
    """Register this device with the broker"""
    payload = {"device_id": DEVICE_ID}
    client.publish(DEVICE_REGISTER_TOPIC, json.dumps(payload))
    logger.info(f"Device registered: {DEVICE_ID}")

def publish_ecg_data(client, ecg_values):
    """Publish ECG data to MQTT topic"""
    payload = {
        "timestamp": datetime.now().isoformat(),
        "values": ecg_values,
    }
    client.publish(STREAM_TOPIC, json.dumps(payload))
    logger.debug(f"Published {len(ecg_values)} values to {STREAM_TOPIC}")

def main():
    """Main streaming loop"""
    global streaming
    
    # Load data
    ecg_data = load_ecg_data()
    len_ecg_data = len(ecg_data)
    # Setup MQTT client
    client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
    client.tls_set()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Connect and start
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()
    logger.info("MQTT client started. Waiting for START command...")
    
    # Register device
    register_device(client)
    
    # Streaming loop
    try:
        row_index = 0
        while True:
            if streaming:
                if row_index >= len_ecg_data:
                    logger.warning("Dataset exhausted. Restarting from beginning...")
                    row_index = 0
                
                ecg_values = ecg_data[row_index].tolist()
                publish_ecg_data(client, ecg_values)
                row_index += 1
                time.sleep(0.25)  # 4 Hz streaming rate
            else:
                time.sleep(0.5)  # Check for commands every 0.5s
                
    except KeyboardInterrupt:
        logger.warning("Stopping client...")
    finally:
        streaming = False
        client.loop_stop()
        client.disconnect()
        logger.success("Disconnected from MQTT broker")


if __name__ == "__main__":
    main()