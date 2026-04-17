#!/usr/bin/env python3
"""
Detect ChatGPT exchange artifacts that are ready for Codex execution.
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
STATUS_RE = re.compile(r"^status:\s*(.+)$", re.IGNORECASE | re.MULTILINE)


def watched_files() -> Iterable[Path]:
    basis = REPO_ROOT / "exchange" / "chatgpt" / "audit_basis" / "current_audit_basis_v1.md"
    if basis.exists():
        yield basis

    patterns = [
        REPO_ROOT / "exchange" / "chatgpt" / "inbox",
        REPO_ROOT / "exchange" / "chatgpt" / "outbox",
        REPO_ROOT / "exchange" / "chatgpt" / "demands",
        REPO_ROOT / "exchange" / "chatgpt" / "ideas",
    ]
    for folder in patterns:
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.md")):
            if path.name.startswith("TEMPLATE__"):
                continue
            yield path


def extract_status(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = STATUS_RE.search(text)
    return m.group(1).strip().lower() if m else "missing"


def main() -> int:
    ready = []
    for path in watched_files():
        status = extract_status(path)
        if status == "ready-for-codex":
            ready.append(path)

    if not ready:
        print("no-action: no artifact with status ready-for-codex")
        return 0

    print("action-required: codex-execution")
    for path in ready:
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
