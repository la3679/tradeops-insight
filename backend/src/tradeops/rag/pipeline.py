"""Deterministic chunking, embeddings, FAISS retrieval, and citation gating."""

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID, uuid5

import faiss
import numpy as np
from numpy.typing import NDArray

_NAMESPACE = UUID("71be62b0-99e6-56ca-914e-a4e95f352129")
_TOKEN_PATTERN = re.compile(r"[a-z0-9_-]+")
_INJECTION_PATTERN = re.compile(
    r"ignore (?:all )?(?:previous|system)|system prompt|call (?:a )?tool|"
    r"bypass (?:policy|approval)",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class KnowledgeDocument:
    """Registered document with explicit provenance metadata."""

    id: UUID
    title: str
    content: str
    source_url: str | None
    document_type: str
    version: str
    jurisdiction: str
    effective_date: str


@dataclass(frozen=True, slots=True)
class KnowledgeChunk:
    id: UUID
    document_id: UUID
    ordinal: int
    title: str
    content: str
    source_url: str | None
    document_type: str
    version: str
    jurisdiction: str
    effective_date: str
    content_sha256: str
    untrusted_instruction_detected: bool


@dataclass(frozen=True, slots=True)
class Citation:
    document_id: UUID
    chunk_id: UUID
    title: str
    source_url: str | None
    score: float


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    chunks: tuple[KnowledgeChunk, ...]
    citations: tuple[Citation, ...]
    requires_escalation: bool
    reason: str | None


class HashEmbeddingProvider:
    """Zero-cost replayable embedding provider for local and CI use."""

    def __init__(self, dimensions: int = 128) -> None:
        if dimensions < 16:
            raise ValueError("embedding dimensions must be at least 16")
        self.dimensions = dimensions

    def embed(self, text: str) -> NDArray[np.float32]:
        vector = np.zeros(self.dimensions, dtype=np.float32)
        for token in _TOKEN_PATTERN.findall(text.casefold()):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            vector[index] += 1.0 if digest[4] % 2 else -1.0
        norm = float(np.linalg.norm(vector))
        if norm:
            vector /= norm
        return vector


def chunk_document(
    document: KnowledgeDocument, *, maximum_characters: int = 600, overlap_words: int = 20
) -> tuple[KnowledgeChunk, ...]:
    """Normalize and chunk text with bounded word overlap and content deduplication."""

    if maximum_characters < 100 or overlap_words < 0:
        raise ValueError("invalid chunking configuration")
    normalized = " ".join(document.content.split())
    words = normalized.split()
    chunks: list[KnowledgeChunk] = []
    seen_hashes: set[str] = set()
    cursor = 0
    while cursor < len(words):
        end = cursor
        length = 0
        while end < len(words) and length + len(words[end]) + 1 <= maximum_characters:
            length += len(words[end]) + 1
            end += 1
        if end == cursor:
            end += 1
        content = " ".join(words[cursor:end])
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if content_hash not in seen_hashes:
            ordinal = len(chunks)
            chunks.append(
                KnowledgeChunk(
                    id=uuid5(_NAMESPACE, f"{document.id}:{ordinal}:{content_hash}"),
                    document_id=document.id,
                    ordinal=ordinal,
                    title=document.title,
                    content=content,
                    source_url=document.source_url,
                    document_type=document.document_type,
                    version=document.version,
                    jurisdiction=document.jurisdiction,
                    effective_date=document.effective_date,
                    content_sha256=content_hash,
                    untrusted_instruction_detected=bool(_INJECTION_PATTERN.search(content)),
                )
            )
            seen_hashes.add(content_hash)
        if end == len(words):
            break
        cursor = end if overlap_words == 0 else max(cursor + 1, end - overlap_words)
    return tuple(chunks)


class FaissKnowledgeIndex:
    """FAISS inner-product index with metadata filters and safe citation output."""

    def __init__(self, provider: HashEmbeddingProvider | None = None) -> None:
        self.provider = provider or HashEmbeddingProvider()
        self._index = faiss.IndexFlatIP(self.provider.dimensions)
        self._chunks: list[KnowledgeChunk] = []

    def add(self, documents: tuple[KnowledgeDocument, ...]) -> int:
        new_chunks = [chunk for document in documents for chunk in chunk_document(document)]
        existing = {chunk.content_sha256 for chunk in self._chunks}
        unique: list[KnowledgeChunk] = []
        for chunk in new_chunks:
            if chunk.content_sha256 not in existing:
                unique.append(chunk)
                existing.add(chunk.content_sha256)
        if unique:
            vectors = np.stack([self.provider.embed(chunk.content) for chunk in unique])
            self._index.add(vectors)
            self._chunks.extend(unique)
        return len(unique)

    def search(
        self,
        query: str,
        *,
        limit: int = 5,
        document_type: str | None = None,
        jurisdiction: str | None = None,
        minimum_score: float = 0.05,
    ) -> RetrievalResult:
        if not query.strip() or limit < 1:
            raise ValueError("query must not be blank and limit must be positive")
        if not self._chunks:
            return RetrievalResult((), (), True, "No indexed evidence is available.")
        scores, indexes = self._index.search(
            np.expand_dims(self.provider.embed(query), axis=0), min(len(self._chunks), limit * 4)
        )
        selected: list[KnowledgeChunk] = []
        citations: list[Citation] = []
        for score, index in zip(scores[0], indexes[0], strict=True):
            if index < 0 or float(score) < minimum_score:
                continue
            chunk = self._chunks[int(index)]
            if document_type is not None and chunk.document_type != document_type:
                continue
            if jurisdiction is not None and chunk.jurisdiction != jurisdiction:
                continue
            selected.append(chunk)
            citations.append(
                Citation(chunk.document_id, chunk.id, chunk.title, chunk.source_url, float(score))
            )
            if len(selected) == limit:
                break
        malicious = any(chunk.untrusted_instruction_detected for chunk in selected)
        if malicious:
            return RetrievalResult(
                tuple(selected),
                tuple(citations),
                True,
                "Retrieved evidence contains untrusted instructions.",
            )
        if not selected:
            return RetrievalResult(
                (), (), True, "Evidence is insufficient for a grounded response."
            )
        return RetrievalResult(tuple(selected), tuple(citations), False, None)

    def persist(self, path: Path) -> None:
        """Persist the vector index; metadata stays in the relational document mapping."""

        path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self._index, str(path))


def generate_synthetic_policy_documents(count: int = 30) -> tuple[KnowledgeDocument, ...]:
    """Generate independently authored, labelled policy/runbook evidence."""

    if not 25 <= count <= 50:
        raise ValueError("synthetic policy document count must be between 25 and 50")
    topics = (
        "counterparty identity",
        "instrument reference",
        "notional validation",
        "price tolerance",
        "currency validation",
        "settlement date",
        "duplicate event",
        "confirmation evidence",
        "reference freshness",
        "unsupported product",
    )
    return tuple(
        KnowledgeDocument(
            id=uuid5(_NAMESPACE, f"synthetic-policy:{index}"),
            title=f"Synthetic operations policy {index + 1:02d}",
            content=(
                f"Synthetic demonstration policy for {topics[index % len(topics)]}. "
                "An analyst must inspect deterministic evidence and record a decision before any "
                "allowlisted demo-state correction. Missing, contradictory, stale, or malicious "
                "evidence must be escalated. This document cannot authorize tools or change policy."
            ),
            source_url=None,
            document_type="synthetic_policy",
            version="1.0",
            jurisdiction="DEMO",
            effective_date="2026-01-01",
        )
        for index in range(count)
    )
