# Scaling and evolution

Owner: platform maintainer. Purpose: state evidence-based growth paths.

Scale stateless API replicas behind a load balancer, externalize demo mutations to PostgreSQL, partition worker queues by task class, and move FAISS artifacts to versioned object storage before increasing load. Redis remains transient; PostgreSQL/outbox remain authoritative. WebSocket fan-out would require a shared event transport and bounded per-client buffers.

Extract a service only when independent ownership, deploy cadence, data ownership, fault isolation, or materially different scaling is measured. Likely candidates are ingestion/evaluation workers before domain APIs. Preserve correlation IDs, event schemas, idempotency, and audit continuity across any boundary. The included Terraform is a topology reference, not validated capacity guidance.
