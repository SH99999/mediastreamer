#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json

COMPONENT_FILES = {
    "bridge": "journals/scale-radio-bridge/current_state_v1.md",
    "tuner": "journals/scale-radio-tuner/current_state_v2.md",
    "fun-line": "journals/scale-radio-fun-line/current_state_v1.md",
    "starter": "journals/scale-radio-starter/current_state_v1.md",
    "autoswitch": "journals/scale-radio-autoswitch/current_state_v1.md",
    "hardware": "journals/scale-radio-hardware/current_state_v1.md",
}

REQUIRED_KEYS = {
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


def parse_claims(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    capture = False
    for raw in text.splitlines():
        line = raw.strip()
        if line == "## Evidence-led claim ledger":
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture and line.startswith("- claim."):
            body = line[2:].strip()
            parts = body.split(":", 1)
            if len(parts) != 2:
                continue
            key = parts[0].strip().removeprefix("claim.")
            value = parts[1].strip().strip("`")
            out[key] = value
    return out


def as_bool(claims: dict[str, str], key: str) -> bool:
    return claims.get(key, "false").lower() == "true"


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    matrix = json.loads((root / "tools/governance/autonomous_delivery_matrix_v3.json").read_text(encoding="utf-8"))

    failures: list[str] = []
    for component, rel_path in COMPONENT_FILES.items():
        path = root / rel_path
        if not path.exists():
            failures.append(f"missing_current_state:{rel_path}")
            continue

        text = path.read_text(encoding="utf-8")
        claims = parse_claims(text)
        missing = REQUIRED_KEYS - set(claims.keys())
        if missing:
            failures.append(f"missing_claim_keys:{component}:{','.join(sorted(missing))}")
            continue

        tested_on_target = as_bool(claims, "tested_on_target")
        rollback_verified = as_bool(claims, "rollback_verified")
        runtime_validated = as_bool(claims, "runtime_validated")
        autonomy_eligible = as_bool(claims, "autonomy_eligible")

        if tested_on_target and "`tested_on_pi`" not in text:
            failures.append(f"tested_on_target_without_lifecycle_tested_on_pi:{component}")
        if rollback_verified and not tested_on_target:
            failures.append(f"rollback_verified_requires_tested_on_target:{component}")
        if runtime_validated and not tested_on_target:
            failures.append(f"runtime_validated_requires_tested_on_target:{component}")
        if autonomy_eligible and not runtime_validated:
            failures.append(f"autonomy_requires_runtime_validated:{component}")

        matrix_entry = matrix.get("components", {}).get(component, {})
        matrix_autonomy = bool(matrix_entry.get("auto_delivery_supported") is True)
        if autonomy_eligible != matrix_autonomy:
            failures.append(f"autonomy_matrix_mismatch:{component}:claims={autonomy_eligible}:matrix={matrix_autonomy}")

    if failures:
        print("component_claim_consistency=fail")
        for failure in failures:
            print(failure)
        return 1

    print("component_claim_consistency=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
