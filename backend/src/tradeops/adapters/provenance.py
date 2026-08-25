"""Offline provenance-manifest validation for committed public-data fixtures."""

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


class ProvenanceError(ValueError):
    """Raised when a manifest is malformed or a fixture hash no longer matches."""


@dataclass(frozen=True, slots=True)
class ProvenanceEntry:
    name: str
    dataset: str
    source_url: str
    terms_url: str
    retrieved_at: str
    transformation: str
    row_count: int
    path: str
    sha256: str


def _entry(value: object) -> ProvenanceEntry:
    if not isinstance(value, dict):
        raise ProvenanceError("every source entry must be an object")
    required = {
        "name",
        "dataset",
        "source_url",
        "terms_url",
        "retrieved_at",
        "transformation",
        "path",
        "sha256",
    }
    if not required.issubset(value) or not isinstance(value.get("row_count"), int):
        raise ProvenanceError("source entry is missing required provenance fields")
    if not all(isinstance(value[key], str) and value[key] for key in required):
        raise ProvenanceError("provenance text fields must be non-empty strings")
    return ProvenanceEntry(
        name=value["name"],
        dataset=value["dataset"],
        source_url=value["source_url"],
        terms_url=value["terms_url"],
        retrieved_at=value["retrieved_at"],
        transformation=value["transformation"],
        row_count=value["row_count"],
        path=value["path"],
        sha256=value["sha256"],
    )


def validate_manifest(manifest_path: Path, repository_root: Path) -> tuple[ProvenanceEntry, ...]:
    """Validate required metadata, repository-contained paths, and SHA-256 hashes."""

    raw: object = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("sources"), list):
        raise ProvenanceError("manifest must contain a sources array")
    entries = tuple(_entry(value) for value in raw["sources"])
    resolved_root = repository_root.resolve()
    for entry in entries:
        fixture = (resolved_root / entry.path).resolve()
        if not fixture.is_relative_to(resolved_root) or not fixture.is_file():
            raise ProvenanceError(
                f"fixture path is missing or outside the repository: {entry.path}"
            )
        actual = hashlib.sha256(fixture.read_bytes()).hexdigest()
        if actual != entry.sha256:
            raise ProvenanceError(f"fixture hash mismatch: {entry.path}")
    return entries
