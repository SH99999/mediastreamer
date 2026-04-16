#!/usr/bin/env python3
"""
Build a single-file context bundle for ChatGPT GUI sessions without shell access.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
BUNDLE_PATH = REPO_ROOT / "exchange" / "chatgpt" / "bundles" / "current_context_bundle_v1.md"
FILES = [
    "docs/agents/chatgpt_start_prompt_git_exchange_v2.md",
    "exchange/chatgpt/PROTOCOL_v1.md",
    "exchange/chatgpt/audit_basis/current_audit_basis_v1.md",
    "exchange/chatgpt/streams/stream_v1.md",
    "exchange/chatgpt/inbox/TEMPLATE__request_v1.md",
    "exchange/chatgpt/inbox/round2-implementation-review__request_v1.md",
    "exchange/chatgpt/outbox/TEMPLATE__response_v1.md",
    "exchange/chatgpt/outbox/round2-implementation-review__response_v1.md",
    "exchange/chatgpt/outbox/TEMPLATE__consensus_owner_decision_v1.md",
    "exchange/chatgpt/outbox/TEMPLATE__owner_decision_packet_v1.md",
]


def main() -> int:
    BUNDLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    lines = [
        "# ChatGPT Context Bundle v1",
        "",
        f"_Generated: {now}_",
        "",
        "## Usage",
        "- Upload this single file in ChatGPT GUI to avoid multi-file permission prompts.",
        "- Keep branch policy from embedded start prompt.",
        "",
    ]
    for rel in FILES:
        path = REPO_ROOT / rel
        lines.extend([f"---", "", f"## File: `{rel}`", ""])
        if not path.exists():
            lines.append("_Missing in repository state._")
            lines.append("")
            continue
        lines.append("```md")
        lines.append(path.read_text(encoding="utf-8").rstrip())
        lines.append("```")
        lines.append("")

    BUNDLE_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(BUNDLE_PATH.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
