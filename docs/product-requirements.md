# Product requirements

Owner: project maintainer. Purpose: define the implemented educational product.

TradeOps Copilot helps analysts investigate synthetic fixed-income exceptions, reviewers control proposed resolution, and auditors inspect evidence and history. Success means deterministic replay, evidence-linked explanations, explicit human approval, enforced role boundaries, and a locally reproducible demo—not autonomous trading or production readiness.

The primary journey is queue → investigation → workflow → review → safe demo mutation → audit. The catalogue covers counterparty, instrument, notional, price, currency, settlement date, duplicate, confirmation, stale reference, unsupported product, missing SSI, and allocation exceptions. Accessibility, degraded states, idempotency, optimistic concurrency, provenance, and observability are first-class requirements.

Non-goals: real orders/trades, brokerage connectivity, financial advice, proprietary data or policy, fully autonomous actions, universal calendars, or invented effectiveness claims.
