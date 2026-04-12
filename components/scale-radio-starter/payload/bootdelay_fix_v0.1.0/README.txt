MediaStreamer Bootdelay Fix v0.1.0

Purpose
- Sets bootdelay=0 in /boot/cmdline.txt.
- Makes a timestamped backup before changing anything.
- Does not touch volumiokiosk, touch_display, systemd services, or audio settings.

Install
- chmod +x install.sh uninstall.sh verify.sh
- sudo bash ./install.sh
- sudo reboot

Verify
- sudo /opt/mediastreamer-bootdelay-fix/verify.sh

Rollback
- sudo bash ./uninstall.sh
- sudo reboot



besser!
cd ~/mediastreamer_bootdelay_fix_v0.1.0
chmod +x verify.sh
sudo bash ./verify.sh

Wenn wieder ein Fehler kommt, poste bitte die Ausgabe von:

ls -l /opt/mediastreamer-bootdelay-fix
ls -l ~/mediastreamer_bootdelay_fix_v0.1.0