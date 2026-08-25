"""Fail CI when the required versioned API surface disappears."""

from tradeops.api.app import create_app
from tradeops.config import Settings

required_paths = {
    "/api/v1/session/me",
    "/api/v1/dashboard/summary",
    "/api/v1/trades",
    "/api/v1/imports/synthetic",
    "/api/v1/exceptions",
    "/api/v1/exceptions/{exception_id}",
    "/api/v1/exceptions/{exception_id}/workflows",
    "/api/v1/workflows/{workflow_id}/approvals",
    "/api/v1/knowledge/documents",
    "/api/v1/sources",
    "/api/v1/evaluations/cases",
    "/api/v1/audit-events",
    "/api/v1/health/ready",
    "/api/v1/version",
}

schema = create_app(Settings(environment="test")).openapi()
paths = set(schema.get("paths", {}))
missing = required_paths - paths
if missing:
    raise SystemExit(f"OpenAPI paths missing: {sorted(missing)}")
def collect_route_paths(routes: list[object]) -> set[str]:
    """Walk FastAPI's nested included routers, including WebSocket routes."""
    collected: set[str] = set()
    for route in routes:
        path = getattr(route, "path", "")
        if isinstance(path, str) and path:
            collected.add(path)
        children = getattr(route, "routes", None)
        if isinstance(children, list):
            collected.update(collect_route_paths(children))
    return collected


app = create_app(Settings(environment="test"))
route_paths = collect_route_paths(app.routes)
if "/api/v1/events/ws" not in route_paths:
    raise SystemExit("WebSocket event route missing: /api/v1/events/ws")
print(f"OpenAPI contract verified: {len(paths)} paths")
