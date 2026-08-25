"""Validate repository-local Markdown links without network access."""

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
missing: list[str] = []

for document in (ROOT / "docs").rglob("*.md"):
    for raw_target in LINK.findall(document.read_text(encoding="utf-8")):
        target = raw_target.split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        resolved = (document.parent / unquote(target)).resolve()
        if ROOT not in resolved.parents and resolved != ROOT:
            missing.append(f"{document.relative_to(ROOT)}: link escapes repository: {target}")
        elif not resolved.exists():
            missing.append(f"{document.relative_to(ROOT)}: missing {target}")

for document in ROOT.glob("*.md"):
    for raw_target in LINK.findall(document.read_text(encoding="utf-8")):
        target = raw_target.split("#", 1)[0]
        if target and "://" not in target and not (ROOT / unquote(target)).exists():
            missing.append(f"{document.name}: missing {target}")

if missing:
    raise SystemExit("\n".join(missing))
print("Documentation local links verified.")
