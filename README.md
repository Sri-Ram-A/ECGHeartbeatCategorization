Here’s a polished and structured version of your README section that’s clearer, easier to follow, and keeps the technical details intact:

---

## Setting up MQTT Communication with FastAPI

This project demonstrates real-time 1-to-2-way communication between Raspberry Pi publishers and a Jetson Nano subscriber using MQTT. Initially, Mosquitto was used for local network communication, later switched to HiveMQ for cross-network connectivity.

---

### **1. Using Mosquitto (Local Network)**

**Install Mosquitto and clients:**

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
```

**Start and enable Mosquitto service:**

```bash
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
sudo systemctl status mosquitto
```

**Install FastAPI and MQTT dependencies:**

```bash
pip install fastapi fastapi-mqtt uvicorn
```

**Run the FastAPI subscriber:**

```bash
uvicorn subscriber:app --host 0.0.0.0 --port 8000
# or
python -m uvicorn subscriber:app --host 0.0.0.0 --port 8000
```

**Verify Mosquitto is listening on the MQTT port (1883):**

```bash
sudo ss -tulnp | grep 1883
```

**Test connectivity from a client (same Wi-Fi network):**

```bash
nc -zv 192.168.43.63 1883
```

**Important Configuration Note:**
To allow Mosquitto to listen on all network interfaces, create a configuration file:

```bash
sudo nano /etc/mosquitto/conf.d/listener.conf
```

Add the following lines:

```
listener 1883
allow_anonymous true
# Do NOT include bind_address unless running multiple listeners
```

> ✅ **Commit reference:** `631ab72` – Basic 1-to-2-way communication code.

---

### **2. Using HiveMQ (Cross-Network)**

To enable communication between devices on different networks, HiveMQ Cloud was used. The subscriber and publisher connect to the HiveMQ broker, enabling MQTT messaging without relying on the same Wi-Fi network.

**.env configuration example:**

```
MQTTS_HOST=your-hivemq-cluster.s1.eu.hivemq.cloud
MQTTS_PORT=8883
MQTT_USERNAME=<your-username>
MQTT_PASSWORD=<your-password>
```

**Publisher and subscriber code** updated to use HiveMQ with TLS (port 8883) for secure cross-network messaging.

> ✅ **Commit reference:** `2de4e49` – Migration to HiveMQ for cross-network connectivity.

---

This structure separates local network setup and HiveMQ cloud setup, includes commands in order, and adds context for why HiveMQ was chosen.

---

