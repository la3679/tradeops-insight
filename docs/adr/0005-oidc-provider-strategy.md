# ADR 0005: OIDC provider strategy

Status: accepted. Use standards-based OIDC and validate RS256 signature, issuer, audience, required timestamps, subject, and mapped realm role at the API. Keycloak provides a reproducible local realm; production may use another conformant provider. A labelled header role is allowed only outside production. This avoids proprietary identity coupling while keeping authorization server-owned.
