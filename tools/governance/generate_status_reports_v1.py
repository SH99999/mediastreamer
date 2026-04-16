#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess


@dataclass
class Report:
    slug: str
    title: str
    body: str
    packet: dict


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section_bullets(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    out: list[str] = []
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


def source_commit(repo_root: Path) -> str:
    return subprocess.check_output(["git", "-C", str(repo_root), "rev-parse", "HEAD"], text=True).strip()


def status_packet(
    component: str,
    canonical_status: str,
    evidence_links: list[str],
    blockers: list[str],
    recommended_owner_action: str,
    next_owner_click: str,
    decision_scoring: dict,
    rollback_action: dict,
    generated_at: str,
    source_commit_id: str,
) -> dict:
    return {
        "schema": "status_packet_v1",
        "component": component,
        "canonical_status": canonical_status,
        "evidence_links": evidence_links,
        "blockers": blockers,
        "recommended_owner_action": recommended_owner_action,
        "next_owner_click": next_owner_click,
        "decision_scoring": decision_scoring,
        "rollback_action": rollback_action,
        "timestamp": generated_at,
        "source_commit": source_commit_id,
    }


def default_decision_scoring(blockers: list[str]) -> dict:
    if blockers:
        return {
            "evidence_quality": 2,
            "rollback_readiness": 2,
            "blast_radius": "medium",
            "confidence": 68,
        }
    return {
        "evidence_quality": 3,
        "rollback_readiness": 3,
        "blast_radius": "low",
        "confidence": 85,
    }


def default_rollback_action(component: str) -> dict:
    return {
        "enabled": True,
        "command": f"git revert <merge_commit_for_{component}>",
        "verification": [
            "rerun governance/report checks",
            "confirm owner action contract fields still render",
        ],
    }


def owner_contract_block(packet: dict) -> list[str]:
    return [
        "## Owner action contract",
        f"- recommended owner action: `{packet['recommended_owner_action']}`",
        f"- next_owner_click: `{packet['next_owner_click']}`",
        f"- decision_scoring.evidence_quality: `{packet['decision_scoring']['evidence_quality']}`",
        f"- decision_scoring.rollback_readiness: `{packet['decision_scoring']['rollback_readiness']}`",
        f"- decision_scoring.blast_radius: `{packet['decision_scoring']['blast_radius']}`",
        f"- decision_scoring.confidence: `{packet['decision_scoring']['confidence']}`",
        f"- rollback_action.command: `{packet['rollback_action']['command']}`",
        f"- source_commit: `{packet['source_commit']}`",
        "",
    ]


def status_from_component(component: str, current_state_path: Path, stream_path: Path, generated_at: str, source_commit_id: str) -> Report:
    cs = read(current_state_path)
    lifecycle = section_bullets(cs, "Lifecycle status")[:6]
    gaps = section_bullets(cs, "Current gaps")[:4]
    next_actions = section_bullets(cs, "Repo-normalized next action")[:3]

    packet = status_packet(
        component=component.lower(),
        canonical_status="functional_acceptance_pending" if gaps else "deploy_candidate_started",
        evidence_links=[current_state_path.as_posix(), stream_path.as_posix()],
        blockers=gaps,
        recommended_owner_action="changes-requested" if gaps else "accept",
        next_owner_click="request_changes" if gaps else "approve_pr",
        decision_scoring=default_decision_scoring(gaps),
        rollback_action=default_rollback_action(component.lower()),
        generated_at=generated_at,
        source_commit_id=source_commit_id,
    )

    body = "\n".join([
        f"# Status {component}",
        "",
        f"_Generated: {generated_at}_",
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
        *owner_contract_block(packet),
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
    return Report(component.lower(), f"Status {component}", body, packet)


def governance_status_report(si_status_path: Path, generated_at: str, source_commit_id: str) -> Report:
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

    packet = status_packet(
        component="governance",
        canonical_status="functional_acceptance_pending" if broken else "deploy_candidate_started",
        evidence_links=[si_status_path.as_posix()],
        blockers=broken,
        recommended_owner_action="changes-requested" if broken else "accept",
        next_owner_click="request_changes" if broken else "approve_pr",
        decision_scoring=default_decision_scoring(broken),
        rollback_action=default_rollback_action("governance"),
        generated_at=generated_at,
        source_commit_id=source_commit_id,
    )

    body = "\n".join([
        "# Status Governance",
        "",
        f"_Generated: {generated_at}_",
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
        *owner_contract_block(packet),
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
    return Report("governance", "Status Governance", body, packet)


def ui_status_report(ui_stream_path: Path, generated_at: str, source_commit_id: str) -> Report:
    text = read(ui_stream_path)
    entries = [ln.strip()[2:].strip() for ln in text.splitlines() if ln.strip().startswith("-")]
    recent = entries[-6:]

    packet = status_packet(
        component="ui",
        canonical_status="deploy_candidate_started",
        evidence_links=[ui_stream_path.as_posix()],
        blockers=[],
        recommended_owner_action="accept",
        next_owner_click="approve_pr",
        decision_scoring=default_decision_scoring([]),
        rollback_action=default_rollback_action("ui"),
        generated_at=generated_at,
        source_commit_id=source_commit_id,
    )

    body = "\n".join([
        "# Status UI",
        "",
        f"_Generated: {generated_at}_",
        "",
        "## Recent governance entries",
        *(f"- {r}" for r in recent),
        "",
        "## Source",
        f"- [UI/GUI stream]({ui_stream_path.as_posix()})",
        "",
        *owner_contract_block(packet),
        "## Visual snapshot",
        "```mermaid",
        "pie",
        "    title UI governance stream",
        f"    \"entries sampled\" : {len(recent)}",
        f"    \"total entries\" : {len(entries)}",
        "```",
        "",
    ])
    return Report("ui", "Status UI", body, packet)


def decisions_report(decisions_path: Path, generated_at: str, source_commit_id: str) -> Report:
    text = read(decisions_path)
    ids = re.findall(r"^###\s+(DEC-[^\n]+)", text, flags=re.MULTILINE)
    locked = len(re.findall(r"^- Status:\s*locked", text, flags=re.MULTILINE))

    packet = status_packet(
        component="decisions",
        canonical_status="payload_present",
        evidence_links=[decisions_path.as_posix()],
        blockers=[],
        recommended_owner_action="defer",
        next_owner_click="defer",
        decision_scoring=default_decision_scoring([]),
        rollback_action=default_rollback_action("decisions"),
        generated_at=generated_at,
        source_commit_id=source_commit_id,
    )

    body = "\n".join([
        "# Status Decisions",
        "",
        f"_Generated: {generated_at}_",
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
        *owner_contract_block(packet),
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
    return Report("decisions", "Status Decisions", body, packet)


def blocker_report(si_status_path: Path, generated_at: str, source_commit_id: str) -> Report:
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

    packet = status_packet(
        component="blocker",
        canonical_status="functional_acceptance_pending" if broken else "deploy_candidate_started",
        evidence_links=[si_status_path.as_posix()],
        blockers=broken + open_decisions,
        recommended_owner_action="run_workflow" if broken or open_decisions else "defer",
        next_owner_click="run_workflow" if broken or open_decisions else "defer",
        decision_scoring=default_decision_scoring(broken + open_decisions),
        rollback_action=default_rollback_action("blocker"),
        generated_at=generated_at,
        source_commit_id=source_commit_id,
    )

    body = "\n".join([
        "# Status Blocker",
        "",
        f"_Generated: {generated_at}_",
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
        *owner_contract_block(packet),
        "## Visual snapshot",
        "```mermaid",
        "pie",
        "    title Blocker buckets",
        f"    \"broken\" : {len(broken)}",
        f"    \"open decisions\" : {len(open_decisions)}",
        "```",
        "",
    ])
    return Report("blocker", "Status Blocker", body, packet)


def write_report(base: Path, report: Report):
    path = base / f"{report.slug}.md"
    path.write_text(report.body, encoding="utf-8")

    packet_dir = base / "packets"
    packet_dir.mkdir(parents=True, exist_ok=True)
    packet_path = packet_dir / f"{report.slug}.json"
    packet_path.write_text(json.dumps(report.packet, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate prompt-ready status reports with clickable links and visuals.")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--out-dir", default="reports/status", help="Output directory for generated markdown reports")
    parser.add_argument(
        "--generated-at",
        default=None,
        help="Optional ISO8601 timestamp to stamp all generated reports deterministically",
    )
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    out = root / args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    generated_at = args.generated_at or datetime.now(timezone.utc).isoformat()
    source_commit_id = source_commit(root)

    reports = [
        status_from_component(
            "Tuner",
            root / "journals/scale-radio-tuner/current_state_v2.md",
            root / "journals/scale-radio-tuner/stream_v2.md",
            generated_at,
            source_commit_id,
        ),
        governance_status_report(root / "journals/system-integration-normalization/STATUS_system_integration_normalization_v8.md", generated_at, source_commit_id),
        ui_status_report(root / "journals/system-integration-normalization/ui_gui_stream_v1.md", generated_at, source_commit_id),
        status_from_component(
            "Bridge",
            root / "journals/scale-radio-bridge/current_state_v1.md",
            root / "journals/scale-radio-bridge/stream_v1.md",
            generated_at,
            source_commit_id,
        ),
        decisions_report(root / "journals/system-integration-normalization/DECISIONS_system_integration_normalization_v9.md", generated_at, source_commit_id),
        blocker_report(root / "journals/system-integration-normalization/STATUS_system_integration_normalization_v8.md", generated_at, source_commit_id),
    ]

    for r in reports:
        write_report(out, r)

    index_lines = [
        "# Status Reports Index v1",
        "",
        f"_Generated: {generated_at}_",
        "",
        "Prompt aliases:",
        "- `status tuner` -> [Status Tuner](./tuner.md)",
        "- `status governance` -> [Status Governance](./governance.md)",
        "- `status ui` -> [Status UI](./ui.md)",
        "- `status bridge` -> [Status Bridge](./bridge.md)",
        "- `status decisions` -> [Status Decisions](./decisions.md)",
        "- `status blocker` -> [Status Blocker](./blocker.md)",
        "",
        "Status packet JSON artifacts:",
        "- [tuner](./packets/tuner.json)",
        "- [governance](./packets/governance.json)",
        "- [ui](./packets/ui.json)",
        "- [bridge](./packets/bridge.json)",
        "- [decisions](./packets/decisions.json)",
        "- [blocker](./packets/blocker.json)",
        "",
        "Data sources are repository files so prompts can be handled from Git truth.",
    ]
    (out / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"generated_reports={len(reports)}")
    print(f"output={out}")


if __name__ == "__main__":
    main()
