#!/bin/bash
set -euo pipefail
PKG_VERSION="0.3.4-direct-now-playing-topmost-keeper-patch"
APP_ROOT="/opt/mediastreamer-hybrid"
INSTALL_ROOT="/opt/mediastreamer-direct-now-playing-topmost-keeper-patch-install"
BACKUP_DIR="${INSTALL_ROOT}/backup"
abort() { echo "[mediastreamer-direct-now-playing-topmost-keeper-patch] ERROR: $*" >&2; exit 1; }
[ "${EUID}" -eq 0 ] || abort "Run as root: sudo bash ./install.sh"
mkdir -p "${BACKUP_DIR}" "${INSTALL_ROOT}"
backup_file() { local src="$1" key="$2"; if [ -f "$src" ]; then cp -f "$src" "${BACKUP_DIR}/${key}.bak"; fi; }
backup_file "${APP_ROOT}/server.py" "opt__mediastreamer-hybrid__server.py"
backup_file "${APP_ROOT}/kiosk-wrapper.sh" "opt__mediastreamer-hybrid__kiosk-wrapper.sh"
backup_file "${APP_ROOT}/artwork_keeper.py" "opt__mediastreamer-hybrid__artwork_keeper.py"
install -m 0755 ./server.py "${APP_ROOT}/server.py"
install -m 0755 ./kiosk-wrapper.sh "${APP_ROOT}/kiosk-wrapper.sh"
install -m 0755 ./artwork_keeper.py "${APP_ROOT}/artwork_keeper.py"
install -m 0755 ./verify.sh "${INSTALL_ROOT}/verify.sh"
install -m 0755 ./uninstall.sh "${INSTALL_ROOT}/uninstall.sh"
install -m 0644 ./README.md "${INSTALL_ROOT}/README.md"
install -m 0644 ./PATCH_NOTES.txt "${INSTALL_ROOT}/PATCH_NOTES.txt"
echo "${PKG_VERSION}" > "${INSTALL_ROOT}/version.txt"
rm -f /tmp/mediastreamer-kiosk-ready /tmp/mediastreamer-artwork-keeper.pid /tmp/mediastreamer-artwork-keeper.ready || true
chown -R volumio:volumio "${APP_ROOT}"
systemctl daemon-reload
echo "[mediastreamer-direct-now-playing-topmost-keeper-patch] Patch installed. Reboot required."
echo "[mediastreamer-direct-now-playing-topmost-keeper-patch] Verify after reboot with: sudo bash /opt/mediastreamer-direct-now-playing-topmost-keeper-patch-install/verify.sh"
