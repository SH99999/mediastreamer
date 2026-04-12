#!/usr/bin/env bash
set -euo pipefail

# Apply the exact Bridge 0.2.2-c2 stable payload from the repo into the live Volumio plugin path.
# Inputs: none. Uses the repo-relative stable payload tree.
# Outputs: live plugin files at /data/plugins/user_interface/radioscale_overlay_bridge.
# Side effects: overwrites the live Bridge plugin path, runs plugin install, restarts Volumio, waits for recovery.
# Failure behavior: exits non-zero on copy/install/restart failure before reporting success.
# Dependencies: bash, cp, rm, npm, node, sudo, systemctl, pgrep, Volumio plugin filesystem layout.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPONENT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PAYLOAD_DIR="$COMPONENT_ROOT/payload/022c2_stable"
LIVE_DIR="/data/plugins/user_interface/radioscale_overlay_bridge"
STATE_DIR="/opt/scale-radio/state"

mkdir -p "$STATE_DIR"
echo "bridge_apply_022c2_stable" > "$STATE_DIR/bridge.last_phase"

if [[ ! -f "$PAYLOAD_DIR/index.js" ]]; then
  echo "SR_BRIDGE: missing stable payload index.js at $PAYLOAD_DIR"
  exit 2
fi

mkdir -p "$(dirname "$LIVE_DIR")"
rm -rf "$LIVE_DIR"
mkdir -p "$LIVE_DIR"
cp -a "$PAYLOAD_DIR"/. "$LIVE_DIR"/

if [[ -f "$LIVE_DIR/install.sh" ]]; then
  (cd "$LIVE_DIR" && bash ./install.sh)
fi

chown -R volumio:volumio "$LIVE_DIR" 2>/dev/null || true

echo "SR_BRIDGE: restarting volumio after stable Bridge install"
sudo systemctl restart volumio

echo "SR_BRIDGE: waiting for volumio recovery"
for i in $(seq 1 60); do
  if systemctl is-active --quiet volumio; then
    break
  fi
  sleep 2
done

if ! systemctl is-active --quiet volumio; then
  echo "SR_BRIDGE: volumio did not recover after restart"
  exit 2
fi

echo "SR_BRIDGE: stable Bridge payload applied to $LIVE_DIR"