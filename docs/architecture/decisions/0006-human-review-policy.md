# ADR-0006: Policy-controlled human review

- **Status:** Accepted
- **Date:** 2026-08-24

## Context

The system demonstrates operational recommendations and demo-state transitions. Automatically applying a model suggestion would blur advisory output with authority, weaken auditability, and create unsafe expectations. Requiring review for every harmless step would make the workflow uninformative and cumbersome.

## Decision

Use deterministic policy to assign each proposed action one of three dispositions: `allow_demo`, `require_review`, or `deny`. Model output never selects or overrides the disposition.

Material, uncertain, low-confidence, conflicting, policy-changing, or externally enriched proposals require supervisor review. A review records the reviewer, decision, reason, proposal version, evidence set, policy version, timestamp, correlation ID, and idempotency key. Editing a material proposal creates a new version and triggers policy evaluation again.

Only narrow, reversible synthetic demo-state actions may receive `allow_demo`. No path can execute, route, book, affirm, allocate, confirm, clear, or settle a real trade.

## Consequences

### Positive

- Authority is explicit, deterministic, and auditable.
- Supervisors can approve, reject, edit, request evidence, or escalate.
- Replayed workflow steps cannot silently repeat an approved mutation.
- Denied proposals remain visible for analysis without being executable.

### Negative

- Approval state and optimistic concurrency add domain complexity.
- Demo workflows can pause indefinitely and need expiry handling.
- Policy changes require versioning and migration of pending reviews.

## Guardrails

- Approval commands validate current proposal version and resource version.
- Approval is single-use and bound to the exact proposed action.
- Expired, already-used, superseded, or unauthorized approvals fail closed.
- Audit and outbox records commit with any approved state change.
