#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REPORTS = ["tuner", "governance", "ui", "bridge", "decisions", "blocker"]
REQUIRED_PACKET_KEYS = {
    "schema",
    "component",
    "canonical_status",
    "evidence_links",
    "blockers",
    "recommended_owner_action",
    "next_owner_click",
    "decision_scoring",
    "rollback_action",
    "timestamp",
    "source_commit",
}
ALLOWED_NEXT_OWNER_CLICK = {"approve_pr", "request_changes", "run_workflow", "defer"}


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    failures: list[str] = []

    for slug in REPORTS:
        report_path = root / "reports" / "status" / f"{slug}.md"
        packet_path = root / "reports" / "status" / "packets" / f"{slug}.json"

        if not report_path.exists():
            failures.append(f"missing_report:{report_path.relative_to(root)}")
            continue
        if not packet_path.exists():
            failures.append(f"missing_packet:{packet_path.relative_to(root)}")
            continue

        report_text = report_path.read_text(encoding="utf-8")
        if "## Owner action contract" not in report_text:
            failures.append(f"missing_owner_action_block:{report_path.relative_to(root)}")
        if "next_owner_click:" not in report_text:
            failures.append(f"missing_next_owner_click_in_report:{report_path.relative_to(root)}")
        if "decision_scoring.evidence_quality:" not in report_text:
            failures.append(f"missing_decision_scoring_in_report:{report_path.relative_to(root)}")
        if "rollback_action.command:" not in report_text:
            failures.append(f"missing_rollback_action_in_report:{report_path.relative_to(root)}")
        if "source_commit:" not in report_text:
            failures.append(f"missing_source_commit_in_report:{report_path.relative_to(root)}")

        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        missing_keys = REQUIRED_PACKET_KEYS - set(packet.keys())
        if missing_keys:
            failures.append(
                f"missing_packet_keys:{packet_path.relative_to(root)}:{','.join(sorted(missing_keys))}"
            )
        if packet.get("schema") != "status_packet_v1":
            failures.append(f"invalid_packet_schema:{packet_path.relative_to(root)}")
        if packet.get("next_owner_click") not in ALLOWED_NEXT_OWNER_CLICK:
            failures.append(f"invalid_next_owner_click:{packet_path.relative_to(root)}:{packet.get('next_owner_click')}")
        decision_scoring = packet.get("decision_scoring", {})
        if not isinstance(decision_scoring, dict):
            failures.append(f"invalid_decision_scoring_type:{packet_path.relative_to(root)}")
            decision_scoring = {}
        evidence_quality = decision_scoring.get("evidence_quality")
        rollback_readiness = decision_scoring.get("rollback_readiness")
        blast_radius = decision_scoring.get("blast_radius")
        confidence = decision_scoring.get("confidence")
        if not isinstance(evidence_quality, int) or not (0 <= evidence_quality <= 3):
            failures.append(f"invalid_evidence_quality:{packet_path.relative_to(root)}:{evidence_quality}")
        if not isinstance(rollback_readiness, int) or not (0 <= rollback_readiness <= 3):
            failures.append(f"invalid_rollback_readiness:{packet_path.relative_to(root)}:{rollback_readiness}")
        if blast_radius not in {"low", "medium", "high"}:
            failures.append(f"invalid_blast_radius:{packet_path.relative_to(root)}:{blast_radius}")
        if not isinstance(confidence, int) or not (0 <= confidence <= 100):
            failures.append(f"invalid_confidence:{packet_path.relative_to(root)}:{confidence}")

        rollback_action = packet.get("rollback_action", {})
        if not isinstance(rollback_action, dict):
            failures.append(f"invalid_rollback_action_type:{packet_path.relative_to(root)}")
            rollback_action = {}
        if not isinstance(rollback_action.get("enabled"), bool):
            failures.append(f"invalid_rollback_enabled:{packet_path.relative_to(root)}:{rollback_action.get('enabled')}")
        command = rollback_action.get("command")
        if not isinstance(command, str) or not command.strip():
            failures.append(f"invalid_rollback_command:{packet_path.relative_to(root)}:{command}")
        verification = rollback_action.get("verification")
        if not isinstance(verification, list) or not verification or not all(isinstance(item, str) and item.strip() for item in verification):
            failures.append(f"invalid_rollback_verification:{packet_path.relative_to(root)}")

    if failures:
        print("status_next_owner_click_enforcement=fail")
        for failure in failures:
            print(failure)
        return 1

    print("status_next_owner_click_enforcement=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
