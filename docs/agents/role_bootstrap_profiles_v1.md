# ROLE BOOTSTRAP PROFILES V1

## Purpose
Provide role-oriented startup packs for bootstrap mode-B so onboarding becomes faster without losing governance-critical information.

## Mode model
- `classic`: full standard read-order expectation
- `mode-b`: need-to-know startup packet + deferred packet pointer

Mode-B is optimization only. It does not relax branch doctrine, protected-`main` rules, or owner merge authority.

## Common startup packet (all roles)
1. `AGENTS.md`
2. `tools/governance/agent_git_bootstrap_v1.sh`
3. `docs/agents/agent_git_bootstrap_v1.md`

## Role packets
### tuner
- branch hint: `dev/tuner`
- startup add-on:
  - `journals/scale-radio-tuner/current_state_v2.md`
- deferred packet:
  - `journals/scale-radio-tuner/stream_v2.md`
  - `docs/agents/status_prompt_reports_v1.md`
  - `contracts/repo/release_intake_and_delivery_status_v2.md`

### bridge
- branch hint: `dev/bridge`
- startup add-on:
  - `journals/scale-radio-bridge/current_state_v1.md`
- deferred packet:
  - `journals/scale-radio-bridge/stream_v1.md`
  - `docs/agents/status_prompt_reports_v1.md`
  - `contracts/repo/release_intake_and_delivery_status_v2.md`

### system-integration / governance
- branch hint: `si/<topic>`
- startup add-on:
  - `contracts/repo/system_integration_governance_index_v7.md`
- deferred packet:
  - `docs/agents/system_integration_recovery_onboarding_v7.md`
  - `docs/agents/owner_operational_reference_v1.md`
  - `docs/agents/si_merge_request_executive_summary_v1.md`

### generic
- branch hint: `si/<topic>` or `dev/<component>`
- startup add-on: none
- deferred packet:
  - `contracts/repo/system_integration_governance_index_v7.md`
  - `docs/agents/status_prompt_reports_v1.md`

## Escalation triggers (mode-B -> full read-order)
Escalate to full read-order immediately if one of the following is true:
1. cross-component or system-wide impact
2. change touches contracts, governance workflows, or protected truth operations
3. branch-scope guard, packet enforcement, source-registry lint, or integration check fails
4. deploy/rollback path is changed

## Evidence expectations
Mode-B still requires:
- truthful bootstrap first reply
- deterministic branch + PR path
- required checks for touched scope
