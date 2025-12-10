import os
import json
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig

# --- Configuration & Setup ---
BASE_DIR = Path().resolve().parent
load_dotenv(dotenv_path=str(BASE_DIR / ".env"))
# Using 1883 (standard) typically means no SSL, 8883 is often used for SSL/TLS
# Use 8883 and ssl=True if you need secure connection.

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = "sensor/data"
logger.info("Loaded Environment Variables")
mqtt_config = MQTTConfig(
    host=MQTT_HOST,
    port=MQTT_PORT,
    username=MQTT_USERNAME,
    password=MQTT_PASSWORD,
    keepalive=60,
    ssl=True, 
)
fast_mqtt = FastMQTT(config=mqtt_config)
app = FastAPI()
fast_mqtt.init_app(app) 

## 🔗 on_connect: Establishes subscriptions upon connecting to the broker.
@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    fast_mqtt.client.subscribe(MQTT_TOPIC) 
    logger.info(f"Connected: client={client}, flags={flags}, rc={rc}, props={properties}")


## 📩 on_message: Catches all messages that arrive for *any* subscribed topic.
@fast_mqtt.on_message()
async def handle_all_messages(client, topic, payload, qos, properties):
    logger.info("Received message to ALL topics: {}", topic, payload.decode(), qos, properties)


## 📢 subscribe: A convenience decorator to subscribe to a specific topic/pattern and handle only messages for that topic.
@fast_mqtt.subscribe(MQTT_TOPIC)
async def message_to_specific_topic(client, topic, payload, qos, properties):
    data = json.loads(payload.decode())
    logger.info(f"Received message to SPECIFIC topic: {topic} | {data}")


## 🛑 on_disconnect: Runs when the client disconnects.
@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    logger.info("Disconnected")


## ✅ on_subscribe: Runs when a subscription request is ACKNOWLEDGED by the broker.
@fast_mqtt.on_subscribe()
def on_subscribe_ack(client, mid, qos, properties):
    logger.info("Broker acknowledged subscription (mid={}, qos={})", mid, qos)

# --- FastAPI Endpoint ---
@app.get("/")
async def func():
    return {"result": True, "message": "Published"}
