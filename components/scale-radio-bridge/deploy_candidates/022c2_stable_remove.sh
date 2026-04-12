#!/usr/bin/env bash
set -euo pipefail

# Remove the live Bridge plugin from the active runtime path by moving live paths aside.
# Inputs: none.
# Outputs: clean-absent Bridge runtime state from the active Volumio plugin paths.
# Side effects: moves the live plugin path and Bridge config directory into a removed-state archive area.
# Failure behavior: continues on missing paths and exits zero after cleanup.
# Dependencies: bash, mv, mkdir, Volumio plugin filesystem layout.

LIVE_DIR="/data/plugins/user_interface/radioscale_overlay_bridge"
CONFIG_DIR="/data/configuration/user_interface/radioscale_overlay_bridge"
ARCHIVE_ROOT="/opt/scale-radio/removed/bridge"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
STATE_DIR="/opt/scale-radio/state"
mkdir -p "$STATE_DIR" "$ARCHIVE_ROOT"
echo "bridge_remove_022c2_stable" > "$STATE_DIR/bridge.last_phase"

if [[ -d "$LIVE_DIR" ]]; then
  mv "$LIVE_DIR" "$ARCHIVE_ROOT/live.${TIMESTAMP}"
fi
if [[ -d "$CONFIG_DIR" ]]; then
  mv "$CONFIG_DIR" "$ARCHIVE_ROOT/config.${TIMESTAMP}"
fi

echo "SR_BRIDGE: moved live Bridge runtime paths out of active Volumio locations"
