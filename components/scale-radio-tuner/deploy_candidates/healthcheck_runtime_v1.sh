#!/usr/bin/env bash
set -euo pipefail

PAYLOAD_NAME="${1:-unknown}"
LIVE_DIR="/data/plugins/user_interface/radio_scale_peppy"
SERVICE_PATH="/etc/systemd/system/scale_fm_renderer.service"
STATE_DIR="/opt/scale-radio/state"
mkdir -p "$STATE_DIR"
echo "tuner_healthcheck_${PAYLOAD_NAME}" > "$STATE_DIR/tuner.last_phase"

required=(
  "$LIVE_DIR/index.js"
  "$LIVE_DIR/package.json"
  "$LIVE_DIR/run_radio_scale.sh"
  "$LIVE_DIR/run_renderer_daemon.sh"
  "$LIVE_DIR/UIConfig.json"
  "$LIVE_DIR/config.json"
  "$LIVE_DIR/renderer/radio_scale_renderer.py"
  "$LIVE_DIR/renderer/layered_theme.py"
  "$LIVE_DIR/systemd/scale_fm_renderer.service"
  "$LIVE_DIR/node_modules/kew"
)

for path in "${required[@]}"; do
  if [[ ! -e "$path" ]]; then
    echo "SR_TUNER: missing required live path $path"
    exit 2
  fi
done

if [[ ! -f "$SERVICE_PATH" ]]; then
  echo "SR_TUNER: missing installed renderer service unit $SERVICE_PATH"
  exit 2
fi

if ! systemctl is-active --quiet volumio; then
  echo "SR_TUNER: volumio is not active"
  exit 2
fi
if ! systemctl is-active --quiet volumio-kiosk; then
  echo "SR_TUNER: volumio-kiosk is not active"
  exit 2
fi
if ! systemctl is-active --quiet scale_fm_renderer.service; then
  echo "SR_TUNER: scale_fm_renderer.service is not active"
  exit 2
fi
if [[ "$(pgrep -fc chromium || true)" -lt 1 ]]; then
  echo "SR_TUNER: chromium is not running"
  exit 2
fi
if [[ "$(pgrep -fc Xorg || true)" -lt 1 ]]; then
  echo "SR_TUNER: Xorg is not running"
  exit 2
fi

echo "SR_TUNER: Tuner runtime healthcheck passed for $PAYLOAD_NAME"
