import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from datetime import datetime
import json
import socket
import os
from pathlib import Path
from dotenv import load_dotenv
from getmac import get_mac_address 
import time
import random

BASE_DIR = Path().resolve().parent
load_dotenv(dotenv_path=str(BASE_DIR  / ".env"))

MQTT_HOST = os.getenv("MQTT_HOST","localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = "sensor/data"
KEEP_ALIVE = 60

client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
client.tls_set()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_HOST, MQTT_PORT, KEEP_ALIVE)

client.loop_start()  # start background loop


while True:
    data = {
        "sender": str(socket.gethostname()) + str(get_mac_address()),
        "temperature": random.randint(28, 40),
        "timestamp": str(datetime.now())
    }

    result = client.publish(MQTT_TOPIC, json.dumps(data))
    result.wait_for_publish()
    print("Published:", data)

    time.sleep(1)  # 1-second interval
    
client.loop_stop()
client.disconnect()
