"""FAISS metadata, search, filter, and persistence tests."""

from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from tradeops_ai.embeddings import DeterministicEmbeddingProvider
from tradeops_ai.retrieval import RegisteredDocument, TextChunk, chunk_document
from tradeops_ai.vector_index import FaissVectorIndex
from tradeops_domain.errors import DomainValidationError


def _chunk(document_id: str, content: str, *, document_type: str = "runbook") -> TextChunk:
    document = RegisteredDocument(
        document_id=document_id,
        version="v1",
        title=document_id,
        document_type=document_type,
        jurisdiction="demo-us",
        effective_date=date(2026, 8, 1),
        source_locator=f"repo://data/policies/{document_id}.md",
        content=content,
    )
    return chunk_document(document)[0]


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_search_returns_relevant_deterministic_candidate() -> None:
    chunks = (
        _chunk("PRICE-RUNBOOK", "price variance tolerance confirmation price review"),
        _chunk("SETTLEMENT-RUNBOOK", "settlement business day holiday calendar"),
        _chunk("ENTITY-RUNBOOK", "legal entity LEI name status"),
    )
    index = await FaissVectorIndex.build(chunks, DeterministicEmbeddingProvider())

    candidates = await index.search("price tolerance review", limit=2)

    assert candidates[0].chunk.document_id == "PRICE-RUNBOOK"
    assert candidates[0].score >= candidates[1].score


@pytest.mark.anyio
async def test_build_rejects_empty_chunk_set() -> None:
    with pytest.raises(DomainValidationError, match="chunks"):
        await FaissVectorIndex.build((), DeterministicEmbeddingProvider())


@pytest.mark.anyio
async def test_search_applies_metadata_filters() -> None:
    chunks = (
        _chunk("RUNBOOK", "price review", document_type="runbook"),
        _chunk("POLICY", "price review", document_type="policy"),
    )
    index = await FaissVectorIndex.build(chunks, DeterministicEmbeddingProvider())

    candidates = await index.search("price", document_type="policy")

    assert [candidate.chunk.document_id for candidate in candidates] == ["POLICY"]


@pytest.mark.anyio
async def test_saved_index_reloads_with_matching_manifest(tmp_path: Path) -> None:
    chunks = (_chunk("RUNBOOK", "price tolerance evidence"),)
    provider = DeterministicEmbeddingProvider(dimensions=16)
    index = await FaissVectorIndex.build(chunks, provider)
    index_path = tmp_path / "index.faiss"
    manifest_path = tmp_path / "index.json"
    index.save(index_path=index_path, manifest_path=manifest_path)

    loaded = FaissVectorIndex.load(
        index_path=index_path,
        manifest_path=manifest_path,
        chunks=chunks,
        embedding_provider=provider,
    )

    assert (await loaded.search("price"))[0].chunk.chunk_id == chunks[0].chunk_id


@pytest.mark.anyio
async def test_load_rejects_tampered_index(tmp_path: Path) -> None:
    chunks = (_chunk("RUNBOOK", "price tolerance evidence"),)
    provider = DeterministicEmbeddingProvider(dimensions=16)
    index = await FaissVectorIndex.build(chunks, provider)
    index_path = tmp_path / "index.faiss"
    manifest_path = tmp_path / "index.json"
    index.save(index_path=index_path, manifest_path=manifest_path)
    index_path.write_bytes(index_path.read_bytes() + b"tampered")

    with pytest.raises(DomainValidationError, match="digest"):
        FaissVectorIndex.load(
            index_path=index_path,
            manifest_path=manifest_path,
            chunks=chunks,
            embedding_provider=provider,
        )


@pytest.mark.anyio
async def test_search_limit_is_bounded() -> None:
    chunks = (_chunk("RUNBOOK", "price tolerance evidence"),)
    index = await FaissVectorIndex.build(chunks, DeterministicEmbeddingProvider())

    with pytest.raises(DomainValidationError, match="limit"):
        await index.search("price", limit=101)


@pytest.mark.anyio
async def test_load_rejects_chunk_mapping_change(tmp_path: Path) -> None:
    chunks = (_chunk("RUNBOOK", "price tolerance evidence"),)
    provider = DeterministicEmbeddingProvider(dimensions=16)
    index = await FaissVectorIndex.build(chunks, provider)
    index_path = tmp_path / "index.faiss"
    manifest_path = tmp_path / "index.json"
    index.save(index_path=index_path, manifest_path=manifest_path)

    with pytest.raises(DomainValidationError, match="chunk mapping"):
        FaissVectorIndex.load(
            index_path=index_path,
            manifest_path=manifest_path,
            chunks=(replace(chunks[0], content_sha256="0" * 64),),
            embedding_provider=provider,
        )


@pytest.mark.anyio
async def test_load_rejects_embedding_provider_change(tmp_path: Path) -> None:
    chunks = (_chunk("RUNBOOK", "price tolerance evidence"),)
    provider = DeterministicEmbeddingProvider(dimensions=16)
    index = await FaissVectorIndex.build(chunks, provider)
    index_path = tmp_path / "index.faiss"
    manifest_path = tmp_path / "index.json"
    index.save(index_path=index_path, manifest_path=manifest_path)

    with pytest.raises(DomainValidationError, match="provider"):
        FaissVectorIndex.load(
            index_path=index_path,
            manifest_path=manifest_path,
            chunks=chunks,
            embedding_provider=DeterministicEmbeddingProvider(dimensions=32),
        )
