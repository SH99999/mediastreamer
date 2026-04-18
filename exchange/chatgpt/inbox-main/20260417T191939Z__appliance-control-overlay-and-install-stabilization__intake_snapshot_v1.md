# appliance-control-overlay-and-install-stabilization intake snapshot v1

status: pickup-ready
pickup_rule: main-inbox-v1
snapshot_immutable: true
snapshot_id: 20260417T191939Z
created_at_utc: 2026-04-17T19:19:39Z
trigger_command: ship to codex

## codex pickup contract
- execution_branch: codex-owned sequential target execution from this exchange package
- pickup_ready_marker: status: pickup-ready
- pickup_source: exchange/chatgpt/inbox-main/
- source_write_branch: integration/chatgpt

## source artifacts
- demand_intake: exchange/chatgpt/demands/appliance-control-overlay-and-install-stabilization__intake_v1.md
- materialized_protocol: exchange/chatgpt/protocol-main/appliance-control-overlay-and-install-stabilization__protocol_v1.md
- live_session: exchange/chatgpt/sessions/appliance-control-overlay-and-install-stabilization__live_v1.md

## objective
- replace the unstable Rotary Encoder II dependency with a project-native appliance/frontpanel control solution
- stabilize Fun Line and Tuner startup/open/render behavior
- improve Bridge Spotify hit reliability and code-path robustness
- preserve the current code baseline separately
- fix plugin install/autostart and post-install enable-state issues

## locked decisions
1. `ship to codex` for ChatGPT-authored exchange writes uses `integration/chatgpt`.
2. this exchange package is canonical for execution scope; issue-based intakes from the mistaken routing must not override it.
3. current code baseline must be preserved separately.
4. HiFiBerry conflicts must be explicitly avoided.
5. UX alignment applies to Fun Line, Bridge, and Tuner.

## open decisions
1. final governed naming/boundary for the new frontpanel control plugin.
2. exact retained-baseline preservation mechanism.
3. shared-vs-separate root-cause strategy for startup/render lifecycle defects.
4. final formal pin-map after HiFiBerry conflict review.

## risks
1. duplicate execution risk from accidentally created issue artifacts.
2. cross-component lifecycle/startup defects may require shared fixes.
3. install/autostart/enable-state behavior may involve packaging + postinstall + UI/runtime state synchronization.

## execution requests
1. create a Codex-owned canonical execution/distribution manifest if work fans out across multiple targets.
2. implement the hardware/frontpanel replacement planning and stabilization work.
3. execute the Fun Line, Bridge, Tuner, and install/autostart fixes.
4. follow with governance/doc clarification for the ChatGPT write-path rule if the repo docs remain ambiguous.

## related git objects
- demand_path: exchange/chatgpt/demands/appliance-control-overlay-and-install-stabilization__intake_v1.md
- protocol_path: exchange/chatgpt/protocol-main/appliance-control-overlay-and-install-stabilization__protocol_v1.md
- snapshot_path: exchange/chatgpt/inbox-main/20260417T191939Z__appliance-control-overlay-and-install-stabilization__intake_snapshot_v1.md
- live_session_path: exchange/chatgpt/sessions/appliance-control-overlay-and-install-stabilization__live_v1.md
