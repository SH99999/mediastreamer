## 1.10.2
- first-show pointer hydration fix
- exit UI pre-roll to reduce white flashes
- pointer anti-flicker deadbands and double-buffer visible mode

# Changelog

## 1.10.0

- added resident renderer service bootstrap script and systemd unit
- added renderer PID marker for service-aware process detection
- made overlay startup aware of externally managed resident renderer processes
- kept plugin-spawn fallback when the resident service is not running
- refreshed developer comments and release/install notes

## 1.9.7-safe

- safe release based on the proven 1.9.3 full-frame renderer path
- keeps the selected station playing when leaving the overlay and refreshes radioscale_base in the background
- built-in OE1 seed entries removed from defaults and install-time playlist seeding
- duplicate open guard and 1.9.3 tuning/re-entry fixes remain active
