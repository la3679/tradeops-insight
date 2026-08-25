# Domain glossary

- **Owner:** Product and domain maintainers
- **Purpose:** Keep implementation, UI, tests, and documentation aligned on portfolio-safe language.

| Term              | Meaning in TradeOps Copilot                                                                                                                         |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Synthetic trade   | An invented fixed-income record with a reserved `TRD-DEMO-*` identifier. It is never an order or a real transaction.                                |
| Trade event       | A versioned imported/generated fact about a synthetic trade, identified by `EVT-DEMO-*`. Duplicate detection operates on events and trade versions. |
| Reference record  | A versioned, provenance-stamped entity or instrument fact from an approved fixture or public source.                                                |
| Exception         | A deterministic finding that a synthetic trade or its evidence does not satisfy one documented reconciliation rule.                                 |
| Exception family  | One of the twelve stable categories used for queueing, metrics, evaluation, and runbooks.                                                           |
| Evidence          | Bounded facts supporting a finding or recommendation. Retrieved text is untrusted evidence, never executable instruction.                           |
| Severity          | Operational urgency: low, medium, high, or critical.                                                                                                |
| Risk              | Deterministic review risk: low, medium, high, or critical. A model cannot lower it.                                                                 |
| Proposal          | An advisory, versioned suggested demo-state change with assumptions, evidence, and citations.                                                       |
| Approval          | A single-use supervisor decision bound to an exact proposal and resource version.                                                                   |
| Resolution action | An idempotent mutation of synthetic application state after policy and authorization checks. It cannot affect real trading systems.                 |
| Workflow run      | A persisted execution of the governed investigation graph, including node outcomes and provider metadata.                                           |
| Audit event       | An append-only application record of a material command or decision; it is distinct from diagnostic logs and traces.                                |

## Entity reconciliation language

- A **missing or invalid LEI** is absent, malformed, or fails deterministic check-digit validation.
- An **unknown entity** has a valid-shaped LEI that is absent from the approved reference snapshot.
- An **inactive entity** is present but explicitly inactive in that snapshot.
- A **legal-name mismatch** means normalized input matches neither the reference legal name nor an approved alias.

These findings are data-quality signals, not legal, compliance, credit, or investment conclusions.
