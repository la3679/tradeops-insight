"""Machine-checkable public and synthetic data provenance contracts."""

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime
from enum import StrEnum
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlparse

from tradeops_domain.errors import DomainValidationError

_SOURCE_ID = re.compile(r"^[a-z][a-z0-9-]{1,63}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class LicenseDecision(StrEnum):
    """Current project decision for a registered source."""

    APPROVED = "approved"
    CONDITIONAL = "conditional"
    RESTRICTED = "restricted"


def _required_string(data: Mapping[str, object], key: str, *, maximum: int = 500) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise DomainValidationError(field=key, reason=f"must contain 1 to {maximum} characters")
    return value


def _string_tuple(data: Mapping[str, object], key: str) -> tuple[str, ...]:
    value = data.get(key)
    if not isinstance(value, list) or not value or not all(isinstance(item, str) for item in value):
        raise DomainValidationError(field=key, reason="must be a nonempty string array")
    return tuple(value)


def _https_url(*, field: str, value: str) -> None:
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.hostname:
        raise DomainValidationError(field=field, reason="must be an absolute HTTPS URL")


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceRegistration:
    """Reviewed source, license, fields, and network boundary."""

    source_id: str
    name: str
    owner: str
    source_url: str
    terms_url: str
    license_id: str
    decision: LicenseDecision
    intended_fields: tuple[str, ...]
    allowed_hosts: tuple[str, ...]
    reviewed_on: date
    reviewer: str

    def __post_init__(self) -> None:
        if _SOURCE_ID.fullmatch(self.source_id) is None:
            raise DomainValidationError(field="source_id", reason="must be a lowercase slug")
        for field, value in (
            ("name", self.name),
            ("owner", self.owner),
            ("license_id", self.license_id),
            ("reviewer", self.reviewer),
        ):
            if not value.strip() or len(value) > 200:
                raise DomainValidationError(field=field, reason="must contain 1 to 200 characters")
        _https_url(field="source_url", value=self.source_url)
        _https_url(field="terms_url", value=self.terms_url)
        if not self.intended_fields:
            raise DomainValidationError(field="intended_fields", reason="must not be empty")
        if not self.allowed_hosts:
            raise DomainValidationError(field="allowed_hosts", reason="must not be empty")
        for host in self.allowed_hosts:
            if host != host.casefold() or "." not in host or "/" in host:
                raise DomainValidationError(
                    field="allowed_hosts", reason="contains an invalid host"
                )

    @classmethod
    def from_mapping(cls, data: Mapping[str, object]) -> "SourceRegistration":
        """Validate one untrusted JSON registry object."""

        try:
            decision = LicenseDecision(_required_string(data, "decision", maximum=20))
            reviewed_on = date.fromisoformat(_required_string(data, "reviewed_on", maximum=10))
        except ValueError as error:
            raise DomainValidationError(
                field="source_registry", reason="invalid enum or date"
            ) from error
        return cls(
            source_id=_required_string(data, "source_id", maximum=64),
            name=_required_string(data, "name", maximum=200),
            owner=_required_string(data, "owner", maximum=200),
            source_url=_required_string(data, "source_url"),
            terms_url=_required_string(data, "terms_url"),
            license_id=_required_string(data, "license_id", maximum=200),
            decision=decision,
            intended_fields=_string_tuple(data, "intended_fields"),
            allowed_hosts=_string_tuple(data, "allowed_hosts"),
            reviewed_on=reviewed_on,
            reviewer=_required_string(data, "reviewer", maximum=200),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class ProvenanceRecord:
    """Lineage attached to one fetched or generated artifact."""

    source_id: str
    source_locator: str
    retrieved_at: datetime
    content_sha256: str
    transformation_version: str
    synthetic: bool

    def __post_init__(self) -> None:
        if _SOURCE_ID.fullmatch(self.source_id) is None:
            raise DomainValidationError(field="source_id", reason="must be a lowercase slug")
        if not self.source_locator.strip() or len(self.source_locator) > 2_000:
            raise DomainValidationError(
                field="source_locator",
                reason="must contain 1 to 2000 characters",
            )
        if self.retrieved_at.tzinfo is None or self.retrieved_at.utcoffset() != UTC.utcoffset(
            self.retrieved_at
        ):
            raise DomainValidationError(field="retrieved_at", reason="must be timezone-aware UTC")
        if _SHA256.fullmatch(self.content_sha256) is None:
            raise DomainValidationError(field="content_sha256", reason="must be lowercase SHA-256")
        if not self.transformation_version.strip() or len(self.transformation_version) > 100:
            raise DomainValidationError(
                field="transformation_version",
                reason="must contain 1 to 100 characters",
            )


def content_digest(content: bytes) -> str:
    """Return the lowercase digest used by manifests and derived records."""

    return sha256(content).hexdigest()


def load_source_registry(path: Path) -> tuple[SourceRegistration, ...]:
    """Load and validate the complete source registry from UTF-8 JSON."""

    parsed = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(parsed, list) or not parsed:
        raise DomainValidationError(field="source_registry", reason="must be a nonempty array")
    registrations: list[SourceRegistration] = []
    for item in parsed:
        if not isinstance(item, dict) or not all(isinstance(key, str) for key in item):
            raise DomainValidationError(field="source_registry", reason="items must be objects")
        registrations.append(SourceRegistration.from_mapping(item))
    if len({registration.source_id for registration in registrations}) != len(registrations):
        raise DomainValidationError(
            field="source_registry", reason="source_id values must be unique"
        )
    return tuple(registrations)
