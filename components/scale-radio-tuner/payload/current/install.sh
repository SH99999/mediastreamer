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

export DEBIAN_FRONTEND=noninteractive
echo "Installing Scale FM Overlay dependencies"
run_sudo apt-get update
run_sudo apt-get -y install python3-pygame python3-pil fonts-dejavu-core alsa-utils --no-install-recommends

PLUGIN_DIR="/data/plugins/user_interface/radio_scale_peppy"
PLAYLIST_DIR="/data/playlist"
PLAYLIST_PATH="$PLAYLIST_DIR/radioscale_base"
FAV_DIR="/data/favourites"
MY_WEB_RADIO_PATH="$FAV_DIR/my-web-radio"

[ -d "$PLAYLIST_DIR" ] || run_sudo mkdir -p "$PLAYLIST_DIR"
[ -d "$FAV_DIR" ] || run_sudo mkdir -p "$FAV_DIR"

python3 <<'PY2'
import json
from pathlib import Path
seed = [
  {"service": "webradio", "name": "Hitradio OE3", "uri": "https://orf-live.ors-shoutcast.at/oe3-q2a", "title": "Hitradio OE3"},
  {"service": "webradio", "name": "FM4", "uri": "https://orf-live.ors-shoutcast.at/fm4-q2a", "title": "FM4"},
  {"service": "webradio", "name": "RADIO WIEN", "uri": "https://orf-live.ors-shoutcast.at/wie-q2a", "title": "RADIO WIEN"},
  {"service": "webradio", "name": "Deep House Radio", "uri": "https://streaming.shoutcast.com/dhr", "title": "Deep House Radio"},
  {"service": "webradio", "name": "CHILLOUT ANTENNE", "uri": "https://stream.antenne.de/chillout/stream/mp3", "title": "CHILLOUT ANTENNE"},
  {"service": "webradio", "name": "OLDIE ANTENNE", "uri": "https://stream.antenne.de/oldie-antenne/stream/mp3", "title": "OLDIE ANTENNE"},
  {"service": "webradio", "name": "Antenne Kärnten", "uri": "https://live.antenne.at/ak", "title": "Antenne Kärnten"},
  {"service": "webradio", "name": "Kronehit", "uri": "https://secureonair.krone.at/kronehit1058.mp3", "title": "Kronehit"}
]
playlist_path = Path('/data/playlist/radioscale_base')
if not playlist_path.exists():
    entries = [{"service": i["service"], "uri": i["uri"], "title": i["title"], "artist": "", "album": "", "albumart": "", "type": "webradio"} for i in seed]
    playlist_path.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
my_web_radio = Path('/data/favourites/my-web-radio')
try:
    existing_text = my_web_radio.read_text(encoding='utf-8') if my_web_radio.exists() else ''
    existing = json.loads(existing_text) if existing_text.strip() else []
    if not isinstance(existing, list):
        existing = []
except Exception:
    existing = []
seen = {(str(x.get('name','')).strip().lower(), str(x.get('uri','')).strip()) for x in existing if isinstance(x, dict)}
changed = False
for item in seed:
    key = (item['name'].strip().lower(), item['uri'].strip())
    if key not in seen:
        existing.append({"service": "webradio", "name": item['name'], "uri": item['uri']})
        seen.add(key)
        changed = True
if changed or not my_web_radio.exists():
    my_web_radio.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
PY2

if [ -d "$PLUGIN_DIR" ]; then
  run_sudo chmod +x "$PLUGIN_DIR/run_radio_scale.sh" || true
  run_sudo chmod +x "$PLUGIN_DIR/install.sh" || true
  run_sudo chmod +x "$PLUGIN_DIR/uninstall.sh" || true
fi

SERVICE_SRC="$PLUGIN_DIR/systemd/scale_fm_renderer.service"
SERVICE_DST="/etc/systemd/system/scale_fm_renderer.service"

if [ -f "$SERVICE_SRC" ]; then
  run_sudo cp "$SERVICE_SRC" "$SERVICE_DST"
  run_sudo chmod 644 "$SERVICE_DST"
  run_sudo chmod +x "$PLUGIN_DIR/run_renderer_daemon.sh" || true
  run_sudo systemctl daemon-reload || true
  run_sudo systemctl enable scale_fm_renderer.service || true
  run_sudo systemctl restart scale_fm_renderer.service || true
fi

echo "plugininstallend"
exit 0
