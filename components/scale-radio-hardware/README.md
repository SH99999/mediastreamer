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
- keep source-of-truth under `components/scale-radio-hardware/`
- maintain the `current_dev` Rotary Encoder II Angle Bridge plugin as the standalone validation lane
- preserve HiFiBerry-safe wiring discipline
- validate live angle reading and button mapping on the target Pi before broader integration

## Current artifact in `payload/current_dev`
- plugin: **Rotary Encoder II Angle Bridge** (`system_hardware`)
- GUI support for:
  - AS5600 sensor probing + calibration
  - live angle action mapping
  - Rotary Encoder II style button mapping (transport / volume step / custom emit)

## See also
- `journals/scale-radio-hardware/current_state_v1.md`
- `journals/scale-radio-hardware/stream_v1.md`
