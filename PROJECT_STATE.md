# Project state

## Current checkpoint

- **Phase:** 1 — architecture and service skeleton
- **Branch:** `feature/initial-project-release`
- **Canonical repository:** `la3679/tradeops-insight` (private; rename to `tradeops-copilot` is pending)
- **Lovable project:** `d5b87042-8fcf-41cf-aa66-075bf21f45ba`
- **Baseline source commit:** `5bcd2c578498136844041f9d359a64f8d38971ef`
- **Last pushed feature commit:** `957d92207413b211046baf1e158ca27eb0517d5e`

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

## Last verified commands

| Command                            | Result                         |
| ---------------------------------- | ------------------------------ |
| `prettier --check .`               | Passed                         |
| `eslint .`                         | Passed                         |
| `tsc --noEmit`                     | Passed                         |
| `vite build`                       | Passed                         |
| `ruff format --check .`            | Passed                         |
| `ruff check .`                     | Passed                         |
| `mypy apps/api/src apps/api/tests` | Passed                         |
| `pytest --cov=tradeops_api`        | Passed: 4 tests, 100% coverage |
| `uv build --package tradeops-api`  | Passed                         |

## Known issues

- The GitHub repository and Lovable display name still use `tradeops-insight`; rename is pending.
- The frontend starter has no test runner or coverage gate yet.
- Direct private Git cloning is unavailable in this workspace; connected APIs are used for remote commits.
- Docker is not installed in the current verification runtime; Compose validation requires CI or another environment.

## Next three actions

1. Add request correlation, stable errors, and boundary tests.
2. Add the deterministic synthetic exception-domain model and first reconciliation rules.
3. Add persistence models, an initial migration, and local PostgreSQL/Redis infrastructure.
