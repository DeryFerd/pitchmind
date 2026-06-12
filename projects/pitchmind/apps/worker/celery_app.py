import os

from celery import Celery

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
)
celery_app.autodiscover_tasks(["apps.worker.tasks"])
