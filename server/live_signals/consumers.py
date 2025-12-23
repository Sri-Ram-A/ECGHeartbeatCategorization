# app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ECGConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.doctor_id = self.scope["url_route"]["kwargs"]["doctor_id"] # type: ignore
        self.patient_id = self.scope["url_route"]["kwargs"]["patient_id"] # type: ignore
        self.group_name = f"live_signals_{self.doctor_id}_{self.patient_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # No need to allow incoming messages from client in this flow,hence not implemented
    async def receive(self, text_data=None, bytes_data=None):
        # Optionally handle client pings or control messages
        pass

    # Handler called when channel_layer.group_send sends with type "ecg.message"
    async def ecg_message(self, event):
        # event["data"] is expected to be JSON-serializable payload
        await self.send(text_data=json.dumps(event["data"]))
