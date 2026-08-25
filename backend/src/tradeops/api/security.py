"""OIDC identity boundary and server-enforced role requirements."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Annotated, Protocol, cast

import jwt
from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

from tradeops.config import Settings


class Role(StrEnum):
    ANALYST = "analyst"
    REVIEWER = "reviewer"
    AUDITOR = "auditor"
    ADMINISTRATOR = "administrator"


@dataclass(frozen=True, slots=True)
class Principal:
    subject: str
    display_name: str
    role: Role


class TokenDecoder(Protocol):
    """Boundary for signature-validating bearer token decoders."""

    def decode(self, token: str) -> dict[str, object]: ...


class OidcTokenDecoder:
    """Validate RS256 access tokens against an OIDC issuer's JWKS."""

    def __init__(self, *, issuer: str, audience: str) -> None:
        self._issuer = issuer.rstrip("/")
        self._audience = audience
        self._jwks = PyJWKClient(f"{self._issuer}/protocol/openid-connect/certs", timeout=5)

    def decode(self, token: str) -> dict[str, object]:
        signing_key = self._jwks.get_signing_key_from_jwt(token)
        return cast(
            dict[str, object],
            jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self._audience,
                issuer=self._issuer,
                options={"require": ["exp", "iat", "sub", "iss", "aud"]},
            ),
        )


_bearer = HTTPBearer(auto_error=False)


def _principal_from_claims(claims: dict[str, object]) -> Principal:
    subject = claims.get("sub")
    display_name = claims.get("name") or claims.get("preferred_username") or subject
    realm_access = claims.get("realm_access")
    roles: object = realm_access.get("roles") if isinstance(realm_access, dict) else None
    role_names = (
        {role for role in roles if isinstance(role, str)} if isinstance(roles, list) else set()
    )
    mapped = next((role for role in Role if role.value in role_names), None)
    if not isinstance(subject, str) or not isinstance(display_name, str) or mapped is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Required role is absent."
        )
    return Principal(subject, display_name, mapped)


def current_principal(
    request: Request,
    x_demo_role: str | None = Header(default=None, alias="X-Demo-Role"),
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)] = None,
) -> Principal:
    """Resolve labelled local identities or a fully validated production token."""

    settings: Settings = request.app.state.settings
    if settings.environment == "production":
        if credentials is None or credentials.scheme.casefold() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="OIDC bearer authentication is required.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        decoder = cast(TokenDecoder, request.app.state.token_decoder)
        try:
            return _principal_from_claims(decoder.decode(credentials.credentials))
        except HTTPException:
            raise
        except jwt.PyJWTError as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer token validation failed.",
                headers={"WWW-Authenticate": "Bearer"},
            ) from error
    try:
        role = Role(x_demo_role or Role.ANALYST)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid demo role."
        ) from error
    return Principal(f"demo:{role}", f"Synthetic {role.value.title()}", role)


def require_roles(*allowed: Role) -> object:
    """Create a dependency that rejects principals outside an explicit role set."""

    def dependency(
        principal: Annotated[Principal, Depends(current_principal)],
    ) -> Principal:
        if principal.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This role is not permitted to perform the requested operation.",
            )
        return principal

    return dependency
