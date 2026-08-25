import ast
from pathlib import Path

FORBIDDEN_DOMAIN_IMPORTS = frozenset(
    {"celery", "fastapi", "httpx", "langchain", "langgraph", "pydantic", "redis", "sqlalchemy"}
)


def test_domain_has_no_framework_or_infrastructure_imports() -> None:
    domain_root = Path(__file__).parents[1] / "src" / "tradeops" / "domain"
    violations: list[str] = []

    for path in domain_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            imports: list[str] = []
            if isinstance(node, ast.Import):
                imports = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports = [node.module]
            for imported in imports:
                if imported.partition(".")[0] in FORBIDDEN_DOMAIN_IMPORTS:
                    violations.append(f"{path.name}: {imported}")

    assert violations == []
