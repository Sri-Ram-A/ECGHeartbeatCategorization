from celery import shared_task
from django.db import transaction
from datetime import datetime
import json
from ecg.client.redis import get_redis
from django.utils import timezone
from datetime import timezone as dt_timezone
from .models import SensorReadings
import redis
r = get_redis()
ECG_STREAM_NAME_PATTERN = "ecg:session:*"

def get_all_ecg_streams(redis_client:redis.Redis):
    # https://www.dragonflydb.io/code-examples/getting-all-keys-matching-pattern-redis-python
    return [stream_name for stream_name in redis_client.scan_iter(ECG_STREAM_NAME_PATTERN)]


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def persist_ecg_stream(self, stream_key:str):
    """stream_key example: ecg:session:12/45"""

    # 1. Read first entry → get session_id
    entries = r.xrange(stream_key, count=1)
    if not entries:
        return  # stream empty return
    first_id, first_data = entries[0]
    session_id = int(first_data["session_id"])

    # 2. Read remaining ECG data
    ecg_entries = r.xrange(stream_key, min=first_id, max="+")
    readings = []
    for entry_id, data in ecg_entries:
        if "session_id" in data:
            continue  # skip first metadata row
        ts_ns = int(data["ts"])
        timestamp = datetime.fromtimestamp(
            ts_ns / 1e9,
            tz=dt_timezone.utc
        )
        values = json.loads(data["values"])
        readings.append(
            SensorReadings(
                session_id=session_id,
                timestamp=timestamp,
                ecg_values=values
            )
        )
    if not readings:
        return

    # 3. Bulk write (atomic)
    with transaction.atomic():
        SensorReadings.objects.bulk_create(
            readings,
            batch_size=200,
            ignore_conflicts=True
        )


@shared_task
def persist_all_ecg_streams():
    streams = get_all_ecg_streams(r)
    for stream in streams:
        persist_ecg_stream.delay(stream)
