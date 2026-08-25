# ADR 0004: Offline retrieval and explicit agent graph

Status: Accepted — 2026-08-24

## Decision

Local and CI retrieval uses a deterministic signed hash embedding with a FAISS inner-product index. Production-capable embedding adapters may be configured later, but core behavior never requires an API key. Chunk metadata remains relational and citations always contain document and chunk IDs, title, source URL when present, and retrieval score.

The orchestration is a typed thirteen-node LangGraph rather than a generic agent loop. Deterministic validation gates model-assisted classification and drafting. Every material synthetic-state correction interrupts for a human decision, and only approve/edit routes reach the allowlisted executor. Provider fallback is explicitly labelled `mock-fallback`.

Retrieved text is untrusted evidence. Instruction-like content is cited for audit but forces escalation and cannot select tools, modify graph routing, or authorize an action.
