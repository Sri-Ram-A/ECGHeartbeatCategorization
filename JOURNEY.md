# FastAPI-MQTT
-   https://sabuhish.github.io/fastapi-mqtt/getting-started/
-   https://sabuhish.github.io/fastapi-mqtt/example/

![Meaning of some fastapi decorators](image.png)
```python
2025-12-08 12:03:34.071 | INFO | subscriber:connect:39 - Connected: client=<gmqtt.client.Client object at 0x777494e418e0>, flags=0, rc=0, props={'receive_maximum': [10], 'topic_alias_maximum': [5]}
      INFO   Application startup complete.
2025-12-08 12:03:34.458 | INFO | subscriber:on_subscribe_ack:66 - Broker acknowledged subscription (mid=1, qos=(0,))
2025-12-08 12:03:34.458 | INFO | subscriber:on_subscribe_ack:66 - Broker acknowledged subscription (mid=2, qos=(0,))
2025-12-08 12:03:43.067 | INFO | subscriber:handle_all_messages:46 - Received message to ALL topics: sensor/data
2025-12-08 12:03:43.067 | INFO | subscriber:message_to_specific_topic:54 - Received message to SPECIFIC topic: sensor/data
```

# CustomTkinter
- First code generated from GPT
- https://www.geeksforgeeks.org/python/tkinter-application-to-switch-between-different-page-frames/

# Shifting to fast-api
- https://fastapi.tiangolo.com/advanced/templates/#using-jinja2templates

# Shifted to rest api with fast-api instead of jinja
- https://www.geeksforgeeks.org/python/creating-first-rest-api-with-fastapi/
- https://fastapi.tiangolo.com/tutorial/sql-databases/

# Trying TensorRT
- Install using pip : https://github.com/NVIDIA/TensorRT

# Deployment Desicions :
- Setting up ngrok for backend : 
https://dashboard.ngrok.com/get-started/setup/linux
```bash
ngrok http --url=cub-true-shiner.ngrok-free.app http://127.0.0.1:8000/
```
- Hosting frontend to vercel : https://vercel.com/new/sriramaai23-rvceeduins-projects
- Frontend link : https://ecg-heartbeat-categorization.vercel.app
- Today facing problem due to : localStorage is shared across ALL tabs of the same origin.
- For demo purposes I am going to use : sessionStorage
- Finally in end I will use something else through DRF

# Websocket Connection :
- https://channels.readthedocs.io/en/latest/installation.html
- https://channels.readthedocs.io/en/latest/tutorial/part_2.html
- https://github.com/django/channels/issues/1634

# Frontend
- GSAP : https://gsap.com/resources/React/

# TFlite :
- https://developer.android.com/codelabs/digit-classifier-tflite#1


# using redis streams 
- https://medium.com/subex-ai-labs/working-with-redis-streams-in-python-basic-30f97055f61a
- https://hub.docker.com/_/redis
- GUI to view redis : https://hub.docker.com/r/redis/redisinsight
- But for this to work we should make a network for both containers to communicate 
```bash
# Gpt + custom commands
docker network create redis-network
docker run -d \
  --name redis \
  -p 6379:6379 \
  --network redis-network \
  redis

docker run -d \
  --name redisinsight \
  -p 5540:5540 \
  --network redis-network \
  redis/redisinsight:latest
#   To check if both are in same network
docker network inspect redis-network
docker exec -it redisinsight ping redis
```
```java
// output must be like this if its working
If you get:
PING redis (172.xx.x.x): 56 data bytes
Docker DNS is working. RedisInsight can see Redis.
```
Add Redis connection in GUI

In RedisInsight UI:
```bash
Host: redis
Port: 6379
Username: (leave empty unless ACLs enabled)
Password: (leave empty unless auth enabled)
```

```bash
docker exec -it redis redis-cli
```
 check through python cli
 ```bash
 try:
    response = redisCli.ping()
    print("Redis alive:", response)  # True
except redis.exceptions.ConnectionError as e:
    print("Redis down:", e)
 ```
- https://redis.io/docs/latest/develop/data-types/streams/

# Setting up Celery for db logic
- https://medium.com/@codealfi/building-a-real-time-chat-application-with-django-channels-and-redis-25395a9ffa81
- Very iportant for coding : https://testdriven.io/blog/celery-database-transactions/

- https://www.geeksforgeeks.org/python/celery-integration-with-django/
```bash
cd server
celery -A server worker -l info
# -A → Django project
# worker → run executor
# -l info → log level
```
```bash
celery -A server beat -l info
# This process:
# Wakes up every few seconds
# Sends scheduled tasks to Redis
# Workers pick them up
```

# TimeScaleDB docker with Django 
- https://github.com/jamessewell/django-timescaledb
- First shift from sqlite.db to https://medium.com/@jonas.granlund/running-django-with-postgresql-in-docker-a-step-by-step-guide-f6ab3bf05f44
- Run timescaledb image https://www.tigerdata.com/docs/self-hosted/latest/install/installation-docker
```bash
docker run -d \
--name timescaledb \
-p 5432:5432  \
-v /home/srirama/sr_proj/ECGHeartbeatCategorization/docker/pgdata:/pgdata -e PGDATA=/pgdata -e POSTGRES_PASSWORD=password timescale/timescaledb-ha:pg18
```
```bash
docker exec -it timescaledb bash
psql -U postgres
# If you land in a postgres=# prompt, the DB is alive 🫀
```
PURGE stuck tasks from the broker (IMPORTANT)
Your retries are sitting in Redis (or whatever broker you use).
⚠️ This deletes all pending Celery tasks:
celery -A server purge -f
