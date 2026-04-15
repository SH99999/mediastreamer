# CURRENT STATE — scale-radio-tuner

Status note: this v2 file remains the current tuner deploy-lane truth and is updated here after successful target-Pi validation.

## Component
- normalized component name: `scale-radio-tuner`
- governed artifact pattern: one component with multiple artifacts
- active artifacts in the currently imported payload:
  - `tuner:runtime` (`radio_scale_peppy` overlay plugin)
  - `tuner:service` (`scale_fm_renderer.service` resident renderer service)
- artifact still referenced in legacy component truth and currently out of deploy-lane scope until full integration:
  - `tuner:source_tile` (`radio_scale_source`, hardware-governed via encoder short/long press)
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
- shared wrapper v2 compatibility now also exists for tuner through `tools/deploy/sr-deploy-wrapper-v2.sh`
- manual test workflows now exist through:
  - `.github/workflows/component-test-deploy-v10.yml`
  - `.github/workflows/component-test-rollback-v10.yml`

## Lifecycle status
- `payload_complete`
- `deployment_candidate_started`
- `deploy_ready`
- `deploy_validated_on_pi`
- `rollback_validated_on_pi`
- `manual_runtime_validation_passed`
- `functional_acceptance_open`
- `autonomous_delivery_enabled_for_overlay_lane`

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

## Current gaps
- the currently normalized deploy lane intentionally covers the overlay and resident renderer service only
- `radio_scale_source` remains out of deploy-lane scope until full integration and is currently governed by hardware controls (encoder short/long press)
- first-show pointer sweep after boot remains unresolved
- exit white flashes remain unresolved
- pointer flicker/jitter is not fully solved
- multi-artifact autonomous acceptance is intentionally limited to the active overlay/runtime/service scope until full integration is opened

## Repo-normalized next action
1. keep tuner overlay/runtime/service lane stable under the governed deploy/rollback model
2. keep source-project behavior explicitly documented as hardware-governed until full integration is opened
3. normalize the next component onto the same repo-driven deploy/rollback model after bridge and tuner
