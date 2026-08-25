# RAG ingestion and retrieval design

Owner: AI/platform maintainer. Purpose: document grounding and adversarial controls.

Documents require type, version, jurisdiction, effective date, URL/provenance, and content hash. Normalized text is chunked with bounded overlap and deduplicated by SHA-256. The offline provider creates deterministic hash embeddings; FAISS inner-product search supports metadata filters and a minimum score.

Retrieval returns chunks and structured citations. Empty, weak, stale, contradictory, or instruction-like evidence escalates. Retrieved text is always untrusted data: phrases attempting to override prompts, call tools, or bypass approval are detected and cannot alter the graph. Index persistence is separated from relational metadata so an index can be rebuilt and versioned. Production providers must implement the same typed port, timeouts, budget limits, and provenance contract.
