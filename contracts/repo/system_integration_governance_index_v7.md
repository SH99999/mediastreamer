# SYSTEM INTEGRATION GOVERNANCE INDEX V7

## Purpose
This file is the current entrypoint for system integration governance, recovery, issue routing, autonomous execution doctrine, and the locked operating model for protected-`main` repo truth.

## Directory roles
- `contracts/repo/` = canonical governance and operating doctrine
- `journals/` = factual current-state and append-only change memory
- `docs/agents/` = agent-facing onboarding and recovery material
- `tools/governance/` = machine-readable governance support data used by workflows

## Active SI truth path (authoritative)
Use this exact path for all active SI startup/onboarding flows:
1. `AGENTS.md`
2. `contracts/repo/system_integration_governance_index_v7.md`
3. `docs/agents/si_target_operating_model_v1.md`
4. `journals/system-integration-normalization/STATUS_system_integration_normalization_v8.md`
5. `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v9.md`
6. `journals/system-integration-normalization/stream_v6.md`

Interpretation rule:
- contracts + current SI status/decisions/stream are authoritative
- reports/issues/dashboards/boards/chat memory are derived/supporting surfaces only
- historical SI stream generations are deep-history only and must not be used as active startup truth

## SI onboarding tiers (derived from authority, not parallel truth)
- Tier 0 (safe-start target `< 5 minutes`): branch/remote preflight + active SI truth path + first actions
- Tier 1 (working-context target `< 15 minutes`): active status/decisions/stream + currently enforced operating constraints
- Tier 2 (deep history): older stream generations, superseded docs, and historical addenda for forensic context only

## Meta-freeze rule (stabilization guard)
Do not add new dashboards/prompts/boards/summaries/exchange artifacts unless replacing an existing canonical artifact in the same PR.
Post-freeze rule: no new governance/process/dashboard/board/prompt/meta-layer expansion packages after `si/review-ready-handoff-marker-and-governance-freeze-v1`, except bugfixes/regression fixes/small necessary corrections/direct appliance-delivery support.

## Extended reference set (Tier-1/Tier-2 only; not part of active startup chain)
Use `docs/agents/system_integration_recovery_onboarding_v7.md` as the canonical tier map.
Do not require extended references before Tier-0 safe-start is complete.

Core Tier-1 references:
1. `docs/agents/agent_git_bootstrap_v1.md`
2. `docs/agents/role_bootstrap_reference_map_v1.md`
3. `contracts/repo/protected_main_truth_maintenance_operating_model_v1.md`
4. `contracts/repo/issue_governance_routing_standard_v1.md`
5. `contracts/repo/system_integration_escalation_contract_v1.md`
6. `docs/agents/si_merge_request_executive_summary_v1.md`
7. `contracts/repo/chatgpt_git_exchange_operating_standard_v1.md`
8. `docs/agents/chatgpt_git_exchange_playbook_v1.md`
9. `docs/agents/chatgpt_capture_to_demand_prompt_v1.md`
10. `docs/agents/chatgpt_owner_quickstart_v1.md`

Tier-2 deep-history references are read-only and listed in:
- `contracts/repo/superseded_documents_index_v1.md`
- `docs/agents/system_integration_recovery_onboarding_v7.md`


## Locked operating model
- the repository remains public until further notice
- `main` remains the protected truth branch
- agents and chats work on non-`main` branches
- SI/governance changes must use a dedicated `si/<topic>` branch (not generic branch names), then push that branch and open/update a PR to `main`
- PR lifecycle execution (create/update/rebase/respond) is owned by agents/chats/Codex lanes; owner role is decision/acceptance, not PR authoring
- delivery expectation is `local -> github.com branch -> PR to main` prepared by agents/chats/Codex so owner can use one-click decision flow
- SI handoff must include a prepared merge-request executive summary comment with executive summary + risk level + rollback command + next owner click
- ChatGPT exchange for audit/demand loops should use the governed exchange root `exchange/chatgpt/` with inbox/outbox artifact flow
- Chat-to-demand continuity is mandatory: relevant chat outcomes must be captured to `exchange/chatgpt/sessions/` within 5 minutes, then promoted to `exchange/chatgpt/demands/` at owner command `ship to codex` (internal `chatok`)
- owner review pickup command is `review now`, resolved from demand artifacts marked `ready-for-chatgpt-review`
- Chat execution-gate classification is mandatory for demand/idea items: `now | quick_win | backlog` with promotion rationale and related outputs preserved in repo truth
- execution-gate labels are standardized for owner query/indexing: `gate:now`, `gate:quick-win`, `gate:backlog`
- owner repo-truth queries should be answerable from labels + canonical repo artifacts with direct Git links (no custom-field dependency required)
- agent status reporting should emit `status_packet_v1` payloads and render markdown from packet data for owner-facing views
- `next_owner_click` should be present in all generated status views and validated by enforcement checks
- decision scoring fields and rollback one-click action contract should be present in decision/status packets (`evidence_quality`, `rollback_readiness`, `blast_radius`, `confidence`, `rollback_action`)
- governance source registry should stay authoritative and duplicate-authority lint checks should remain active
- SI branch-scope guard should block governed file mutations from non-`si/*` branches (warn-only mode allowed with `SI_BRANCH_GUARD_ENFORCE=false`)
- owner remains the only merge authority for protected `main` after governance validation gates pass
- after each merge to `main`, all active `si/*`, `dev/*`, and `integration/*` branches must be rebased/refreshed and agents/chats must run bootstrap refresh before further mutations
- merged short-lived `si/*` branches should be deleted after merge unless an explicit retention exception is documented (rollback remains available via `main` revert path)
- deploy/test happens from those branches
- accepted work merges to `main` only after packaged review, owner coordination, and owner acceptance
- journals, decisions, and streams remain mandatory repo truth

## Working rule
- governance truth must live in the repo, not only in chat memory
- system integration changes should leave a trail in governance docs and SI journals
- new work intake, issue routing, escalation, and autonomous execution must use the governed repo model instead of ad-hoc chat memory
- when tooling, connector, access, or other technical execution problems block safe completion, agents must escalate and inform instead of improvising or silently creating partial repo truth
