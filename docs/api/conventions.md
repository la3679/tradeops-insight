# API conventions

- **Owner:** API maintainers
- **Purpose:** Define stable transport behavior shared by every TradeOps Copilot endpoint.

## Versioning and media

Application endpoints are rooted at `/api/v1`. Health endpoints remain unversioned for platform probes. JSON is the default representation; timestamps use UTC RFC 3339 strings and fixed-precision amounts are serialized as strings.

## Request correlation

Every response returns `X-Request-ID`. A caller may supply an identifier containing 1–128 ASCII letters, numbers, dots, underscores, colons, or hyphens. Unsafe or missing identifiers are replaced with a UUID. The same identifier is propagated through audit and asynchronous event envelopes; it is not an authentication credential.

## Errors

Expected application and request-validation errors use one envelope:

```json
{
  "error": {
    "code": "VERSION_CONFLICT",
    "message": "The exception changed after it was loaded.",
    "request_id": "request-7",
    "details": [{ "field": "version", "reason": "stale" }]
  }
}
```

Codes are stable uppercase identifiers. Messages are safe for display and do not contain stack traces, query text, model prompts, tokens, or secret-bearing dependency responses. `details` is bounded, structured, and optional.

## Idempotency and concurrency

State-changing endpoints identified by the API guide require `Idempotency-Key`. Reusing a key with the same canonical request returns the recorded outcome; reusing it with a different request fails with `409 IDEMPOTENCY_CONFLICT`.

Mutable resources expose an integer `version`. Commands include the expected version and fail with `409 VERSION_CONFLICT` when stale. A human approval is bound to the exact proposal and resource versions.

## Pagination and filtering

Collections use opaque cursor pagination with `limit`, `next_cursor`, and `has_more`. Limits have server-side maxima. Filters use documented repeated or scalar query parameters; unknown parameters are rejected after the endpoint contract is finalized. Stable sorting includes a unique tie-breaker.

## OpenAPI

Interactive docs and `/openapi.json` are available in development and test environments and disabled in production by default. Human-authored examples complement the generated contract; neither is an authorization boundary.
