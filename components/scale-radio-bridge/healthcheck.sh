#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="/opt/scale-radio/state"
mkdir -p "$STATE_DIR"
echo "healthcheck" > "$STATE_DIR/bridge.last_phase"

echo "Bridge healthcheck hook entered"
echo "Bridge healthcheck is pending until the real bridge payload and runtime install contract are imported."
