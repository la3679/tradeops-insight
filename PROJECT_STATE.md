# Project State

Last updated: 2026-08-24 (America/Phoenix)

## Resume checkpoint

- Current phase: Phase 1 developer platform remains open; the first Phase 2 domain slice is now implemented.
- Branch: `main`
- Last pushed commit before this checkpoint: `ecec401` (`Scaffold Phase 1 backend foundation`)
- GitHub: `la3679/tradeops-insight`, private, default branch `main`.
- Lovable: `TradeOps Insight` (`d5b87042-8fcf-41cf-aa66-075bf21f45ba`), private and not published.
- Runtime implemented: TanStack Start/React frontend shell with deterministic synthetic overview data, placeholder routes, and component/accessibility tests.
- Runtime implemented: dependency-free FastAPI health contracts, validated process settings, and an inert Celery worker composition root.
- Runtime implemented: immutable synthetic trade facts and the versioned settlement-date mismatch rule with weekend/explicit-holiday handling and review/escalation routes.
- Runtime not implemented: persistence behavior, authentication, model providers, remaining exception-rule families, public-data adapters, and observability integrations.

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
| Backend/domain tests          | Passed               | 23 tests; strict mypy and Ruff passed; 100% measured branch coverage               |
| Integration/E2E tests         | Not run              | Database/queue integration and Playwright harness have not been added yet          |
| Dependency audit              | Passed               | `bun audit`; zero known vulnerabilities after in-range transitive fixes            |
| Secret and source scans       | Not run              | Scheduled for the security foundation and release gates                            |
| Clean-clone startup           | Not run              | Bun is not installed on this Windows host; npm fallback works                      |

## Environment notes

- Node.js: `v22.19.0`
- npm: `11.6.0`
- Python: `3.14.7` managed by `uv`
- Backend lock/tooling: `uv 0.12.2`; 57 resolved packages in `backend/uv.lock`
- Bun: unavailable on this host even though `bun.lock` is committed
- Graphify CLI: `0.9.41`; project-scoped Codex skill registered under `.codex/skills/graphify`
- Graphify code graph: 894 nodes, 1,374 edges, and 106 generated communities from code-only AST extraction; no model/API credits used

## Next three actions

1. Add CI jobs for frontend and backend formatting, lint, strict type checking, tests, and builds.
2. Add the next deterministic exception-rule family without database coupling.
3. Review persistence contracts before creating the first Alembic migration or database adapter.

## Known limitations

- The current UI is a reviewed frontend foundation, not a complete TradeOps workflow.
- Overview values are deterministic synthetic fixtures; they are not measurements or operational claims.
- Placeholder routes intentionally contain no backend, authentication, financial-rule, or model behavior.
- Settlement policy v1 uses only weekends and explicitly supplied holiday dates; it is not a universal market calendar.
