## 1.10.3
- browse-open path now waits briefly for renderer-ready to reduce pre-overlay white flashes
- resident reveal paints an immediate dark pre-frame before the first normal draw cycle
- smoother pointer tuning defaults (higher visible FPS cap, lower deadbands, faster follow gains)
- hidden standby visibility reaction tightened with lower hidden reload/sleep intervals

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
