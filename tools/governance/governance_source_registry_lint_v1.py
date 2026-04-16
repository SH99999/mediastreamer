#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re

SCAN_GLOBS = ["contracts/repo/*.md", "docs/agents/*.md"]


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    registry_path = root / "tools" / "governance" / "governance_source_registry_v1.json"
    failures: list[str] = []

    if not registry_path.exists():
        print("governance_source_registry_lint=fail")
        print("missing_registry:tools/governance/governance_source_registry_v1.json")
        return 1

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    domains = registry.get("domains", [])

    authority_files = [entry.get("authority_file") for entry in domains]
    if len(authority_files) != len(set(authority_files)):
        failures.append("duplicate_authority_file_in_registry")

    files_to_scan: list[Path] = []
    for pattern in SCAN_GLOBS:
        files_to_scan.extend(sorted(root.glob(pattern)))

    for entry in domains:
        domain_id = entry.get("id", "unknown")
        authority_rel = entry.get("authority_file")
        patterns = entry.get("duplicate_forbidden_patterns", [])
        authority_path = root / authority_rel

        if not authority_path.exists():
            failures.append(f"missing_authority_file:{domain_id}:{authority_rel}")
            continue

        for pattern in patterns:
            rx = re.compile(pattern, re.MULTILINE)
            authority_text = authority_path.read_text(encoding="utf-8")
            if not rx.search(authority_text):
                failures.append(f"missing_pattern_in_authority:{domain_id}:{pattern}")

            for candidate in files_to_scan:
                if candidate == authority_path:
                    continue
                text = candidate.read_text(encoding="utf-8")
                if rx.search(text):
                    failures.append(
                        f"duplicate_authority_pattern:{domain_id}:{candidate.relative_to(root)}:{pattern}"
                    )

    if failures:
        print("governance_source_registry_lint=fail")
        for failure in failures:
            print(failure)
        return 1

    print("governance_source_registry_lint=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
