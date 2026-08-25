# Incident-response playbook

Owner: security/operations maintainer. Purpose: coordinate a suspected incident.

1. Triage severity, affected assets, time range, revision, and whether any non-synthetic data is involved.
2. Contain by disabling affected ingress/provider credentials or mutation paths; preserve evidence and do not rewrite logs/history.
3. Collect sanitized logs, audit events, traces, container/image/SBOM versions, identity events, and database/outbox state.
4. Eradicate the cause, rotate exposed credentials, patch with review, and validate from a clean environment.
5. Recover gradually, monitor defined indicators, and confirm audit/event continuity.
6. Document timeline, impact, decisions, root causes, corrective actions, owners, and due dates without sensitive exploit detail.

Real-data exposure is outside intended scope and must be treated as a high-severity boundary violation.
