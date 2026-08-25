# Project state

Last updated: 2026-08-24 (America/Phoenix)

## Release checkpoint

- Phase: release hardening and final verification for `v0.1.0`
- Branch: `main`; GitHub/Lovable-connected repository `la3679/tradeops-insight`
- Scope: complete educational synthetic-data implementation described in the master specification
- Runtime: React/TanStack web, FastAPI modular monolith, Celery worker, PostgreSQL, Redis, Keycloak, OpenTelemetry Collector, Prometheus, and Grafana
- Data: 2,400 deterministic synthetic trades, 300 exceptions across twelve categories, 30 synthetic policy documents, and three one-record hash-verified public fixtures
- AI/RAG: deterministic mock provider, optional provider boundaries, FAISS retrieval/citations/adversarial gates, thirteen-node LangGraph with PostgreSQL checkpoint adapter and review interrupts
- Product: overview, queue, investigation, approval, knowledge, evaluation, observability, audit, settings, role selector, loading/error/empty/permission states, and tablet fallback
- Platform: v1 REST/OpenAPI, OIDC/JWKS production validation, RBAC, idempotency, optimistic versions, outbox/delivery policy, polling/WebSocket, metrics/traces/audit

## Verification evidence

| Gate                                 | Result                                                                                                                |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| frontend format/lint/types/build     | passed; zero lint errors (six inherited Fast Refresh warnings)                                                        |
| frontend tests/coverage              | 20 passed; 100% statements/functions/lines and 94.44% branches on selected meaningful surfaces                        |
| backend format/lint/strict types     | passed                                                                                                                |
| backend unit/integration/API tests   | 74 passed; 96.56% total coverage                                                                                      |
| OpenAPI contract and mock evaluation | 19 paths verified; 50/50 golden cases passed                                                                          |
| Playwright E2E/accessibility         | six Chromium desktop/tablet journeys passed; critical axe scans clean                                                 |
| Compose/Terraform                    | Compose config/build/start verified; Terraform 1.15.8 format/init/validate passed                                     |
| performance                          | API, import, five-client WebSocket, RAG, worker policy, and mock workflow baselines recorded under `docs/performance` |
| dependencies                         | Bun production audit and pip-audit report no known vulnerabilities                                                    |
| secrets                              | Gitleaks scanned reachable history; no leaks after exact fixture-only false-positive allowlisting                     |
| container/config                     | fixed Debian util-linux advisories; Terraform unrestricted-egress finding removed; CI scan rerun pending current push |
| docs                                 | local links verified; indexed release handbook and screenshot present                                                 |

## Safety boundaries and limitations

- Independent educational portfolio project; no affiliation, live trades, brokerage/venue connection, advice, or autonomous real-world action.
- All operational records are generated synthetic data. Public references are minimized, attributed, and fixture-only by default.
- The web-facing local demo mutation service resets on API restart. Durable repositories, migrations, PostgreSQL checkpoints, and outbox persistence are independently implemented/tested; wiring all web demo mutations to durable storage remains an explicit roadmap item.
- Settlement calendar policy is a versioned demonstration, not a universal market calendar.
- Terraform is a validated reference configuration, not an applied or production-certified environment.

## Final actions

1. Commit and push release hardening, then require green CI/security runs.
2. Verify a clean clone and full Compose health.
3. Configure GitHub metadata/protections/public visibility, tag/release `v0.1.0`, and verify public links/badges.
