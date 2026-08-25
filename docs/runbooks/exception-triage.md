# Deterministic exception triage

1. Confirm the record is labelled synthetic and note the rule version.
2. Compare the finding evidence with the original immutable trade/event snapshot.
3. Request more evidence if reference freshness, confirmation, or memo provenance is insufficient.
4. Approve or edit only allowlisted proposed demo-field corrections and only against the current exception version.
5. Reject unsupported changes. Escalate unknown identities, malformed payloads, material numeric differences, contradictory evidence, or stale-version conflicts.
6. Verify the approval and resulting action appear as separate immutable audit events.

The application never transmits or executes a trade. A resolution changes only local synthetic demonstration state.
