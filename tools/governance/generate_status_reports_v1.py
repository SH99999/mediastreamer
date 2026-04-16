#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re


@dataclass
class Report:
    slug: str
    title: str
    body: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section_bullets(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    out = []
    capture = False
    heading_prefix = f"## {heading}"
    for line in lines:
      if line.startswith("## ") and line.strip() == heading_prefix:
        capture = True
        continue
      if capture and line.startswith("## "):
        break
      if capture and line.lstrip().startswith("-"):
        out.append(line.lstrip()[1:].strip())
    return out


def status_from_component(component: str, current_state_path: Path, stream_path: Path) -> Report:
    cs = read(current_state_path)
    lifecycle = section_bullets(cs, "Lifecycle status")[:6]
    gaps = section_bullets(cs, "Current gaps")[:4]
    next_actions = section_bullets(cs, "Repo-normalized next action")[:3]

    body = "\n".join([
        f"# Status {component}",
        "",
        f"_Generated: {datetime.now(timezone.utc).isoformat()}_",
        "",
        "## Quick summary",
        *(f"- {i}" for i in lifecycle),
        "",
        "## Main open points",
        *(f"- {i}" for i in gaps),
        "",
        "## Next actions",
        *(f"- {i}" for i in next_actions),
        "",
        "## Sources",
        f"- [Current state]({current_state_path.as_posix()})",
        f"- [Stream]({stream_path.as_posix()})",
        "",
        "## Visual snapshot",
        "```mermaid",
        "pie",
        "    title Lifecycle snapshot",
        f"    \"lifecycle entries\" : {len(lifecycle)}",
        f"    \"main gaps\" : {len(gaps)}",
        f"    \"next actions\" : {len(next_actions)}",
        "```",
        "",
    ])
    return Report(component.lower(), f"Status {component}", body)


def governance_status_report(si_status_path: Path) -> Report:
    text = read(si_status_path)
    works = []
    partial = []
    broken = []
    mode = None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("- what currently works:"):
            mode = "works"
            continue
        if s.startswith("- what partially works:"):
            mode = "partial"
            continue
        if s.startswith("- what is broken:"):
            mode = "broken"
            continue
        if s.startswith("- what was tested:"):
            mode = None
        if mode and s.startswith("-"):
            value = s[1:].strip()
            if mode == "works":
                works.append(value)
            elif mode == "partial":
                partial.append(value)
            elif mode == "broken":
                broken.append(value)

    body = "\n".join([
        "# Status Governance",
        "",
        f"_Generated: {datetime.now(timezone.utc).isoformat()}_",
        "",
        "## Quick summary",
        *(f"- {w}" for w in works[:6]),
        "",
        "## Partial",
        *(f"- {p}" for p in partial[:4]),
        "",
        "## Blockers",
        *(f"- {b}" for b in broken[:4]),
        "",
        "## Sources",
        f"- [SI status]({si_status_path.as_posix()})",
        "",
        "## Visual snapshot",
        "```mermaid",
        "xychart-beta",
        "    title \"Governance health buckets\"",
        "    x-axis [\"works\", \"partial\", \"broken\"]",
        f"    y-axis \"Count\" 0 --> {max(3, len(works)+len(partial)+len(broken))}",
        f"    bar [{len(works)}, {len(partial)}, {len(broken)}]",
        "```",
        "",
    ])
    return Report("governance", "Status Governance", body)


def ui_status_report(ui_stream_path: Path) -> Report:
    text = read(ui_stream_path)
    entries = [ln.strip()[2:].strip() for ln in text.splitlines() if ln.strip().startswith("-")]
    recent = entries[-6:]
    body = "\n".join([
        "# Status UI",
        "",
        f"_Generated: {datetime.now(timezone.utc).isoformat()}_",
        "",
        "## Recent governance entries",
        *(f"- {r}" for r in recent),
        "",
        "## Source",
        f"- [UI/GUI stream]({ui_stream_path.as_posix()})",
        "",
        "## Visual snapshot",
        "```mermaid",
        "pie",
        "    title UI governance stream",
        f"    \"entries sampled\" : {len(recent)}",
        f"    \"total entries\" : {len(entries)}",
        "```",
        "",
    ])
    return Report("ui", "Status UI", body)


def decisions_report(decisions_path: Path) -> Report:
    text = read(decisions_path)
    ids = re.findall(r"^###\s+(DEC-[^\n]+)", text, flags=re.MULTILINE)
    locked = len(re.findall(r"^- Status:\s*locked", text, flags=re.MULTILINE))
    body = "\n".join([
        "# Status Decisions",
        "",
        f"_Generated: {datetime.now(timezone.utc).isoformat()}_",
        "",
        "## Quick summary",
        f"- total decision entries: {len(ids)}",
        f"- locked decisions: {locked}",
        "",
        "## Recent decision IDs",
        *(f"- {d}" for d in ids[-8:]),
        "",
        "## Source",
        f"- [SI decisions]({decisions_path.as_posix()})",
        "",
        "## Visual snapshot",
        "```mermaid",
        "xychart-beta",
        "    title \"Decisions\"",
        "    x-axis [\"total\", \"locked\"]",
        f"    y-axis \"Count\" 0 --> {max(5, len(ids))}",
        f"    bar [{len(ids)}, {locked}]",
        "```",
        "",
    ])
    return Report("decisions", "Status Decisions", body)


def blocker_report(si_status_path: Path) -> Report:
    text = read(si_status_path)
    broken = []
    open_decisions = []
    mode = None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("- what is broken:"):
            mode = "broken"
            continue
        if s.startswith("## 5. Open Decisions"):
            mode = "open"
            continue
        if s.startswith("## 6."):
            mode = None
        if mode == "broken" and s.startswith("-"):
            broken.append(s[1:].strip())
        if mode == "open" and s.startswith("-"):
            open_decisions.append(s[1:].strip())

    body = "\n".join([
        "# Status Blocker",
        "",
        f"_Generated: {datetime.now(timezone.utc).isoformat()}_",
        "",
        "## Active broken points",
        *(f"- {b}" for b in broken),
        "",
        "## Open decision blockers",
        *(f"- {o}" for o in open_decisions),
        "",
        "## Source",
        f"- [SI status]({si_status_path.as_posix()})",
        "",
        "## Visual snapshot",
        "```mermaid",
        "pie",
        "    title Blocker buckets",
        f"    \"broken\" : {len(broken)}",
        f"    \"open decisions\" : {len(open_decisions)}",
        "```",
        "",
    ])
    return Report("blocker", "Status Blocker", body)


def write_report(base: Path, report: Report):
    path = base / f"{report.slug}.md"
    path.write_text(report.body, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate prompt-ready status reports with clickable links and visuals.")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--out-dir", default="reports/status", help="Output directory for generated markdown reports")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    out = root / args.out_dir
    out.mkdir(parents=True, exist_ok=True)

    reports = [
        status_from_component(
            "Tuner",
            root / "journals/scale-radio-tuner/current_state_v2.md",
            root / "journals/scale-radio-tuner/stream_v2.md",
        ),
        governance_status_report(root / "journals/system-integration-normalization/STATUS_system_integration_normalization_v8.md"),
        ui_status_report(root / "journals/system-integration-normalization/ui_gui_stream_v1.md"),
        status_from_component(
            "Bridge",
            root / "journals/scale-radio-bridge/current_state_v1.md",
            root / "journals/scale-radio-bridge/stream_v1.md",
        ),
        decisions_report(root / "journals/system-integration-normalization/DECISIONS_system_integration_normalization_v9.md"),
        blocker_report(root / "journals/system-integration-normalization/STATUS_system_integration_normalization_v8.md"),
    ]

    for r in reports:
        write_report(out, r)

    index_lines = [
        "# Status Reports Index v1",
        "",
        f"_Generated: {datetime.now(timezone.utc).isoformat()}_",
        "",
        "Prompt aliases:",
        "- `status tuner` -> [Status Tuner](./tuner.md)",
        "- `status governance` -> [Status Governance](./governance.md)",
        "- `status ui` -> [Status UI](./ui.md)",
        "- `status bridge` -> [Status Bridge](./bridge.md)",
        "- `status decisions` -> [Status Decisions](./decisions.md)",
        "- `status blocker` -> [Status Blocker](./blocker.md)",
        "",
        "Data sources are repository files so prompts can be handled from Git truth.",
    ]
    (out / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"generated_reports={len(reports)}")
    print(f"output={out}")


if __name__ == "__main__":
    main()
