# Roadmap

This roadmap describes the evidence expected for the initial public portfolio release. It is a planning aid, not a delivery guarantee.

## Phase 0 — clean-room foundation

- Define users, outcomes, scope, and non-goals.
- Establish contribution, security, licensing, and repository standards.
- Make the generated frontend reproducibly verifiable.

**Exit signal:** the feature branch has a documented safety boundary and passes formatting, linting, type-checking, and production build checks.

## Phase 1 — architecture and service skeleton

- Record system context, components, trust boundaries, and major decisions.
- Add a Python 3.12 `uv` workspace with a FastAPI service and background worker.
- Establish configuration, health, readiness, version, and test conventions.

**Exit signal:** API and web foundations start locally and have automated unit checks.

## Phase 2 — synthetic exception domain

- Model trades, lifecycle events, exceptions, evidence, decisions, and audit entries.
- Add deterministic synthetic-data generators and seed scenarios.
- Introduce PostgreSQL persistence, migrations, Redis-backed work dispatch, and a transactional outbox.

**Exit signal:** a reproducible scenario can be ingested, classified, persisted, and audited without external data.

## Phase 3 — governed copilot workflow

- Add retrieval and provider abstractions with deterministic mock defaults.
- Implement LangGraph orchestration, structured outputs, citations, confidence, and human-in-the-loop controls.
- Keep all recommendations advisory and require explicit approval for state-changing workflow actions.

**Exit signal:** golden scenarios produce reproducible, cited recommendations with policy-enforced review.

## Phase 4 — operations console

- Connect the React console to live APIs.
- Deliver exception queues, detail views, evidence timelines, approval flows, and audit history.
- Meet responsive, accessibility, empty-state, loading-state, and error-state requirements.

**Exit signal:** the end-to-end demo is usable without privileged infrastructure or live financial data.

## Phase 5 — reliability, security, and observability

- Add OIDC integration, role-based authorization, rate limits, and secure headers.
- Instrument traces, metrics, structured logs, and actionable dashboards.
- Add integration, contract, end-to-end, accessibility, load, recovery, and security checks.

**Exit signal:** CI enforces release gates and operational runbooks cover expected failure modes.

## Phase 6 — public release

- Publish deployment templates, architecture assets, evaluation results, and a polished demo guide.
- Complete dependency, secret, license, and provenance checks.
- Review the pull request, rename public surfaces to `tradeops-copilot`, tag the initial release, and publish the portfolio announcement.

**Exit signal:** the repository is public, reproducible, documented, and clearly presented as a synthetic educational system.
