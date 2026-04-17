# SYSTEM INTEGRATION RECOVERY ONBOARDING V7

## Purpose
Fast, governed re-entry for replacement SI lanes with one active authority chain and explicit history separation.

## Active authority chain (single startup truth)
Read only this chain first:
1. `AGENTS.md`
2. `contracts/repo/system_integration_governance_index_v7.md`
3. `docs/agents/si_target_operating_model_v1.md`
4. `journals/system-integration-normalization/STATUS_system_integration_normalization_v8.md`
5. `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v9.md`
6. `journals/system-integration-normalization/stream_v6.md`

Interpretation rule:
- contracts + current SI status/decisions/stream are authoritative
- reports/issues/dashboards/boards/chat memory are derived surfaces only

## Tiered onboarding model (derived from one authority chain)

### Tier 0 — safe-start (`target < 5 minutes`)
Required before mutation:
- run `bash tools/governance/agent_git_bootstrap_v1.sh --role si --mode mode-b`
- confirm branch is `si/<topic>` (never `main`, never `work`)
- confirm remote `git` targets `https://github.com/SH99999/mediastreamer.git`
- confirm bootstrap `base sync` and `push auth` status
- confirm active authority chain above

### Tier 1 — working context (`target < 15 minutes`)
Read only these files after Tier 0:
- `docs/agents/agent_git_bootstrap_v1.md`
- `docs/agents/role_bootstrap_reference_map_v1.md`
- `contracts/repo/protected_main_truth_maintenance_operating_model_v1.md`
- `contracts/repo/issue_governance_routing_standard_v1.md`
- `contracts/repo/system_integration_escalation_contract_v1.md`
- `docs/agents/si_merge_request_executive_summary_v1.md`
- `docs/agents/agent_registry_v1.md`
- `docs/agents/agent_start_index_v1.md`
- `tools/governance/agent_registry_helper_v1.py` (`--list|--start-command|--validate`)

### Tier 2 — deep history (read-only)
Use only for forensic context:
- `journals/system-integration-normalization/stream_v1.md` through `stream_v5.md`
- superseded docs listed in `contracts/repo/superseded_documents_index_v1.md`
- older onboarding/index generations (`v1..v6`) and archived SI optimization notes

Active startup paths must not require Tier-2 files.

## Meta-freeze rule
Do not add new dashboards/prompts/boards/summaries/exchange artifacts unless replacing an existing canonical artifact in the same PR.

## Acceptance criteria for onboarding hardening packages
- Tier 0 safe-start target: `< 5 minutes`
- Tier 1 working-context target: `< 15 minutes`
- active read path materially reduced vs legacy long-chain startup
- no ambiguity between active truth and historical material in startup references

## Locked operating rules
- `main` is protected truth and owner-only merge authority
- SI/governance changes use dedicated `si/<topic>` branch, then PR to `main`
- branch name `work` is invalid for SI-governance truth mutation
- if stream/doc claims conflict with repo state, treat as `repo-truth defect` and repair truth in the same package
- if safe completion is blocked, escalate explicitly instead of fabricating completion
