# Data dictionary

Owner: domain maintainer. Purpose: define canonical concepts.

| Entity                   | Key fields                                                                     | Invariants                                             |
| ------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------ |
| Trade                    | synthetic trade ID, product, currency, notional, price, trade/settlement dates | immutable facts; UTC/event versioning                  |
| Trade event              | event ID, aggregate ID, sequence, occurred-at                                  | append-only and ordered per aggregate                  |
| Exception                | ID, type, severity, status, review route, evidence, version                    | exactly one synthetic trade; optimistic mutation       |
| Workflow                 | ID, exception ID, graph/prompt/provider/model versions, status, steps          | replayable; approval interrupt before tool             |
| Approval                 | workflow, decision, reviewer, expected version                                 | reviewer/admin only; idempotent                        |
| Audit event              | actor, subject, type, time, summary                                            | append-only; no secret contents                        |
| Knowledge document/chunk | provenance, version, jurisdiction, hash, content                               | public/synthetic label; untrusted instructions flagged |
| Outbox event             | ID, aggregate sequence, payload, publication state                             | written with state; at-least-once delivery             |
| Evaluation case/run      | dataset, prompt, provider/model versions, expected/actual                      | deterministic mock replay                              |

Amounts use decimal strings; identifiers are synthetic stable IDs/UUIDs; timestamps are UTC; no committed field contains client or employer data.
