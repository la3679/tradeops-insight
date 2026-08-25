"""Allowlisted GLEIF LEI-record lookup adapter."""

import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlparse

import httpx

from tradeops_data.errors import (
    SourceNotFoundError,
    SourceResponseInvalidError,
    SourceTemporarilyUnavailableError,
)
from tradeops_data.provenance import ProvenanceRecord, content_digest
from tradeops_domain.errors import DomainValidationError
from tradeops_domain.models import CounterpartyReference, EntityStatus

_LEI = re.compile(r"^[A-Z0-9]{20}$")
_BASE_URL = "https://api.gleif.org/api/v1/lei-records"
_MAX_RESPONSE_BYTES = 1_000_000


def _lei_modulus(lei: str) -> int:
    expanded = "".join(str(int(character, 36)) for character in lei)
    remainder = 0
    for offset in range(0, len(expanded), 9):
        remainder = int(f"{remainder}{expanded[offset : offset + 9]}") % 97
    return remainder


def _validate_lei(lei: str) -> None:
    if _LEI.fullmatch(lei) is None or _lei_modulus(lei) != 1:
        raise DomainValidationError(field="lei", reason="must be a valid uppercase LEI")


def _object(value: object, *, field: str) -> Mapping[str, object]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise SourceResponseInvalidError(f"{field} must be an object")
    return value


def _string(data: Mapping[str, object], key: str, *, maximum: int = 500) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise SourceResponseInvalidError(f"{key} must be a bounded string")
    return value


@dataclass(frozen=True, slots=True, kw_only=True)
class GLEIFLookupResult:
    """Validated domain record plus exact response provenance."""

    counterparty: CounterpartyReference
    provenance: ProvenanceRecord


class GLEIFAdapter:
    """Fetch one LEI record through an injected bounded HTTP client."""

    def __init__(self, *, client: httpx.AsyncClient, base_url: str = _BASE_URL) -> None:
        parsed = urlparse(base_url)
        if parsed.scheme != "https" or parsed.hostname != "api.gleif.org":
            raise DomainValidationError(
                field="base_url",
                reason="must use the allowlisted api.gleif.org HTTPS host",
            )
        self._client = client
        self._base_url = base_url.rstrip("/")

    async def lookup(self, lei: str, *, retrieved_at: datetime) -> GLEIFLookupResult:
        """Return a validated counterparty record or a typed source error."""

        _validate_lei(lei)
        response = await self._client.get(
            f"{self._base_url}/{lei}",
            headers={"Accept": "application/vnd.api+json"},
            timeout=5.0,
        )
        if response.status_code == 404:
            raise SourceNotFoundError(f"LEI {lei} was not found")
        if response.status_code == 429 or response.status_code >= 500:
            raise SourceTemporarilyUnavailableError(
                f"GLEIF returned retryable status {response.status_code}"
            )
        if response.status_code != 200:
            raise SourceResponseInvalidError(f"GLEIF returned status {response.status_code}")
        if len(response.content) > _MAX_RESPONSE_BYTES:
            raise SourceResponseInvalidError("GLEIF response exceeded the size limit")

        try:
            body = _object(response.json(), field="response")
            data = _object(body.get("data"), field="data")
            attributes = _object(data.get("attributes"), field="attributes")
            entity = _object(attributes.get("entity"), field="entity")
            legal_name = _object(entity.get("legalName"), field="legalName")
            returned_lei = _string(attributes, "lei", maximum=20)
            name = _string(legal_name, "name", maximum=200)
            raw_status = _string(entity, "status", maximum=20)
        except (ValueError, TypeError) as error:
            raise SourceResponseInvalidError("GLEIF response was not valid JSON") from error

        if returned_lei != lei:
            raise SourceResponseInvalidError("GLEIF response LEI did not match the request")
        if raw_status not in {"ACTIVE", "INACTIVE"}:
            raise SourceResponseInvalidError("GLEIF entity status was unsupported")

        digest = content_digest(response.content)
        counterparty = CounterpartyReference(
            lei=returned_lei,
            legal_name=name,
            status=EntityStatus.ACTIVE if raw_status == "ACTIVE" else EntityStatus.INACTIVE,
            retrieved_at=retrieved_at,
            source_version=digest,
        )
        provenance = ProvenanceRecord(
            source_id="gleif-lei",
            source_locator=str(response.request.url),
            retrieved_at=retrieved_at,
            content_sha256=digest,
            transformation_version="gleif-adapter-v1",
            synthetic=False,
        )
        return GLEIFLookupResult(counterparty=counterparty, provenance=provenance)
