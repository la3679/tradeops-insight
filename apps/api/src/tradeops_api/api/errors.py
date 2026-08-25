"""Stable public error contracts and exception translation."""

from collections.abc import Mapping

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field


class ErrorItem(BaseModel):
    """One bounded field or policy error."""

    model_config = ConfigDict(frozen=True)

    field: str | None = None
    reason: str


class ErrorBody(BaseModel):
    """Machine-readable error payload nested under the top-level envelope."""

    model_config = ConfigDict(frozen=True)

    code: str = Field(pattern=r"^[A-Z][A-Z0-9_]+$")
    message: str
    request_id: str
    details: tuple[ErrorItem, ...] = ()


class ErrorEnvelope(BaseModel):
    """Error response returned by every versioned API boundary."""

    model_config = ConfigDict(frozen=True)

    error: ErrorBody


class AppError(Exception):
    """Expected application error safe to expose at the HTTP boundary."""

    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int,
        details: tuple[ErrorItem, ...] = (),
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        self.headers = dict(headers or {})


def _request_id(request: Request) -> str:
    return str(getattr(request.state, "request_id", "unavailable"))


def _response(
    *,
    request: Request,
    status_code: int,
    code: str,
    message: str,
    details: tuple[ErrorItem, ...] = (),
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    envelope = ErrorEnvelope(
        error=ErrorBody(
            code=code,
            message=message,
            request_id=_request_id(request),
            details=details,
        )
    )
    return JSONResponse(
        status_code=status_code,
        content=envelope.model_dump(mode="json"),
        headers=dict(headers or {}),
    )


async def app_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Translate an expected application error without leaking internals."""

    if not isinstance(exc, AppError):  # defensive registration boundary
        raise exc
    return _response(
        request=request,
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details,
        headers=exc.headers,
    )


async def validation_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Normalize Pydantic/FastAPI validation failures."""

    if not isinstance(exc, RequestValidationError):  # defensive registration boundary
        raise exc
    details = tuple(
        ErrorItem(
            field=".".join(str(segment) for segment in error["loc"]),
            reason=str(error["type"]),
        )
        for error in exc.errors()
    )
    return _response(
        request=request,
        status_code=422,
        code="VALIDATION_ERROR",
        message="The request did not satisfy the API contract.",
        details=details,
    )


def install_exception_handlers(application: FastAPI) -> None:
    """Register stable application and validation exception handlers."""

    application.add_exception_handler(AppError, app_error_handler)
    application.add_exception_handler(RequestValidationError, validation_error_handler)
