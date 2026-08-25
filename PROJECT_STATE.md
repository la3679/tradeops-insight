# Project State

Last updated: 2026-08-24 (America/Phoenix)

## Resume checkpoint

- Current phase: Phase 0 discovery and safety, with the reviewed frontend foundation already present.
- Branch: `main`
- Last pushed commit before this checkpoint: `5bcd2c5` (`Add project README`)
- GitHub: `la3679/tradeops-insight`, private, default branch `main`.
- Lovable: `TradeOps Insight` (`d5b87042-8fcf-41cf-aa66-075bf21f45ba`), private and not published.
- Runtime implemented: TanStack Start/React frontend shell with deterministic synthetic overview data and placeholder routes.
- Runtime not implemented: API, worker, persistence, authentication, model providers, exception rules, public-data adapters, and observability stack.

## Safety boundaries

- The repository is an independent educational portfolio project.
- Trades and operational records must remain deterministic and synthetic.
- Public reference data requires recorded provenance and license review before it is committed.
- The application must not connect to trading venues, brokerage accounts, or institutional systems.
- Backend security, authorization, financial rules, persistence, and model behavior are implemented and reviewed outside Lovable.

## Verification status

| Check                      | Status               | Evidence                                                                              |
| -------------------------- | -------------------- | ------------------------------------------------------------------------------------- |
| Dependency install         | Passed               | `npm install --ignore-scripts`; npm reported zero known vulnerabilities on 2026-08-24 |
| TypeScript                 | Passed               | `npx tsc --noEmit`                                                                    |
| Production build           | Passed               | `npm run build` with Vite 8.1.5                                                       |
| Formatting                 | Passed               | `npm run format:check`                                                                |
| Lint                       | Passed with warnings | `npm run lint`; zero errors and six inherited Fast Refresh export warnings            |
| Unit/integration/E2E tests | Not run              | Test harness has not been added yet                                                   |
| Security and secret scans  | Not run              | Scheduled for the security foundation and release gates                               |
| Clean-clone startup        | Not run              | Bun is not installed on this Windows host; npm fallback works                         |

## Environment notes

- Node.js: `v22.19.0`
- npm: `11.6.0`
- Bun: unavailable on this host even though `bun.lock` is committed
- Graphify CLI: `0.9.41`; project-scoped Codex skill registered under `.codex/skills/graphify`
- Graphify code graph: 623 nodes, 1,011 edges, and 80 generated communities from code-only AST extraction; no model/API credits used

## Next three actions

1. Add the frontend test harness (Vitest, React Testing Library, and accessibility smoke coverage) and make `npm run verify` authoritative.
2. Finalize Phase 1 architecture ADRs and scaffold the Python API/worker boundary without adding external integrations or secrets.
3. Add deterministic synthetic domain models and the first independently testable exception-rule family.

## Known limitations

- The current UI is a reviewed frontend foundation, not a complete TradeOps workflow.
- Overview values are deterministic synthetic fixtures; they are not measurements or operational claims.
- Placeholder routes intentionally contain no backend, authentication, financial-rule, or model behavior.
