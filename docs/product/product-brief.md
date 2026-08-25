# TradeOps Copilot product brief

**Status:** Approved portfolio scope

**Owner:** Love Jayesh Ahir

**Document purpose:** Define the public, clean-room product boundary before implementation.

## Summary

TradeOps Copilot is an auditable operations console for investigating synthetic fixed-income trade exceptions. It demonstrates how deterministic reconciliation, retrieval-augmented generation, typed agent orchestration, human approval, and end-to-end observability can work together without connecting to a brokerage, exchange, order-management system, settlement network, or real trading account.

The repository is an independent educational portfolio project. It is not affiliated with, endorsed by, or derived from the proprietary systems of any financial institution. All trade records, policies, approvals, outcomes, and operational metrics are synthetic. Public sources may enrich legal-entity, issuer, and Treasury reference context only when their current terms permit the intended use.

## Problem

Trade-operations analysts often need to combine structured records, reference data, free-text notes, policy evidence, workflow history, and human judgment. A useful portfolio system should show how those inputs can be reconciled while keeping calculations deterministic, model output advisory, side effects allowlisted, and every decision reviewable.

## Users

- **Operations analyst:** investigates exceptions, reviews evidence, and submits recommendations.
- **Supervisor:** approves, edits, rejects, requests more evidence, or escalates proposed synthetic resolutions.
- **Auditor:** inspects evidence, workflow steps, tool summaries, approvals, and immutable application audit events without changing state.
- **Administrator:** manages demo thresholds, source synchronization, model-provider configuration, and local roles.

## Core outcome

A user can load or generate a deterministic synthetic dataset, detect one or more documented exception categories, run a persisted workflow, inspect cited evidence and deterministic checks, pause for human review, resume safely, and apply only an explicitly approved demo-state change.

## Required capabilities

1. Deterministic ingestion, validation, reconciliation, and exception classification.
2. Typed LangGraph state, explicit nodes, persisted checkpoints, bounded retries, and safe interruption/resumption.
3. Retrieval over versioned synthetic policy/runbook documents with provenance and verifiable citations.
4. A deterministic mock provider as the no-key default, plus optional configurable OpenAI, Bedrock, and local adapters.
5. Narrow Pydantic-validated tools with authorization, idempotency, telemetry, and explicit human approval before material actions.
6. A versioned FastAPI REST/WebSocket surface with consistent errors, correlation IDs, optimistic concurrency, pagination, and server-enforced RBAC.
7. An accessible React/TypeScript operations console covering overview, queue, investigation, approval, knowledge, evaluation, observability, audit, settings, and disclaimer journeys.
8. Transactional event publication, an idempotent worker, structured logs, OpenTelemetry traces, Prometheus metrics, and local dashboards.
9. Offline deterministic tests and evaluations, clean-clone commands, security controls, data provenance, and reproducible documentation.

## Exception scope

The initial release covers twelve synthetic exception families: invalid or missing LEI; legal-name mismatch; unknown or inactive entity; synthetic instrument mismatch; quantity/notional mismatch; price-tolerance breach; currency mismatch; settlement-date mismatch; duplicate trade/event; missing or contradictory confirmation/memo; stale reference data; and unsupported or malformed payload.

Every family requires typed detection, severity/risk rules, a resolvable case, an escalation case, human-readable evidence, suggested next actions, audit events, and tests.

## Product principles

- **Deterministic authority:** models may classify, summarize, and draft; code owns money, dates, permissions, validation, and action authorization.
- **Evidence before action:** proposals cite versioned evidence or refuse/escalate.
- **Least agency:** no unrestricted shell, network, database, or arbitrary-code tool is exposed to a model.
- **Human control:** material or uncertain changes always stop for a supervisor decision.
- **Replayability:** mock-mode fixtures, workflow IDs, prompt versions, and provider metadata support safe replay.
- **Graceful degradation:** deterministic operations, manual review, and audit remain available when external services fail.
- **Honest measurement:** performance, evaluation, and security results are published only when reproduced by committed commands and labeled with their environment.

## Initial architecture boundary

The system uses three deployable units: a web application, a FastAPI API/orchestrator, and a background worker. PostgreSQL is the source of truth, Redis supports asynchronous delivery and real-time fan-out, and document/vector storage remains behind typed ports. This modular-monolith-plus-worker shape keeps the portfolio credible without manufacturing microservices.

## Release success

The initial public release is successful when a clean clone runs in no-key mock mode; all twelve exception families and critical role journeys are covered; the graph pauses and resumes safely; citations and refusals are evaluated; CI, security, type, test, and build gates pass; public-data use is traceable and license-safe; and the complete reachable history contains no secrets, private data, employer material, or proprietary identifiers.
