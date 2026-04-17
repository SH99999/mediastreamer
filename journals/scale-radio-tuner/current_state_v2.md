# CURRENT STATE — scale-radio-tuner

Status note: this v2 file remains the current tuner deploy-lane truth and is updated here after successful target-Pi validation and autonomous-delivery promotion.

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
- tuner is now enabled in `tools/governance/autonomous_delivery_matrix_v3.json`

## Lifecycle status
- `payload_complete`
- `deployment_candidate_started`
- `deploy_ready`
- `tested_on_pi`
- `functional_acceptance_open`

## Evidence-led claim ledger
- claim.repo_ready_payload_present: `true`
- claim.deploy_ready: `true`
- claim.tested_on_target: `true`
- claim.rollback_verified: `true`
- claim.runtime_validated: `true`
- claim.autonomy_eligible: `true`
- claim.tested_scope: `overlay/runtime/service lane on target Pi; source tile remains out of deploy scope`
- claim.evidence_path: `journals/scale-radio-tuner/current_state_v2.md; journals/scale-radio-tuner/stream_v2.md; tools/governance/autonomous_delivery_matrix_v3.json`
- claim.rollback_path: `.github/workflows/component-test-rollback-v10.yml (component=tuner, payload=current)`
- claim.source_ref: `reports/status/packets/tuner.json`

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
- the currently normalized deploy lane intentionally covers the overlay and resident renderer service only
- `radio_scale_source` remains out of deploy-lane scope until full integration and is currently governed by hardware controls (encoder short/long press)
- first-show pointer sweep after boot remains unresolved
- exit white flashes remain unresolved
- pointer flicker/jitter is not fully solved
- multi-artifact autonomous acceptance is intentionally limited to the active overlay/runtime/service scope until full integration is opened

## Repo-normalized next action
1. keep tuner overlay/runtime/service lane stable under the governed deploy/rollback model
2. keep source-project behavior explicitly documented as hardware-governed until full integration is opened
3. normalize the separate `radio_scale_source` artifact if the governed component must again ship both overlay and source as one deploy lane
4. normalize the next component onto the same repo-driven deploy/rollback model after bridge and tuner
