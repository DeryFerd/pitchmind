FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml .
COPY packages/ packages/
COPY apps/ apps/

RUN pip install --no-cache-dir \
    fastapi sqlalchemy psycopg2-binary pydantic pydantic-settings httpx \
    celery redis ollama reportlab stripe

ENV PYTHONPATH=/app/packages/db:/app/apps
CMD ["celery", "-A", "apps.worker.celery_app", "worker", "--loglevel=info"]
