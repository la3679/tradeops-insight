# ADR 0003: Relational persistence and idempotency

Status: Accepted — 2026-08-24

## Decision

PostgreSQL is the authoritative local store. SQLAlchemy models and Alembic migrations define the schema; domain code remains independent of either library. UUID identifiers, UTC timestamps, fixed-precision numerics, foreign keys, queue indexes, optimistic exception versions, and unique idempotency keys are explicit in the first migration.

Declarative model files are excluded from behavioral coverage because they contain schema declarations rather than executable decisions. Migration drift, repository behavior, and domain policies are tested separately.

## Consequences

- A migration must accompany every relational contract change.
- `alembic check` is a release gate.
- Approval and resolution writes require both an exception version and an idempotency key.
- Model-assisted components cannot write to the database directly; they use reviewed application ports.
