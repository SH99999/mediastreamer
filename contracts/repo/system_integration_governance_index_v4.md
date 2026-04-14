# SYSTEM INTEGRATION GOVERNANCE INDEX V4

## Purpose
This file is the current entrypoint for system integration governance, recovery, issue routing, and autonomous execution doctrine.

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
6. `contracts/repo/component_journal_policy_v2.md`
7. `contracts/repo/new_component_intake_standard_v2.md`
8. `contracts/repo/issue_governance_routing_standard_v1.md`
9. `contracts/repo/autonomous_execution_and_chat_intake_standard_v1.md`
10. `contracts/repo/system_integration_escalation_contract_v1.md`
11. `contracts/repo/system_integration_chat_setup_and_working_agreements_v1.md`
12. `contracts/repo/chatgpt_github_connection_model_v1.md`
13. `docs/agents/system_integration_recovery_onboarding_v4.md`
14. `journals/system-integration-normalization/STATUS_system_integration_normalization_v5.md`
15. `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v5.md`
16. `journals/system-integration-normalization/stream_v1.md`

## Working rule
- governance truth must live in the repo, not only in chat memory
- system integration changes should leave a trail in governance docs and SI journals
- new work intake, issue routing, escalation, and autonomous execution must use the governed repo model instead of ad-hoc chat memory
