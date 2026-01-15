from django.apps import AppConfig

class EcgConfig(AppConfig):
    name = 'ecg'
    ### Added by me below all lines
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        try:
            from ecg.client.redis import get_redis
            from ecg.client.mqtt import mqtt_client
            from loguru import logger
            r = get_redis()
            r.ping()
            logger.info("Redis Available")
        except Exception as e:
            logger.critical(f"Redis check failed: {e}")
            raise
        """Initialize MQTT client when Django starts"""
        mqtt_client.connect()