# ADR-0002: LangGraph for governed orchestration

- **Status:** Accepted
- **Date:** 2026-08-24

## Context

Exception investigation needs explicit state transitions, bounded retries, persistence, evidence gathering, refusal paths, and human review. A free-form agent loop would make control flow and resumption difficult to inspect. Hand-rolling a workflow runtime would recreate persistence and interrupt semantics without improving the product demonstration.

## Decision

Use LangGraph as an application-level orchestration runtime behind a project-owned port. Define typed graph state and named nodes for deterministic checks, retrieval, advisory drafting, policy, review interruption, approved application, and audit completion.

Compile production graphs with a durable checkpointer. Treat nodes as replayable: side effects are idempotent, carry idempotency keys, and occur only after policy and authorization. Human review uses explicit interrupts and resumes with validated commands. Graph state stores references to evidence and provider metadata rather than secrets or unrestricted raw context.

The deterministic mock provider is the default. LangGraph, model providers, and retrieval adapters do not become domain dependencies.

## Consequences

### Positive

- Control flow, state, pauses, retries, and terminal outcomes are inspectable.
- Persisted checkpoints support recovery and human-in-the-loop review.
- Deterministic node tests and replayable evaluation fixtures are practical.
- Provider choice remains separate from workflow policy.

### Negative

- Developers must understand checkpoint and replay semantics.
- Node changes require compatibility care for in-flight state.
- Side effects before a pause or retry can repeat unless designed idempotently.

## Guardrails

- No node exposes unrestricted shell, code execution, SQL, filesystem, network, or database mutation to a model.
- Interrupt ordering is stable within a released graph version.
- Workflow schema and prompt versions are recorded with each run.
- A missing citation, invalid structured output, exhausted retry, or uncertain policy routes to refusal or human review.

## References

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [LangGraph Graph API replay guidance](https://docs.langchain.com/oss/python/langgraph/graph-api)
