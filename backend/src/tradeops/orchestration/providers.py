"""Provider abstraction with explicit mock, failure, and circuit-breaker behavior."""

from dataclasses import dataclass
from typing import Protocol


class ProviderUnavailable(RuntimeError):
    """A configured provider cannot safely complete the requested operation."""


@dataclass(frozen=True, slots=True)
class Classification:
    label: str
    confidence: float
    provider: str
    model: str


@dataclass(frozen=True, slots=True)
class ResolutionDraft:
    summary: str
    action: str
    provider: str
    model: str


class ModelProvider(Protocol):
    """Only the bounded model capabilities used by the workflow."""

    @property
    def name(self) -> str: ...

    def classify(self, exception_type: str, evidence: tuple[str, ...]) -> Classification: ...

    def draft_resolution(
        self, exception_type: str, evidence: tuple[str, ...]
    ) -> ResolutionDraft: ...


class MockModelProvider:
    """Replayable zero-cost provider used by default and in deterministic evaluations."""

    name = "mock"

    def classify(self, exception_type: str, evidence: tuple[str, ...]) -> Classification:
        confidence = 0.92 if evidence else 0.0
        return Classification(exception_type, confidence, self.name, "mock-v1")

    def draft_resolution(self, exception_type: str, evidence: tuple[str, ...]) -> ResolutionDraft:
        if not evidence:
            raise ProviderUnavailable("mock provider requires evidence")
        return ResolutionDraft(
            summary=f"Review the deterministic {exception_type} evidence before correction.",
            action="propose_demo_field_correction",
            provider=self.name,
            model="mock-v1",
        )


class UnavailableModelProvider:
    """Test and operational adapter representing a configured provider outage."""

    name = "unavailable"

    def classify(self, exception_type: str, evidence: tuple[str, ...]) -> Classification:
        raise ProviderUnavailable("configured model provider is unavailable")

    def draft_resolution(self, exception_type: str, evidence: tuple[str, ...]) -> ResolutionDraft:
        raise ProviderUnavailable("configured model provider is unavailable")


class ResilientModelProvider:
    """Bounded circuit breaker that records deterministic fallback explicitly."""

    def __init__(self, primary: ModelProvider, *, failure_threshold: int = 2) -> None:
        if failure_threshold < 1:
            raise ValueError("failure_threshold must be positive")
        self._primary = primary
        self._fallback = MockModelProvider()
        self._threshold = failure_threshold
        self._failures = 0

    @property
    def name(self) -> str:
        return self._primary.name if self._failures < self._threshold else "mock-fallback"

    def classify(self, exception_type: str, evidence: tuple[str, ...]) -> Classification:
        if self._failures >= self._threshold:
            fallback = self._fallback.classify(exception_type, evidence)
            return Classification(
                fallback.label, fallback.confidence, "mock-fallback", fallback.model
            )
        try:
            return self._primary.classify(exception_type, evidence)
        except ProviderUnavailable:
            self._failures += 1
            fallback = self._fallback.classify(exception_type, evidence)
            return Classification(
                fallback.label, fallback.confidence, "mock-fallback", fallback.model
            )

    def draft_resolution(self, exception_type: str, evidence: tuple[str, ...]) -> ResolutionDraft:
        if self._failures >= self._threshold:
            fallback = self._fallback.draft_resolution(exception_type, evidence)
            return ResolutionDraft(
                fallback.summary, fallback.action, "mock-fallback", fallback.model
            )
        try:
            return self._primary.draft_resolution(exception_type, evidence)
        except ProviderUnavailable:
            self._failures += 1
            fallback = self._fallback.draft_resolution(exception_type, evidence)
            return ResolutionDraft(
                fallback.summary, fallback.action, "mock-fallback", fallback.model
            )
