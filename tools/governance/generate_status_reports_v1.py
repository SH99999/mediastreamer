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


def section_claim_map(text: str, heading: str) -> dict[str, str]:
    lines = text.splitlines()
    out: dict[str, str] = {}
    capture = False
    heading_prefix = f"## {heading}"
    for line in lines:
        if line.startswith("## ") and line.strip() == heading_prefix:
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture and line.lstrip().startswith("- claim."):
            body = line.lstrip()[2:].strip()
            key_value = body.split(":", 1)
            if len(key_value) != 2:
                continue
            key = key_value[0].strip().removeprefix("claim.")
            value = key_value[1].strip().strip("`")
            out[key] = value
    return out


def source_commit(repo_root: Path) -> str:
    return subprocess.check_output(["git", "-C", str(repo_root), "rev-parse", "HEAD"], text=True).strip()


def component_matrix_key(component: str) -> str:
    mapping = {
        "tuner": "tuner",
        "bridge": "bridge",
        "fun line": "fun-line",
        "fun-line": "fun-line",
    }
    return mapping.get(component.lower(), component.lower())


def autonomy_supported(repo_root: Path, component: str) -> bool:
    matrix_path = repo_root / "tools/governance/autonomous_delivery_matrix_v3.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    key = component_matrix_key(component)
    component_data = matrix.get("components", {}).get(key, {})
    return bool(component_data.get("auto_delivery_supported") is True)


def status_packet(
    component: str,
    canonical_status: str,
    evidence_links: list[str],
    blockers: list[str],
    recommended_owner_action: str,
    next_owner_click: str,
    decision_scoring: dict,
    rollback_action: dict,
    claim_classes: dict,
    component_claims: dict,
    runtime_claim: dict | None,
    autonomy_claim: dict | None,
    generated_at: str,
    source_commit_id: str,
) -> dict:
    packet = {
        "schema": "status_packet_v1",
        "component": component,
        "canonical_status": canonical_status,
        "evidence_links": evidence_links,
        "blockers": blockers,
        "recommended_owner_action": recommended_owner_action,
        "next_owner_click": next_owner_click,
        "decision_scoring": decision_scoring,
        "rollback_action": rollback_action,
        "claim_classes": claim_classes,
        "component_claims": component_claims,
        "timestamp": generated_at,
        "source_commit": source_commit_id,
    }
    if runtime_claim is not None:
        packet["runtime_claim"] = runtime_claim
    if autonomy_claim is not None:
        packet["autonomy_claim"] = autonomy_claim
    return packet


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
    runtime_claim = packet.get("runtime_claim")
    autonomy_claim = packet.get("autonomy_claim")
    runtime_evidence = runtime_claim["evidence_path"] if isinstance(runtime_claim, dict) else "n/a"
    runtime_scope = runtime_claim["tested_scope"] if isinstance(runtime_claim, dict) else "n/a"
    autonomy_evidence = autonomy_claim["evidence_path"] if isinstance(autonomy_claim, dict) else "n/a"
    autonomy_scope = autonomy_claim["tested_scope"] if isinstance(autonomy_claim, dict) else "n/a"
    return [
        "## Owner action contract",
        f"- recommended owner action: `{packet['recommended_owner_action']}`",
        f"- next_owner_click: `{packet['next_owner_click']}`",
        f"- claim_classes.governance_docs: `{packet['claim_classes']['governance_docs']}`",
        f"- claim_classes.runtime_validation: `{packet['claim_classes']['runtime_validation']}`",
        f"- claim_classes.autonomy_eligibility: `{packet['claim_classes']['autonomy_eligibility']}`",
        f"- component_claims.repo_ready_payload_present: `{packet['component_claims']['repo_ready_payload_present']}`",
        f"- component_claims.deploy_ready: `{packet['component_claims']['deploy_ready']}`",
        f"- component_claims.tested_on_target: `{packet['component_claims']['tested_on_target']}`",
        f"- component_claims.rollback_verified: `{packet['component_claims']['rollback_verified']}`",
        f"- component_claims.runtime_validated: `{packet['component_claims']['runtime_validated']}`",
        f"- component_claims.autonomy_eligible: `{packet['component_claims']['autonomy_eligible']}`",
        f"- runtime_claim.evidence_path: `{runtime_evidence}`",
        f"- runtime_claim.tested_scope: `{runtime_scope}`",
        f"- autonomy_claim.evidence_path: `{autonomy_evidence}`",
        f"- autonomy_claim.tested_scope: `{autonomy_scope}`",
        f"- decision_scoring.evidence_quality: `{packet['decision_scoring']['evidence_quality']}`",
        f"- decision_scoring.rollback_readiness: `{packet['decision_scoring']['rollback_readiness']}`",
        f"- decision_scoring.blast_radius: `{packet['decision_scoring']['blast_radius']}`",
        f"- decision_scoring.confidence: `{packet['decision_scoring']['confidence']}`",
        f"- rollback_action.command: `{packet['rollback_action']['command']}`",
        f"- source_commit: `{packet['source_commit']}`",
        "",
    ]


def status_from_component(component: str, current_state_path: Path, stream_path: Path, generated_at: str, source_commit_id: str, repo_root: Path) -> Report:
    cs = read(current_state_path)
    component_slug = component_matrix_key(component)
    lifecycle = section_bullets(cs, "Lifecycle status")[:6]
    gaps = section_bullets(cs, "Current gaps")[:4]
    next_actions = section_bullets(cs, "Repo-normalized next action")[:3]

    claims = section_claim_map(cs, "Evidence-led claim ledger")

    def as_bool(key: str) -> bool:
        return claims.get(key, "false").lower() == "true"

    component_claims = {
        "repo_ready_payload_present": as_bool("repo_ready_payload_present"),
        "deploy_ready": as_bool("deploy_ready"),
        "tested_on_target": as_bool("tested_on_target"),
        "rollback_verified": as_bool("rollback_verified"),
        "runtime_validated": as_bool("runtime_validated"),
        "autonomy_eligible": as_bool("autonomy_eligible"),
        "tested_scope": claims.get("tested_scope", "not-specified"),
        "evidence_path": claims.get("evidence_path", current_state_path.as_posix()),
        "rollback_path": claims.get("rollback_path", default_rollback_action(component.lower())["command"]),
        "source_ref": claims.get("source_ref", source_commit_id),
    }

    runtime_validated = component_claims["runtime_validated"]
    runtime_claim = None
    if runtime_validated:
        runtime_claim = {
            "evidence_path": component_claims["evidence_path"],
            "tested_scope": component_claims["tested_scope"],
            "source_ref": component_claims["source_ref"],
            "rollback_verification": component_claims["rollback_path"],
        }

    matrix_support = autonomy_supported(repo_root, component)
    is_autonomy_eligible = runtime_validated and component_claims["autonomy_eligible"] and matrix_support
    autonomy_claim = None
    if is_autonomy_eligible:
        autonomy_claim = {
            "evidence_path": component_claims["evidence_path"],
            "tested_scope": component_claims["tested_scope"],
            "source_ref": component_claims["source_ref"],
            "rollback_path": component_claims["rollback_path"],
        }

    packet = status_packet(
        component=component_slug,
        canonical_status="functional_acceptance_open" if gaps else "deployment_candidate_started",
        evidence_links=[current_state_path.as_posix(), stream_path.as_posix()],
        blockers=gaps,
        recommended_owner_action="changes-requested" if gaps else "accept",
        next_owner_click="request_changes" if gaps else "approve_pr",
        decision_scoring=default_decision_scoring(gaps),
        rollback_action=default_rollback_action(component_slug),
        claim_classes={
            "governance_docs": "accepted",
            "runtime_validation": "validated" if runtime_validated else "not_claimed",
            "autonomy_eligibility": "eligible" if is_autonomy_eligible else "not_claimed",
        },
        component_claims={
            **component_claims,
            "autonomy_eligible": is_autonomy_eligible,
        },
        runtime_claim=runtime_claim,
        autonomy_claim=autonomy_claim,
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
    return Report(component_slug, f"Status {component}", body, packet)


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
        canonical_status="functional_acceptance_open" if broken else "deployment_candidate_started",
        evidence_links=[si_status_path.as_posix()],
        blockers=broken,
        recommended_owner_action="changes-requested" if broken else "accept",
        next_owner_click="request_changes" if broken else "approve_pr",
        decision_scoring=default_decision_scoring(broken),
        rollback_action=default_rollback_action("governance"),
        claim_classes={
            "governance_docs": "accepted",
            "runtime_validation": "not_claimed",
            "autonomy_eligibility": "not_claimed",
        },
        component_claims={
            "repo_ready_payload_present": False,
            "deploy_ready": False,
            "tested_on_target": False,
            "rollback_verified": False,
            "runtime_validated": False,
            "autonomy_eligible": False,
            "tested_scope": "governance/docs status view",
            "evidence_path": si_status_path.as_posix(),
            "rollback_path": default_rollback_action("governance")["command"],
            "source_ref": source_commit_id,
        },
        runtime_claim=None,
        autonomy_claim=None,
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
        canonical_status="deployment_candidate_started",
        evidence_links=[ui_stream_path.as_posix()],
        blockers=[],
        recommended_owner_action="accept",
        next_owner_click="approve_pr",
        decision_scoring=default_decision_scoring([]),
        rollback_action=default_rollback_action("ui"),
        claim_classes={
            "governance_docs": "accepted",
            "runtime_validation": "not_claimed",
            "autonomy_eligibility": "not_claimed",
        },
        component_claims={
            "repo_ready_payload_present": False,
            "deploy_ready": False,
            "tested_on_target": False,
            "rollback_verified": False,
            "runtime_validated": False,
            "autonomy_eligible": False,
            "tested_scope": "ui governance stream status view",
            "evidence_path": ui_stream_path.as_posix(),
            "rollback_path": default_rollback_action("ui")["command"],
            "source_ref": source_commit_id,
        },
        runtime_claim=None,
        autonomy_claim=None,
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
        claim_classes={
            "governance_docs": "accepted",
            "runtime_validation": "not_claimed",
            "autonomy_eligibility": "not_claimed",
        },
        component_claims={
            "repo_ready_payload_present": False,
            "deploy_ready": False,
            "tested_on_target": False,
            "rollback_verified": False,
            "runtime_validated": False,
            "autonomy_eligible": False,
            "tested_scope": "decision log status view",
            "evidence_path": decisions_path.as_posix(),
            "rollback_path": default_rollback_action("decisions")["command"],
            "source_ref": source_commit_id,
        },
        runtime_claim=None,
        autonomy_claim=None,
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
        canonical_status="functional_acceptance_open" if broken else "deployment_candidate_started",
        evidence_links=[si_status_path.as_posix()],
        blockers=broken + open_decisions,
        recommended_owner_action="run_workflow" if broken or open_decisions else "defer",
        next_owner_click="run_workflow" if broken or open_decisions else "defer",
        decision_scoring=default_decision_scoring(broken + open_decisions),
        rollback_action=default_rollback_action("blocker"),
        claim_classes={
            "governance_docs": "accepted",
            "runtime_validation": "not_claimed",
            "autonomy_eligibility": "not_claimed",
        },
        component_claims={
            "repo_ready_payload_present": False,
            "deploy_ready": False,
            "tested_on_target": False,
            "rollback_verified": False,
            "runtime_validated": False,
            "autonomy_eligible": False,
            "tested_scope": "si blocker status view",
            "evidence_path": si_status_path.as_posix(),
            "rollback_path": default_rollback_action("blocker")["command"],
            "source_ref": source_commit_id,
        },
        runtime_claim=None,
        autonomy_claim=None,
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
            root,
        ),
        governance_status_report(root / "journals/system-integration-normalization/STATUS_system_integration_normalization_v8.md", generated_at, source_commit_id),
        ui_status_report(root / "journals/system-integration-normalization/ui_gui_stream_v1.md", generated_at, source_commit_id),
        status_from_component(
            "Bridge",
            root / "journals/scale-radio-bridge/current_state_v1.md",
            root / "journals/scale-radio-bridge/stream_v1.md",
            generated_at,
            source_commit_id,
            root,
        ),
        status_from_component(
            "Fun Line",
            root / "journals/scale-radio-fun-line/current_state_v1.md",
            root / "journals/scale-radio-fun-line/stream_v1.md",
            generated_at,
            source_commit_id,
            root,
        ),
        status_from_component(
            "Starter",
            root / "journals/scale-radio-starter/current_state_v1.md",
            root / "journals/scale-radio-starter/stream_v1.md",
            generated_at,
            source_commit_id,
            root,
        ),
        status_from_component(
            "Autoswitch",
            root / "journals/scale-radio-autoswitch/current_state_v1.md",
            root / "journals/scale-radio-autoswitch/stream_v1.md",
            generated_at,
            source_commit_id,
            root,
        ),
        status_from_component(
            "Hardware",
            root / "journals/scale-radio-hardware/current_state_v1.md",
            root / "journals/scale-radio-hardware/stream_v1.md",
            generated_at,
            source_commit_id,
            root,
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
        "- `status fun-line` -> [Status Fun Line](./fun-line.md)",
        "- `status starter` -> [Status Starter](./starter.md)",
        "- `status autoswitch` -> [Status Autoswitch](./autoswitch.md)",
        "- `status hardware` -> [Status Hardware](./hardware.md)",
        "- `status decisions` -> [Status Decisions](./decisions.md)",
        "- `status blocker` -> [Status Blocker](./blocker.md)",
        "",
        "Status packet JSON artifacts:",
        "- [tuner](./packets/tuner.json)",
        "- [governance](./packets/governance.json)",
        "- [ui](./packets/ui.json)",
        "- [bridge](./packets/bridge.json)",
        "- [fun-line](./packets/fun-line.json)",
        "- [starter](./packets/starter.json)",
        "- [autoswitch](./packets/autoswitch.json)",
        "- [hardware](./packets/hardware.json)",
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
