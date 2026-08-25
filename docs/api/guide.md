# API guide

Owner: API maintainer. Purpose: describe the versioned contract and safe usage.

Base URL is `http://127.0.0.1:8000/api/v1`; interactive OpenAPI is `/docs`. Reads accept `X-Demo-Role` locally. Production ignores this shortcut and requires an OIDC bearer token. Mutations require allowed roles and an `Idempotency-Key` of 8–160 characters. Approvals also require `expected_exception_version`.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/exceptions -Headers @{"X-Demo-Role"="analyst"}
Invoke-RestMethod http://127.0.0.1:8000/api/v1/evaluations/runs -Method Post -Headers @{"X-Demo-Role"="administrator";"Idempotency-Key"="demo-eval-0001"}
```

Core resources: session, dashboard, trades, synthetic import, exceptions, workflows/approvals, knowledge, sources/sync, evaluations, audit, events, health, version, and metrics. WebSocket `/api/v1/events/ws?role=analyst` sends a bounded safe snapshot in local mode; `/events` is the polling fallback. Errors use stable problem JSON with a request ID. The centralized TypeScript client in `src/lib/tradeops-api.ts` narrows unknown payloads; components do not scatter fetch calls.
