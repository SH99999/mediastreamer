#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REPORTS = ["tuner", "governance", "ui", "bridge", "fun-line", "starter", "autoswitch", "hardware", "decisions", "blocker"]
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
    "claim_classes",
    "component_claims",
    "timestamp",
    "source_commit",
}
ALLOWED_NEXT_OWNER_CLICK = {"approve_pr", "request_changes", "run_workflow", "defer"}


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    failures: list[str] = []
    matrix = json.loads((root / "tools" / "governance" / "autonomous_delivery_matrix_v3.json").read_text(encoding="utf-8"))

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
        if "claim_classes.governance_docs:" not in report_text:
            failures.append(f"missing_claim_classes_in_report:{report_path.relative_to(root)}")
        if "component_claims.deploy_ready:" not in report_text:
            failures.append(f"missing_component_claims_in_report:{report_path.relative_to(root)}")
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

        claim_classes = packet.get("claim_classes", {})
        if not isinstance(claim_classes, dict):
            failures.append(f"invalid_claim_classes_type:{packet_path.relative_to(root)}")
            claim_classes = {}
        governance_docs = claim_classes.get("governance_docs")
        runtime_validation = claim_classes.get("runtime_validation")
        autonomy_eligibility = claim_classes.get("autonomy_eligibility")
        if governance_docs not in {"accepted", "pending"}:
            failures.append(f"invalid_claim_governance_docs:{packet_path.relative_to(root)}:{governance_docs}")
        if runtime_validation not in {"not_claimed", "validated"}:
            failures.append(f"invalid_claim_runtime_validation:{packet_path.relative_to(root)}:{runtime_validation}")
        if autonomy_eligibility not in {"not_claimed", "eligible"}:
            failures.append(f"invalid_claim_autonomy_eligibility:{packet_path.relative_to(root)}:{autonomy_eligibility}")

        runtime_claim = packet.get("runtime_claim")
        if runtime_validation == "validated":
            if not isinstance(runtime_claim, dict):
                failures.append(f"missing_runtime_claim_for_validated_status:{packet_path.relative_to(root)}")
            else:
                for key in ("evidence_path", "tested_scope", "source_ref", "rollback_verification"):
                    value = runtime_claim.get(key)
                    if not isinstance(value, str) or not value.strip():
                        failures.append(f"invalid_runtime_claim_{key}:{packet_path.relative_to(root)}")
        elif runtime_claim is not None:
            failures.append(f"runtime_claim_present_without_validated_status:{packet_path.relative_to(root)}")

        autonomy_claim = packet.get("autonomy_claim")
        if autonomy_eligibility == "eligible":
            if not isinstance(autonomy_claim, dict):
                failures.append(f"missing_autonomy_claim_for_eligible_status:{packet_path.relative_to(root)}")
            else:
                for key in ("evidence_path", "tested_scope", "source_ref", "rollback_path"):
                    value = autonomy_claim.get(key)
                    if not isinstance(value, str) or not value.strip():
                        failures.append(f"invalid_autonomy_claim_{key}:{packet_path.relative_to(root)}")
        elif autonomy_claim is not None:
            failures.append(f"autonomy_claim_present_without_eligible_status:{packet_path.relative_to(root)}")

        component_claims = packet.get("component_claims", {})
        if not isinstance(component_claims, dict):
            failures.append(f"invalid_component_claims_type:{packet_path.relative_to(root)}")
            component_claims = {}
        required_component_claim_keys = {
            "repo_ready_payload_present",
            "deploy_ready",
            "tested_on_target",
            "rollback_verified",
            "runtime_validated",
            "autonomy_eligible",
            "tested_scope",
            "evidence_path",
            "rollback_path",
            "source_ref",
        }
        missing_component_claims = required_component_claim_keys - set(component_claims.keys())
        if missing_component_claims:
            failures.append(
                f"missing_component_claim_keys:{packet_path.relative_to(root)}:{','.join(sorted(missing_component_claims))}"
            )
        for key in ("repo_ready_payload_present", "deploy_ready", "tested_on_target", "rollback_verified", "runtime_validated", "autonomy_eligible"):
            value = component_claims.get(key)
            if not isinstance(value, bool):
                failures.append(f"invalid_component_claim_bool_{key}:{packet_path.relative_to(root)}:{value}")
        for key in ("tested_scope", "evidence_path", "rollback_path", "source_ref"):
            value = component_claims.get(key)
            if not isinstance(value, str) or not value.strip():
                failures.append(f"invalid_component_claim_text_{key}:{packet_path.relative_to(root)}")

        if component_claims.get("runtime_validated") is True and claim_classes.get("runtime_validation") != "validated":
            failures.append(f"runtime_claim_class_mismatch:{packet_path.relative_to(root)}")
        if component_claims.get("autonomy_eligible") is True and claim_classes.get("autonomy_eligibility") != "eligible":
            failures.append(f"autonomy_claim_class_mismatch:{packet_path.relative_to(root)}")

        component_name = packet.get("component")
        if isinstance(component_name, str):
            matrix_entry = matrix.get("components", {}).get(component_name)
            if isinstance(matrix_entry, dict):
                matrix_auto = matrix_entry.get("auto_delivery_supported")
                if isinstance(matrix_auto, bool) and component_claims.get("autonomy_eligible") is True and matrix_auto is not True:
                    failures.append(f"autonomy_matrix_mismatch:{packet_path.relative_to(root)}:{component_name}")

    if failures:
        print("status_next_owner_click_enforcement=fail")
        for failure in failures:
            print(failure)
        return 1

    print("status_next_owner_click_enforcement=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
