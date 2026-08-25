# ADR-0003: PostgreSQL, Redis, and transactional outbox

- **Status:** Accepted
- **Date:** 2026-08-24

## Context

Application state, approvals, audit history, workflow metadata, and asynchronous work must survive process failure. Publishing a queue message after a database commit creates a failure window; publishing before commit can expose work for state that never became authoritative. Redis is useful for short-lived delivery and fan-out but is not the right source of truth for the portfolio's audit requirements.

## Decision

Use PostgreSQL as the authoritative store and SQLAlchemy 2 async sessions for application persistence. Schema changes use versioned Alembic migrations. Store times in UTC, money and quantities as fixed-precision decimals, and identifiers as application-generated UUIDs.

Write domain state, audit entries, and versioned outbox records in one database transaction. A worker leases undispatched outbox records, publishes typed messages to Redis-backed delivery, and records delivery metadata. Consumers are idempotent and persist their processing key before acknowledging work.

Use Redis for work delivery, rate limits, short-lived locks, caches, and WebSocket fan-out. Redis data can be rebuilt; it never overrides PostgreSQL state.

## Consequences

### Positive

- Authoritative state and publication intent commit atomically.
- Duplicate delivery is safe and visible.
- Redis loss does not erase the audit trail or requested work.
- Local development uses common, well-supported infrastructure.

### Negative

- Delivery is at least once, so every consumer must be idempotent.
- Outbox leasing, retention, and poison-message handling need operational checks.
- Integration tests require PostgreSQL and Redis in addition to fast in-memory unit tests.

## Guardrails

- Outbox payloads carry schema name, version, event ID, aggregate ID, correlation ID, creation time, and synthetic-data classification.
- Payloads contain references and bounded metadata, not secrets or unrestricted documents.
- Leasing uses database concurrency controls; retries use bounded exponential backoff and a dead-letter state.
- Audit rows are append-only through application permissions.
