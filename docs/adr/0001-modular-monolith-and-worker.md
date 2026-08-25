# ADR 0001: Modular Monolith with a Background Worker

- Status: Accepted
- Date: 2026-08-24

## Context

The portfolio must demonstrate API, workflow, retrieval, audit, asynchronous processing, and observability patterns without manufacturing operational complexity. Splitting each capability into a separate service would add deployment and failure modes before the domain boundaries are proven.

## Decision

Use one modular FastAPI backend codebase and one worker process, supported by PostgreSQL, Redis, and a storage abstraction. The web console is deployed separately. Domain and application modules expose typed boundaries that infrastructure adapters implement.

The API and worker may run different entry points and scale independently while sharing versioned domain and application packages. Background commands are idempotent and correlated with durable audit/outbox records.

## Consequences

Benefits:

- Deterministic rules remain easy to test without infrastructure.
- Local startup and debugging stay understandable.
- API and worker behavior share domain invariants without duplicating them.
- Future service candidates remain visible through ports and module ownership.

Tradeoffs:

- Backend modules share a release lifecycle initially.
- Strict dependency checks and review are needed to prevent accidental coupling.
- A later extraction requires explicit ownership of schemas, events, and migrations.

## Revisit when

A module needs materially different scaling, isolation, deployment cadence, data ownership, or operational ownership, and measurements show that process-level separation is insufficient.
