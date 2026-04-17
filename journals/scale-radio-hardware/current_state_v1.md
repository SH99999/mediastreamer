# CURRENT STATE — scale-radio-hardware

## Component
- normalized component name: `scale-radio-hardware`
- governed role: donor-hardware integration and standalone hardware validation lane
- active work lane: `dev/hardware`

## Repo truth
- dedicated branch `dev/hardware` exists
- component remains dev-lane only and is not mature enough for `main`
- source-of-truth payload now includes a repo-native Rotary Encoder II Angle Bridge plugin under `components/scale-radio-hardware/payload/current_dev/`

## Lifecycle status
- `payload_partial`
- `functional_acceptance_open`

## Evidence-led claim ledger
- claim.repo_ready_payload_present: `true`
- claim.deploy_ready: `false`
- claim.tested_on_target: `false`
- claim.rollback_verified: `false`
- claim.runtime_validated: `false`
- claim.autonomy_eligible: `false`
- claim.tested_scope: `source-level validation only (Node syntax check + GUI/control-flow review); no target Pi runtime proof yet`
- claim.evidence_path: `components/scale-radio-hardware/payload/current_dev/; journals/scale-radio-hardware/current_state_v1.md; journals/scale-radio-hardware/stream_v1.md`
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
- standalone Volumio validation plugin remains required so sensor and control mapping can be tested independently of Radio Scale runtime

## Current known working behavior
- phase-1 reuse scope is clarified and locked
- AS5600 is the selected phase-1 sensor baseline
- safe initial wiring rules for Pi 4B + HiFiBerry DAC+ ADC Pro were defined
- repo payload now includes a unified plugin GUI for angle sensing + Rotary Encoder II style button action mapping (transport, volume step, custom emit)

## Current gaps
- no confirmed repo-integrated Pi-validated baseline yet
- no confirmed production-ready install/rollback path in repo yet
- live AS5600 communication on target Pi remains unvalidated
- direct GPIO interrupt-driven physical button capture is not yet implemented in this lane
- mechanical bracket/adapter dimensions remain open until real measurements are captured

## Repo-normalized next action
1. keep this component on `dev/hardware`
2. run target Pi validation for AS5600 I2C communication and live angle reads
3. validate button mapping behavior against real hardware button events (after selecting GPIO strategy)
4. add deploy/rollback evidence only after target-Pi runtime validation passes
