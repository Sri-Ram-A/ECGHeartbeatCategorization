import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import json
import os
import time
from datetime import datetime
from loguru import logger
from dotenv import load_dotenv
from pathlib import Path

# ENV + CONFIG
BASE_DIR = Path(__file__).resolve().parents[1]
print(BASE_DIR)
load_dotenv(BASE_DIR / ".env")

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# MQTT TOPICS
ECG_STREAM_TOPIC = "stream/+/+"
PREDICTION_TOPIC_FMT = "prediction/{doctor_id}/{patient_id}"

# MODEL (LOAD ONCE)
def load_model():
    """Load ML model once at startup."""
    logger.success("Model loaded into memory (Jetson Nano)")
    return "dummy_model"

MODEL = load_model()

# INFERENCE
def run_model(values):
    """Run inference on ECG values."""
    # Example dummy logic
    prediction = "Dead"
    confidence = 0.72
    return prediction, confidence

# MQTT CALLBACKS
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logger.success("Jetson connected to MQTT broker")
        client.subscribe(ECG_STREAM_TOPIC, qos=1)
        logger.info(f"Subscribed to {ECG_STREAM_TOPIC}")
    else:
        logger.error(f"MQTT connection failed | rc={rc}")

def on_disconnect(client, userdata, rc, properties=None):
    logger.warning("Jetson disconnected from MQTT broker")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        topic = msg.topic
        # stream/{doctor}/{patient}
        _, doctor_id, patient_id = topic.split("/")
        values = payload.get("values")
        timestamp = payload.get("timestamp")
        if not values:
            logger.warning("Empty ECG payload received")
            return
        logger.info(f"Recieved values of length  : {len(values)}")
        prediction, confidence = run_model(values)

        out = {
            "prediction": prediction,
            "confidence": confidence,
            "timestamp": timestamp,
            "processed_at": datetime.utcnow().isoformat(),
        }

        pred_topic = PREDICTION_TOPIC_FMT.format(
            doctor_id=doctor_id,
            patient_id=patient_id        )

        client.publish(pred_topic, json.dumps(out), qos=1)
        logger.success(f"PREDICTED | D:{doctor_id} P:{patient_id} → {prediction} ({confidence})")

    except Exception as e:
        logger.exception(f"Error processing ECG stream: {e}")

# MAIN
def main():
    logger.info("Starting Jetson Nano ECG Inference Worker")
    client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id="jetson-nano-worker"
    )
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.tls_set()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warning("Jetson worker shutting down")
    finally:
        client.loop_stop()
        client.disconnect()
        logger.success("Jetson worker disconnected cleanly")

# ENTRY POINT
if __name__ == "__main__":
    main()
