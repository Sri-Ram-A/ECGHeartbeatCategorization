# ecg/redis_client.py
import redis
from django.conf import settings

def get_redis():
    return redis.Redis(host="localhost",port=6379,decode_responses=True,socket_connect_timeout=1,socket_timeout=1,)
