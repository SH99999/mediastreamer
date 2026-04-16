#!/usr/bin/env python3
import re
from pathlib import Path

REQUIRED_FILES = [
    'contracts/repo/owner_decision_click_automation_standard_v1.md',
    'docs/agents/owner_operational_reference_v1.md',
    'tools/governance/scale_radio_governance_delivery_views_v1.md',
    '.github/workflows/owner-decision-click-sync.yml',
    '.github/workflows/pr-governance-review.yml',
    '.github/workflows/governance-closeout.yml',
]


def must_exist(root: Path, rel: str, failures: list):
    p = root / rel
    if not p.exists():
        failures.append(f'missing_file:{rel}')


def must_contain(root: Path, rel: str, pattern: str, failures: list):
    p = root / rel
    if not p.exists():
        failures.append(f'missing_for_pattern:{rel}')
        return
    text = p.read_text(encoding='utf-8')
    if not re.search(pattern, text, flags=re.MULTILINE):
        failures.append(f'missing_pattern:{rel}:{pattern}')


def main():
    root = Path(__file__).resolve().parents[2]
    failures = []

    for rel in REQUIRED_FILES:
        must_exist(root, rel, failures)

    must_contain(root, 'contracts/repo/owner_decision_click_automation_standard_v1.md', r'OWNER_DECISION_AUTOMATION_ENABLED', failures)
    must_contain(root, '.github/workflows/owner-decision-click-sync.yml', r'owner-decision-v1', failures)
    must_contain(root, '.github/workflows/owner-decision-click-sync.yml', r'OWNER_DECISION_AUTOMATION_ENABLED', failures)
    must_contain(root, 'docs/agents/owner_operational_reference_v1.md', r'decision\s*:\s*accept \| changes-requested \| reject', failures)

    if failures:
        print('governance_model_robustness=fail')
        for f in failures:
            print(f)
        raise SystemExit(1)

    print('governance_model_robustness=ok')


if __name__ == '__main__':
    main()
