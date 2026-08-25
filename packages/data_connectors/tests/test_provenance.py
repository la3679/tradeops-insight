"""Machine-checkable provenance and source-registry tests."""

from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import pytest

from tradeops_data.provenance import (
    LicenseDecision,
    ProvenanceRecord,
    content_digest,
    load_source_registry,
)
from tradeops_domain.errors import DomainValidationError

ROOT = Path(__file__).parents[3]


def test_committed_source_registry_is_valid_and_unique() -> None:
    registrations = load_source_registry(ROOT / "data/provenance/sources.json")

    assert {source.source_id for source in registrations} == {"gleif-lei", "project-synthetic"}
    gleif = next(source for source in registrations if source.source_id == "gleif-lei")
    assert gleif.decision is LicenseDecision.APPROVED
    assert gleif.allowed_hosts == ("api.gleif.org",)


def test_content_digest_is_deterministic() -> None:
    assert content_digest(b"synthetic fixture\n") == content_digest(b"synthetic fixture\n")
    assert content_digest(b"synthetic fixture\n") != content_digest(b"synthetic fixture")


def test_provenance_record_requires_digest_and_utc() -> None:
    record = ProvenanceRecord(
        source_id="project-synthetic",
        source_locator="generator:seed=42",
        retrieved_at=datetime(2026, 8, 24, tzinfo=UTC),
        content_sha256=content_digest(b"demo"),
        transformation_version="generator-v1",
        synthetic=True,
    )

    with pytest.raises(DomainValidationError, match="content_sha256"):
        replace(record, content_sha256="not-a-digest")
    with pytest.raises(DomainValidationError, match="retrieved_at"):
        replace(record, retrieved_at=datetime(2026, 8, 24))  # noqa: DTZ001


def test_source_registry_rejects_insecure_url(tmp_path: Path) -> None:
    registry = tmp_path / "sources.json"
    registry.write_text(
        """[
          {
            "source_id": "unsafe-source",
            "name": "Unsafe",
            "owner": "Example",
            "source_url": "http://example.com/data",
            "terms_url": "https://example.com/terms",
            "license_id": "Example",
            "decision": "restricted",
            "intended_fields": ["none"],
            "allowed_hosts": ["example.com"],
            "reviewed_on": "2026-08-24",
            "reviewer": "Project maintainer"
          }
        ]""",
        encoding="utf-8",
    )

    with pytest.raises(DomainValidationError, match="source_url"):
        load_source_registry(registry)
