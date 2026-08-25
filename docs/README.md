# Documentation

TradeOps Copilot documentation is organized by the decision or audience it supports.

## Start here

- [Product brief](product/product-brief.md) — intended users, outcomes, and release boundaries.
- [Non-goals](product/non-goals.md) — explicit exclusions and safety constraints.
- [Project state](../PROJECT_STATE.md) — current checkpoint, verification status, and next actions.
- [Roadmap](../ROADMAP.md) — release phases and acceptance signals.
- [Changelog](../CHANGELOG.md) — user-visible changes by release.

## Documentation map

| Area            | Purpose                                                           | Status      |
| --------------- | ----------------------------------------------------------------- | ----------- |
| `product/`      | Product scope, personas, workflows, and non-goals                 | In progress |
| `architecture/` | System views, trust boundaries, and architecture decisions        | Planned     |
| `api/`          | API conventions, examples, and generated schema guidance          | Planned     |
| `operations/`   | Local development, deployment, observability, and runbooks        | Planned     |
| `security/`     | Threat model, authentication, authorization, and secure defaults  | Planned     |
| `data/`         | Synthetic-data contracts, lineage, and source licensing           | Planned     |
| `evaluations/`  | Quality dimensions, fixtures, and reproducible evaluation reports | Planned     |

## Documentation rules

Documentation must use synthetic examples, must not imply trade-execution capability, and must distinguish deterministic rules from model-assisted recommendations. Architecture changes require an ADR. Operational claims require a reproducible command, test, or runbook.
