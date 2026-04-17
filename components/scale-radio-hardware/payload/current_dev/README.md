# Rotary Encoder II Angle Bridge (Volumio 4)

Standalone `system_hardware` plugin for Volumio 4 (Bookworm) that combines:

- **AS5600 angle sensor** support (I²C)
- **Rotary Encoder II style button action layer** (GUI-driven mapping)

This component is meant for hardware validation and integration staging on `dev/hardware`.

## Features

- Live AS5600 polling with calibration (raw min/max, invert direction)
- Angle actions:
  - monitor only
  - toast current percent
  - map angle to Volumio volume
  - call another plugin method (`callMethod`)
- Button actions (manual trigger from GUI):
  - transport commands (play/pause, next, previous)
  - volume step up/down
  - custom plugin `callMethod`
- Exposes backend state via `getCurrentState()`

## Wiring for AS5600

- 3.3V -> AS5600 VCC
- GND -> AS5600 GND
- GPIO2 / SDA -> AS5600 SDA
- GPIO3 / SCL -> AS5600 SCL

Default address: `0x36`

## Quick start

1. Enable I²C in Volumio / Raspberry Pi.
2. Install and enable the plugin.
3. In **Sensor & Wiring**, keep bus `1` and address `0x36`.
4. Click **Probe sensor now**.
5. In **Calibration**, capture min and max.
6. Choose an angle action in **Live angle action**.
7. Optionally enable **Buttons** and test with the GUI buttons.

## Notes

- This plugin uses `socket.io-client` `1.7.4` for Volumio socket calls.
- Direct physical GPIO button interrupts are intentionally out of scope for this first repo-normalized bridge step; GUI button triggers are provided for deterministic validation.
