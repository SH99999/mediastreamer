# appliance-control-overlay-and-install-stabilization protocol snapshot v1

status: active
actor: chatgpt-codex
source_live_session: exchange/chatgpt/sessions/appliance-control-overlay-and-install-stabilization__live_v1.md
source_demand_intake: exchange/chatgpt/demands/appliance-control-overlay-and-install-stabilization__intake_v1.md
last_event_utc: 2026-04-17T19:19:39Z

## current objective
- hand over a no-loss execution package for appliance control replacement, overlay/render startup stabilization, bridge Spotify hardening, tuner smoothness/performance work, and install/autostart defect fixing

## material events
### event 001
- event_utc: 2026-04-17T19:19:39Z
- event_type: ship-to-codex-promotion
- actor: chatgpt
- summary: owner requested that the above requirements be handed to Codex via the exchange path with no more friction; the package was materialized on `integration/chatgpt` and promoted to `ready-for-codex`.
- locked_decisions:
  1. `ship to codex` for ChatGPT-authored exchange writes uses `integration/chatgpt`.
  2. this exchange package is canonical for execution scope; accidentally created issue-based intake artifacts are non-canonical for this handoff.
  3. existing code baseline must be preserved separately.
  4. HiFiBerry conflicts must be explicitly avoided in hardware/frontpanel changes.
  5. UX alignment applies to Fun Line, Bridge, and Tuner.
- open_decisions:
  1. final governed naming/boundary for the Rotary Encoder II replacement plugin.
  2. exact retained-baseline preservation mechanism.
  3. shared-vs-separate root-cause fix path for startup/render lifecycle defects.
  4. final formal pin-map after HiFiBerry conflict analysis.
- risks:
  1. duplicate execution risk from accidentally created issue-based artifacts.
  2. cross-component lifecycle defects may require shared fixes.
  3. packaging/postinstall/runtime state may all contribute to autostart and enable-toggle defects.
- execution_requests:
  1. create a Codex-owned canonical execution/distribution manifest for any cross-branch fan-out.
  2. start implementation across hardware/frontpanel, fun-line, bridge, tuner, and install behavior.
  3. tighten ChatGPT exchange governance docs after handoff so the write-path rule is explicit.
- related_git_objects:
  - live_session: exchange/chatgpt/sessions/appliance-control-overlay-and-install-stabilization__live_v1.md
  - demand_intake: exchange/chatgpt/demands/appliance-control-overlay-and-install-stabilization__intake_v1.md
  - main_inbox_snapshot: exchange/chatgpt/inbox-main/20260417T191939Z__appliance-control-overlay-and-install-stabilization__intake_snapshot_v1.md
  - source_branch: integration/chatgpt
  - source_pr_url:
  - review_target_artifacts:
