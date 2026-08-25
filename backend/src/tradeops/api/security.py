"""Local demo identity boundary and role requirements."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, status

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


def current_principal(
    request: Request,
    x_demo_role: str | None = Header(default=None, alias="X-Demo-Role"),
) -> Principal:
    """Resolve a labelled demo principal only outside production."""

    settings: Settings = request.app.state.settings
    if settings.environment == "production":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="OIDC bearer authentication is required in production.",
        )
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
