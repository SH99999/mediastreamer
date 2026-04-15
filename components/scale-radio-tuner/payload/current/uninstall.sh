#!/bin/bash
set -euo pipefail

run_sudo() {
  if sudo -n true 2>/dev/null; then
    sudo "$@"
    return
  fi
  if [ -n "${PI_SUDO_PASSWORD:-}" ]; then
    printf '%s\n' "$PI_SUDO_PASSWORD" | sudo -S -p '' "$@"
    return
  fi
  echo "SR_TUNER: sudo access required but PI_SUDO_PASSWORD is not available" >&2
  exit 2
}

echo "Removing Scale FM Overlay runtime"
rm -rf /data/plugins/user_interface/radio_scale_peppy/runtime || true
run_sudo systemctl disable --now scale_fm_renderer.service || true
run_sudo rm -f /etc/systemd/system/scale_fm_renderer.service || true
run_sudo systemctl daemon-reload || true
