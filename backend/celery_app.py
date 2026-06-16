from celery import Celery
import os
from dotenv import load_dotenv
import ssl
load_dotenv()

celery = Celery(
    'apiops',
    broker=os.getenv('REDIS_URL'),
    backend=os.getenv('REDIS_URL'),
    include=['tasks']
)

celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    broker_use_ssl={
        "ssl_cert_reqs": ssl.CERT_NONE
    },
    redis_backend_use_ssl={
        "ssl_cert_reqs": ssl.CERT_NONE
    },
)

celery.conf.beat_schedule = {
    "auto-analyse-logs": {
        "task": "analyse_logs",
        "schedule": 300.0,  # every 5 minutes
    },
    "auto-detect-cpu-anomalies": {
        "task": "detect_metric_anomalies",
        "args": ["cpu_usage"],
        "schedule": 300.0,
    },
    "auto-detect-memory-anomalies": {
        "task": "detect_metric_anomalies",
        "args": ["memory_usage"],
        "schedule": 300.0,
    },
    "auto-detect-response-anomalies": {
        "task": "detect_metric_anomalies",
        "args": ["response_time"],
        "schedule": 300.0,
    },
}