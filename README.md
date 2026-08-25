# TradeOps Copilot

Auditable agentic AI platform for triaging, investigating, and resolving synthetic fixed-income trade exceptions with deterministic controls, LangGraph, retrieval-augmented generation, human approval, and full-stack observability.

> [!IMPORTANT]
> TradeOps Copilot is an independent educational portfolio project built with synthetic and public data. It is not affiliated with, endorsed by, or derived from the proprietary systems of any financial institution. It does not execute trades or provide financial advice.

## Current status

The repository is under active initial-release development. The reviewed frontend foundation currently provides an accessible operations shell, a deterministic synthetic overview, and honest placeholders for planned workflows. Backend, workflow, retrieval, authentication, and data capabilities are added only after their tests and architecture decisions are committed.

See [`PROJECT_STATE.md`](PROJECT_STATE.md) for the exact phase, verified commands, known issues, and next actions.

## Implemented foundation

- Strict TypeScript and TanStack Start/Vite application.
- Responsive institutional operations shell with semantic navigation and skip link.
- Deterministic synthetic overview metrics, exception table, queue lanes, and category visualization.
- About page with clean-room scope and full disclaimer.
- Placeholder routes that do not claim unfinished behavior.
- Light/dark design tokens and explicit verified, pending, severe, and informational states.
- Documented clean-room, security, review, and contribution standards.

## Local frontend setup

Requirements: Node.js 22 or 24 and npm.

```bash
npm ci
npm run dev
```

Open the local URL printed by Vite. The current frontend uses checked-in deterministic mock data and requires no API key.

## Quality commands

```bash
npm run format:check
npm run lint
npm run typecheck
npm run build
npm run verify
```

The root `Makefile` exposes equivalent commands for a consistent repository interface.

## Scope and safety

- Product brief: [`docs/product/product-brief.md`](docs/product/product-brief.md)
- Non-goals: [`docs/product/non-goals.md`](docs/product/non-goals.md)
- Data decisions: [`DATA_LICENSES.md`](DATA_LICENSES.md)
- Security reporting: [`SECURITY.md`](SECURITY.md)
- Contribution workflow: [`CONTRIBUTING.md`](CONTRIBUTING.md)

All trades, memos, policies, approvals, outcomes, users, and operational metrics are synthetic. Public records may provide reference context only when provenance and current terms are recorded.

## License

Source code and project-authored documentation are available under the [Apache License 2.0](LICENSE). Third-party software and public data remain under their respective terms.
