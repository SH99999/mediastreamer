# Scale Radio Fun Line

## Purpose
Scale Radio Fun Line is the non-core overlay / experience-layer component for fun-mode visuals over the existing MediaStreamer / Volumio runtime.

## Current role
- governed component: `scale-radio-fun-line`
- current work lane: `dev/fun-line`
- authoritative runtime baseline: `0.4.2`
- first production actor to carry forward: Dog Line

## Boundaries
This component is an overlay / experience layer.
It is not a core renderer, playback engine, or ownership-master component.

## Current focus
- preserve the `0.4.2` runtime baseline
- keep open/close/encoder/GPIO hooks stable
- avoid two simultaneously heavy active renderers with Radio Scale
- reintroduce only one production visual pass first: Dog Line

## Deploy contract paths
- payload pointer: `components/scale-radio-fun-line/payload/current/`
- deploy candidates:
  - `components/scale-radio-fun-line/deploy_candidates/apply_payload_v1.sh`
  - `components/scale-radio-fun-line/deploy_candidates/healthcheck_runtime_v1.sh`
  - `components/scale-radio-fun-line/deploy_candidates/remove_active_v1.sh`

## See also
- `journals/scale-radio-fun-line/current_state_v1.md`
- `journals/scale-radio-fun-line/stream_v1.md`
- `contracts/repo/overlay_component_contract_v1.md`
