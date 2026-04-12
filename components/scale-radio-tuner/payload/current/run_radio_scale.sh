#!/bin/bash
set -e

PLUGIN_DIR="${RADIO_SCALE_PLUGIN_DIR:-/data/plugins/user_interface/radio_scale_peppy}"
export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-/home/volumio/.Xauthority}"
export SDL_VIDEODRIVER="${SDL_VIDEODRIVER:-x11}"
export SDL_VIDEO_WINDOW_POS=0,0
export SDL_AUDIODRIVER="${SDL_AUDIODRIVER:-dummy}"
export PYGAME_HIDE_SUPPORT_PROMPT=1

cd "$PLUGIN_DIR"
exec /usr/bin/python3 ./renderer/radio_scale_renderer.py
