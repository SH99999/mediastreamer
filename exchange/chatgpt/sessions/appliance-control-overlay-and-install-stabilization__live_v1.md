# appliance-control-overlay-and-install-stabilization live session v1

status: chatok
actor: chatgpt
last_material_update_utc: 2026-04-17T19:19:39Z

## source/context
- source chat/session: governed chat on 2026-04-17 covering hardware control replacement, fun-line defects, bridge Spotify defects, tuner renderer/performance defects, legacy preservation, and autostart install behavior
- source timestamp (UTC): 2026-04-17T19:19:39Z
- participants: owner + chatgpt

## current objective
- materialize the owner requirements into a single non-loss ChatGPT->Codex handoff package for appliance-control, overlay startup/render stabilization, bridge Spotify hardening, tuner smoothness/performance, and install/autostart behavior

## locked decisions so far
1. `ship to codex` handoff for ChatGPT-authored exchange artifacts must use the existing `integration/chatgpt` write branch.
2. this handoff is canonical through `exchange/chatgpt/sessions/`, `exchange/chatgpt/demands/`, `exchange/chatgpt/protocol-main/`, and `exchange/chatgpt/inbox-main/`, not through issue intake.
3. Codex should treat any issue artifacts created during misrouting as non-canonical for execution scope and should use the exchange artifacts as source of truth for this package.
4. legacy code/starting-point code must be preserved in a separate directory/release or equivalent retained baseline instead of being overwritten in place.
5. tuner and fun-line renderer/startup defects are high-priority execution items and must be addressed together with the new UX direction.

## open decisions
1. final governed name and component boundary for the Rotary Encoder II replacement plugin.
2. whether the replacement belongs as a new component/plugin or as a formally extended hardware/frontpanel lane.
3. exact preservation mechanism for the existing code baseline: parallel release, archive directory, retained legacy subtree, or another governed equivalent.
4. final pin-map adjustments required to avoid conflicts between the angle sensor and the HiFiBerry card while remaining close to current wiring reality.

## active implementation asks
1. replace Rotary Encoder II with a project-native appliance/frontpanel control plugin with a MediaStreamer/Scale Radio aligned name.
2. provide a config page and support angle sensor input, pushbuttons, LEDs, current appliance control behaviors, and useful standard Volumio actions.
3. remove failure modes where configured-but-missing targets, overlay/web-emit coupling, or partial install states can hang/crash the control path.
4. stabilize Fun Line startup and overlay opening; remove white/black flicker; improve animation/asset quality; align to the newer UX direction.
5. audit and improve Bridge Spotify hit reliability and relevant code paths; align bridge overlay UX to the newer guidance.
6. stabilize Tuner renderer startup; improve turn/rotation performance; smooth needle motion and remove jumping/sprinting; align to newer UX guidance.
7. preserve the current code baseline separately.
8. ensure all autostart-capable plugins install cleanly on the Pi and investigate/fix the post-install middle-state enable toggle issue seen on Tuner and Fun Line.

## active risks/blockers
1. previous Rotary Encoder II behavior appears to crash/hang in the presence of overlays and/or configured-but-not-installed targets.
2. renderer/open lifecycle defects may share a cross-component root cause across Fun Line and Tuner.
3. HiFiBerry wiring/resource conflicts must be explicitly avoided before formal pin-map changes.
4. accidental issue-based intake artifacts exist and could cause duplicate execution if Codex does not treat this exchange package as canonical.

## non-loss requirements
1. do not lose the owner requirement that `ship to codex` uses `integration/chatgpt` for ChatGPT-authored exchange writes.
2. do not lose the requirement to preserve the existing code baseline separately.
3. do not lose the requirement that Tuner and Fun Line autostart/enable behavior on install must be fixed, not merely documented.
4. do not lose the requirement that UX alignment applies to Fun Line, Bridge, and Tuner.
5. do not lose the requirement that the hardware/control replacement must avoid HiFiBerry conflicts.

## promotion note
- this live session has been promoted to demand intake via `ship to codex`
