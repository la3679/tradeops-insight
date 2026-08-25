"""Versioned document normalization and deterministic chunk construction."""

import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from hashlib import sha256

from tradeops_domain.errors import DomainValidationError

_WHITESPACE = re.compile(r"[ \t]+")
_BREAKS = re.compile(r"\n{3,}")


@dataclass(frozen=True, slots=True, kw_only=True)
class RegisteredDocument:
    """Approved bounded source document before chunking."""

    document_id: str
    version: str
    title: str
    document_type: str
    jurisdiction: str | None
    effective_date: date | None
    source_locator: str
    content: str

    def __post_init__(self) -> None:
        for field, value, maximum in (
            ("document_id", self.document_id, 100),
            ("version", self.version, 100),
            ("title", self.title, 500),
            ("document_type", self.document_type, 50),
            ("source_locator", self.source_locator, 2_000),
            ("content", self.content, 1_000_000),
        ):
            if not value.strip() or len(value) > maximum:
                raise DomainValidationError(
                    field=field,
                    reason=f"must contain 1 to {maximum} characters",
                )


@dataclass(frozen=True, slots=True, kw_only=True)
class ChunkingConfig:
    """Versioned character window with bounded overlap."""

    maximum_characters: int = 1_200
    overlap_characters: int = 150
    version: str = "characters-v1"

    def __post_init__(self) -> None:
        if self.maximum_characters < 200 or self.maximum_characters > 8_000:
            raise DomainValidationError(
                field="maximum_characters",
                reason="must be between 200 and 8000",
            )
        if self.overlap_characters < 0 or self.overlap_characters >= self.maximum_characters:
            raise DomainValidationError(
                field="overlap_characters",
                reason="must be nonnegative and smaller than maximum_characters",
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class TextChunk:
    """Stable citation and embedding unit."""

    chunk_id: str
    document_id: str
    document_version: str
    ordinal: int
    content: str
    content_sha256: str
    title: str
    document_type: str
    jurisdiction: str | None
    effective_date: date | None
    source_locator: str
    chunking_version: str


def normalize_text(content: str) -> str:
    """Normalize Unicode, line endings, horizontal whitespace, and blank runs."""

    normalized = unicodedata.normalize("NFKC", content).replace("\r\n", "\n").replace("\r", "\n")
    normalized = "\n".join(_WHITESPACE.sub(" ", line).strip() for line in normalized.splitlines())
    return _BREAKS.sub("\n\n", normalized).strip()


def _window_end(content: str, start: int, maximum: int) -> int:
    hard_end = min(len(content), start + maximum)
    if hard_end == len(content):
        return hard_end
    break_at = content.rfind("\n\n", start, hard_end)
    if break_at <= start:
        break_at = content.rfind(" ", start, hard_end)
    return break_at if break_at > start else hard_end


def chunk_document(
    document: RegisteredDocument,
    config: ChunkingConfig | None = None,
) -> tuple[TextChunk, ...]:
    """Create stable, overlapping chunks and remove duplicate content windows."""

    resolved = config or ChunkingConfig()
    content = normalize_text(document.content)
    if not content:
        raise DomainValidationError(field="content", reason="normalization produced empty text")

    chunks: list[TextChunk] = []
    seen_digests: set[str] = set()
    start = 0
    while start < len(content):
        end = _window_end(content, start, resolved.maximum_characters)
        window = content[start:end].strip()
        digest = sha256(window.encode()).hexdigest()
        if digest not in seen_digests:
            ordinal = len(chunks)
            chunks.append(
                TextChunk(
                    chunk_id=f"{document.document_id}:{document.version}:{ordinal:04d}",
                    document_id=document.document_id,
                    document_version=document.version,
                    ordinal=ordinal,
                    content=window,
                    content_sha256=digest,
                    title=document.title,
                    document_type=document.document_type,
                    jurisdiction=document.jurisdiction,
                    effective_date=document.effective_date,
                    source_locator=document.source_locator,
                    chunking_version=resolved.version,
                )
            )
            seen_digests.add(digest)
        if end == len(content):
            break
        start = max(start + 1, end - resolved.overlap_characters)

    return tuple(chunks)
