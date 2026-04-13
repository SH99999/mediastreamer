# CURRENT STATE — scale-radio-autoswitch

## Component
- normalized component name: `scale-radio-autoswitch`
- governed role: analog-input signal detection and tape-monitor style source switching helper
- active work lane: `dev/autoswitch`

## Repo truth
- component branch `dev/autoswitch` exists
- legacy handover already provides concrete script/service mapping into component paths
- component is runtime-validated enough to document clearly, but still not integrated enough for `main` truth

## Lifecycle status
- `payload_complete`
- `functional_acceptance_open`

## Accepted runtime posture
- ALSA amplitude detection via `arecord + sox`
- VINL1 / VINR1 routing on HiFiBerry DAC+ ADC Pro
- authoritative runtime entrypoint: `revox-autoswitch.service`
- asymmetric debounce:
  - engage fast
  - disengage slower

## Current known working behavior
- amplitude polling logic works
- threshold-based switching logic works with the `0.02` baseline
- systemd auto-restart behavior exists
- manual toggle fallback script exists
- component explicitly avoids `mpd.conf` injection and abandons the old loopback strategy

## Current gaps
- previous playback source restore is unresolved
- renderer-visible tape-state export is unresolved
- interaction with future overlay ownership signaling remains unresolved
- long-duration runtime validation is still open
- branch should remain dev-only for now

## Repo-normalized next action
1. add a simple exported tape-active state visible to renderer/overlay consumers
2. decide whether source restore belongs here or in a source-engine layer
3. add card-index detection fallback if needed
4. only after that consider promotion beyond the dev lane
