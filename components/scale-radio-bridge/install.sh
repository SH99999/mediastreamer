#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="/opt/scale-radio/state"
mkdir -p "$STATE_DIR"
echo "install" > "$STATE_DIR/bridge.last_phase"

echo "Bridge install hook entered"
echo "This hook becomes executable after the real bridge payload is imported into the repo path."
