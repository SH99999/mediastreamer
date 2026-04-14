# SYSTEM INTEGRATION CHAT SETUP AND WORKING AGREEMENTS V1

## Purpose
This file documents the current setup, role, and working agreements of the system integration / normalization lane so that another chat can continue without rebuilding the operating model from memory.

## Current role of this lane
System integration / normalization is responsible for:
- git management and repo-control-plane changes
- branch doctrine and branch hygiene
- workflow model and deploy/rollback semantics
- repository governance and document normalization
- cross-component consistency and handoff quality

This lane is not the owner of detailed specialist feature implementation inside Bridge, Tuner, Starter, AutoSwitch, Fun Line, or Hardware.

## Current repository footing
- repository: `SH99999/mediastreamer`
- canonical truth branch: `main`
- active component branches currently recognized:
  - `dev/bridge`
  - `dev/tuner`
  - `dev/starter`
  - `dev/autoswitch`
  - `dev/fun-line`
  - `dev/hardware`
- open governance/process work known at the time of writing:
  - PR `#40` from branch `process-v1` is open and contains process docs for technology change handling, component interdependency mapping, repo-truth cleanup backlog, and status/decision review cadence

## Current operational baseline
- `main` is the operator-visible control plane for workflows, governance, contracts, and accepted stable repo truth
- active component work belongs on `dev/<component>` unless governance explicitly promotes that component block to `main`
- deployment uses clean-replace semantics, not update-in-place
- deploy and rollback workflows live on `main` and operate against a selected `git_ref`
- the repo-shipped wrapper model is the accepted workflow entrypoint model
- rollback for plugin-based components must also handle Volumio plugin unregistration when relevant

## Established git process
1. identify whether the change is component-local or repo-control-plane
2. make repo-control-plane and governance changes in a dedicated working branch
3. keep change scope reviewable and explicit
4. open a PR to `main`
5. operator review/approval/merge remains the acceptance gate
6. after merge, keep active `dev/<component>` branches aligned to current `main` whenever practical
7. whenever repo truth changes materially, update the matching governance and journal files

## Documentation agreements established here
- governance doctrine belongs in `contracts/repo/`
- system integration journals belong in `journals/system-integration-normalization/`
- agent-recovery and onboarding material belongs in `docs/agents/`
- repo-facing documentation is in English
- chat memory alone is not sufficient for operational truth
- if a working rule matters later, it should be written into the repo

## Journal agreements established here
- SI/N must maintain repo-native status, decisions, and stream files
- active components must keep `current_state_v1.md` and `stream_v1.md`
- stream files should stay factual and append-only
- current-state files should reflect tested reality, not intention

## Replacement-chat rule
A replacement chat should not start by inventing new structure, renaming governance paths, or replaying old debates from memory.

It should first read the governance index, onboarding file, and SI journals, then inspect current open PRs and active branches, and only then propose further repo changes.

## Immediate unresolved areas
- PR `#40` is still pending review and merge
- non-bridge deploy maturity is still uneven
- some repo-truth cleanup and superseded-document cleanup still remain
- governance and journal discipline should continue to be tightened without creating parallel doctrine tracks
