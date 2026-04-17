# ROLE BOOTSTRAP REFERENCE MAP V1

## Purpose
Reduce cross-reference maintenance by providing one canonical pointer map for mode-B bootstrap profiles.

## Single-source links
- role pack definitions: `docs/agents/role_bootstrap_profiles_v1.md`
- bootstrap command contract: `docs/agents/agent_git_bootstrap_v1.md`
- SI/global governance index: `contracts/repo/system_integration_governance_index_v7.md`

## Shared deferred references (all roles)
- `docs/agents/status_prompt_reports_v1.md`
- `contracts/repo/release_intake_and_delivery_status_v2.md`

## Role-specific entrypoints
### tuner
- startup state source: `journals/scale-radio-tuner/current_state_v2.md`
- stream source: `journals/scale-radio-tuner/stream_v2.md`

### bridge
- startup state source: `journals/scale-radio-bridge/current_state_v1.md`
- stream source: `journals/scale-radio-bridge/stream_v1.md`

### hardware
- startup state source: `journals/scale-radio-hardware/current_state_v1.md`
- stream source: `journals/scale-radio-hardware/stream_v1.md`

### fun-line
- startup state source: `journals/scale-radio-fun-line/current_state_v1.md`
- stream source: `journals/scale-radio-fun-line/stream_v1.md`

### autoswitch
- startup state source: `journals/scale-radio-autoswitch/current_state_v1.md`
- stream source: `journals/scale-radio-autoswitch/stream_v1.md`

### ux
- startup governance source: `contracts/repo/ui_gui_governance_standard_v1.md`
- stream source: `journals/system-integration-normalization/ui_gui_stream_v1.md`

### system-integration / governance
- startup governance source: `contracts/repo/system_integration_governance_index_v7.md`
- onboarding source: `docs/agents/system_integration_recovery_onboarding_v7.md`
- owner handoff source: `docs/agents/si_merge_request_executive_summary_v1.md`
- active-truth chain source: `AGENTS.md` -> `system_integration_governance_index_v7.md` -> `si_target_operating_model_v1.md` -> current SI status/decisions/stream
- tier map source (authoritative): Tier 0/1/2 definitions in `docs/agents/system_integration_recovery_onboarding_v7.md`

### generic
- default governance source: `contracts/repo/system_integration_governance_index_v7.md`

## Maintenance rule
When role packs change, update this map first and then update role profiles so bootstrap mode-B can keep a single stable deferred pointer.
