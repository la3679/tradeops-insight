"""Cross-cutting HTTP boundary behavior."""

import re
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import RequestResponseEndpoint

REQUEST_ID_HEADER = "X-Request-ID"
_SAFE_REQUEST_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


def _resolve_request_id(candidate: str | None) -> str:
    if candidate is not None and _SAFE_REQUEST_ID.fullmatch(candidate):
        return candidate
    return str(uuid4())


def install_http_middleware(application: FastAPI) -> None:
    """Add request correlation without trusting arbitrary header content."""

    @application.middleware("http")
    async def correlate_request(request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = _resolve_request_id(request.headers.get(REQUEST_ID_HEADER))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response
