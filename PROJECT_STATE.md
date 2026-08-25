# Project State

Last updated: 2026-08-24 (America/Phoenix)

## Resume checkpoint

- Current phase: Phase 2 relational schema and complete deterministic rule catalogue pass locally; repository/API behavior is in progress.
- Branch: `main`
- Last pushed commit before this checkpoint: `84f6180` (`feat(domain): detect settlement-date mismatches`)
- GitHub: `la3679/tradeops-insight`, private, default branch `main`.
- Lovable: `TradeOps Insight` (`d5b87042-8fcf-41cf-aa66-075bf21f45ba`), private and not published.
- Runtime implemented: TanStack Start/React frontend shell with deterministic synthetic overview data, placeholder routes, and component/accessibility tests.
- Runtime implemented: dependency-free FastAPI health contracts, validated process settings, and an inert Celery worker composition root.
- Runtime implemented: immutable synthetic trade facts and the versioned settlement-date mismatch rule with weekend/explicit-holiday handling and review/escalation routes.
- Runtime implemented: Compose-managed PostgreSQL, Redis, Keycloak, OpenTelemetry Collector, API, worker, and web services plus pinned GitHub CI jobs.
- Runtime implemented: first Alembic schema for the full documented relational entity set and a deterministic 2,400-trade generator with 300 exception-bearing records across all twelve required categories.
- Runtime not implemented: repository behavior, authentication, model providers, public-data adapters, and observability integrations.

## Safety boundaries

- The repository is an independent educational portfolio project.
- Trades and operational records must remain deterministic and synthetic.
- Public reference data requires recorded provenance and license review before it is committed.
- The application must not connect to trading venues, brokerage accounts, or institutional systems.
- Backend security, authorization, financial rules, persistence, and model behavior are implemented and reviewed outside Lovable.

## Verification status

| Check                         | Status               | Evidence                                                                           |
| ----------------------------- | -------------------- | ---------------------------------------------------------------------------------- |
| Dependency install            | Passed               | Bun lockfile updated with the frontend test toolchain                              |
| TypeScript                    | Passed               | `npx tsc --noEmit`                                                                 |
| Production build              | Passed               | `npm run build` with Vite 8.1.5                                                    |
| Formatting                    | Passed               | `npm run format:check`                                                             |
| Lint                          | Passed with warnings | `npm run lint`; zero errors and six inherited Fast Refresh export warnings         |
| Frontend unit/component tests | Passed               | `npm run test`; 11 tests across four files                                         |
| Automated accessibility smoke | Passed               | `npm run test:a11y`; axe reported zero violations in the rendered overview fixture |
| Backend/domain tests          | Passed               | 30 tests; strict mypy and Ruff passed; 100% measured branch coverage               |
| Compose configuration         | Passed               | `docker compose config --quiet`                                                    |
| Local stack startup           | Passed               | Seven services started; API, web, Keycloak, and collector probes succeeded         |
| Integration/E2E tests         | Not run              | Database/queue integration and Playwright harness have not been added yet          |
| Dependency audit              | Passed               | `bun audit`; zero known vulnerabilities after in-range transitive fixes            |
| Secret and source scans       | Not run              | Scheduled for the security foundation and release gates                            |
| Clean-clone startup           | Partially passed     | Pinned container builds and full local stack startup passed; fresh clone pending   |

## Environment notes

- Node.js: `v22.19.0`
- npm: `11.6.0`
- Python: `3.14.7` managed by `uv`
- Backend lock/tooling: `uv 0.12.2`; 67 resolved packages in `backend/uv.lock`
- Bun: `1.4.0` in the pinned web container; unavailable directly on this Windows host
- Docker: Engine `29.5.3`; Compose `v5.1.4`
- Graphify CLI: `0.9.41`; project-scoped Codex skill registered under `.codex/skills/graphify`
- Graphify code graph: 899 nodes, 1,381 edges, and 115 generated communities from code-only AST extraction; no model/API credits used

## Next three actions

1. Implement reviewed repository contracts and PostgreSQL integration tests.
2. Add source provenance, document ingestion, retrieval, and adversarial evidence tests.
3. Add typed API contracts and integration tests over the local PostgreSQL/Redis stack.

## Known limitations

- The current UI is a reviewed frontend foundation, not a complete TradeOps workflow.
- Overview values are deterministic synthetic fixtures; they are not measurements or operational claims.
- Placeholder routes intentionally contain no backend, authentication, financial-rule, or model behavior.
- Settlement policy v1 uses only weekends and explicitly supplied holiday dates; it is not a universal market calendar.
