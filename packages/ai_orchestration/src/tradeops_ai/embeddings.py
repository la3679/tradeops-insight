"""Embedding port and deterministic no-key implementation."""

import math
import re
from hashlib import sha256
from typing import Protocol

from tradeops_domain.errors import DomainValidationError

_TOKEN = re.compile(r"[\w-]+", re.UNICODE)


class EmbeddingProvider(Protocol):
    """Narrow batch embedding boundary."""

    @property
    def dimensions(self) -> int: ...

    @property
    def provider_id(self) -> str: ...

    async def embed(self, texts: tuple[str, ...]) -> tuple[tuple[float, ...], ...]: ...


class DeterministicEmbeddingProvider:
    """Hashing-vector baseline for tests and the no-key demo."""

    def __init__(self, *, dimensions: int = 64) -> None:
        if dimensions < 8 or dimensions > 4_096:
            raise DomainValidationError(field="dimensions", reason="must be between 8 and 4096")
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    @property
    def provider_id(self) -> str:
        return f"deterministic-hashing-v1:{self._dimensions}"

    async def embed(self, texts: tuple[str, ...]) -> tuple[tuple[float, ...], ...]:
        vectors: list[tuple[float, ...]] = []
        for text in texts:
            if not text.strip() or len(text) > 100_000:
                raise DomainValidationError(
                    field="texts",
                    reason="items must contain 1 to 100000 characters",
                )
            values = [0.0] * self._dimensions
            for token in _TOKEN.findall(text.casefold()):
                digest = sha256(token.encode()).digest()
                index = int.from_bytes(digest[:4]) % self._dimensions
                sign = 1.0 if digest[4] % 2 == 0 else -1.0
                values[index] += sign
            magnitude = math.sqrt(sum(value * value for value in values))
            if magnitude == 0:
                values[0] = 1.0
                magnitude = 1.0
            vectors.append(tuple(value / magnitude for value in values))
        return tuple(vectors)
