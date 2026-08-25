"""Domain-specific failure taxonomy."""


class DomainError(Exception):
    """Base class for expected domain failures."""


class DomainValidationError(DomainError, ValueError):
    """A constructed domain value violates a structural invariant."""

    def __init__(self, *, field: str, reason: str) -> None:
        super().__init__(f"{field}: {reason}")
        self.field = field
        self.reason = reason
