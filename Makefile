.PHONY: bootstrap dev seed data-sync format lint typecheck test test-integration test-e2e eval security docs-check build verify

bootstrap:
	npx bun@1.4.0 install --frozen-lockfile
	uv sync --directory backend --all-groups --locked

dev:
	docker compose up --build

seed:
	docker compose up -d postgres redis api
	docker compose exec api uv run --locked --no-dev alembic upgrade head

data-sync:
	uv run --directory backend --locked pytest --no-cov tests/adapters/test_provenance.py

format:
	npx prettier --write .
	uv run --directory backend --locked ruff format .

lint:
	npm run lint
	uv run --directory backend --locked ruff check .

typecheck:
	npm run typecheck
	uv run --directory backend --locked mypy src tests

test:
	npm run test:coverage
	uv run --directory backend --locked pytest

test-integration:
	uv run --directory backend --locked pytest --no-cov tests/adapters tests/worker

test-e2e:
	npm run test:e2e

eval:
	uv run --directory backend --locked python ../scripts/run_eval.py

security:
	npx bun@1.4.0 audit --production
	uv export --directory backend --locked --no-dev --no-emit-project --format requirements-txt --output-file requirements-audit.txt
	uvx pip-audit -r backend/requirements-audit.txt

docs-check:
	uv run --directory backend --locked python ../scripts/check_docs.py
	docker run --rm -v "$(CURDIR)/infra/terraform/aws:/workspace" -w /workspace hashicorp/terraform:1.15.8 fmt -check -recursive

build:
	npm run build
	docker compose build api worker web

verify:
	npm run verify
	uv run --directory backend --locked python ../scripts/validate_openapi.py
	uv run --directory backend --locked python ../scripts/run_eval.py
	uv run --directory backend --locked python ../scripts/check_docs.py
	docker compose config --quiet
