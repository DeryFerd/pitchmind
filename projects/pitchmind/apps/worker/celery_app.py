import os

from celery import Celery
from celery.schedules import crontab

broker = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6380/0")
backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6380/1")

celery_app = Celery("pitchmind", broker=broker, backend=backend)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    beat_schedule={
        "weekly-geo-digest": {
            "task": "email.send_weekly_digest",
            "schedule": crontab(hour=9, minute=0, day_of_week=1),
        },
    },
)
celery_app.autodiscover_tasks(["apps.worker.tasks"])
