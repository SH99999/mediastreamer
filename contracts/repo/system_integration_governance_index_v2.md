# SYSTEM INTEGRATION GOVERNANCE INDEX V2

## Purpose
This file is the current entrypoint for system integration governance, recovery, journal truth, and new-component intake.

## Directory roles
- `contracts/repo/` = canonical governance and operating doctrine
- `journals/` = factual current-state and append-only change memory
- `docs/agents/` = agent-facing onboarding and recovery material

## Read order
1. `AGENTS.md`
2. `contracts/repo/branch_strategy_v2.md`
3. `contracts/repo/component_artifact_model_v1.md`
4. `contracts/repo/naming_and_release_numbering_standard_v1.md`
5. `contracts/repo/release_intake_and_delivery_status_v2.md`
6. `contracts/repo/component_journal_policy_v2.md`
7. `contracts/repo/new_component_intake_standard_v1.md`
8. `contracts/repo/system_integration_chat_setup_and_working_agreements_v1.md`
9. `contracts/repo/chatgpt_github_connection_model_v1.md`
10. `docs/agents/system_integration_recovery_onboarding_v2.md`
11. `journals/system-integration-normalization/STATUS_system_integration_normalization_v3.md`
12. `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v3.md`
13. `journals/system-integration-normalization/stream_v1.md`

## Working rule
- governance truth must live in the repo, not only in chat memory
- system integration changes should leave a trail in governance docs and SI journals
- new components should use the standard intake path instead of ad-hoc structure
