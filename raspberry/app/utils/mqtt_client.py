import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from datetime import datetime
import json
import socket
import os
import time
import random
from pathlib import Path
from dotenv import load_dotenv
from getmac import get_mac_address

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=str(BASE_DIR / ".env"))

class MQTTPublisher:
    def __init__(self, callback=None):
        self.callback = callback
        self.running = False
        
        self.host = os.getenv("MQTT_HOST", "localhost")
        self.port = int(os.getenv("MQTT_PORT", 8883))
        self.username = os.getenv("MQTT_USERNAME")
        self.password = os.getenv("MQTT_PASSWORD")
        self.topic = "sensor/data"
        
        self.client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
        
        # Only set TLS if using secure port
        if self.port == 8883:
            try:
                self.client.tls_set()
            except:
                pass  # Skip TLS if not configured
        
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
    
    def start(self):
        try:
            self.client.connect(self.host, self.port, 60)
            self.client.loop_start()
            self.running = True
            
            while self.running:
                temp = round(random.uniform(36.0, 38.5), 1)
                
                data = {
                    "sender": f"{socket.gethostname()}-{get_mac_address()}",
                    "temperature": temp,
                    "timestamp": str(datetime.now())
                }
                
                result = self.client.publish(self.topic, json.dumps(data))
                
                if self.callback:
                    self.callback(temp)
                
                time.sleep(2)  # Publish every 2 seconds
                
        except Exception as e:
            print(f"MQTT Error: {e}")
    
    def stop(self):
        self.running = False
        self.client.loop_stop()
        self.client.disconnect()