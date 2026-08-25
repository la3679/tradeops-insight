.PHONY: bootstrap format format-check lint typecheck test build verify run-api

bootstrap:
	npm ci
	uv sync --all-packages

format:
	npm run format
	uv run ruff format .

format-check:
	npm run format:check
	uv run ruff format --check .

lint:
	npm run lint
	uv run ruff check .

typecheck:
	npm run typecheck
	uv run mypy apps/api/src apps/api/tests packages/data_connectors/src packages/data_connectors/tests packages/domain/src packages/domain/tests

test:
	uv run pytest --cov=tradeops_api --cov-report=term-missing

build:
	npm run build
	uv build --package tradeops-api

verify: format-check lint typecheck test build

run-api:
	uv run uvicorn tradeops_api.main:app --app-dir apps/api/src --reload
