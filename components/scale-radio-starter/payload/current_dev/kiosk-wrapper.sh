#!/bin/bash
set -euo pipefail
SERVER_HOST="127.0.0.1"
STATE_API_PORT="7700"
READY_MARKER="/tmp/mediastreamer-kiosk-ready"
KEEPER_PIDFILE="/tmp/mediastreamer-artwork-keeper.pid"
KEEPER_READYFILE="/tmp/mediastreamer-artwork-keeper.ready"
NOW_PLAYING_URL="http://127.0.0.1:4004/"
VOLUMIO_ROOT_URL="http://127.0.0.1:3000/"
TARGET_MODE="nowplaying"
LAUNCHER_URL="http://127.0.0.1:${STATE_API_PORT}/index.html"
ARTWORK_FILE="/opt/mediastreamer-hybrid/www/assets/appliance_artwork.png"
KEEPER_SCRIPT="/opt/mediastreamer-hybrid/artwork_keeper.py"
rm -f "$READY_MARKER" "$KEEPER_PIDFILE" "$KEEPER_READYFILE" 2>/dev/null || true
while true; do
  timeout 2 bash -c "</dev/tcp/${SERVER_HOST}/${STATE_API_PORT}" >/dev/null 2>&1 && break
  sleep 0.2
done
python3 - <<'PY'
import json, time
from pathlib import Path
p = Path('/opt/mediastreamer-hybrid/state/state.json')
try:
    data = json.loads(p.read_text(encoding='utf-8'))
except Exception:
    data = {}
data['standby'] = False
data['startup_completed'] = False
data['startup_started_at'] = int(time.time() * 1000)
data['version'] = '0.3.4-direct-now-playing-topmost-keeper-patch'
p.write_text(json.dumps(data), encoding='utf-8')
PY
if [ -f /data/volumiokiosk/Default/Preferences ]; then
  sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /data/volumiokiosk/Default/Preferences 2>/dev/null || true
  sed -i 's/"exit_type":"Crashed"/"exit_type":"None"/' /data/volumiokiosk/Default/Preferences 2>/dev/null || true
fi
if [ -L /data/volumiokiosk/SingletonCookie ]; then
  rm -rf /data/volumiokiosk/Singleton*
fi
if curl -s --max-time 2 -I "${NOW_PLAYING_URL}" >/dev/null 2>&1; then
  TARGET_MODE="nowplaying"
elif curl -s --max-time 2 -I "${VOLUMIO_ROOT_URL}" >/dev/null 2>&1; then
  TARGET_MODE="volumio"
fi
openbox-session &
xsetroot -solid black
xset -dpms
xset s off
xset s noblank

start_artwork_keeper() {
  rm -f "$KEEPER_PIDFILE" "$KEEPER_READYFILE" 2>/dev/null || true
  if [ -f "$KEEPER_SCRIPT" ] && [ -f "$ARTWORK_FILE" ]; then
    python3 "$KEEPER_SCRIPT" --image "$ARTWORK_FILE" --pidfile "$KEEPER_PIDFILE" --readyfile "$KEEPER_READYFILE" >/tmp/mediastreamer-artwork-keeper.log 2>&1 &
    for i in $(seq 1 24); do
      [ -f "$KEEPER_READYFILE" ] && return 0
      sleep 0.10
    done
  fi
  return 0
}

stop_artwork_keeper() {
  if [ -f "$KEEPER_PIDFILE" ]; then
    PID=$(cat "$KEEPER_PIDFILE" 2>/dev/null || true)
    if [ -n "${PID:-}" ] && kill -0 "$PID" >/dev/null 2>&1; then
      kill "$PID" >/dev/null 2>&1 || true
      wait "$PID" 2>/dev/null || true
    fi
  fi
  rm -f "$KEEPER_PIDFILE" "$KEEPER_READYFILE" >/dev/null 2>&1 || true
}

while true; do
  start_artwork_keeper
  touch "$READY_MARKER" 2>/dev/null || true
  /usr/bin/chromium-browser \
    --simulate-outdated-no-au='Tue, 31 Dec 2099 23:59:59 GMT' \
    --force-device-scale-factor=1 \
    --kiosk \
    --touch-events \
    --no-first-run \
    --noerrdialogs \
    --disable-breakpad \
    --disable-crash-reporter \
    --disable-background-networking \
    --disable-remote-extensions \
    --disable-pinch \
    --disable-session-crashed-bubble \
    --disable-features=Translate,MediaRouter,PaintHolding \
    --default-background-color=000000 \
    --user-data-dir='/data/volumiokiosk' \
    "${LAUNCHER_URL}?target=${TARGET_MODE}"
  stop_artwork_keeper
  rm -f "$READY_MARKER" 2>/dev/null || true
  sleep 0.5
done
