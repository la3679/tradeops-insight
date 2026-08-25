# Operations runbook

Owner: operations maintainer. Purpose: operate and diagnose the local demo.

Start `docker compose up --build -d`; inspect `docker compose ps`; probe `/api/v1/health/live`, `/ready`, `/metrics`, web port 3000, Keycloak 8080, Prometheus 9090, and Grafana 3001. Use request/workflow IDs to correlate API, worker, audit, traces, and events.

For elevated 5xx/latency: preserve logs and metrics, check database/Redis/identity/collector health, stop new mutations, and restart only the affected stateless service. For queue lag: check Redis and worker, retain outbox rows, then resume delivery; duplicate consumers are safe by event ID. For provider/retrieval failure: keep mock/fallback or escalate—never bypass citations or approval. For WebSocket failure: clients use polling.

Demo state is recoverable by API restart; PostgreSQL volumes persist until explicitly removed. Never run `docker compose down -v` during an investigation unless loss is intended and confirmed.
