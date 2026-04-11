# INTEGRATION FREEZE V1

Project: Scale Radio / RadioScaleOS Appliance Track on Volumio 4

This document defines the single leading integration truth across the currently imported authoritative handovers. It does not invent new component-local features, does not rename frozen runtime contracts, and does not upgrade non-leading variants.

## 1. GLOBAL STATE MODEL

### 1.1 System layer
- `system.boot.transition` = starter handover path active
- `system.power.visible` = system not in standby
- `system.power.hidden` = standby active

Global idle, deep-idle, FPS-cap and render-throttling semantics are not globally stabilized in the imported handovers and are therefore not promoted to authoritative system states here.

### 1.2 Display and overlay layer
- `display.owner.none` = Volumio GUI or Now Playing visible, no heavy overlay owns the screen
- `display.owner.scale_radio_tuner` = tuner overlay may actively render
- `display.owner.scale_radio_fun_line` = fun-line overlay may actively render

The only authoritative shared owner arbitration file is `/tmp/mediastreamer_active_overlay.json`.

### 1.3 Component layer
- Starter: `hidden`, `visible`, `transition`
- Tuner: `visible_active`, `hidden_idle`, `hidden_deep_idle`, `source_open_request_received`, `exit_to_regular_volumio_gui`
- Fun Line: `closed`, `visible`, `hidden_idle`
- AutoSwitch: `tape_monitor_enabled`, `tape_monitor_disabled`
- Bridge: provider states for track normalization, lyrics, Spotify match, cache readiness and backoff

## 2. GLOBAL EVENT CONTRACT

No new global event bus is introduced. Existing runtime methods remain valid legacy contracts. Freeze v1 adds canonical semantic naming above them.

### 2.1 Canonical event families
- `system.startup.begin`
- `system.startup.handover.preferred`
- `system.startup.handover.fallback`
- `system.power.standby.request`
- `system.power.wake.request`
- `display.overlay.request.scale_radio_tuner`
- `display.overlay.request.scale_radio_fun_line`
- `display.overlay.exit_to_gui`
- `display.owner.change`
- `tuner.mode.request.scale_radio`
- `tuner.mode.request.normal_gui`
- `tuner.control.status.request`
- `autoswitch.signal.detected`
- `autoswitch.signal.lost_confirmed`
- `autoswitch.route.enable`
- `autoswitch.route.disable`
- `bridge.poll.tick`
- `bridge.track.changed`
- `bridge.lyrics.fetch.requested`
- `bridge.spotify.lookup.started`

### 2.2 Frozen legacy runtime methods that remain valid
Tuner:
- `gpio13OpenScale`
- `encoder1ShortPress`
- `encoder1LongPress`
- `setScaleMode`
- `setNormalMode`
- `getControlStatus`

Fun Line:
- `gpio13OpenFun`
- `encoder1ShortPress`
- `encoder1LongPress`

Starter:
- `mediastreamer-shellctl standby`
- `mediastreamer-shellctl wake`
- `mediastreamer-shellctl status`

## 3. OVERLAY / DISPLAY OWNER MATRIX

| Display owner | Visible surface | Tuner | Fun Line | Bridge | AutoSwitch | Starter |
|---|---|---|---|---|---|---|
| `system.startup` | startup and handover shell | not leading | not leading | hidden | hidden | leading |
| `display.owner.none` | Volumio GUI or Now Playing | `hidden_idle` | `closed` | provider only | background | not leading |
| `display.owner.scale_radio_tuner` | Radio Scale / Tuner | `visible_active` | must not be heavy-active | provider only | background | not leading |
| `display.owner.scale_radio_fun_line` | Fun Line | must be `hidden_deep_idle` | `visible` | provider only | background | not leading |

No authoritative display-owner contract is yet stabilized for an AutoSwitch-specific aux or peppy-owned foreground state.

## 4. COMPONENT DEPENDENCY MATRIX

| Component | Type | Direct dependencies |
|---|---|---|
| Starter | system runtime | Volumio 4, touch_display, Chromium or kiosk runtime, local targets `:4004` and `:3000` |
| Tuner | primary visible overlay | Volumio source and browse path, Touch Display, Rotary Encoder II, Now Playing, shared owner file |
| AutoSwitch | audio routing and service layer | ALSA, arecord, sox, bc, amixer, systemd |
| Bridge | provider layer | Volumio REST on `:3000`, Node runtime, Python and sqlite, OpenSSL, Spotify APIs, LRCLIB |
| Fun Line | secondary overlay | Volumio plugin runtime, Chromium or kiosk runtime, Tuner coexistence, shared owner file |

## 5. CONFLICT LIST

1. Heavy-renderer conflict between Tuner and Fun Line. Only one may actively render at a time.
2. Starter baseline conflict with later startup experiments. Post-`v0.2.2` startup lines remain non-leading.
3. Tuner contract break risk if public methods, `scale_fm_renderer.service` or classic spawn fallback are changed.
4. Fun Line config/importer ambiguity. `0.4.2` is leading runtime baseline; later config and importer lines are not normalized as working.
5. AutoSwitch intended aux and peppy resume behavior is broader than the currently proven handover contract.
6. Bridge role expansion is forbidden. It remains provider-layer only.
7. State semantics differ across Starter, Tuner and Fun Line; Freeze v1 keeps them layered instead of flattening them into one false universal state model.

## 6. INTEGRATION ORDER

1. Starter
   - `mediastreamer_bootdelay_fix_v0.1.0`
   - `mediastreamer_hybrid_startup_standby_v0.2.2_stable`
2. Tuner
   - `Scale FM Overlay 1.10.2`
   - `Scale FM Source 1.10.2`
3. Fun Line
   - `fun_linea_overlay_0.4.2.zip`
   - `fun_linea_source_0.4.2.zip`
4. AutoSwitch
   - `revox_autoswitch_v2_asymmetric_delay_logic`
5. Bridge
   - `radioscale_overlay_bridge_0.2.3_db_cache_r1.zip`

This is the authoritative global installation and integration order.

## 7. RELEASE BASELINE V1

Starter:
- `mediastreamer_bootdelay_fix_v0.1.0`
- `mediastreamer_hybrid_startup_standby_v0.2.2_stable`

Tuner:
- `Scale FM Overlay 1.10.2`
- `Scale FM Source 1.10.2`

AutoSwitch:
- `revox_autoswitch_v2_asymmetric_delay_logic`

Bridge:
- authoritative: `radioscale_overlay_bridge_0.2.3_db_cache_r1.zip`
- rollback anchor: `rsob_022sf22l.zip`

Fun Line:
- `fun_linea_overlay_0.4.2.zip`
- `fun_linea_source_0.4.2.zip`

Frozen shared contracts:
- startup handover order remains `4004 -> 3000`
- shared owner arbitration file remains `/tmp/mediastreamer_active_overlay.json`
- Tuner public methods remain unchanged
- Fun Line open and close methods remain unchanged
- Bridge remains provider-only
- AutoSwitch remains ALSA and systemd based

## 8. REGRESSION MATRIX V1

A change is regression-critical if it does any of the following:
- breaks the starter handover order `4004 -> 3000`
- breaks `mediastreamer-shellctl` standby, wake or status
- renames or removes `scale_fm_renderer.service`
- changes frozen Tuner method names
- removes classic Tuner spawn fallback
- ignores the shared owner file
- allows Fun Line to remain heavy-active while hidden
- changes AutoSwitch ADC routing assumptions without explicit revalidation
- moves Bridge away from polling-first provider behavior without explicit revalidation
- mixes post-`0.2.2` starter experiments into the authoritative baseline
- mixes Tuner `1.10.2` with older leading-line alternatives
- mixes Bridge `0.2.3_db_cache_r1` with the later `0.3.x` UI line
- treats Fun Line `0.5.x` or `0.6.x` as release-leading runtime

## Normalization note

Freeze v1 is the first integrated repository copy of the system truth. It is derived from the imported authoritative handovers and the repo governance baseline, without inventing new implementation details.