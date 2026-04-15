# STREAM — scale-radio-fun-line

- 2026-04-13: Initial repo journal created from legacy fun-line status and decision handover.
- 2026-04-13: Fun Line normalized as an overlay / experience-layer component, not a core renderer or ownership-master component.
- 2026-04-13: `0.4.2` recorded as the only authoritative runtime baseline.
- 2026-04-13: Hard coordination rule recorded: Fun Line and Radio Scale must not run as two heavy active renderers at the same time.
- 2026-04-13: Dog Line recorded as the first production actor to carry forward.
- 2026-04-13: Repo payload normalization and config/importer revalidation remain open tasks.

- 2026-04-15: Added repo deploy candidate scripts (`apply_payload_v1.sh`, `healthcheck_runtime_v1.sh`, `remove_active_v1.sh`) for Fun Line under `components/scale-radio-fun-line/deploy_candidates/`.
- 2026-04-15: Added governed payload pointer `components/scale-radio-fun-line/payload/current/` so lock-aware v10 deploy and rollback workflows can be executed for Fun Line testing.
- 2026-04-15: Enabled wrapper support for `fun-line` in `sr-deploy-wrapper-v2.sh` and `sr-deploy-wrapper-v3.sh` with `current_dev|current -> current` alias resolution.
- 2026-04-15: Updated autonomous delivery matrix v3 to include `fun-line` with `dev/fun-line` + `current` defaults and v10 workflow bindings.
- 2026-04-15: Replaced metadata-only plugin entrypoint with a real controller export (`ControllerFunLineaOverlay`) and lifecycle handlers (`onVolumioStart`, `onStart`, `onStop`, `getUIConfig`) to satisfy runtime initialization expectations.
