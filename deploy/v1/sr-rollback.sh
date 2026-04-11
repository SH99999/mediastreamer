#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-latest-good}"
STATE_DIR="/opt/scale-radio/state"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "$TARGET" == "latest-good" ]]; then
  if [[ ! -f "$STATE_DIR/last_successful_ref" ]]; then
    echo "No last_successful_ref found in $STATE_DIR"
    exit 1
  fi
  TARGET="$(cat "$STATE_DIR/last_successful_ref")"
fi

echo "Rolling back to ref=$TARGET"
"$SCRIPT_DIR/sr-deploy.sh" bundle "$TARGET"
