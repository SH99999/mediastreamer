# Scale Radio AutoSwitch

## Purpose
Scale Radio AutoSwitch monitors analog input level and performs tape-monitor style switching behavior for the HiFiBerry DAC+ ADC Pro path.

## Current role
- governed component: `scale-radio-autoswitch`
- current work lane: `dev/autoswitch`
- authoritative runtime entrypoint: `revox-autoswitch.service`
- active detection model: ALSA amplitude polling via `arecord + sox`

## Boundaries
This component owns signal detection, ADC routing, and service-driven switching behavior.
It does not own renderer visuals, source-tile UX, or MPD configuration rewriting.

## Current focus
- preserve the ALSA polling architecture
- keep VINL1 / VINR1 routing as the approved mixer path
- add renderer-visible tape-state export
- decide ownership for previous-source restore behavior

## See also
- `journals/scale-radio-autoswitch/current_state_v1.md`
- `journals/scale-radio-autoswitch/stream_v1.md`
