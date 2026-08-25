# TradeOps Copilot

TradeOps Copilot is an independent educational portfolio project for investigating synthetic fixed-income trade exceptions. The repository contains a React operations console, a typed FastAPI/Celery backend foundation, deterministic domain rules, and a reproducible local infrastructure stack.

> TradeOps Copilot is an independent educational portfolio project built with synthetic and public data. It is not affiliated with, endorsed by, or derived from the proprietary systems of any financial institution. It does not execute trades or provide financial advice.

## Current scope

Implemented:

- Accessible TanStack Start application shell and responsive navigation
- Overview dashboard with clearly labeled deterministic synthetic fixtures
- Route foundations for exceptions, knowledge, evaluations, observability, audit, settings, and About
- Shared design tokens and focused UI primitives
- Loading, empty, and permission-denied presentation states
- Vitest and React Testing Library coverage for fixtures, state primitives, and overview components
- Automated axe accessibility smoke coverage for the overview content
- Project-scoped Graphify code graph for lower-context repository navigation
- FastAPI API and Celery worker composition roots with validated, masked configuration
- Immutable synthetic trade facts and a deterministic settlement-date mismatch rule
- Docker Compose services for the web app, API, worker, PostgreSQL, Redis, Keycloak, and OpenTelemetry Collector
- Pinned frontend/backend CI and local pre-commit verification

Not yet implemented:

- Persistence schemas/repositories and application-facing API contracts
- Authentication and authorization enforcement
- Remaining deterministic exception-rule families
- Model providers, RAG, agent orchestration, or external data adapters
- End-to-end workflows or production deployment

See [PROJECT_STATE.md](PROJECT_STATE.md) for the exact checkpoint and next actions.

## Local development

For the complete local stack, install Docker Desktop and start its Linux container engine. Then run:

```powershell
git clone https://github.com/la3679/tradeops-insight.git
cd tradeops-insight
npm run stack:up
```

Local services:

- Web console: `http://127.0.0.1:3000`
- API documentation: `http://127.0.0.1:8000/docs`
- Keycloak: `http://127.0.0.1:8080`
- API readiness: `http://127.0.0.1:8000/api/v1/health/ready`

The defaults in `.env.example` are deliberately non-secret local demonstration values. Override them in an untracked `.env` when needed. Stop the stack without deleting its named volumes using `npm run stack:down`.

For host-based development, use Node.js 24.15, Bun 1.4, Python 3.14.7, and uv 0.12.2:

```powershell
npm install
npm run backend:sync
npm run dev
```

No API key or paid service is required for the deterministic local foundation.

## Verification

```powershell
npm run verify
```

Individual checks are also available:

```powershell
npm run format:check
npm run lint
npm run typecheck
npm run test
npm run test:a11y
npm run build
npm run verify:backend
npm run stack:config
```

Tests use deterministic local fixtures and do not require an API key or network access.

## Architecture and safety

- [Product brief](docs/product-brief.md)
- [Architecture baseline](docs/architecture.md)
- [ADR 0001: Modular monolith with a background worker](docs/adr/0001-modular-monolith-and-worker.md)
- [ADR 0002: Python runtime and task queue](docs/adr/0002-python-runtime-and-task-queue.md)
- [Domain glossary](docs/domain-glossary.md)
- [Repository agent boundaries](AGENTS.md)

All trade and operational data must remain deterministic and synthetic. Public reference fixtures require source and license provenance before they are committed. Backend security, authorization, financial rules, persistence, and model behavior are outside Lovable's ownership boundary.

## Lovable

The frontend foundation is connected to the private [TradeOps Insight Lovable project](https://lovable.dev/projects/d5b87042-8fcf-41cf-aa66-075bf21f45ba). Commits pushed to the connected branch sync to Lovable. Lovable output remains draft material that requires review and tests.
