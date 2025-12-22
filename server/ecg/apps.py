from django.apps import AppConfig

class EcgConfig(AppConfig):
    name = 'ecg'
    ### Added by me below all lines
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        """Initialize MQTT client when Django starts"""
        from .mqtt_client import mqtt_client
        mqtt_client.connect()