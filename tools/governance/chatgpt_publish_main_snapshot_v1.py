#!/usr/bin/env python3
"""Publish canonical append-only ChatGPT intake snapshots for Codex pickup on main."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parents[2]
DEMANDS = REPO_ROOT / "exchange" / "chatgpt" / "demands"
INBOX_MAIN = REPO_ROOT / "exchange" / "chatgpt" / "inbox-main"
PROTOCOL_MAIN = REPO_ROOT / "exchange" / "chatgpt" / "protocol-main"
STATUS_RE = re.compile(r"^status:\s*(.+)$", re.IGNORECASE | re.MULTILINE)


def slugify(value: str) -> str:
    out = "".join(c.lower() if c.isalnum() else "-" for c in value.strip())
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def extract_status(text: str) -> str:
    m = STATUS_RE.search(text)
    return m.group(1).strip().lower() if m else "missing"


def extract_section(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.strip().lower() == heading.lower():
            start = idx + 1
            break
    if start is None:
        return ["- (missing)"]
    out: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        out.append(line)
    return out or ["- (empty)"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--execution-branch", default="")
    parser.add_argument("--demand-path", default="")
    parser.add_argument("--protocol-path", default="")
    args = parser.parse_args()

    topic = slugify(args.topic)
    if not topic:
        raise SystemExit("topic must contain alphanumeric characters")

    demand_path = Path(args.demand_path) if args.demand_path else DEMANDS / f"{topic}__intake_v1.md"
    if not demand_path.is_absolute():
        demand_path = REPO_ROOT / demand_path
    if not demand_path.exists():
        raise SystemExit(f"demand file not found: {demand_path.relative_to(REPO_ROOT)}")

    demand_text = demand_path.read_text(encoding="utf-8")
    status = extract_status(demand_text)
    if status != "ready-for-codex":
        raise SystemExit(f"demand status must be ready-for-codex, got: {status}")

    protocol_path = Path(args.protocol_path) if args.protocol_path else PROTOCOL_MAIN / f"{topic}__protocol_v1.md"
    if not protocol_path.is_absolute():
        protocol_path = REPO_ROOT / protocol_path

    now = datetime.now(timezone.utc).replace(microsecond=0)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    now_iso = now.isoformat().replace("+00:00", "Z")
    snapshot_name = f"{stamp}__{topic}__intake_snapshot_v1.md"
    snapshot_path = INBOX_MAIN / snapshot_name
    INBOX_MAIN.mkdir(parents=True, exist_ok=True)

    execution_branch = args.execution_branch or f"si/{topic}-v1"

    lines = [
        f"# {topic} intake snapshot v1",
        "",
        "status: pickup-ready",
        "pickup_rule: main-inbox-v1",
        "snapshot_immutable: true",
        f"snapshot_id: {stamp}",
        f"created_at_utc: {now_iso}",
        "trigger_command: ship to codex",
        "",
        "## codex pickup contract",
        f"- execution_branch: {execution_branch}",
        "- pickup_ready_marker: status: pickup-ready",
        "- pickup_source: exchange/chatgpt/inbox-main/",
        "",
        "## source artifacts",
        f"- demand_intake: {demand_path.relative_to(REPO_ROOT)}",
        f"- materialized_protocol: {protocol_path.relative_to(REPO_ROOT)}",
        "",
        "## objective",
        *extract_section(demand_text, "## objective"),
        "",
        "## locked decisions",
        *extract_section(demand_text, "## locked decisions"),
        "",
        "## open decisions",
        *extract_section(demand_text, "## open decisions"),
        "",
        "## risks",
        *extract_section(demand_text, "## risks"),
        "",
        "## execution requests",
        *extract_section(demand_text, "## required implementation"),
        "",
        "## related git objects",
        f"- demand_path: {demand_path.relative_to(REPO_ROOT)}",
        f"- protocol_path: {protocol_path.relative_to(REPO_ROOT)}",
        f"- snapshot_path: {snapshot_path.relative_to(REPO_ROOT)}",
    ]
    snapshot_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"main_inbox_snapshot={snapshot_path.relative_to(REPO_ROOT)}")
    print("pickup_status=pickup-ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
