FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml .
COPY packages/ packages/
COPY apps/api/ apps/api/

RUN pip install --no-cache-dir \
    fastapi uvicorn sqlalchemy psycopg2-binary pydantic pydantic-settings \
    python-jose httpx reportlab stripe

ENV PYTHONPATH=/app/packages/db:/app/apps
EXPOSE 8000
CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
