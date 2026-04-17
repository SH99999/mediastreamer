#!/usr/bin/env python3
"""
Detect ChatGPT exchange artifacts that are ready for promotion or Codex execution.
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
        REPO_ROOT / "exchange" / "chatgpt" / "sessions",
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


def has_codex_trigger(path: Path) -> bool:
    text = path.read_text(encoding="utf-8").lower()
    return "codex_trigger: ship-to-codex" in text


def main() -> int:
    promote = []
    ready = []
    for path in watched_files():
        status = extract_status(path)
        if "/sessions/" in str(path) and status == "chatok":
            topic = path.stem.replace("__live_v1", "")
            demand = REPO_ROOT / "exchange" / "chatgpt" / "demands" / f"{topic}__intake_v1.md"
            if demand.exists() and extract_status(demand) == "ready-for-codex":
                pass
            else:
                promote.append(path)
        if status == "ready-for-codex":
            ready.append(path)

    if not ready and not promote:
        print("no-action: no artifact with status chatok or ready-for-codex")
        return 0

    if promote:
        print("action-required: ship-to-codex (internal chatok promotion)")
        for path in promote:
            print(path.relative_to(REPO_ROOT))

    if ready:
        print("action-required: codex-execution")
        for path in ready:
            print(path.relative_to(REPO_ROOT))
            if "/demands/" in str(path) and not has_codex_trigger(path):
                print(f"warning: missing codex_trigger marker in {path.relative_to(REPO_ROOT)}")

    if promote and not ready:
        print("next-step: run ship-to-codex promotion helper to set demand status ready-for-codex")
    elif ready:
        print("next-step: run codex execution from listed ready-for-codex artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
