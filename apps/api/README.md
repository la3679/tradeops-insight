# TradeOps API

The API owns transport validation, authentication and authorization boundaries, deterministic application policy, and governed workflow control. It does not execute trades or expose unrestricted tools to a model.

## Run locally

From the repository root:

```bash
uv sync --all-packages
uv run uvicorn tradeops_api.main:app --app-dir apps/api/src --reload
```

Then open:

- `GET http://127.0.0.1:8000/health/live`
- `GET http://127.0.0.1:8000/health/ready`
- `GET http://127.0.0.1:8000/api/v1/meta/version`
- `http://127.0.0.1:8000/docs`

`/health/live` is process-local. `/health/ready` will acquire required-dependency checks as persistence and delivery adapters are introduced.

## Test

```bash
uv run pytest apps/api/tests --cov=tradeops_api --cov-report=term-missing
```
