# Update and install Mosquitto
sudo apt update
sudo apt install mosquitto mosquitto-clients

# Start Mosquitto service
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# Make sure the Mosquitto broker is running by checking its status:
sudo systemctl status mosquitto
pip install fastapi fastapi-mqtt uvicorn
uvicorn <python_file_name>:app --host 0.0.0.0 --port 8000
> uvicorn subscriber:app --host 0.0.0.0 --port 8000
> python -m uvicorn subscriber:app --host 0.0.0.0 --port 8000
sudo ss -tulnp | grep 1883

## in client
nc -zv 192.168.43.63 1883