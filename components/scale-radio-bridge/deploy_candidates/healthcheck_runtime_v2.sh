#!/usr/bin/env bash
set -euo pipefail

PAYLOAD_NAME="${1:-unknown}"
LIVE_DIR="/data/plugins/user_interface/radioscale_overlay_bridge"
CONFIG_DIR="/data/configuration/user_interface/radioscale_overlay_bridge"
STATE_DIR="/opt/scale-radio/state"
mkdir -p "$STATE_DIR"
echo "bridge_healthcheck_${PAYLOAD_NAME}" > "$STATE_DIR/bridge.last_phase"

required=(
  "$LIVE_DIR/index.js"
  "$LIVE_DIR/config.json"
  "$LIVE_DIR/UIConfig.json"
  "$LIVE_DIR/package.json"
  "$LIVE_DIR/public/index.html"
  "$LIVE_DIR/public/style.css"
  "$LIVE_DIR/public/app.js"
  "$LIVE_DIR/i18n/strings_en.json"
)

for path in "${required[@]}"; do
  if [[ ! -f "$path" ]]; then
    echo "SR_BRIDGE: missing required live file $path"
    exit 2
  fi
done

if [[ ! -d "$CONFIG_DIR" ]]; then
  echo "SR_BRIDGE: missing Bridge config directory $CONFIG_DIR"
  exit 2
fi

if [[ ! -d "$LIVE_DIR/node_modules/kew" ]]; then
  echo "SR_BRIDGE: missing required dependency $LIVE_DIR/node_modules/kew"
  exit 2
fi

if ! systemctl is-active --quiet volumio; then
  echo "SR_BRIDGE: volumio is not active"
  exit 2
fi

if ! systemctl is-active --quiet volumio-kiosk; then
  echo "SR_BRIDGE: volumio-kiosk is not active"
  exit 2
fi

if [[ "$(pgrep -fc chromium || true)" -lt 1 ]]; then
  echo "SR_BRIDGE: chromium is not running"
  exit 2
fi

if [[ "$(pgrep -fc Xorg || true)" -lt 1 ]]; then
  echo "SR_BRIDGE: Xorg is not running"
  exit 2
fi

echo "SR_BRIDGE: Bridge runtime healthcheck passed for $PAYLOAD_NAME"
