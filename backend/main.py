import os
import json
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mqtt import FastMQTT, MQTTConfig
from routes import router as http_router,SessionDep
from models import RecordingSession
from fastapi import HTTPException, Depends
from sqlmodel import Session, select
from typing import Annotated
import models
SessionDep = Annotated[Session, Depends(models.get_session)]
# Configuration & Setup
BASE_DIR = Path(__file__).parent
load_dotenv(dotenv_path=str(BASE_DIR / ".env"))
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
logger.info("Loaded Environment Variables")

# MQTT Configuration
mqtt_config = MQTTConfig(host=MQTT_HOST, port=MQTT_PORT, username=MQTT_USERNAME, password=MQTT_PASSWORD, keepalive=60, ssl=True)
fast_mqtt = FastMQTT(config=mqtt_config)
# FastAPI App Setup
app = FastAPI(title="ECG Backend with MQTT")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://ecg-heartbeat-categorization.vercel.app"],
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
    models.create_db_and_tables()
    logger.success("Database initialized")

# MQTT Event Handlers
@fast_mqtt.on_connect()
def on_connect(client, flags, rc, properties):
    # Confirms the TCP + MQTT handshake
    logger.success(f"Connected to MQTT broker")

@fast_mqtt.on_disconnect()
def on_disconnect(client, packet, exc=None):
    logger.warning("Disconnected from MQTT broker")

@fast_mqtt.on_subscribe()
def on_subscribe_ack(client, mid, qos, properties):
    # Fires when the broker confirms a subscription
    logger.info(f"Subscription acknowledged (mid={mid}, qos={qos})")

# ECG Data Handler
@fast_mqtt.subscribe("stream/+/+")
async def handle_ecg_stream(client, topic, payload, qos, properties):
    """Process incoming ECG data from Raspberry Pi"""
    try:
        # Split topic to get the wildcard parts
        parts = topic.split("/") 
        stream_name,device,patient_id = parts
        # Parse payload
        data = json.loads(payload.decode())
        timestamp = data.get('timestamp')
        values = data.get('values')
        logger.info(f"{timestamp:>20} | {device:>10} | Values: {str(values):>30}")
    except Exception as e:
        logger.error(f"Error processing ECG stream: {e}")

        # TODO: Add your processing logic here:
        # - Store in database
        # - Run ML inference
        # - Detect anomalies
        # - Broadcast to frontend via WebSocket

# HTTP Endpoints for MQTT Control
@app.post("/mqtt/start/{doctor_id}/{patient_id}")
async def start_streaming(doctor_id: int,patient_id: int,session: SessionDep):
    topic = f"commands/{doctor_id}/{patient_id}"

    # --- 2. Prevent duplicate active sessions ---
    active_stmt = select(RecordingSession).where(
       RecordingSession.doctor_id == doctor_id,
       RecordingSession.patient_id == patient_id,
       RecordingSession.stopped_at.is_(None)
    )
    active = session.exec(active_stmt).first()
    if active:
        raise HTTPException(400, "Recording session already running")

    # --- 3. Create recording session ---
    recording = RecordingSession(doctor_id=doctor_id,patient_id=patient_id,verdict="pending")
    session.add(recording)
    session.commit()
    session.refresh(recording)

    # --- 4. Send MQTT START ---
    fast_mqtt.publish(topic, "start")
    logger.info(f"Sent START command to {topic}")

    return {
        "status": "success",
        "session_id": recording.id,
        "message": "Streaming started"
    }

@app.post("/mqtt/stop/{doctor_id}/{patient_id}")
async def stop_streaming(doctor_id: int,patient_id: int,session: SessionDep):
    stmt = select(RecordingSession).where(
       RecordingSession.doctor_id == doctor_id,
       RecordingSession.patient_id == patient_id,
       RecordingSession.stopped_at.is_(None)
    ).order_by(RecordingSession.started_at.desc())
    recording = session.exec(stmt).first()
    if not recording:
        raise HTTPException(404, "No active recording session found")
    recording.stopped_at = datetime.now()
    session.add(recording)
    session.commit()

    topic = f"commands/{doctor_id}/{patient_id}"
    fast_mqtt.publish(topic, "stop")
    logger.warning(f"Sent STOP command to {topic}")
    return {
        "status": "success",
        "session_id": recording.id,
        "message": "Streaming stopped"
    }


@app.get("/")
async def root():
    return {
        "service": "ECG Backend",
        "mqtt_enabled": True,
    }

# Run Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 