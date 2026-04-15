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
- 2026-04-15: Tuner was promoted into the autonomous delivery matrix with `dev/tuner` and payload `current` as the governed defaults.
