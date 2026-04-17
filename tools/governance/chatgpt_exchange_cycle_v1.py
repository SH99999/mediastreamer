#!/usr/bin/env python3
"""
Initialize a governed ChatGPT exchange cycle.
Creates request/response files from templates, optional demand intake,
and appends a stream entry.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
EXCHANGE_ROOT = REPO_ROOT / "exchange" / "chatgpt"
INBOX = EXCHANGE_ROOT / "inbox"
OUTBOX = EXCHANGE_ROOT / "outbox"
DEMANDS = EXCHANGE_ROOT / "demands"
SESSIONS = EXCHANGE_ROOT / "sessions"
STREAM = EXCHANGE_ROOT / "streams" / "stream_v1.md"
REQ_TEMPLATE = INBOX / "TEMPLATE__request_v1.md"
RESP_TEMPLATE = OUTBOX / "TEMPLATE__response_v1.md"
DEMAND_TEMPLATE = DEMANDS / "TEMPLATE__intake_v1.md"
LIVE_TEMPLATE = SESSIONS / "TEMPLATE__live_v1.md"


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
        default="chatgpt",
        choices=["codex", "chatgpt"],
        help="who initialized this cycle entry",
    )
    parser.add_argument(
        "--branch-plan",
        default="si/<topic>",
        help="planned implementation branch path",
    )
    parser.add_argument(
        "--create-demand",
        action="store_true",
        help="also create a demand intake artifact from template",
    )
    parser.add_argument(
        "--create-live",
        action="store_true",
        help="also create a live session artifact from template",
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

    live_rel = "n/a"
    if args.create_live:
        live_name = f"{topic}__live_v1.md"
        live_file = SESSIONS / live_name
        if live_file.exists():
            raise SystemExit("live session file already exists for topic")
        live_file.write_text(render_template(LIVE_TEMPLATE, topic, cycle_id), encoding="utf-8")
        live_rel = f"exchange/chatgpt/sessions/{live_name}"

    demand_rel = "n/a"
    if args.create_demand:
        demand_name = f"{topic}__intake_v1.md"
        demand_file = DEMANDS / demand_name
        if demand_file.exists():
            raise SystemExit("demand intake file already exists for topic")
        demand_file.write_text(render_template(DEMAND_TEMPLATE, topic, cycle_id), encoding="utf-8")
        demand_rel = f"exchange/chatgpt/demands/{demand_name}"

    ensure_stream()
    with STREAM.open("a", encoding="utf-8") as fh:
        fh.write(
            f"\n### {now.date()} / cycle {cycle_id} / {topic}\n"
            f"- actor: `{args.actor}`\n"
            f"- request: `exchange/chatgpt/inbox/{request_name}`\n"
            f"- response: `exchange/chatgpt/outbox/{response_name}`\n"
            f"- live session: `{live_rel}`\n"
            f"- demand: `{demand_rel}`\n"
            f"- branch plan: `{args.branch_plan}`\n"
            f"- owner decision needed: `accept | changes-requested | reject`\n"
            f"- status transition: `live -> ship-to-codex (internal chatok) -> ready-for-codex`\n"
        )

    print(f"initialized cycle: {cycle_id}")
    print(request_file.relative_to(REPO_ROOT))
    print(response_file.relative_to(REPO_ROOT))
    if args.create_live:
        print(live_rel)
    if args.create_demand:
        print(demand_rel)
    print(STREAM.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
