.PHONY: dev-up dev-down api web worker migrate beat test lint

PYTHONPATH := packages/db;packages/geo-engine;packages/site-auditor;packages/harness;.

dev-up:
	docker compose -f infra/docker-compose.yml up -d

dev-down:
	docker compose -f infra/docker-compose.yml down

migrate:
	cd packages/db && alembic upgrade head

api:
	set PYTHONPATH=$(PYTHONPATH)&& uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000

web:
	cd apps/web && npm run dev

worker:
	set PYTHONPATH=$(PYTHONPATH)&& celery -A apps.worker.celery_app worker --loglevel=info

beat:
	set PYTHONPATH=$(PYTHONPATH)&& celery -A apps.worker.celery_app beat --loglevel=info

test:
	set PYTHONPATH=$(PYTHONPATH)&& pytest tests/ -v --tb=short

lint:
	ruff check apps/ packages/
