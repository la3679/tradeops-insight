# Project State

Last updated: 2026-08-24 (America/Phoenix)

## Resume checkpoint

- Current phase: Phase 1 developer platform, with the frontend verification harness implemented.
- Branch: `main`
- Last pushed commit before this checkpoint: `0955447` (`Add project checkpoint and Graphify navigation`)
- GitHub: `la3679/tradeops-insight`, private, default branch `main`.
- Lovable: `TradeOps Insight` (`d5b87042-8fcf-41cf-aa66-075bf21f45ba`), private and not published.
- Runtime implemented: TanStack Start/React frontend shell with deterministic synthetic overview data, placeholder routes, and component/accessibility tests.
- Runtime not implemented: API, worker, persistence, authentication, model providers, exception rules, public-data adapters, and observability stack.

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
| Integration/E2E tests         | Not run              | Backend contracts and Playwright harness have not been added yet                   |
| Dependency audit              | Passed               | `bun audit`; zero known vulnerabilities after in-range transitive fixes            |
| Secret and source scans       | Not run              | Scheduled for the security foundation and release gates                            |
| Clean-clone startup           | Not run              | Bun is not installed on this Windows host; npm fallback works                      |

## Environment notes

- Node.js: `v22.19.0`
- npm: `11.6.0`
- Bun: unavailable on this host even though `bun.lock` is committed
- Graphify CLI: `0.9.41`; project-scoped Codex skill registered under `.codex/skills/graphify`
- Graphify code graph: 754 nodes, 1,158 edges, and 92 generated communities from code-only AST extraction; no model/API credits used

## Next three actions

1. Finalize Phase 1 architecture ADRs and scaffold the Python API/worker boundary without adding external integrations or secrets.
2. Add deterministic synthetic domain models and the first independently testable exception-rule family.
3. Add CI jobs for frontend formatting, lint, strict type checking, tests, and production build.

## Known limitations

- The current UI is a reviewed frontend foundation, not a complete TradeOps workflow.
- Overview values are deterministic synthetic fixtures; they are not measurements or operational claims.
- Placeholder routes intentionally contain no backend, authentication, financial-rule, or model behavior.
