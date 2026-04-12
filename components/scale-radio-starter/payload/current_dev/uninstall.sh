#!/bin/bash
set -euo pipefail
APP_ROOT="/opt/mediastreamer-hybrid"
INSTALL_ROOT="/opt/mediastreamer-direct-now-playing-topmost-keeper-patch-install"
BACKUP_DIR="${INSTALL_ROOT}/backup"
abort() { echo "[mediastreamer-direct-now-playing-topmost-keeper-patch] ERROR: $*" >&2; exit 1; }
[ "${EUID}" -eq 0 ] || abort "Run as root: sudo bash ./uninstall.sh"
restore() { local key="$1" dst="$2"; local src="${BACKUP_DIR}/${key}.bak"; [ -f "$src" ] && cp -f "$src" "$dst"; }
restore "opt__mediastreamer-hybrid__server.py" "${APP_ROOT}/server.py"
restore "opt__mediastreamer-hybrid__kiosk-wrapper.sh" "${APP_ROOT}/kiosk-wrapper.sh"
restore "opt__mediastreamer-hybrid__artwork_keeper.py" "${APP_ROOT}/artwork_keeper.py"
rm -f /tmp/mediastreamer-kiosk-ready /tmp/mediastreamer-artwork-keeper.pid /tmp/mediastreamer-artwork-keeper.ready || true
chown -R volumio:volumio "${APP_ROOT}" || true
systemctl daemon-reload
rm -rf "${INSTALL_ROOT}"
echo "[mediastreamer-direct-now-playing-topmost-keeper-patch] Patch uninstall complete. Reboot required."
