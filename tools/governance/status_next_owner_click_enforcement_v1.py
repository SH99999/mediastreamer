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

    if failures:
        print("status_next_owner_click_enforcement=fail")
        for failure in failures:
            print(failure)
        return 1

    print("status_next_owner_click_enforcement=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
