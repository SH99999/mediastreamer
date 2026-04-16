#!/usr/bin/env python3
"""
Initialize a governed ChatGPT exchange cycle.
Creates request/response files from templates and appends a stream entry.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
EXCHANGE_ROOT = REPO_ROOT / "exchange" / "chatgpt"
INBOX = EXCHANGE_ROOT / "inbox"
OUTBOX = EXCHANGE_ROOT / "outbox"
STREAM = EXCHANGE_ROOT / "streams" / "stream_v1.md"
REQ_TEMPLATE = INBOX / "TEMPLATE__request_v1.md"
RESP_TEMPLATE = OUTBOX / "TEMPLATE__response_v1.md"


def slugify(value: str) -> str:
    out = "".join(c.lower() if c.isalnum() else "-" for c in value.strip())
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def ensure_stream() -> None:
    STREAM.parent.mkdir(parents=True, exist_ok=True)
    if STREAM.exists():
        return
    STREAM.write_text(
        "# ChatGPT Exchange Stream v1\n\n## Entries\n",
        encoding="utf-8",
    )


def render_template(path: Path, topic: str, cycle_id: str) -> str:
    content = path.read_text(encoding="utf-8")
    content = content.replace("<topic>", topic)
    return f"<!-- cycle_id: {cycle_id} -->\n" + content


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True, help="exchange topic label")
    parser.add_argument(
        "--actor",
        default="codex",
        choices=["codex", "chatgpt"],
        help="who initialized this cycle entry",
    )
    parser.add_argument(
        "--branch-plan",
        default="si/<topic>",
        help="planned implementation branch path",
    )
    args = parser.parse_args()

    topic = slugify(args.topic)
    if not topic:
        raise SystemExit("topic must contain alphanumeric characters")

    now = datetime.now(timezone.utc)
    cycle_id = now.strftime("%Y%m%d-%H%M%S")
    request_name = f"{topic}__request_v1.md"
    response_name = f"{topic}__response_v1.md"
    request_file = INBOX / request_name
    response_file = OUTBOX / response_name

    if request_file.exists() or response_file.exists():
        raise SystemExit("request/response file already exists for topic")

    request_file.write_text(render_template(REQ_TEMPLATE, topic, cycle_id), encoding="utf-8")
    response_file.write_text(render_template(RESP_TEMPLATE, topic, cycle_id), encoding="utf-8")

    ensure_stream()
    with STREAM.open("a", encoding="utf-8") as fh:
        fh.write(
            f"\n### {now.date()} / cycle {cycle_id} / {topic}\n"
            f"- actor: `{args.actor}`\n"
            f"- request: `exchange/chatgpt/inbox/{request_name}`\n"
            f"- response: `exchange/chatgpt/outbox/{response_name}`\n"
            f"- branch plan: `{args.branch_plan}`\n"
            f"- owner decision needed: `accept | changes-requested | reject`\n"
            f"- status: `initialized`\n"
        )

    print(f"initialized cycle: {cycle_id}")
    print(request_file.relative_to(REPO_ROOT))
    print(response_file.relative_to(REPO_ROOT))
    print(STREAM.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
