"""Document normalization, chunking, and deterministic embedding tests."""

from dataclasses import replace
from datetime import date

import pytest

from tradeops_ai.embeddings import DeterministicEmbeddingProvider
from tradeops_ai.retrieval import ChunkingConfig, RegisteredDocument, chunk_document, normalize_text
from tradeops_domain.errors import DomainValidationError


def _document(content: str) -> RegisteredDocument:
    return RegisteredDocument(
        document_id="RUNBOOK-DEMO-001",
        version="v1",
        title="Synthetic price exception runbook",
        document_type="runbook",
        jurisdiction="demo-us",
        effective_date=date(2026, 8, 1),
        source_locator="repo://data/policies/runbook-demo-001.md",
        content=content,
    )


def test_normalization_is_stable_and_preserves_paragraphs() -> None:
    content = "Price\t review\r\n\r\n\r\n  Confirm   evidence.  "

    assert normalize_text(content) == "Price review\n\nConfirm evidence."


def test_chunk_ids_and_digests_are_replayable() -> None:
    content = " ".join(f"synthetic-term-{index}" for index in range(200))
    config = ChunkingConfig(maximum_characters=240, overlap_characters=40)

    first = chunk_document(_document(content), config)
    second = chunk_document(_document(content), config)

    assert first == second
    assert len(first) > 2
    assert first[0].chunk_id == "RUNBOOK-DEMO-001:v1:0000"
    assert all(len(chunk.content) <= 240 for chunk in first)


def test_chunking_rejects_empty_normalized_content() -> None:
    with pytest.raises(DomainValidationError, match="content"):
        chunk_document(_document(" \n\t "))


@pytest.mark.anyio
async def test_deterministic_embeddings_are_normalized_and_replayable() -> None:
    provider = DeterministicEmbeddingProvider(dimensions=16)
    texts = ("price exception evidence", "settlement date evidence")

    first = await provider.embed(texts)
    second = await provider.embed(texts)

    assert first == second
    assert len(first) == 2
    assert all(len(vector) == 16 for vector in first)
    assert all(abs(sum(value * value for value in vector) - 1.0) < 1e-9 for vector in first)


@pytest.mark.anyio
async def test_embedding_rejects_blank_input() -> None:
    with pytest.raises(DomainValidationError, match="texts"):
        await DeterministicEmbeddingProvider().embed(("",))


@pytest.mark.parametrize("dimensions", [7, 4_097])
def test_embedding_dimensions_are_bounded(dimensions: int) -> None:
    with pytest.raises(DomainValidationError, match="dimensions"):
        DeterministicEmbeddingProvider(dimensions=dimensions)


def test_chunk_overlap_must_be_smaller_than_window() -> None:
    with pytest.raises(DomainValidationError, match="overlap_characters"):
        replace(ChunkingConfig(), overlap_characters=1_200)
