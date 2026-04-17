#!/usr/bin/env python3
"""Promote a governed live session artifact into a demand intake artifact."""

from __future__ import annotations

import argparse
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SESSIONS = REPO_ROOT / "exchange" / "chatgpt" / "sessions"
DEMANDS = REPO_ROOT / "exchange" / "chatgpt" / "demands"
DEMAND_TEMPLATE = DEMANDS / "TEMPLATE__intake_v1.md"
PROTOCOL_MAIN = REPO_ROOT / "exchange" / "chatgpt" / "protocol-main"
STATUS_RE = re.compile(r"^status:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
EVENT_RE = re.compile(r"^### event (\d+)$", re.MULTILINE)


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
        return ["- (missing in live session)"]

    out: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        out.append(line)
    return out or ["- (empty in live session)"]


def replace_status(text: str, new_status: str) -> str:
    if STATUS_RE.search(text):
        return STATUS_RE.sub(f"status: {new_status}", text, count=1)
    return f"status: {new_status}\n" + text


def next_event_id(text: str) -> int:
    found = [int(m.group(1)) for m in EVENT_RE.finditer(text)]
    return (max(found) + 1) if found else 1


def ensure_protocol(topic: str) -> Path:
    PROTOCOL_MAIN.mkdir(parents=True, exist_ok=True)
    protocol_path = PROTOCOL_MAIN / f"{topic}__protocol_v1.md"
    if protocol_path.exists():
        return protocol_path
    template_source = PROTOCOL_MAIN / "TEMPLATE__protocol_snapshot_v1.md"
    template = template_source.read_text(encoding="utf-8").replace("<topic>", topic)
    protocol_path.write_text(template + "\n", encoding="utf-8")
    return protocol_path


def append_protocol_event(topic: str, now_iso: str, live_path: Path, demand_path: Path) -> Path:
    protocol_path = ensure_protocol(topic)
    text = protocol_path.read_text(encoding="utf-8")
    event_id = next_event_id(text)
    event_block = "\n".join(
        [
            f"### event {event_id:03d}",
            f"- event_utc: {now_iso}",
            "- event_type: ship-to-codex-promotion",
            "- actor: codex",
            "- summary: promotion from live session to ready-for-codex demand intake completed",
            "- decisions:",
            "  1. owner-visible trigger remains `ship to codex`.",
            "- open_questions:",
            "  1. none recorded in this event.",
            "- risks_blockers:",
            "  1. none recorded in this event.",
            "- execution_requests:",
            "  1. execute demand on declared SI branch and prepare PR to main.",
            "- related_git_objects:",
            f"  - live_session: {live_path.relative_to(REPO_ROOT)}",
            f"  - demand_intake: {demand_path.relative_to(REPO_ROOT)}",
            "  - source_branch:",
            "  - source_pr_url:",
            "  - review_target_artifacts:",
            "",
        ]
    )
    if not text.endswith("\n"):
        text += "\n"
    text += event_block
    text = re.sub(r"^last_event_utc:\s*.*$", f"last_event_utc: {now_iso}", text, count=1, flags=re.MULTILINE)
    protocol_path.write_text(text, encoding="utf-8")
    return protocol_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--force", action="store_true", help="allow promotion even when live status is not chatok/live")
    parser.add_argument(
        "--ship-to-codex",
        action="store_true",
        help="owner-minimal handoff command; internalizes chatok and promotes to ready-for-codex",
    )
    parser.add_argument(
        "--publish-main-snapshot",
        action="store_true",
        help="publish canonical pickup snapshot under exchange/chatgpt/inbox-main/",
    )
    args = parser.parse_args()

    topic = slugify(args.topic)
    if not topic:
        raise SystemExit("topic must contain alphanumeric characters")

    live_path = SESSIONS / f"{topic}__live_v1.md"
    demand_path = DEMANDS / f"{topic}__intake_v1.md"

    if not live_path.exists():
        raise SystemExit(f"live session not found: {live_path.relative_to(REPO_ROOT)}")

    live_text = live_path.read_text(encoding="utf-8")
    live_status = extract_status(live_text)
    if live_status not in {"chatok", "live"} and not args.force:
        raise SystemExit("live session status must be live|chatok for promotion (or use --force)")
    if args.ship_to_codex and live_status == "live":
        live_text = replace_status(live_text, "chatok")
        live_status = "chatok"

    demand_template = DEMAND_TEMPLATE.read_text(encoding="utf-8")
    demand_text = demand_template.replace("<topic>", topic)

    mapped = {
        "## source/context": extract_section(live_text, "## source/context"),
        "## objective": extract_section(live_text, "## current objective"),
        "## locked decisions": extract_section(live_text, "## locked decisions so far"),
        "## open decisions": extract_section(live_text, "## open decisions"),
        "## required implementation": extract_section(live_text, "## active implementation asks"),
        "## risks": extract_section(live_text, "## active risks/blockers"),
        "## non-loss requirements": extract_section(live_text, "## non-loss requirements"),
    }

    lines = []
    demand_lines = demand_text.splitlines()
    i = 0
    while i < len(demand_lines):
        line = demand_lines[i]
        lines.append(line)
        if line.strip() in mapped:
            i += 1
            while i < len(demand_lines) and not demand_lines[i].startswith("## "):
                i += 1
            lines.extend(mapped[line.strip()])
            continue
        i += 1

    out = "\n".join(lines) + "\n"
    out = replace_status(out, "ready-for-codex")
    now = datetime.now(timezone.utc).isoformat()
    protocol_path = append_protocol_event(topic, now, live_path, demand_path)
    snapshot_path = ""
    if args.ship_to_codex or args.publish_main_snapshot:
        cmd = [
            "python3",
            str(REPO_ROOT / "tools" / "governance" / "chatgpt_publish_main_snapshot_v1.py"),
            "--topic",
            topic,
            "--demand-path",
            str(demand_path.relative_to(REPO_ROOT)),
            "--protocol-path",
            str(protocol_path.relative_to(REPO_ROOT)),
        ]
        if args.ship_to_codex:
            cmd.extend(["--execution-branch", f"si/{topic}-v1"])
        proc = subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True, check=True)
        for line in proc.stdout.splitlines():
            if line.startswith("main_inbox_snapshot="):
                snapshot_path = line.split("=", 1)[1].strip()
    out += (
        "\n## promotion metadata\n"
        f"- promoted_from_live: `{live_path.relative_to(REPO_ROOT)}`\n"
        f"- promoted_at_utc: `{now}`\n"
        "- codex_trigger: `ship-to-codex`\n"
        "- promotion_trigger: `chatok`\n"
        f"- materialized_protocol: `{protocol_path.relative_to(REPO_ROOT)}`\n"
        f"- main_inbox_snapshot: `{snapshot_path}`\n"
    )

    demand_path.write_text(out, encoding="utf-8")
    live_path.write_text(replace_status(live_text, "chatok"), encoding="utf-8")

    print(f"promoted: {live_path.relative_to(REPO_ROOT)} -> {demand_path.relative_to(REPO_ROOT)}")
    print(f"materialized_protocol={protocol_path.relative_to(REPO_ROOT)}")
    if snapshot_path:
        print(f"main_inbox_snapshot={snapshot_path}")
    print("demand_status=ready-for-codex")
    if args.ship_to_codex:
        print("owner_command=ship-to-codex")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
