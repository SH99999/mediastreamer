# One-Click Ecosystem Integration Check v1

_Generated: 2026-04-16T22:46:42.021789+00:00_

## Summary
- checks_total: 6
- checks_passed: 6
- checks_failed: 0
- avg_check_runtime_seconds: 0.287

## Results
### ✅ python3
- command: `python3 tools/governance/generate_status_reports_v1.py --repo-root . --out-dir reports/status --generated-at 2026-04-16T00:00:00+00:00`
- elapsed_seconds: `0.105`
- output:
```text
generated_reports=10
output=/workspace/mediastreamer/reports/status
```

### ✅ python3
- command: `python3 tools/governance/status_next_owner_click_enforcement_v1.py`
- elapsed_seconds: `0.060`
- output:
```text
status_next_owner_click_enforcement=ok
```

### ✅ python3
- command: `python3 tools/governance/component_claim_consistency_check_v1.py`
- elapsed_seconds: `0.060`
- output:
```text
component_claim_consistency=ok
```

### ✅ python3
- command: `python3 tools/governance/governance_source_registry_lint_v1.py`
- elapsed_seconds: `0.057`
- output:
```text
governance_source_registry_lint=ok
```

### ✅ bash
- command: `bash -lc "printf 'contracts/repo/owner_decision_scoring_and_rollback_contract_v1.md\n' > /tmp/changed_files_guard.txt && python3 tools/governance/si_branch_scope_guard_v1.py --branch si/governance-integration-check-v1 --changed-files /tmp/changed_files_guard.txt --enforce true"`
- elapsed_seconds: `1.441`
- output:
```text
si_branch_scope_guard=ok
governed_changes=1
```

### ✅ one_click_presence
- command: `inline check`
- elapsed_seconds: `0.001`
- output:
```text
one_click_contract_missing=0
```

## One-click perspective
- integrity proof: all contract checks pass
- correctness proof: required one-click fields exist across all generated status reports
- speed note: average local check runtime is sub-second on this run

## Executed checks
1. report generation
2. next-owner-click enforcement
3. component claim consistency check
4. source registry lint
5. SI branch-scope guard
6. one-click field presence sweep
