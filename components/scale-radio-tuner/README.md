# Scale Radio Tuner

## Purpose
Scale Radio Tuner is the governed radio-scale experience component for Volumio, including the tuner overlay, source-entry artifact, and resident renderer service.

## Current role
- governed component: `scale-radio-tuner`
- current work lane: `dev/tuner`
- active artifacts:
  - `Scale FM Overlay`
  - `Scale FM Source`
  - `scale_fm_renderer.service`
- current authoritative baseline: `1.10.2`

## Boundaries
This component owns the tuner-visible experience and its source-entry/runtime path.
It does not own Fun Line itself, autoswitch logic, or broader frontpanel-engine scope.

## Current focus
- validate the `1.10.2` baseline on target Pi
- preserve the fixed public method contract and service name
- verify deep-idle and owner-arbitration behavior
- reduce first-show pointer sweep, exit white flashes, and pointer jitter

## See also
- `journals/scale-radio-tuner/current_state_v1.md`
- `journals/scale-radio-tuner/stream_v1.md`
- `contracts/repo/component_artifact_model_v1.md`
