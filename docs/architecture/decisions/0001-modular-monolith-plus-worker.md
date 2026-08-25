# ADR-0001: Modular monolith plus worker

- **Status:** Accepted
- **Date:** 2026-08-24

## Context

The project must demonstrate clear boundaries, asynchronous processing, durable workflows, and independent web scaling without manufacturing operational complexity. A microservice fleet would add deployment, networking, versioning, and consistency problems that do not improve this portfolio's core evidence.

## Decision

Use three deployable units: the React web console, a FastAPI API/orchestrator, and a Python background worker. The API and worker share framework-independent domain and application modules. PostgreSQL is authoritative; Redis supports delivery and fan-out.

Modules communicate through typed application ports. Domain code does not import FastAPI, Celery, LangGraph, a model SDK, a vector store, or a public-source client. Cross-process work uses versioned task and event envelopes rather than importing worker implementation into request handlers.

## Consequences

### Positive

- A clean clone has a tractable local topology.
- Domain rules stay testable without infrastructure or provider credentials.
- API and worker can scale and fail independently where it matters.
- Database transactions can cover application state, audit entries, and outbox messages.

### Negative

- API and worker releases must remain compatible with shared schemas.
- A monorepo change can affect multiple deployables.
- Module boundaries require review because the runtime does not enforce network separation.

## Rejected alternatives

- **Single web/API process:** long-running work and retry behavior would compete with request handling.
- **Microservices per domain:** disproportionate operational cost and distributed consistency risk.
- **Serverless functions for every operation:** awkward for persisted graph execution, local replay, and long-lived streaming.
