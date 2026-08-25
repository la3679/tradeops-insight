# Testing strategy

Owner: engineering maintainer. Purpose: map behavior to verification.

- domain and unit tests cover invariants, rules, retrieval, graph routing, provider fallback, tools, delivery, settings, and metrics
- PostgreSQL integration tests cover migrations, repositories, idempotent seed/query, checkpoints, and outbox contracts
- API tests cover auth, roles, validation, rate/body/CORS headers, conflicts, polling/WebSocket, and OpenAPI presence
- React tests cover data/client narrowing, components, state primitives, and axe accessibility
- Playwright covers analyst/reviewer, auditor read-only/accessibility, administrator denial, idempotent replay, desktop Chromium, and 768px tablet
- the 50-case suite covers deterministic AI/RAG behavior; k6 records local demo latency only

Run `npm run verify`, then `npm run test:e2e`. Contract/eval checks are the commands in the root README. Coverage excludes generated UI/library files and is used to find missing behavior—not to justify meaningless tests.
