# ADR-0004: Local-first retrieval behind typed ports

- **Status:** Accepted
- **Date:** 2026-08-24

## Context

The system needs reproducible retrieval over a small, versioned synthetic corpus. The initial release must run without a hosted account or model key, while leaving a credible boundary for a managed vector store later. Retrieval results are untrusted evidence candidates and must preserve source and version metadata.

## Decision

Define project-owned document, embedding, and vector-index ports. Use a local FAISS implementation for the default demo and tests. Persist a corpus manifest containing document ID, version, content digest, source type, license/provenance reference, chunking version, embedding-provider ID, embedding-model ID, dimensions, and index creation time.

Use a deterministic local embedding implementation for no-key tests and demonstrations. Optional OpenAI or other embedding adapters are configuration-selected, validate dimensions, and never run in offline CI. Retrieval returns typed candidates with stable chunk IDs and scores; the workflow separately applies relevance, citation, and refusal policy.

## Consequences

### Positive

- Clean clones can build and query a deterministic index offline.
- Provider and vector-store replacements do not enter domain rules.
- Indexes can be invalidated when content, chunking, or embeddings change.
- Citations can resolve to exact versioned chunks.

### Negative

- Local FAISS is process-local and unsuitable for distributed write coordination.
- Deterministic test embeddings do not model production semantic quality.
- Index lifecycle and compatibility metadata add implementation work.

## Guardrails

- Only approved synthetic or license-compatible documents enter the corpus.
- Index files are derived artifacts; the manifest and source documents are authoritative.
- Retrieved text is never interpreted as executable instruction.
- A score alone cannot authorize an action; missing or weak evidence triggers review or refusal.
