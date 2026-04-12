Scale FM Overlay 1.10.2

# Scale FM Overlay 1.10.0

This release introduces a **resident renderer service** path for Volumio 4.

## What changed

- the Python / pygame renderer can now be preloaded in **hidden standby** at boot
- overlay open no longer needs to pay the full PNG/font/process cold-start cost when the service is active
- Node.js logic remains in `index.js`; the renderer still consumes only JSON runtime files
- a renderer PID marker and renderer-ready marker were added for safer service-aware fallback logic

## Boot / runtime model

1. `install.sh` installs `scale_fm_renderer.service`
2. systemd starts `run_renderer_daemon.sh` as user `volumio`
3. the daemon waits for the local X11 socket and launches the renderer in resident mode
4. the renderer stays hidden while `ui_mode=normal`
5. opening the overlay switches `ui_mode=scale` and reuses the warm renderer

## Relevant entry points

- Source tile / browse URI: `scalefm` / `scalefm/open`
- GPIO 13 short press method: `gpio13OpenScale`
- Encoder 1 long press exit method: `encoder1LongPress`

## Runtime markers

- `runtime/state.json` - current Volumio / tuning state consumed by the renderer
- `runtime/settings.json` - renderer settings
- `runtime/renderer_ready.json` - written by the renderer after the first visible frame
- `runtime/renderer.pid` - PID marker used for service-aware process detection

## Notes

- internal plugin ids stay unchanged: `radio_scale_peppy` and `radio_scale_source`
- the service path is best-effort and still falls back to direct plugin spawn if the resident renderer is not yet running
- the package was syntax-checked locally, but not live-tested on the target Pi from inside this environment


## 1.10.2 resident standby behaviour
- hidden standby uses idle / deep-idle instead of a running draw loop
- visible rendering is capped for Pi-friendly operation
- shared overlay owner marker: `/tmp/mediastreamer_active_overlay.json`
