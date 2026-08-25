# ADR-0008: OpenTelemetry observability

- **Status:** Accepted
- **Date:** 2026-08-24

## Context

Exception workflows span browser requests, API transactions, asynchronous jobs, graph nodes, retrieval, and optional provider calls. Troubleshooting requires shared correlation without placing secret-bearing payloads in telemetry. A provider-specific monitoring SDK would make local and reference deployments inconsistent.

## Decision

Instrument services with OpenTelemetry APIs and semantic conventions. Export OTLP to an OpenTelemetry Collector. The local stack routes traces to a trace backend, metrics to Prometheus, and dashboards to Grafana. Application logs are structured JSON on stdout and include trace/span correlation where available.

Use a bounded application vocabulary for exception family, workflow state, outcome, provider class, and dependency. High-cardinality identifiers belong in traces or logs, not metric labels. Model telemetry records provider/model identifiers, duration, token usage when available, validation outcome, and redacted content digests—not raw prompts, raw retrieved chunks, or responses.

## Consequences

### Positive

- Trace context follows request, outbox, worker, and graph boundaries.
- Instrumentation remains portable across local and cloud backends.
- Prometheus alerts and Grafana dashboards are reproducible.
- Privacy and cardinality constraints are designed in rather than retrofitted.

### Negative

- Context propagation across asynchronous delivery needs explicit envelopes.
- Collector and dashboard configuration require version control and tests.
- Sampling can complicate incident reconstruction unless audit events remain independent.

## Guardrails

- Telemetry field names and cardinality are reviewed like API contracts.
- Authorization headers, tokens, secrets, raw prompts, and unrestricted document content are denied fields.
- Audit events are application records, not a substitute for telemetry or vice versa.
- Readiness does not depend on an optional telemetry backend; export failures are bounded and observable.

## References

- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)
