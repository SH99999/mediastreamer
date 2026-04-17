#!/usr/bin/env python3
"""Append compact event entries to a materialized chat protocol artifact."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parents[2]
SESSIONS = REPO_ROOT / "exchange" / "chatgpt" / "sessions"
TEMPLATE = SESSIONS / "TEMPLATE__protocol_v1.md"
EVENT_RE = re.compile(r"^### event (\d+)$", re.MULTILINE)


def slugify(value: str) -> str:
    out = "".join(c.lower() if c.isalnum() else "-" for c in value.strip())
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def next_event_id(text: str) -> int:
    found = [int(m.group(1)) for m in EVENT_RE.finditer(text)]
    return (max(found) + 1) if found else 1


def ensure_protocol(topic: str) -> Path:
    path = SESSIONS / f"{topic}__protocol_v1.md"
    if path.exists():
        return path
    text = TEMPLATE.read_text(encoding="utf-8").replace("<topic>", topic)
    path.write_text(text + "\n", encoding="utf-8")
    return path


def replace_scalar(text: str, key: str, value: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:\s*(.*)$", re.MULTILINE)
    if pattern.search(text):
        return pattern.sub(f"{key}: {value}", text, count=1)
    return f"{key}: {value}\n{text}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--event-type", required=True)
    parser.add_argument("--actor", default="codex")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--source-branch", default="")
    parser.add_argument("--source-pr-url", default="")
    parser.add_argument("--live-session", default="")
    parser.add_argument("--demand-intake", default="")
    args = parser.parse_args()

    topic = slugify(args.topic)
    if not topic:
        raise SystemExit("topic must contain alphanumeric characters")

    protocol_path = ensure_protocol(topic)
    text = protocol_path.read_text(encoding="utf-8")
    event_id = next_event_id(text)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    event_block = "\n".join(
        [
            f"### event {event_id:03d}",
            f"- event_utc: {now}",
            f"- event_type: {args.event_type}",
            f"- actor: {args.actor}",
            f"- summary: {args.summary}",
            "- decisions:",
            "  1.",
            "- open_questions:",
            "  1.",
            "- risks_blockers:",
            "  1.",
            "- execution_requests:",
            "  1.",
            "- related_git_objects:",
            f"  - live_session: {args.live_session or f'exchange/chatgpt/sessions/{topic}__live_v1.md'}",
            f"  - demand_intake: {args.demand_intake or f'exchange/chatgpt/demands/{topic}__intake_v1.md'}",
            f"  - source_branch: {args.source_branch}",
            f"  - source_pr_url: {args.source_pr_url}",
            "  - review_target_artifacts:",
            "",
        ]
    )

    if not text.endswith("\n"):
        text += "\n"
    text += event_block
    text = replace_scalar(text, "last_event_utc", now)
    protocol_path.write_text(text, encoding="utf-8")

    print(f"protocol_updated={protocol_path.relative_to(REPO_ROOT)}")
    print(f"event_id={event_id:03d}")
    print(f"event_utc={now}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
