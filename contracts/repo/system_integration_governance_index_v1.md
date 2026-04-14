# SYSTEM INTEGRATION GOVERNANCE INDEX V1

## Purpose
This file is the stable entrypoint for system integration / normalization governance, recovery, and journal truth.

## Directory roles
- `contracts/repo/` = canonical governance and operating doctrine
- `journals/` = factual current-state and append-only change memory
- `docs/agents/` = agent-facing onboarding, skills, and recovery material

## Read order for a replacement chat
1. `AGENTS.md`
2. `contracts/repo/branch_strategy_v2.md`
3. `contracts/repo/component_artifact_model_v1.md`
4. `contracts/repo/naming_and_release_numbering_standard_v1.md`
5. `contracts/repo/release_intake_and_delivery_status_v2.md`
6. `contracts/repo/component_journal_policy_v2.md`
7. `contracts/repo/system_integration_chat_setup_and_working_agreements_v1.md`
8. `contracts/repo/chatgpt_github_connection_model_v1.md`
9. `docs/agents/system_integration_recovery_onboarding_v1.md`
10. `journals/system-integration-normalization/STATUS_system_integration_normalization_v2.md`
11. `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v2.md`
12. `journals/system-integration-normalization/stream_v1.md`

## Active component journal map
- `journals/scale-radio-bridge/current_state_v1.md`
- `journals/scale-radio-bridge/stream_v1.md`
- `journals/scale-radio-tuner/current_state_v1.md`
- `journals/scale-radio-tuner/stream_v1.md`
- `journals/scale-radio-starter/current_state_v1.md`
- `journals/scale-radio-starter/stream_v1.md`
- `journals/scale-radio-autoswitch/current_state_v1.md`
- `journals/scale-radio-autoswitch/stream_v1.md`
- `journals/scale-radio-fun-line/current_state_v1.md`
- `journals/scale-radio-fun-line/stream_v1.md`
- `journals/scale-radio-hardware/current_state_v1.md`
- `journals/scale-radio-hardware/stream_v1.md`

## System integration journal map
- `journals/system-integration-normalization/STATUS_system_integration_normalization_v1.md`
- `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v1.md`
- `journals/system-integration-normalization/STATUS_system_integration_normalization_v2.md`
- `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v2.md`
- `journals/system-integration-normalization/stream_v1.md`

## Working rule
- governance truth must live in the repo, not only in chat memory
- system integration changes should leave a trail in governance docs and SI journals
- a new chat should start from these files before proposing repo-control-plane changes
