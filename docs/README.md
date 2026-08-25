# Documentation

TradeOps Copilot documentation is organized by the decision or audience it supports.

## Start here

- [Product brief](product/product-brief.md) — intended users, outcomes, and release boundaries.
- [Non-goals](product/non-goals.md) — explicit exclusions and safety constraints.
- [Project state](../PROJECT_STATE.md) — current checkpoint, verification status, and next actions.
- [Roadmap](../ROADMAP.md) — release phases and acceptance signals.
- [Changelog](../CHANGELOG.md) — user-visible changes by release.
- [Developer setup](operations/development.md) — supported runtimes, bootstrap, checks, and local API use.
- [API conventions](api/conventions.md) — versioning, correlation, errors, concurrency, and idempotency.
- [Domain glossary](product/domain-glossary.md) — synthetic trade, exception, evidence, and review language.
- [Exception catalog](product/exception-catalog.md) — the twelve rule families and review posture.
- [Deterministic reconciliation](data/reconciliation.md) — rule inputs, order, outputs, and replay contract.
- [Synthetic data methodology](data/synthetic-methodology.md) — reserved identifiers, seed control, and scenario balance.
- [Public source adapters](data/public-sources.md) — implemented GLEIF boundary and excluded sources.
- [Data dictionary](data/data-dictionary.md) — authoritative tables, ownership, and invariants.
- [AI system card](evaluations/ai-system-card.md) — intended model behavior, authority boundary, and limitations.
- [RAG design](architecture/rag-design.md) — document ingestion, retrieval, citations, and evaluation.
- [Governed workflow](architecture/workflow.md) — typed LangGraph state, routing, and review boundary.

## Documentation map

| Area            | Purpose                                                           | Status      |
| --------------- | ----------------------------------------------------------------- | ----------- |
| `product/`      | Product scope, personas, workflows, and non-goals                 | In progress |
| `architecture/` | System views, trust boundaries, and architecture decisions        | In progress |
| `api/`          | API conventions, examples, and generated schema guidance          | In progress |
| `operations/`   | Local development, deployment, observability, and runbooks        | In progress |
| `security/`     | Threat model, authentication, authorization, and secure defaults  | Planned     |
| `data/`         | Synthetic-data contracts, lineage, and source licensing           | In progress |
| `evaluations/`  | Quality dimensions, fixtures, and reproducible evaluation reports | In progress |

## Documentation rules

Documentation must use synthetic examples, must not imply trade-execution capability, and must distinguish deterministic rules from model-assisted recommendations. Architecture changes require an ADR. Operational claims require a reproducible command, test, or runbook.
