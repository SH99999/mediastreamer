#!/usr/bin/env bash
set -euo pipefail

PAYLOAD_NAME="${1:-bridge}"
LIVE_DIR="/data/plugins/user_interface/radioscale_overlay_bridge"
CONFIG_DIR="/data/configuration/user_interface/radioscale_overlay_bridge"
ARCHIVE_ROOT="/opt/scale-radio/removed/bridge"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
STATE_DIR="/opt/scale-radio/state"
mkdir -p "$STATE_DIR" "$ARCHIVE_ROOT"
echo "bridge_remove_${PAYLOAD_NAME}" > "$STATE_DIR/bridge.last_phase"

if [[ -d "$LIVE_DIR" ]]; then
  mv "$LIVE_DIR" "$ARCHIVE_ROOT/live.${PAYLOAD_NAME}.${TIMESTAMP}"
fi
if [[ -d "$CONFIG_DIR" ]]; then
  mv "$CONFIG_DIR" "$ARCHIVE_ROOT/config.${PAYLOAD_NAME}.${TIMESTAMP}"
fi

sudo systemctl restart volumio

for i in $(seq 1 60); do
  if systemctl is-active --quiet volumio; then
    break
  fi
  sleep 2
done

if ! systemctl is-active --quiet volumio; then
  echo "SR_BRIDGE: volumio did not recover after Bridge removal"
  exit 2
fi

echo "SR_BRIDGE: removed active Bridge runtime for $PAYLOAD_NAME"
