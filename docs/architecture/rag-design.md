# RAG ingestion and retrieval design

- **Owner:** AI and data maintainers
- **Purpose:** Define a reproducible evidence pipeline that treats retrieved content as untrusted data.

## Ingestion

1. Register an approved synthetic or license-compatible document and provenance.
2. Normalize Unicode, line endings, horizontal whitespace, and blank-line runs.
3. Split bounded overlapping windows, preferring paragraph and word boundaries.
4. Hash and deduplicate exact chunk content.
5. Assign stable `document:version:ordinal` chunk IDs and preserve type, jurisdiction, effective date, source locator, digest, and chunking version.
6. Embed through the configured embedding port and build an index with matching provider/model/dimension metadata.

The deterministic hashing embedder is the no-key default for tests and control-flow demonstrations. It is not a semantic-quality claim. Optional hosted embeddings must record provider/model/dimensions and rebuild an incompatible index.

## Retrieval and generation

Retrieval applies query embedding, candidate search, and metadata filtering before returning typed evidence candidates. Generation receives bounded snippets marked as untrusted evidence. Retrieved text cannot redefine instructions, select tools, reduce risk, or authorize an action.

An advisory proposal must cite exact chunk IDs. Missing, weak, stale, contradictory, or injection-like evidence routes to refusal or human review. Citation presence is necessary but not sufficient: later gates verify cited chunks exist and support the claimed action.

## Evaluation

Versioned cases measure Recall@k, MRR or nDCG, citation precision/completeness, groundedness, answer relevance, unsupported-claim rate, refusal/escalation correctness, latency, and optional-provider usage. Adversarial documents explicitly ask the model to ignore policy or call forbidden tools; passing behavior treats those strings only as evidence content.
