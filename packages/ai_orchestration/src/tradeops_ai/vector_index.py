"""Local FAISS cosine-similarity index with validated metadata mapping."""

import json
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from pathlib import Path
from typing import Any

import faiss
import numpy as np

from tradeops_ai.embeddings import EmbeddingProvider
from tradeops_ai.retrieval import TextChunk
from tradeops_domain.errors import DomainValidationError


@dataclass(frozen=True, slots=True, kw_only=True)
class SearchCandidate:
    """One scored, metadata-resolved retrieval result."""

    chunk: TextChunk
    score: float


class FaissVectorIndex:
    """Small local index; writes are rebuilt rather than coordinated across processes."""

    def __init__(
        self,
        *,
        index: Any,
        chunks: tuple[TextChunk, ...],
        embedding_provider: EmbeddingProvider,
    ) -> None:
        if index.d != embedding_provider.dimensions:
            raise DomainValidationError(field="index", reason="embedding dimensions do not match")
        if index.ntotal != len(chunks):
            raise DomainValidationError(field="index", reason="chunk mapping count does not match")
        self._index = index
        self._chunks = chunks
        self._embedding_provider = embedding_provider

    @classmethod
    async def build(
        cls,
        chunks: tuple[TextChunk, ...],
        embedding_provider: EmbeddingProvider,
    ) -> "FaissVectorIndex":
        if not chunks:
            raise DomainValidationError(field="chunks", reason="must not be empty")
        vectors = await embedding_provider.embed(tuple(chunk.content for chunk in chunks))
        matrix = np.asarray(vectors, dtype=np.float32)
        if matrix.shape != (len(chunks), embedding_provider.dimensions):
            raise DomainValidationError(field="embeddings", reason="returned unexpected dimensions")
        faiss.normalize_L2(matrix)
        index = faiss.IndexFlatIP(embedding_provider.dimensions)
        index.add(matrix)
        return cls(index=index, chunks=chunks, embedding_provider=embedding_provider)

    async def search(
        self,
        query: str,
        *,
        limit: int = 5,
        document_type: str | None = None,
        jurisdiction: str | None = None,
        effective_on: date | None = None,
    ) -> tuple[SearchCandidate, ...]:
        if limit < 1 or limit > 100:
            raise DomainValidationError(field="limit", reason="must be between 1 and 100")
        vector = await self._embedding_provider.embed((query,))
        matrix = np.asarray(vector, dtype=np.float32)
        faiss.normalize_L2(matrix)
        scores, positions = self._index.search(matrix, len(self._chunks))
        candidates: list[SearchCandidate] = []
        for score, position in zip(scores[0], positions[0], strict=True):
            if position < 0:
                continue
            chunk = self._chunks[int(position)]
            if document_type is not None and chunk.document_type != document_type:
                continue
            if jurisdiction is not None and chunk.jurisdiction != jurisdiction:
                continue
            if (
                effective_on is not None
                and chunk.effective_date is not None
                and chunk.effective_date > effective_on
            ):
                continue
            candidates.append(SearchCandidate(chunk=chunk, score=float(score)))
            if len(candidates) == limit:
                break
        return tuple(candidates)

    def save(self, *, index_path: Path, manifest_path: Path) -> None:
        """Persist derived index bytes and the exact chunk/provider mapping."""

        faiss.write_index(self._index, str(index_path))
        index_digest = sha256(index_path.read_bytes()).hexdigest()
        manifest = {
            "format_version": "faiss-manifest-v1",
            "provider_id": self._embedding_provider.provider_id,
            "dimensions": self._embedding_provider.dimensions,
            "index_sha256": index_digest,
            "chunks": [
                {"chunk_id": chunk.chunk_id, "content_sha256": chunk.content_sha256}
                for chunk in self._chunks
            ],
        }
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    @classmethod
    def load(
        cls,
        *,
        index_path: Path,
        manifest_path: Path,
        chunks: tuple[TextChunk, ...],
        embedding_provider: EmbeddingProvider,
    ) -> "FaissVectorIndex":
        """Load only when bytes, provider, dimensions, and chunk mapping match."""

        raw: object = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise DomainValidationError(field="manifest", reason="must be an object")
        expected_chunks = [
            {"chunk_id": chunk.chunk_id, "content_sha256": chunk.content_sha256} for chunk in chunks
        ]
        if raw.get("provider_id") != embedding_provider.provider_id:
            raise DomainValidationError(
                field="manifest", reason="embedding provider does not match"
            )
        if raw.get("dimensions") != embedding_provider.dimensions:
            raise DomainValidationError(
                field="manifest", reason="embedding dimensions do not match"
            )
        if raw.get("chunks") != expected_chunks:
            raise DomainValidationError(field="manifest", reason="chunk mapping does not match")
        if raw.get("index_sha256") != sha256(index_path.read_bytes()).hexdigest():
            raise DomainValidationError(field="manifest", reason="index digest does not match")
        return cls(
            index=faiss.read_index(str(index_path)),
            chunks=chunks,
            embedding_provider=embedding_provider,
        )
