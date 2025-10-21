from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
import json

app = FastAPI()
MQTT_BROKER = "localhost"

# MQTT_BROKER = "172.16.34.32"
MQTT_PORT = 1883

# Set MQTT broker address (point to Raspberry Pi IP if broker is there)
mqtt_config = MQTTConfig(
    host= MQTT_BROKER, 
    port= MQTT_PORT,
    keepalive=60
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