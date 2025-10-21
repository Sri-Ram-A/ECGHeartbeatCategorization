import paho.mqtt.client as mqtt
import time
import json
import socket


MQTT_BROKER = "192.168.43.63"

MQTT_PORT = 1883
MQTT_TOPIC = "sensor/data"

client = mqtt.Client()
client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    60
)
data = {
    "sender":socket.gethostname(),
    "temperature":30,
    "timestamp":time.time()
}
client.publish(
    MQTT_TOPIC,
    json.dumps(data)
)
print("Published data")