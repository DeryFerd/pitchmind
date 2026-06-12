.PHONY: dev-up dev-down api web worker migrate

dev-up:
	docker compose -f infra/docker-compose.yml up -d

dev-down:
	docker compose -f infra/docker-compose.yml down

migrate:
	cd packages/db && alembic upgrade head

api:
	set PYTHONPATH=packages/db;apps&& uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000

web:
	cd apps/web && npm run dev

worker:
	set PYTHONPATH=packages/db;apps&& celery -A apps.worker.celery_app worker --loglevel=info
