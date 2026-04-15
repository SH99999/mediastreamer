# CURRENT STATE — scale-radio-tuner

Status note: this v2 file remains the current tuner deploy-lane truth and is updated here after successful target-Pi validation and autonomous-delivery promotion.

## Component
- normalized component name: `scale-radio-tuner`
- governed artifact pattern: one component with multiple artifacts
- active artifacts in the currently imported payload:
  - `Scale FM Overlay`
  - resident renderer service `scale_fm_renderer.service`
- artifact still referenced in legacy component truth but not yet normalized in the active deploy lane:
  - `Scale FM Source`
- active work lane: `dev/tuner`

## Repo truth
- component root exists at `components/scale-radio-tuner/`
- a real imported payload exists at `components/scale-radio-tuner/payload/current/`
- earlier top-level tuner install/configure/healthcheck hooks were placeholder deploy-contract scaffolding only
- a real repo-driven deploy candidate lane now exists at:
  - `components/scale-radio-tuner/deploy_candidates/apply_payload_v1.sh`
  - `components/scale-radio-tuner/deploy_candidates/healthcheck_runtime_v1.sh`
  - `components/scale-radio-tuner/deploy_candidates/remove_active_v1.sh`
- generic deploy wrapper support now exists through `tools/deploy/sr-deploy-wrapper-v3.sh`
- manual test workflows now exist through:
  - `.github/workflows/component-test-deploy-v10.yml`
  - `.github/workflows/component-test-rollback-v10.yml`
- tuner is now enabled in `tools/governance/autonomous_delivery_matrix_v3.json`

## Lifecycle status
- `payload_complete`
- `deployment_candidate_started`
- `deploy_ready`
- `deploy_validated_on_pi`
- `rollback_validated_on_pi`
- `manual_runtime_validation_passed`
- `autonomous_delivery_enabled`
- `functional_acceptance_open`

## Accepted baseline
- authoritative overlay/render baseline in repo: `1.10.2`
- external names:
  - `Scale FM Overlay`
  - `Scale FM Source`
- internal identifiers that must remain stable:
  - `radio_scale_peppy`
  - `radio_scale_source`
  - `scale_fm_renderer.service`

## Current known working behavior
- tuner payload includes the full `radio_scale_peppy` overlay runtime, renderer Python code, layered Braun HD theme assets, launch scripts, and systemd unit
- install script provisions Python renderer dependencies and seeds playlist/favourites state
- deploy lane installs the payload directly to `/data/plugins/user_interface/radio_scale_peppy`, runs `npm install`, executes the payload install script, and validates the renderer service/runtime path
- rollback lane archives the active tuner runtime and removes the active renderer service cleanly
- both deploy and rollback are now validated on the target Pi through the governed lock-aware workflow lane
- tuner is now enabled for autonomous delivery dispatch via the shared control plane

## Current gaps
- the currently normalized deploy lane covers the overlay and resident renderer service only
- the separate `radio_scale_source` artifact is still not imported as a deployable repo payload in this lane
- first-show pointer sweep after boot remains unresolved
- exit white flashes remain unresolved
- pointer flicker/jitter is not fully solved

## Repo-normalized next action
1. normalize the separate `radio_scale_source` artifact if the governed component must again ship both overlay and source as one deploy lane
2. normalize the next component onto the same repo-driven deploy/rollback model after bridge and tuner
