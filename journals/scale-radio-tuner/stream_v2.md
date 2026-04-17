# STREAM — scale-radio-tuner

Status note: this v2 file supersedes `stream_v1.md` as the current tuner stream because the repository now has a real manual deploy/rollback lane for the imported `1.10.2` tuner payload.

## Entries
- 2026-04-13: Initial repo journal created from legacy tuner status and decision handover.
- 2026-04-13: Tuner normalized as one component with multiple artifacts rather than separate branches per plugin.
- 2026-04-13: Authoritative overlay/render baseline recorded as `1.10.2`.
- 2026-04-13: Repo truth recorded that tuner did not yet have the same repo-driven deploy maturity as bridge.
- 2026-04-15: Verified that the imported tuner payload already exists in repo at `components/scale-radio-tuner/payload/current/` and contains the `radio_scale_peppy` overlay runtime, renderer scripts, and `scale_fm_renderer.service`.
- 2026-04-15: Added real deploy candidate scripts under `components/scale-radio-tuner/deploy_candidates/` for apply, runtime healthcheck, and rollback.
- 2026-04-15: Added generic wrapper support for tuner via `tools/deploy/sr-deploy-wrapper-v3.sh`.
- 2026-04-15: Added manual workflow generation `component-test-deploy-v10.yml` and `component-test-rollback-v10.yml` so tuner can now enter the same lock-aware Pi test-slot model as bridge.
- 2026-04-15: Kept the separate `radio_scale_source` artifact explicit as a remaining deploy-lane gap instead of pretending the full multi-artifact tuner contract is already imported.
- 2026-04-15: Added non-interactive privileged execution support for tuner deploy/rollback through `PI_SUDO_PASSWORD` on the runner.
- 2026-04-15: Manual tuner deploy succeeded on the target Pi.
- 2026-04-15: Manual tuner rollback succeeded on the target Pi.
- 2026-04-15: Autonomous delivery matrix v3 now marks tuner as supported with `dev/tuner` + `current` defaults and v10 deploy/rollback workflows.
- 2026-04-15: Shared wrapper compatibility was expanded so `tools/deploy/sr-deploy-wrapper-v2.sh` now resolves and executes tuner deploy/rollback contracts, not only bridge.
- 2026-04-15: Tuner artifact-role language was normalized in current-state (`tuner:runtime`, `tuner:service`, `tuner:source_tile`) to keep multi-artifact acceptance explicit.
- 2026-04-15: Scope decision recorded that source-project behavior remains hardware-governed (encoder short/long press) and therefore out of deploy-lane scope until full integration is explicitly opened.
- 2026-04-15: Revalidated active tuner deploy scope on `dev/tuner` as `tuner:runtime` (`radio_scale_peppy`) plus `tuner:service` (`scale_fm_renderer.service`); `tuner:source_tile` (`radio_scale_source`) remains hardware-governed and out of deploy-lane scope.
- 2026-04-15: Tuned pointer smoothing defaults for more fluid motion (higher follow/lock gain, smaller visual/pixel deadbands), added renderer overlay-owner poll throttling for lower hidden-loop overhead, and added a startup dark guard frame on visibility switch to reduce white flash during overlay open.
- 2026-04-16: Normalized lifecycle vocabulary to canonical taxonomy (`tested_on_pi`) and added an evidence-led claim ledger so runtime/rollback/autonomy claims stay aligned with matrix + status packet truth.
