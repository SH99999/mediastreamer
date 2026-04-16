#!/usr/bin/env python3
"""
Detect whether ChatGPT artifacts are ready for Codex review/evaluation.
"""

from __future__ import annotations

from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[2]
WATCH_FILES = [
    REPO_ROOT / "exchange" / "chatgpt" / "audit_basis" / "current_audit_basis_v1.md",
]
WATCH_FILES.extend(sorted((REPO_ROOT / "exchange" / "chatgpt" / "inbox").glob("*__request_v*.md")))

STATUS_RE = re.compile(r"^status:\s*(.+)$", re.IGNORECASE | re.MULTILINE)


def extract_status(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = STATUS_RE.search(text)
    return m.group(1).strip().lower() if m else "missing"


def main() -> int:
    ready = []
    for path in WATCH_FILES:
        if not path.exists():
            continue
        status = extract_status(path)
        if status == "ready-for-codex":
            ready.append(path)

    if not ready:
        print("no-action: no file with status ready-for-codex")
        return 0

    print("action-required: codex-review")
    for path in ready:
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
