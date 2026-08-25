# Project state

## Current checkpoint

- **Phase:** 2 — domain and data foundation
- **Branch:** `feature/initial-project-release`
- **Canonical repository:** `la3679/tradeops-insight` (private; rename to `tradeops-copilot` is pending)
- **Lovable project:** `d5b87042-8fcf-41cf-aa66-075bf21f45ba`
- **Baseline source commit:** `5bcd2c578498136844041f9d359a64f8d38971ef`
- **Last pushed feature commit:** `dd09ccb6410361db8e886ffa6464a364d77c2a7a`

## Completed

- Resolved connected GitHub and Lovable identities.
- Confirmed no pre-existing TradeOps repository or duplicate Lovable project.
- Created the private Lovable project and connected its GitHub sync.
- Created `feature/initial-project-release` from `main`.
- Added persistent Lovable project knowledge covering clean-room, security, UI, and review boundaries.
- Reviewed the generated frontend foundation and reconstructed the synced tree in the verification workspace.
- Documented the approved product scope and non-goals.
- Added repository, contribution, security, support, licensing, and data-attribution standards.
- Replaced generated metadata and established repeatable frontend quality commands.
- Added the documentation index, release roadmap, and changelog.
- Recorded system, trust-boundary, persistence, identity, retrieval, model, review, telemetry, and data-governance decisions.
- Added the Python 3.12 `uv` workspace and FastAPI service with liveness, readiness, version, and production-schema controls.
- Added async API contract tests with a 90% coverage gate.
- Added stable request correlation and error-envelope contracts.
- Implemented all twelve deterministic exception families behind a framework-free reconciliation facade.
- Added a seeded 3,000-trade/360-exception default dataset and a balanced fast-test profile.
- Added a machine-checked source/provenance registry and bounded offline-tested GLEIF adapter.
- Added the core SQLAlchemy schema, initial Alembic migration, data dictionary, and PostgreSQL offline SQL validation.
- Added loopback-only PostgreSQL/Redis Compose services with persistent volumes and health checks.

## Last verified commands

| Command                           | Result                                  |
| --------------------------------- | --------------------------------------- |
| `prettier --check .`              | Passed                                  |
| `eslint .`                        | Passed                                  |
| `tsc --noEmit`                    | Passed                                  |
| `vite build`                      | Passed                                  |
| `ruff format --check .`           | Passed                                  |
| `ruff check .`                    | Passed                                  |
| `mypy` across Python packages     | Passed                                  |
| `pytest` with branch coverage     | Passed: 92 tests, 95.7% coverage        |
| `uv build --package tradeops-api` | Passed                                  |
| `alembic ... upgrade head --sql`  | Passed; PostgreSQL DDL rendered offline |
| Parse `compose.yaml` with PyYAML  | Passed                                  |

## Known issues

- The GitHub repository and Lovable display name still use `tradeops-insight`; rename is pending.
- The frontend starter has no test runner or coverage gate yet.
- Direct private Git cloning is unavailable in this workspace; connected APIs are used for remote commits.
- Docker is not installed in the current verification runtime; container startup and live migration require CI or another environment.
- The worker, workflow persistence tables, RAG, and provider adapters are not implemented yet.

## Next three actions

1. Add workflow, knowledge, approval, tool-call, and evaluation persistence tables.
2. Add transactional import/repository methods and an idempotent worker/outbox consumer.
3. Add mock-first provider, retrieval, and typed LangGraph orchestration packages.
