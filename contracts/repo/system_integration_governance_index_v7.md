# SYSTEM INTEGRATION GOVERNANCE INDEX V7

## Purpose
This file is the current entrypoint for system integration governance, recovery, issue routing, autonomous execution doctrine, and the locked operating model for protected-`main` repo truth.

## Directory roles
- `contracts/repo/` = canonical governance and operating doctrine
- `journals/` = factual current-state and append-only change memory
- `docs/agents/` = agent-facing onboarding and recovery material
- `tools/governance/` = machine-readable governance support data used by workflows

## Read order
1. `AGENTS.md`
2. `contracts/repo/branch_strategy_v2.md`
3. `contracts/repo/component_artifact_model_v1.md`
4. `contracts/repo/naming_and_release_numbering_standard_v1.md`
5. `contracts/repo/release_intake_and_delivery_status_v2.md`
6. `contracts/repo/status_taxonomy_contract_v1.md`
7. `contracts/repo/status_packet_reporting_contract_v1.md`
8. `contracts/repo/governance_source_registry_standard_v1.md`
9. `contracts/repo/si_branch_scope_guard_standard_v1.md`
10. `contracts/repo/component_journal_policy_v2.md`
11. `contracts/repo/new_component_intake_standard_v2.md`
12. `contracts/repo/issue_governance_routing_standard_v1.md`
13. `contracts/repo/autonomous_execution_and_chat_intake_standard_v1.md`
14. `contracts/repo/system_integration_escalation_contract_v1.md`
15. `contracts/repo/protected_main_truth_maintenance_operating_model_v1.md`
16. `contracts/repo/deploy_target_exclusivity_standard_v1.md`
17. `contracts/repo/deploy_process_standard_v1.md`
18. `contracts/repo/ui_gui_governance_standard_v1.md`
19. `contracts/repo/truthful_execution_and_negative_answer_standard_v1.md`
20. `contracts/repo/git_release_tagging_standard_v1.md`
21. `contracts/repo/governance_unification_delivery_plan_v1.md`
22. `contracts/repo/ui_ux_stage_b_autonomous_loop_standard_v1.md`
23. `contracts/repo/deployment_test_strategy_standard_v1.md`
24. `contracts/repo/owner_decision_click_automation_standard_v1.md`
25. `contracts/repo/owner_decision_scoring_and_rollback_contract_v1.md`
26. `contracts/repo/chatgpt_git_exchange_operating_standard_v1.md`
27. `docs/agents/agent_git_bootstrap_v1.md`
28. `docs/agents/status_prompt_reports_v1.md`
29. `docs/agents/system_integration_recovery_onboarding_v7.md`
30. `docs/agents/owner_operational_reference_v1.md`
31. `docs/agents/si_merge_request_executive_summary_v1.md`
32. `docs/agents/chatgpt_git_exchange_playbook_v1.md`
33. `journals/system-integration-normalization/STATUS_system_integration_normalization_v8.md`
34. `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v9.md`
35. `journals/system-integration-normalization/stream_v6.md`
36. `journals/system-integration-normalization/ui_gui_stream_v1.md`
37. `tools/governance/scale_radio_governance_delivery_views_v1.md`


## Locked operating model
- the repository remains public until further notice
- `main` remains the protected truth branch
- agents and chats work on non-`main` branches
- SI/governance changes must use a dedicated `si/<topic>` branch (not generic branch names), then push that branch and open/update a PR to `main`
- PR lifecycle execution (create/update/rebase/respond) is owned by agents/chats/Codex lanes; owner role is decision/acceptance, not PR authoring
- delivery expectation is `local -> github.com branch -> PR to main` prepared by agents/chats/Codex so owner can use one-click decision flow
- SI handoff must include a prepared merge-request executive summary comment with executive summary + risk level + rollback command + next owner click
- ChatGPT exchange for audit/demand loops should use the governed exchange root `exchange/chatgpt/` with inbox/outbox artifact flow
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
