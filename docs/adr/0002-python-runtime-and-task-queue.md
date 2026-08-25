# ADR 0002: Python runtime and durable task queue boundary

- Status: Accepted for the Phase 1 foundation
- Date: 2026-08-24

## Context

The target architecture needs a typed API process and separately runnable worker. Long-running document, reference-data, and batch-evaluation work must not execute in HTTP request handlers. The foundation must be reproducible while avoiding premature external connections or business behavior.

## Decision

Use Python 3.14 with a `uv`-managed project and committed universal lockfile. Use FastAPI as the HTTP composition root and Celery with Redis as the initial durable task-queue boundary. Configure JSON-only serialization, UTC, late acknowledgements, and rejection on worker loss. Do not start or probe Redis during imports, tests, or API startup.

PostgreSQL, SQLAlchemy, Alembic, and Psycopg are pinned as the intended persistence toolchain, but engines, sessions, schemas, and migrations are deferred until domain contracts and persistence ownership receive separate review.

## Consequences

- API and worker processes can evolve independently without prematurely splitting services.
- A checked-in lockfile makes local and CI dependency resolution reproducible.
- Redis becomes an operational dependency only when the worker is explicitly run.
- Idempotency keys, retry policy, dead-letter handling, and queue topology must be decided before the first production-like task is added.
- An architecture test guards the domain package against framework and infrastructure imports.
