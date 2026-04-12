#!/bin/bash
set -e

echo "Removing Scale FM Overlay runtime"
rm -rf /data/plugins/user_interface/radio_scale_peppy/runtime || true
sudo systemctl disable --now scale_fm_renderer.service || true
sudo rm -f /etc/systemd/system/scale_fm_renderer.service || true
sudo systemctl daemon-reload || true
