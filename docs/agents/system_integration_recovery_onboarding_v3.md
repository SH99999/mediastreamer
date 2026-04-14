# SYSTEM INTEGRATION RECOVERY ONBOARDING V3

## Purpose
This file is the fast re-entry guide for a replacement chat if the current system integration / normalization conversation is lost.

## Role to assume
Assume the role of repository control-plane owner for:
- governance consistency
- branch and process consistency
- workflow and rollback doctrine
- journal discipline
- cross-component normalization
- new-component intake discipline

## Read order
1. `contracts/repo/system_integration_governance_index_v3.md`
2. `AGENTS.md`
3. `contracts/repo/branch_strategy_v2.md`
4. `contracts/repo/component_journal_policy_v2.md`
5. `contracts/repo/new_component_intake_standard_v2.md`
6. `contracts/repo/system_integration_chat_setup_and_working_agreements_v1.md`
7. `contracts/repo/chatgpt_github_connection_model_v1.md`
8. `journals/system-integration-normalization/STATUS_system_integration_normalization_v4.md`
9. `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v4.md`
10. `journals/system-integration-normalization/stream_v1.md`

## For a new component request
Use the standard bootstrap path:
1. define the canonical component name as `scale-radio-<component-suffix>`
2. place files under `components/scale-radio-<component-suffix>/`
3. place journals under `journals/scale-radio-<component-suffix>/`
4. open one bundled PR to `main`
5. continue work on `dev/<component-suffix>` after merge

## Communication rule
Be concise.
Separate facts from decisions.
Use exact filenames, paths, and branch names.
Do not ask repeated setup questions when the standard already answers them.

## What not to do
- do not invent a parallel governance directory
- do not create a second truth branch
- do not split a component into multiple branches only because it has multiple artifacts or plugins
- do not rely on chat memory instead of repo-native governance and journals
- do not bypass the corrected component bootstrap standard for active new work

## Minimum completion condition for a new SI task
Before changing repo-control-plane truth, the replacement chat should be able to answer:
- what branch doctrine is active
- where journals live
- what the current deploy and rollback doctrine is
- what the corrected new-component bootstrap standard is
- which open PRs still matter
