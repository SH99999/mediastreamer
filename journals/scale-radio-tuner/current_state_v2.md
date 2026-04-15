# CURRENT STATE — scale-radio-tuner

Status note: this v2 file supersedes `current_state_v1.md` as the current tuner deploy-lane addendum.

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

## Lifecycle status
- `payload_complete`
- `deployment_candidate_started`
- `deploy_ready`
- `tested_on_pi_open`
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
- deploy lane now installs the payload directly to `/data/plugins/user_interface/radio_scale_peppy`, runs `npm install`, executes the payload install script, and validates the renderer service/runtime path
- rollback lane archives the active tuner runtime and removes the active renderer service cleanly

## Current gaps
- the currently normalized deploy lane covers the overlay and resident renderer service only
- the separate `radio_scale_source` artifact is still not imported as a deployable repo payload in this lane
- the new manual deploy/rollback lane is not yet validated on the target Pi
- first-show pointer sweep after boot remains unresolved
- exit white flashes remain unresolved
- pointer flicker/jitter is not fully solved

## Repo-normalized next action
1. run `component-test-deploy-v10` for `component=tuner`, `git_ref=main`, `payload=current`, `target=primary`
2. validate tuner open/close, renderer service, and rollback on the target Pi
3. decide whether tuner can enter the autonomous delivery matrix after first Pi validation
4. import or normalize the separate `radio_scale_source` artifact if the governed component must again ship both overlay and source as one deploy lane
