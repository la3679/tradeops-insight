# TradeOps Copilot Product Brief

## Purpose

TradeOps Copilot is an independent educational portfolio application for investigating synthetic fixed-income trade exceptions. It demonstrates safe orchestration, deterministic validation, evidence-backed recommendations, human review, and auditability at portfolio scale.

It does not execute trades, provide financial advice, or represent the systems or practices of any financial institution.

## Users and outcomes

- Operations analysts inspect a synthetic exception queue, evidence, and proposed next steps.
- Supervisors approve, edit, reject, or escalate proposed synthetic-state changes.
- Auditors inspect an append-only decision trail containing evidence, tool activity, workflow state, and human decisions.
- Demo administrators configure non-sensitive local settings and synthetic dataset generation.

## First release journey

1. Generate or import a deterministic synthetic dataset.
2. Validate its schema and detect deterministic exception categories.
3. Enrich a case only through typed, allowlisted adapters.
4. Retrieve relevant synthetic policy evidence with citations.
5. Produce an advisory resolution proposal and validate it against deterministic policy checks.
6. Pause material or uncertain changes for human review.
7. Apply only the approved synthetic-state change and retain the complete audit trail.

## Non-goals

- Real trading, settlement, brokerage, exchange, or order-management connectivity
- Employer code, data, prompts, schemas, branding, or operational procedures
- Production adoption, performance, accuracy, savings, or compliance claims
- Frontend enforcement of authorization, pricing, risk, or settlement rules
- A mandatory paid model or cloud service for the default demo

## Data policy

All trades, positions, counterparties, and events are synthetic. Small public reference fixtures may be introduced only after their source, terms, retrieval time, transformation, row count, and checksum are recorded. External and retrieved content is untrusted input, never instruction text.

## Release principle

The default local experience must remain deterministic, offline-capable, and useful without credentials. Optional external providers and public-data synchronization sit behind typed adapters and cannot weaken the mock-mode path.
