# STREAM — system_integration_normalization

Status note: this v3 file supersedes `stream_v2.md` as the current SI/N stream because target deploy/test exclusivity and lock-aware workflow alignment materially changed the operating model after the earlier v2 alignment snapshot.

## Entries
### 2026-04-12 / main / PR #26 merged
- governance v2 docs landed on `main`
- the first repo-native SI/N status and decision files were added
- purpose: move SI/N truth out of placeholder docs and into repo form

### 2026-04-13 / main / PR #31 merged
- branch doctrine, component artifact model, and naming/release numbering standards were added
- purpose: stop recurring branch and multi-artifact ambiguity

### 2026-04-13 / main / PR #32 merged
- repo-level agent onboarding files and skills were added
- purpose: reduce repeated context rebuilding for future agent work

### 2026-04-13 / main / PR #33 merged
- canonical governance source precedence and overlay contract docs were added
- purpose: reduce doctrine conflicts and give overlay behavior a formal governance home

### 2026-04-13 / main / PR #35 merged
- governance CI wording was corrected after a brittle text-match failure
- purpose: keep governance checks usable against real repo wording

### 2026-04-13 / main / PR #36 merged
- initial component current-state and stream journals were added for Bridge, Tuner, Starter, AutoSwitch, Fun Line, and Hardware
- purpose: move active component handoff memory into repo-native journals

### 2026-04-13 / main / PR #37 merged
- missing tuner current-state journal gap was closed
- purpose: restore journal completeness for active components

### 2026-04-13 / main / PR #38 merged
- stub component READMEs were replaced with short governed component overviews
- purpose: improve human and agent pickup quality at component roots

### 2026-04-13 / main / PR #39 merged
- CI checks for active component journals and READMEs were added
- purpose: turn journal discipline into repo-enforced hygiene

### 2026-04-14 / main / PR #40 merged
- process docs for technology changes, component interdependency mapping, repo-truth cleanup backlog, and status/decision review cadence were added
- purpose: normalize liveable interdependency handling and active review discipline

### 2026-04-14 / main / PR #41 merged
- SI recovery onboarding and continuity docs were added
- purpose: reduce chat-loss risk and keep SI/N operating memory inside Git

### 2026-04-14 / main / PR #42 merged
- corrected new-component intake governance and SI doctrine updates were added
- purpose: make new component bootstrap repeatable and repo-native

### 2026-04-14 / main / PR #43 merged
- remaining intake follow-up docs and AGENTS replacement notes were added
- purpose: close gaps left behind by the earlier intake merge sequence

### 2026-04-14 / main / PR #44 merged
- AGENTS references were updated
- purpose: reduce stale onboarding pointers

### 2026-04-14 / main / PR #46 merged
- old AGENTS bootstrap wording was removed
- purpose: avoid pointing future chats at outdated intake behavior

### 2026-04-14 / main / PR #48 merged
- one-click rebase workflow for `dev/*` and `integration/*` branches was added
- purpose: reduce manual branch alignment work

### 2026-04-14 / main / PR #50 merged
- weekly governance report issue workflow was added
- purpose: create a repo-native recurring oversight loop

### 2026-04-14 / main / PR #52 merged
- issue governance routing and automation workflows were added
- purpose: turn repo truth into a managed operating queue

### 2026-04-14 / main / PR #53 merged
- governance closeout workflow was added
- purpose: close the issue loop after merges

### 2026-04-14 / main / PR #55 merged
- autonomy layer, escalation workflows, and repo sanity controls were added
- purpose: move toward lower-admin autonomous execution from repo truth

### 2026-04-14 / main / PR #57 and PR #58 merged
- intake and PR routing behavior was corrected
- purpose: keep label-driven automation responsive to real events

### 2026-04-14 / main / PR #60 merged
- corrected issue-intake normalizer v2 was added
- purpose: unblock the first live governance-loop validation

### 2026-04-14 / main / PR #61 merged
- first live governance-loop validation was recorded
- purpose: confirm the governed demand path is active in repo truth

### 2026-04-14 / si-alignment-v1 / current branch
- SI governance index v5 was added
- protected-main truth maintenance operating model was added
- SI recovery onboarding v5 was added
- SI status v6 and decisions v6 were added
- stream v2 and `ag_new.txt` were created to align protected-main SI truth under connector mutation limits
- purpose: align SI repo truth to the locked public/protected-main operating model

### 2026-04-14 / si-alignment-v1 / current branch / deploy exclusivity follow-up
- deploy target exclusivity standard was added
- lock-aware deploy, rollback, explicit release, and autonomous orchestrator workflow generations were added
- the Pi target state model `free`, `deploying`, `test_open`, `rollback_running`, and `blocked` was locked as repo truth
- SI status v7 and decisions v7 were added
- purpose: prevent overlapping deploy/test windows on the same target Pi and preserve valid runtime acceptance evidence
