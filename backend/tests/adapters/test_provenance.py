"""Provenance fixture integrity tests."""

import json
from pathlib import Path

import pytest

from tradeops.adapters.provenance import ProvenanceError, validate_manifest


def test_committed_manifest_and_fixture_hashes_are_valid() -> None:
    root = Path(__file__).parents[3]

    entries = validate_manifest(root / "data/provenance/manifest.json", root)

    assert len(entries) == 3
    assert sum(entry.row_count for entry in entries) == 3
    assert all(entry.source_url.startswith("https://") for entry in entries)


@pytest.mark.parametrize(
    "payload, expected",
    [
        ({"sources": ["bad"]}, "object"),
        ({"sources": [{"row_count": "one"}]}, "required"),
        ([], "sources array"),
    ],
)
def test_manifest_rejects_malformed_entries(tmp_path: Path, payload: object, expected: str) -> None:
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ProvenanceError, match=expected):
        validate_manifest(manifest, tmp_path)


def test_manifest_rejects_missing_and_changed_fixture(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    entry = {
        "name": "sample",
        "dataset": "sample",
        "source_url": "https://example.test/data",
        "terms_url": "https://example.test/terms",
        "retrieved_at": "2026-01-01T00:00:00Z",
        "transformation": "test",
        "row_count": 1,
        "path": "sample.json",
        "sha256": "0" * 64,
    }
    manifest.write_text(json.dumps({"sources": [entry]}), encoding="utf-8")

    with pytest.raises(ProvenanceError, match="missing or outside"):
        validate_manifest(manifest, tmp_path)

    (tmp_path / "sample.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ProvenanceError, match="hash mismatch"):
        validate_manifest(manifest, tmp_path)
