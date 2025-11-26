import os
import json
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig

BASE_DIR = Path().resolve().parent

load_dotenv(dotenv_path=str(BASE_DIR  / ".env" ))
MQTT_HOST = os.getenv("MQTT_HOST","localhost")
MQTT_PORT = MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
logger.info("Loaded Environment Variables")
app = FastAPI()

mqtt_config = MQTTConfig(
    host=MQTT_HOST,
    port=MQTT_PORT,
    username=MQTT_USERNAME,
    password=MQTT_PASSWORD,
    keepalive=60,
    ssl=True,  
)

fast_mqtt = FastMQTT(config = mqtt_config)
fast_mqtt.init_app(app)

# Optional: MQTT connected handler
@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    print("Connected to MQTT broker!")
    fast_mqtt.client.subscribe("sensor/data")

# Message handler
@fast_mqtt.on_message()
async def handle_message(client, topic, payload, qos, properties):
    try:
        data = json.loads(payload.decode())
        print(f"Received on {topic}: {data}")
    except Exception as e:
        print(f"Error decoding message: {e}, Raw payload: {payload}")


# Optional: Root endpoint
@app.get("/")
def index():
    return {"message": "FastAPI-MQTT on Jetson is running"}