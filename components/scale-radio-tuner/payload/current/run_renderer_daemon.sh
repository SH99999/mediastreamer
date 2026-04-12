#!/bin/bash
set -e

PLUGIN_DIR="${RADIO_SCALE_PLUGIN_DIR:-/data/plugins/user_interface/radio_scale_peppy}"
RUNTIME_DIR="$PLUGIN_DIR/runtime"
mkdir -p "$RUNTIME_DIR"

export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-/home/volumio/.Xauthority}"
export SDL_VIDEODRIVER="${SDL_VIDEODRIVER:-x11}"
export SDL_AUDIODRIVER="${SDL_AUDIODRIVER:-dummy}"
export PYGAME_HIDE_SUPPORT_PROMPT=1
export RADIO_SCALE_PLUGIN_DIR="$PLUGIN_DIR"
export RADIO_SCALE_RESIDENT=1

# Wait for the local X11 socket so the renderer can create the hidden window
# without failing during early boot. This keeps boot-time retries inside the
# service bootstrap script instead of hammering Volumio's plugin logs.
while [ ! -S /tmp/.X11-unix/X0 ]; do
  sleep 2
done

cd "$PLUGIN_DIR"
exec /usr/bin/python3 ./renderer/radio_scale_renderer.py
