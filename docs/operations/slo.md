# SLI/SLO proposal

Owner: operations maintainer. Purpose: define candidate measures before production validation.

Candidate SLIs are API successful-request ratio, p95 non-LLM latency, workflow completion/escalation ratio, outbox oldest age, worker retry/dead-letter rate, WebSocket/poll delivery freshness, and evidence-gate outcomes. Candidate objectives require representative load, dependency budgets, and stakeholder review; this repository does not claim them.

Suggested initial evaluation windows: 28-day availability and latency, 24-hour event freshness, and per-release safety/evaluation gates. Exclude planned maintenance only through an explicit policy. Alerts should consume an error budget and link to a runbook rather than page on every single demo error.
