# Scale Radio Hardware

## Purpose
Scale Radio Hardware governs the donor-hardware integration track, especially retained SABA MT201 controls and the standalone hardware-validation lane for magnetic angle sensing.

## Current role
- governed component: `scale-radio-hardware`
- current work lane: `dev/hardware`
- phase-1 retained parts: knob, shaft, flywheel
- phase-1 sensor baseline: AS5600 over I2C

## Boundaries
This component owns donor-hardware reuse, sensor validation, and hardware-facing documentation.
It does not own the radio-scale renderer, source logic, or final frontpanel-engine production integration.

## Current focus
- normalize source-of-truth under `components/scale-radio-hardware/`
- keep the AS5600 tester as a standalone validation lane
- preserve HiFiBerry-safe wiring discipline
- validate live angle reading on the target Pi before broader integration

## See also
- `journals/scale-radio-hardware/current_state_v1.md`
- `journals/scale-radio-hardware/stream_v1.md`
