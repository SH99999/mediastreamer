# STREAM — scale-radio-tuner

Historical note: `stream_v2.md` is the active tuner stream. Keep this v1 file read-only for historical context.

- 2026-04-13: Initial repo journal created from legacy tuner status and decision handover.
- 2026-04-13: Tuner normalized as one component with multiple artifacts: overlay, source, and resident renderer service.
- 2026-04-13: Authoritative tuner baseline recorded as the resident-renderer lineage culminating in `1.10.2`.
- 2026-04-13: Locked public method contract and fixed `scale_fm_renderer.service` naming carried into repo truth.
- 2026-04-13: Shared overlay-owner handling via `/tmp/mediastreamer_active_overlay.json` recorded as governed behavior.
- 2026-04-13: Remaining gaps recorded as runtime validation, first-show pointer sweep, exit white flashes, pointer jitter, and incomplete OE1 cleanup.

- 2026-04-15: Revalidated active tuner deploy scope on `dev/tuner` as `tuner:runtime` (`radio_scale_peppy`) plus `tuner:service` (`scale_fm_renderer.service`); `tuner:source_tile` (`radio_scale_source`) remains hardware-governed and out of deploy-lane scope.
- 2026-04-15: Tuned pointer smoothing defaults for more fluid motion (higher follow/lock gain, smaller visual/pixel deadbands), added renderer overlay-owner poll throttling for lower hidden-loop overhead, and added a startup dark guard frame on visibility switch to reduce white flash during overlay open.
