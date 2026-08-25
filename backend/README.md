# TradeOps backend foundation

This package is the reviewed backend boundary for the TradeOps Copilot portfolio project. It currently provides composition roots, configuration, liveness and readiness contracts, and an inert Celery worker configuration. It does not connect to a database, Redis, a model provider, or any trading system.

All examples and future fixtures must remain deterministic and clearly synthetic.

## Local commands

```powershell
npm run backend:sync
npm run verify:backend
npm run verify
```

Run the API with `uv run --project backend --locked tradeops-api`. It listens on `127.0.0.1:8000` and exposes `/api/v1/health/live` and `/api/v1/health/ready`. Starting the worker requires an explicitly provisioned Redis broker and is outside the default verification path.
