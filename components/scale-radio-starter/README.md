# Scale Radio Starter

## Purpose
Scale Radio Starter governs the accepted startup/runtime glue baseline for MediaStreamer on top of the existing Volumio / touch_display / kiosk stack.

## Current role
- governed component: `scale-radio-starter`
- current work lane: `dev/starter`
- accepted stable baseline:
  - `mediastreamer_bootdelay_fix_v0.1.0`
  - `mediastreamer_hybrid_startup_standby_v0.2.2_stable`

## Boundaries
This component owns startup glue, boot handover, and the accepted hybrid runtime control surface.
It does not own final appliance-grade startup visuals or imply that deep-idle / FPS-cap / render-throttling are already solved here.

## Current focus
- preserve the accepted stable baseline
- keep `4004` as preferred handover target and `3000` as fallback
- keep `mediastreamer-shellctl standby|wake|status` as the runtime control contract
- archive later appliance/direct-now-playing variants as nonleading experiments only

## See also
- `journals/scale-radio-starter/current_state_v1.md`
- `journals/scale-radio-starter/stream_v1.md`
