# Data dictionary

- **Owner:** Domain and persistence maintainers
- **Purpose:** Describe authoritative core records, ownership, and high-value invariants.

| Table                                      | Owner/boundary                             | Key invariants                                                                                  |
| ------------------------------------------ | ------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| `users`, `roles`, `user_roles`             | Identity adapter/application authorization | OIDC issuer+subject unique; provider claims map to stable application roles                     |
| `counterparties`, `issuers`, `instruments` | Reference-data adapters                    | source/version retained; instrument IDs use `INST-DEMO-*`; references are versioned             |
| `trades`                                   | Trade aggregate                            | `TRD-DEMO-*` unique; optimistic `latest_version` positive                                       |
| `trade_events`                             | Import boundary                            | `EVT-DEMO-*` and idempotency key unique; raw bounded JSON retained for audit                    |
| `trade_versions`                           | Normalization/domain application           | immutable trade+version unique; Decimal precision; positive values; settlement not before trade |
| `exceptions`                               | Exception application service              | trade/version ownership; stable family; mutable state guarded by `version`                      |
| `exception_evidence`                       | Reconciliation/retrieval                   | bounded facts and optional provenance attached to one exception                                 |
| `audit_events`                             | Audit service                              | append-only application event with actor, resource, correlation, and bounded payload            |
| `outbox_messages`                          | Transaction boundary/worker                | unique event, versioned schema, correlation, availability, attempts, delivery state             |
| `idempotency_records`                      | Command boundary                           | scope+key unique and bound to request digest plus recorded response                             |
| `documents`, `document_chunks`             | Knowledge ingestion/retrieval              | versioned documents; stable chunk IDs, digests, metadata, and positive token counts             |
| `workflow_runs`, `workflow_steps`          | Graph orchestrator                         | stable thread/graph/prompt/provider versions; unique node attempt and state version             |
| `tool_calls`                               | Safe tool boundary                         | authorization reference, input digest, bounded output metadata, latency, and error code         |
| `approvals`, `resolution_actions`          | Human review/executor                      | single-use idempotency; exact proposal/exception versions; before/after demo values             |
| `evaluation_cases`, runs, results          | Evaluation runner                          | versioned cases/config; one result per run/case; bounded score and latency                      |
| `data_source_sync_runs`                    | Admin/worker                               | source ID, counts, cursor, lifecycle, actor, and bounded failure code                           |

All primary keys are UUIDs. Application times are timezone-aware UTC. Monetary and quantity fields use fixed-precision `NUMERIC`; binary floating point is prohibited. PostgreSQL is authoritative and Redis data is rebuildable.

Each migration names its fixed table set and renders PostgreSQL DDL offline. Existing table definitions are changed only through a new migration; migration-chain and upgrade-from-empty checks protect the reviewed sequence.
