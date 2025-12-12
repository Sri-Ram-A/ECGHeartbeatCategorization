import os
import json
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mqtt import FastMQTT, MQTTConfig
from routes import router as http_router
from models import create_db_and_tables

# Configuration & Setup
BASE_DIR = Path(__file__).parent
load_dotenv(dotenv_path=str(BASE_DIR / ".env"))
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
PATIENT_ID = "P-123"
logger.info("Loaded Environment Variables")

# MQTT Configuration
mqtt_config = MQTTConfig(
    host=MQTT_HOST,
    port=MQTT_PORT,
    username=MQTT_USERNAME,
    password=MQTT_PASSWORD,
    keepalive=60,
    ssl=True,  # TLS encryption for port 8883
)

fast_mqtt = FastMQTT(config=mqtt_config)

# FastAPI App Setup
app = FastAPI(title="ECG Backend with MQTT")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MQTT
fast_mqtt.init_app(app)

# Include HTTP Routes
app.include_router(http_router)

# Database Initialization
@app.on_event("startup")
def startup():
    create_db_and_tables()
    logger.success("Database initialized")

# MQTT Event Handlers
@fast_mqtt.on_connect()
def on_connect(client, flags, rc, properties):
    """Subscribe to ECG stream topic when connected"""
    ecg_topic = f"ecg/{PATIENT_ID}/stream"
    fast_mqtt.client.subscribe(ecg_topic)
    logger.success(f"Connected to MQTT broker | Subscribed to: {ecg_topic}")

@fast_mqtt.on_disconnect()
def on_disconnect(client, packet, exc=None):
    logger.warning("Disconnected from MQTT broker")

@fast_mqtt.on_subscribe()
def on_subscribe_ack(client, mid, qos, properties):
    logger.info(f"Subscription acknowledged (mid={mid}, qos={qos})")

# ECG Data Handler
@fast_mqtt.subscribe(f"ecg/{PATIENT_ID}/stream")
async def handle_ecg_stream(client, topic, payload, qos, properties):
    """Process incoming ECG data from Raspberry Pi"""
    try:
        data = json.loads(payload.decode())
        logger.info(f"📊 ECG Data received from {data.get('sender', 'unknown')}")
        logger.debug(f"Timestamp: {data.get('timestamp')}")
        logger.debug(f"Values: {data.get('values')}")
        
        # TODO: Add your processing logic here:
        # - Store in database
        # - Run ML inference
        # - Detect anomalies
        # - Broadcast to frontend via WebSocket
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode ECG payload: {e}")
    except Exception as e:
        logger.error(f"Error processing ECG data: {e}")

# HTTP Endpoints for MQTT Control
@app.post("/mqtt/start-streaming")
async def start_streaming():
    """Send START command to Raspberry Pi"""
    topic = f"commands/{PATIENT_ID}"
    fast_mqtt.publish(topic, "start")
    logger.info(f"Sent START command to {topic}")
    return {"status": "success", "message": "Streaming started"}


@app.post("/mqtt/stop-streaming")
async def stop_streaming():
    """Send STOP command to Raspberry Pi"""
    topic = f"commands/{PATIENT_ID}"
    fast_mqtt.publish(topic, "stop")
    logger.warning(f"Sent STOP command to {topic}")
    return {"status": "success", "message": "Streaming stopped"}


@app.get("/mqtt/status")
async def mqtt_status():
    """Check MQTT connection status"""
    is_connected = fast_mqtt.client.is_connected if hasattr(fast_mqtt.client, 'is_connected') else False
    return {
        "mqtt_connected": is_connected,
        "broker": MQTT_HOST,
        "port": MQTT_PORT,
        "patient_id": PATIENT_ID
    }

@app.get("/")
async def root():
    return {
        "service": "ECG Backend",
        "mqtt_enabled": True,
        "patient_id": PATIENT_ID
    }

# Run Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 