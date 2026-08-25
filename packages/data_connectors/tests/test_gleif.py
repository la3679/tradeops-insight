"""GLEIF adapter contract tests using recorded-shaped in-memory responses."""

from datetime import UTC, datetime

import httpx
import pytest

from tradeops_data.errors import (
    SourceNotFoundError,
    SourceResponseInvalidError,
    SourceTemporarilyUnavailableError,
)
from tradeops_data.gleif import GLEIFAdapter
from tradeops_domain.errors import DomainValidationError
from tradeops_domain.models import EntityStatus

RETRIEVED_AT = datetime(2026, 8, 24, 18, tzinfo=UTC)


def _lei(prefix: str = "DEMOLEI00000000001") -> str:
    expanded = "".join(str(int(character, 36)) for character in f"{prefix}00")
    return f"{prefix}{98 - (int(expanded) % 97):02d}"


def _payload(lei: str, *, status: str = "ACTIVE") -> dict[str, object]:
    return {
        "data": {
            "type": "lei-records",
            "id": lei,
            "attributes": {
                "lei": lei,
                "entity": {
                    "legalName": {"name": "Northstar Demo Capital"},
                    "status": status,
                },
            },
        }
    }


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_lookup_maps_active_entity_and_provenance() -> None:
    lei = _lei()

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.host == "api.gleif.org"
        assert request.headers["Accept"] == "application/vnd.api+json"
        return httpx.Response(200, json=_payload(lei), request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await GLEIFAdapter(client=client).lookup(lei, retrieved_at=RETRIEVED_AT)

    assert result.counterparty.status is EntityStatus.ACTIVE
    assert result.provenance.source_id == "gleif-lei"
    assert result.provenance.content_sha256 == result.counterparty.source_version


@pytest.mark.anyio
async def test_lookup_maps_inactive_status() -> None:
    lei = _lei()

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=_payload(lei, status="INACTIVE"), request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await GLEIFAdapter(client=client).lookup(lei, retrieved_at=RETRIEVED_AT)

    assert result.counterparty.status is EntityStatus.INACTIVE


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("status", "error_type"),
    [
        (404, SourceNotFoundError),
        (429, SourceTemporarilyUnavailableError),
        (503, SourceTemporarilyUnavailableError),
        (403, SourceResponseInvalidError),
    ],
)
async def test_http_statuses_map_to_typed_errors(
    status: int,
    error_type: type[Exception],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(error_type):
            await GLEIFAdapter(client=client).lookup(_lei(), retrieved_at=RETRIEVED_AT)


@pytest.mark.anyio
async def test_invalid_schema_fails_closed() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": {"attributes": {}}}, request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(SourceResponseInvalidError, match="entity"):
            await GLEIFAdapter(client=client).lookup(_lei(), retrieved_at=RETRIEVED_AT)


@pytest.mark.anyio
async def test_adapter_rejects_non_allowlisted_base_url() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError(f"unexpected request: {request.url}")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(DomainValidationError, match="base_url"):
            GLEIFAdapter(client=client, base_url="https://example.com/lei")


@pytest.mark.anyio
async def test_adapter_rejects_invalid_lei_before_request() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError(f"unexpected request: {request.url}")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(DomainValidationError, match="lei"):
            await GLEIFAdapter(client=client).lookup("not-a-lei", retrieved_at=RETRIEVED_AT)
