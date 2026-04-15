# STREAM — system_integration_normalization

Status note: this v6 file supersedes `stream_v5.md` as the current SI/N stream because tuner now has a real repo-driven manual deploy/rollback lane after Bridge proved the lock-aware runtime path on the Pi.

## Entries
### 2026-04-12 / main / PR #26 merged
- governance v2 docs landed on `main`
- the first repo-native SI/N status and decision files were added
- purpose: move SI/N truth out of placeholder docs and into repo form

### 2026-04-13 to 2026-04-14 / main / merged governance sequence
- branch doctrine, artifact model, naming/release numbering, SI recovery onboarding, issue governance, weekly governance reports, autonomy layer, escalation workflows, and repo sanity controls were added across the governance build-out sequence
- purpose: convert the repository into an issue-driven, workflow-backed control plane

### 2026-04-14 / main / PR #62 merged
- protected-main truth maintenance operating model was added
- SI status v6, decisions v6, and stream v2 were added
- purpose: align SI truth to the locked public + protected-main operating model

### 2026-04-15 / main / follow-up SI truth alignment
- truthful execution and negative-answer rule was added to governed repo doctrine
- Git release tagging standard was added
- governance index and recovery onboarding were refreshed to the active SI truth chain
- purpose: keep repo truth trustworthy and keep replacement SI chats on the active document chain

### 2026-04-15 / main / Bridge validation follow-up
- bridge deploy pointer resolution and lock-aware rollback recovery fixes landed through PR #67
- bridge deploy and rollback were then validated on the target Pi
- purpose: prove the lock-aware deploy/test slot model with one real reference component

### 2026-04-15 / tuner-deploy-lane-1 / current branch
- verified that the imported tuner payload already exists in repo at `components/scale-radio-tuner/payload/current/`
- replaced the old placeholder tuner deploy hooks with real deploy candidate scripts under `components/scale-radio-tuner/deploy_candidates/`
- added `tools/deploy/sr-deploy-wrapper-v3.sh` so bridge and tuner can both use the generic wrapper family
- added `component-test-deploy-v10.yml` and `component-test-rollback-v10.yml` for manual tuner validation on the target Pi
- updated tuner current-state and stream truth to reflect the new deploy lane and the still-open `radio_scale_source` gap
- updated SI status to reflect that bridge is validated and tuner is now a real manual deploy candidate awaiting Pi validation
- purpose: move the next active component from legacy placeholder deploy doctrine into an actually executable repo-driven lane without pretending Pi validation already happened
