#!/usr/bin/env bash
set -euo pipefail

PAYLOAD_NAME="${1:-}"
if [[ -z "$PAYLOAD_NAME" ]]; then
  echo "SR_TUNER: missing payload name"
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPONENT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PAYLOAD_DIR="$COMPONENT_ROOT/payload/${PAYLOAD_NAME}"
LIVE_DIR="/data/plugins/user_interface/radio_scale_peppy"
CONFIG_DIR="/data/configuration/user_interface/radio_scale_peppy"
ARCHIVE_ROOT="/opt/scale-radio/removed/tuner"
STATE_DIR="/opt/scale-radio/state"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"

mkdir -p "$STATE_DIR" "$ARCHIVE_ROOT"
echo "tuner_apply_${PAYLOAD_NAME}" > "$STATE_DIR/tuner.last_phase"

if [[ ! -f "$PAYLOAD_DIR/index.js" ]]; then
  echo "SR_TUNER: missing payload index.js at $PAYLOAD_DIR"
  exit 2
fi
if [[ ! -f "$PAYLOAD_DIR/run_radio_scale.sh" ]]; then
  echo "SR_TUNER: missing payload launcher run_radio_scale.sh at $PAYLOAD_DIR"
  exit 2
fi
if [[ ! -f "$PAYLOAD_DIR/systemd/scale_fm_renderer.service" ]]; then
  echo "SR_TUNER: missing renderer service unit at $PAYLOAD_DIR/systemd/scale_fm_renderer.service"
  exit 2
fi

if [[ -d "$LIVE_DIR" ]]; then
  mv "$LIVE_DIR" "$ARCHIVE_ROOT/live.before_${PAYLOAD_NAME}.${TIMESTAMP}"
fi
if [[ -d "$CONFIG_DIR" ]]; then
  mv "$CONFIG_DIR" "$ARCHIVE_ROOT/config.before_${PAYLOAD_NAME}.${TIMESTAMP}"
fi

mkdir -p "$(dirname "$LIVE_DIR")"
mkdir -p "$LIVE_DIR"
cp -a "$PAYLOAD_DIR"/. "$LIVE_DIR"/
chmod +x "$LIVE_DIR/run_radio_scale.sh" "$LIVE_DIR/run_renderer_daemon.sh" "$LIVE_DIR/install.sh" "$LIVE_DIR/uninstall.sh" 2>/dev/null || true

if [[ -f "$LIVE_DIR/package.json" ]]; then
  (cd "$LIVE_DIR" && npm install --omit=dev)
fi

if [[ -f "$LIVE_DIR/install.sh" ]]; then
  (cd "$LIVE_DIR" && bash ./install.sh)
fi

chown -R volumio:volumio "$LIVE_DIR" 2>/dev/null || true
sudo systemctl restart volumio

for i in $(seq 1 60); do
  if systemctl is-active --quiet volumio; then
    break
  fi
  sleep 2
done

if ! systemctl is-active --quiet volumio; then
  echo "SR_TUNER: volumio did not recover after installing $PAYLOAD_NAME"
  exit 2
fi

echo "SR_TUNER: applied Tuner payload $PAYLOAD_NAME"
