# CURRENT STATE — scale-radio-hardware

## Component
- normalized component name: `scale-radio-hardware`
- governed role: donor-hardware integration and standalone hardware validation lane
- active work lane: `dev/hardware`

## Repo truth
- dedicated branch `dev/hardware` exists
- legacy handover provides strong scope and decision truth, but repo source normalization is still incomplete and should remain on the dev lane
- component is not mature enough for `main`

## Lifecycle status
- `payload_partial`
- `functional_acceptance_open`

## Evidence-led claim ledger
- claim.repo_ready_payload_present: `false`
- claim.deploy_ready: `false`
- claim.tested_on_target: `false`
- claim.rollback_verified: `false`
- claim.runtime_validated: `false`
- claim.autonomy_eligible: `false`
- claim.tested_scope: `hardware validation lane only; no deploy/rollback runtime proof on target Pi yet`
- claim.evidence_path: `journals/scale-radio-hardware/current_state_v1.md; journals/scale-radio-hardware/stream_v1.md`
- claim.rollback_path: `not-applicable (non-deploy hardware lane)`
- claim.source_ref: `reports/status/packets/hardware.json`

## Accepted hardware posture
- retained donor parts in phase 1:
  - original SABA MT201 tuning knob
  - shaft
  - flywheel
- phase-1 sensing baseline:
  - AS5600 magnetic angle sensor
  - I2C-first test path
  - HiFiBerry-safe wiring discipline
- standalone Volumio validation plugin is required so the sensor path can be tested independently of Radio Scale runtime

## Current known working behavior
- phase-1 reuse scope is clarified and locked
- AS5600 is the selected phase-1 sensor baseline
- magnet requirement and orientation/calibration posture are clarified
- safe initial wiring rules for Pi 4B + HiFiBerry DAC+ ADC Pro were defined
- standalone hardware validation lane concept already exists

## Current gaps
- no confirmed repo-integrated Pi-validated baseline yet
- no confirmed production-ready install/rollback path in repo yet
- live AS5600 communication on target Pi remains unvalidated
- mechanical bracket/adapter dimensions remain open until real measurements are captured
- preset-button reuse remains open

## Repo-normalized next action
1. keep this component on `dev/hardware`
2. normalize source-of-truth under `components/scale-radio-hardware/`
3. commit the standalone AS5600 tester as source, not only as generated artifact
4. validate I2C communication and live angle reading on the target Pi
