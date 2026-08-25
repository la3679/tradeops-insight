# ADR-0005: OIDC and server-side role authorization

- **Status:** Accepted
- **Date:** 2026-08-24

## Context

The console has analyst, supervisor, auditor, and administrator journeys. Browser-only role checks are cosmetic and forgeable. The local demo needs reproducible identity behavior, while deployments should integrate with standard identity providers rather than store passwords in the application.

## Decision

Use OpenID Connect authorization code flow with PKCE for interactive users. Provide Keycloak configuration for local development and keep provider-specific details behind configuration. The API validates issuer, audience, signature, expiry, and allowed algorithms using cached discovery and JWKS metadata.

Map narrowly scoped external claims to project roles through server configuration. Every protected endpoint declares an application permission; the API evaluates permissions and resource conditions. Worker tasks carry an authenticated actor snapshot and the authorizing decision reference, not a reusable access token.

Use an explicitly enabled, synthetic-only development identity mode for fast local and test workflows. It is disabled by default outside development and cannot be selected through a request header.

## Consequences

### Positive

- The application does not own password storage or recovery.
- The same permission model works with local and hosted OIDC providers.
- Authorization remains enforceable independent of frontend routes and controls.
- Audit events can identify both the actor and authorization decision.

### Negative

- OIDC discovery, key rotation, clock skew, and claim mapping require careful tests.
- Keycloak adds a local container and configuration surface.
- Deployment operators must configure redirect URIs and claims correctly.

## Guardrails

- Reject tokens with unexpected issuer, audience, algorithm, expiry, or missing subject.
- Never log tokens, authorization headers, PKCE verifiers, or raw identity-provider responses.
- Default-deny unmapped roles and unknown permissions.
- Re-evaluate authorization at state-changing API boundaries; UI visibility never grants permission.
