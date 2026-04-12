# Braun HD Theme

This theme now uses both PNG layers and `theme.json`.

## What belongs in PNG artwork

Use PNG layers for anything that should look printed or physically built into
the appliance:

- glass reflections
- backlight glow
- recessed scale bed
- permanent numbers / tick print
- permanent branding / labels
- marker sprite styling

## What belongs in theme.json

Use `theme.json` for anything you want to tune without touching Python code:

- text positions
- panel geometry
- font switching
- colors
- whether generated scale numbers or station labels are shown
- dimmed logo position / alpha
- VU meter placement scaffold
- pointer sprite offsets

## Optional per-station runtime overrides

Stations in `runtime/settings.json` may now include:

- `label_dx`
- `label_dy`
- `marker_dx`
- `marker_dy`
- `label_lines`

That lets you fine-tune label placement for custom scales without changing the
renderer.
