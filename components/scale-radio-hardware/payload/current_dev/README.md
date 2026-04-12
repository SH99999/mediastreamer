# AS5600 Angle Tester for Volumio 4

Standalone `system_hardware` plugin for Volumio 4 (Bookworm) to test an AS5600 angle sensor without RadioScale.

## What it does

- Reads AS5600 over I²C
- Manual one-shot sensor probe from the plugin settings page
- Stores raw min/max calibration values
- Supports live polling with these actions:
  - monitor only
  - toast current percent
  - map knob position to Volumio volume
  - call another plugin method using `callMethod`
- Exposes a backend method `getCurrentState()` for later integration

## Wiring

Standard Raspberry Pi I²C wiring:

- 3.3V -> AS5600 VCC
- GND -> AS5600 GND
- GPIO2 / SDA -> AS5600 SDA
- GPIO3 / SCL -> AS5600 SCL

Default address: `0x36`

## First test

1. Enable I²C in Volumio / Raspberry Pi.
2. Install and enable the plugin.
3. Open plugin settings.
4. Leave bus = `1`, address = `0x36`.
5. Click **Probe sensor now**.
6. Turn the knob and probe again.
7. Capture min and max.
8. Set **Function while turning** to **Toast current percent**.
9. Enable live polling and save.
10. Turn the knob and verify toasts.

## Custom emit

For integration testing with another plugin, choose **Call another plugin method** and configure:

- endpoint: for example `user_interface/radio_scale_peppy`
- method: the backend method to call
- additional JSON: any extra payload object

The plugin automatically adds:

```json
{
  "sensor": {
    "rawAngle": 1234,
    "normalized": 0.301,
    "percent": 30,
    "bucket": 6,
    "magnetDetected": true,
    "magnetTooWeak": false,
    "magnetTooStrong": false
  }
}
```

## Notes

- This plugin uses `socket.io-client` version `1.7.4`, matching the Bookworm GPIO Buttons plugin pattern.
- It uses the `i2c-bus` Node module for direct Linux I²C access.
