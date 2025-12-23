https://docs.djangoproject.com/en/6.0/intro/tutorial01/
https://www.django-rest-framework.org/tutorial/quickstart/
https://pypi.org/project/django-cors-headers/
https://pypi.org/project/drf-spectacular/
```bash
📡 API Endpoints
Authentication
POST /api/register/doctor/ - Register doctor
POST /api/register/patient/ - Register patient
POST /api/login/doctor/ - Doctor login
POST /api/login/patient/ - Patient login
Lists
GET /api/patients/ - Get all patients
GET /api/doctors/ - Get all doctors
Streaming Control
POST /mqtt/start/<doctor_id>/<patient_id>/ - Start ECG streaming
POST /mqtt/stop/<doctor_id>/<patient_id>/ - Stop ECG streaming
Health Check
GET / - Service health check
🎯 MQTT Topics
Subscribed Topics
stream/+/+ - ECG data streams (format: stream/<doctor_id>/<patient_id>)
devices/register - Device registration
Published Topics
commands/<doctor_id>/<patient_id> - Start/stop commands
```
# How paho-mqtt works
- https://www.emqx.com/en/blog/how-to-use-mqtt-in-python