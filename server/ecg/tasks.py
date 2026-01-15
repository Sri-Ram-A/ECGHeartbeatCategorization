from celery import shared_task
from django.db import transaction,IntegrityError
from datetime import datetime
import json
from ecg.client.redis import get_redis
from django.utils import timezone
from datetime import timezone as dt_timezone
from .models import SensorReadings,RecordingSession
import redis
import logging
logger = logging.getLogger(__name__)
r = get_redis()
ECG_STREAM_NAME_PATTERN = "ecg:session:*"

def get_all_ecg_streams(redis_client:redis.Redis):
    # https://www.dragonflydb.io/code-examples/getting-all-keys-matching-pattern-redis-python
    return [stream_name for stream_name in redis_client.scan_iter(ECG_STREAM_NAME_PATTERN)]


@shared_task(
    bind=True,
    autoretry_for=(redis.RedisError, ConnectionError, TimeoutError),
    retry_backoff=5,
    retry_kwargs={"max_retries": 5},
)
def persist_ecg_stream(self, stream_key: str):

    entries = r.xrange(stream_key, count=1)
    if not entries:
        logger.warning(f"Empty stream: {stream_key}")
        return

    _, first_data = entries[0]

    try:
        session_id = int(first_data["session_id"])
    except (KeyError, ValueError):
        logger.error(f"Invalid session metadata in {stream_key}")
        return

    # 🚨 HARD CHECK — NO CREATION
    try:
        session = RecordingSession.objects.get(id=session_id)
    except RecordingSession.DoesNotExist:
        logger.warning(
            f"Session {session_id} does not exist. "
            f"Skipping ECG stream {stream_key}"
        )
        return  # ← THIS is the critical change

    ecg_entries = r.xrange(stream_key, min="-", max="+")
    readings = []

    for entry_id, data in ecg_entries:
        if "session_id" in data:
            continue

        try:
            ts_ns = int(data["ts"])
            timestamp = datetime.fromtimestamp(ts_ns / 1e9, tz=dt_timezone.utc)
            values = json.loads(data["values"])
        except Exception as e:
            logger.warning(f"Malformed ECG entry {entry_id}: {e}")
            continue

        readings.append(
            SensorReadings(
                session=session,
                timestamp=timestamp,
                ecg_values=values,
            )
        )

    if not readings:
        logger.info(f"No ECG readings for {stream_key}")
        return

    try:
        with transaction.atomic():
            SensorReadings.objects.bulk_create(
                readings,
                batch_size=500,
                ignore_conflicts=True,
            )
    except IntegrityError as e:
        logger.error(f"DB integrity error for {stream_key}: {e}")
        return

    logger.info(
        f"Persisted {len(readings)} ECG rows for session {session_id}"
    )


@shared_task
def persist_all_ecg_streams():
    streams = get_all_ecg_streams(r)
    for stream in streams:
        persist_ecg_stream.delay(stream)
