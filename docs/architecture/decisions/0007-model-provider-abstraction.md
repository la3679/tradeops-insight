# ADR-0007: Model provider abstraction and deterministic fallback

- **Status:** Accepted
- **Date:** 2026-08-24

## Context

The initial release must work without paid credentials, remain testable offline, and show an optional high-quality hosted-model integration. Provider SDK types, retry behavior, and response formats must not leak into policy or domain logic.

## Decision

Define a narrow provider port that accepts a versioned task, redacted synthetic context, an output schema, timeout, and correlation metadata. It returns typed content plus provider, model, request, usage, latency, and safety metadata.

Ship a deterministic mock provider as the default and the only provider used by CI. Add an optional OpenAI adapter using the Responses API and Structured Outputs for schema-constrained results. Keep optional Bedrock and local adapters as configuration-selected implementations of the same port. Embedding providers use a separate interface from generation providers.

Provider configuration is explicit at process start. There is no silent cross-provider fallback for a single workflow run; an unavailable configured provider produces a recorded retry, refusal, or human-review outcome. This avoids changing behavior and data-handling boundaries without operator intent.

## Consequences

### Positive

- No-key demonstrations and tests are reproducible.
- Application policy remains independent of model vendors.
- Typed metadata supports evaluation, cost reporting, and incident analysis.
- Provider failures degrade to deterministic/manual paths.

### Negative

- The port supports only the common capabilities the product actually needs.
- Provider-specific safety and usage metadata requires normalization.
- Real-provider behavior needs opt-in evaluations outside deterministic CI.

## Guardrails

- Validate every response against the requested schema and bounded size.
- Never send secrets, authorization tokens, real financial data, or unrestricted documents.
- Do not log raw prompts or responses by default; store approved redacted summaries and digests.
- Limit retries, total latency, input size, output size, and tool calls.

## References

- [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses)
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [OpenAI embeddings](https://platform.openai.com/docs/guides/embeddings)
