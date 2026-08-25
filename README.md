# TradeOps Copilot

TradeOps Copilot is an independent educational portfolio project for investigating synthetic fixed-income trade exceptions. The current repository contains the reviewed React/TypeScript frontend foundation and the Phase 0 product and architecture baseline.

> TradeOps Copilot is an independent educational portfolio project built with synthetic and public data. It is not affiliated with, endorsed by, or derived from the proprietary systems of any financial institution. It does not execute trades or provide financial advice.

## Current scope

Implemented:

- Accessible TanStack Start application shell and responsive navigation
- Overview dashboard with clearly labeled deterministic synthetic fixtures
- Route foundations for exceptions, knowledge, evaluations, observability, audit, settings, and About
- Shared design tokens and focused UI primitives
- Loading, empty, and permission-denied presentation states
- Project-scoped Graphify code graph for lower-context repository navigation

Not yet implemented:

- Backend API, worker, persistence, authentication, or authorization
- Financial and exception-classification rules
- Model providers, RAG, agent orchestration, or external data adapters
- End-to-end workflows or production deployment

See [PROJECT_STATE.md](PROJECT_STATE.md) for the exact checkpoint and next actions.

## Local development

Requirements:

- Node.js 22 or another version supported by the pinned frontend toolchain
- npm 11, or Bun when available

```powershell
git clone https://github.com/la3679/tradeops-insight.git
cd tradeops-insight
npm install
npm run dev
```

The default development server prints its local URL after startup. No API key or paid service is required for the current frontend foundation.

## Verification

```powershell
npm run verify
```

Individual checks are also available:

```powershell
npm run format:check
npm run lint
npm run typecheck
npm run build
```

The test harness is the next frontend-platform milestone and is not yet represented by a passing test command.

## Architecture and safety

- [Product brief](docs/product-brief.md)
- [Architecture baseline](docs/architecture.md)
- [ADR 0001: Modular monolith with a background worker](docs/adr/0001-modular-monolith-and-worker.md)
- [Repository agent boundaries](AGENTS.md)

All trade and operational data must remain deterministic and synthetic. Public reference fixtures require source and license provenance before they are committed. Backend security, authorization, financial rules, persistence, and model behavior are outside Lovable's ownership boundary.

## Lovable

The frontend foundation is connected to the private [TradeOps Insight Lovable project](https://lovable.dev/projects/d5b87042-8fcf-41cf-aa66-075bf21f45ba). Commits pushed to the connected branch sync to Lovable. Lovable output remains draft material that requires review and tests.
