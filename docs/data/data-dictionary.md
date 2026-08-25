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

All primary keys are UUIDs. Application times are timezone-aware UTC. Monetary and quantity fields use fixed-precision `NUMERIC`; binary floating point is prohibited. PostgreSQL is authoritative and Redis data is rebuildable.

The initial migration currently binds to the reviewed metadata revision to make offline SQL and upgrade-from-empty verification possible. Before a released migration is followed by another revision, its table operations will be frozen explicitly so later metadata changes cannot alter historical behavior.
