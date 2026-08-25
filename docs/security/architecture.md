# Security architecture

Owner: security maintainer. Purpose: define enforced security boundaries.

Local mode offers conspicuously labelled synthetic roles for usability. Production mode fails closed without a signed RS256 bearer token and validates issuer, audience, `exp`, `iat`, `sub`, and mapped role from JWKS with a bounded timeout. Analyst, reviewer, auditor, and administrator capabilities are checked by the API; frontend visibility is not authorization.

Strict CORS, maximum body size, bounded pagination, fixed-window rate limiting, security headers, stable problem responses, request IDs, input schemas, idempotency, and optimistic concurrency constrain requests. External source names/hosts are allowlisted. Model calls sit behind typed ports and cannot call arbitrary network/file/database tools. Resolution is an allowlisted application command after approval.

Secrets come from environment/deployment secret storage and are masked in settings. CI uses read-only default permissions, pinned actions, dependency review, CodeQL, Gitleaks, Trivy, and SBOM generation. Local passwords are public demo values and explicitly invalid for reuse.
