# SYSTEM INTEGRATION RECOVERY ONBOARDING V1

## Purpose
This file is the fast re-entry guide for a replacement chat if the current system integration / normalization conversation is lost.

## Role to assume
Assume the role of repository control-plane owner for:
- governance consistency
- branch/process consistency
- workflow and rollback doctrine
- journal discipline
- cross-component normalization

Do not assume ownership of deep specialist implementation inside component payloads unless the repo state clearly requires it.

## Current repo truth snapshot
- repository: `SH99999/mediastreamer`
- default truth branch: `main`
- active component branches:
  - `dev/bridge`
  - `dev/tuner`
  - `dev/starter`
  - `dev/autoswitch`
  - `dev/fun-line`
  - `dev/hardware`
- current known open governance/process PR at handoff time:
  - PR `#40` from `process-v1`
- current workflow doctrine:
  - workflows live on `main`
  - deploy/rollback operate against a selected `git_ref`
  - clean-replace semantics are required
- currently best-validated deploy lane:
  - Bridge from `dev/bridge`

## Read order
1. `contracts/repo/system_integration_governance_index_v1.md`
2. `AGENTS.md`
3. `contracts/repo/branch_strategy_v2.md`
4. `contracts/repo/component_journal_policy_v2.md`
5. `contracts/repo/system_integration_chat_setup_and_working_agreements_v1.md`
6. `contracts/repo/chatgpt_github_connection_model_v1.md`
7. `journals/system-integration-normalization/STATUS_system_integration_normalization_v2.md`
8. `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v2.md`
9. `journals/system-integration-normalization/stream_v1.md`
10. relevant component `current_state_v1.md` and `stream_v1.md` files

## First actions for a replacement chat
1. verify current open PRs and their merge state
2. verify current active branches and whether any `dev/<component>` branch has drifted behind `main`
3. read SI status, decisions, and stream before proposing new governance
4. read the relevant component journals before touching deployment or rollback doctrine
5. update the repo rather than relying on reconstructed chat memory

## What not to do
- do not invent a parallel governance directory
- do not create a second truth branch
- do not split a component into multiple branches only because it has multiple artifacts or plugins
- do not treat chat memory as stronger than repo-native governance and journal truth
- do not loosen clean-replace or rollback doctrine without explicit repo updates

## Immediate open themes at handoff time
- PR `#40` still needs operator review/approval/merge
- process discipline for technology changes and interdependency handling is being formalized further
- non-bridge deploy maturity is still not as proven as Bridge
- governance cleanup should stay additive and coherent, not fragment into competing documents

## Minimum completion condition for a new SI task
Before changing repo-control-plane truth, the replacement chat should be able to answer:
- what branch doctrine is active
- where the component journals live
- what the current deploy/rollback doctrine is
- which PRs are still open
- which docs are canonical versus merely historical
