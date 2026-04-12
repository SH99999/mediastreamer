#!/bin/bash
set -euo pipefail
echo '=== hybrid topmost keeper patch service ==='
systemctl status mediastreamer-hybrid.service --no-pager || true

echo
echo '=== state ==='
cat /opt/mediastreamer-hybrid/state/state.json || true

echo
echo '=== kiosk wrapper target ==='
grep -nE 'READY_MARKER|KEEPER_PIDFILE|KEEPER_READYFILE|NOW_PLAYING_URL|VOLUMIO_ROOT_URL|TARGET_MODE|LAUNCHER_URL|ARTWORK_FILE|KEEPER_SCRIPT|default-background-color|start_artwork_keeper|stop_artwork_keeper' /opt/mediastreamer-hybrid/kiosk-wrapper.sh || true

echo
echo '=== artwork keeper script ==='
head -90 /opt/mediastreamer-hybrid/artwork_keeper.py 2>/dev/null || true

echo
echo '=== current plymouth theme ==='
plymouth-set-default-theme || true

echo
echo '=== current cmdline token ==='
grep -o 'bootdelay=[^ ]*' /proc/cmdline || true

echo
echo '=== visible theme directory ==='
ls -l /usr/share/plymouth/themes/volumio-adaptive | grep -E 'appliance_artwork|volumio-adaptive.script' || true

echo
echo '=== plymouth quit drop-in ==='
sed -n '1,120p' /etc/systemd/system/plymouth-quit.service.d/mediastreamer-direct-now-playing-topmost-keeper.conf 2>/dev/null || echo 'missing'

echo
echo '=== ready marker references ==='
grep -Rni 'mediastreamer-kiosk-ready\|artwork-keeper' /opt/mediastreamer-hybrid /etc/systemd/system 2>/dev/null || true

echo
echo '=== local launcher health ==='
curl -s http://127.0.0.1:7700/api/healthz || true

echo
echo '=== shellctl path ==='
command -v mediastreamer-shellctl || true
