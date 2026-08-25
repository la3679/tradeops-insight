# Threat model

Owner: security maintainer. Purpose: identify assets, trust boundaries, abuse cases, and controls.

Assets are role assignments, workflow/approval state, audit integrity, configuration secrets, provenance, model/provider credentials, and service availability. Boundaries exist at browser/API, identity/API, public content/ingestion, model/orchestration, API/data stores, worker/event transport, and telemetry exporters.

| Threat                    | Primary controls                                                                    | Residual risk                     |
| ------------------------- | ----------------------------------------------------------------------------------- | --------------------------------- |
| forged identity or role   | RS256 JWKS, issuer/audience/time checks, server RBAC                                | identity-provider compromise      |
| unauthorized mutation     | role dependency, idempotency, optimistic version, review interrupt                  | privileged account misuse         |
| prompt/document injection | untrusted-content detection, structured state, citation/policy gate, tool allowlist | novel indirect injection          |
| replay/duplicate/reorder  | idempotency keys, event IDs, aggregate sequences, deferred gaps                     | prolonged transport outage        |
| data or secret leakage    | synthetic-only data, minimization, masked config, safe logging                      | operator misconfiguration         |
| request/resource abuse    | size limit, rate limit, pagination bounds, timeouts                                 | single-node demo exhaustion       |
| dependency/supply chain   | locks, pinned actions/images, Dependabot, CodeQL, Trivy, SBOM                       | undisclosed vulnerabilities       |
| audit tampering           | append-only model and correlated actor/subject/time                                 | local administrator controls host |

This model covers the repository demo, not a financial institution or production certification.
