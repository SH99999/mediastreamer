# appliance-control-overlay-and-install-stabilization intake v1

status: ready-for-codex
actor: chatgpt

## source/context
- source chat/session: exchange/chatgpt/sessions/appliance-control-overlay-and-install-stabilization__live_v1.md
- source timestamp (UTC): 2026-04-17T19:19:39Z
- participants: owner + chatgpt

## objective
- execute a coordinated stabilization and delivery package across hardware/frontpanel control, fun-line, bridge, tuner, and install/autostart behavior without losing the current code baseline

## locked decisions
1. `ship to codex` handoff for ChatGPT-authored exchange artifacts uses `integration/chatgpt` as the write branch.
2. the canonical execution source for this package is the exchange artifact set, not the accidentally created issue-based intake artifacts.
3. legacy/current implementation code must be retained separately as starting-point truth rather than overwritten without preservation.
4. hardware/control replacement must avoid conflicts with the HiFiBerry card.
5. UX alignment applies to Fun Line, Bridge, and Tuner in this package.

## open decisions
1. final governed name and boundary for the Rotary Encoder II replacement plugin.
2. exact preservation strategy for the current code baseline.
3. whether root-cause startup/render lifecycle fixes should be implemented once in shared runtime/overlay control or separately per component.
4. exact formal pin-map adjustments required after HiFiBerry conflict analysis.

## required implementation
1. create/plan the Rotary Encoder II replacement as a project-native appliance/frontpanel control plugin with Volumio config page, angle sensor support, pushbuttons, LEDs, current appliance-control functions, and useful standard Volumio actions.
2. eliminate failure modes where missing configured targets, overlay/web-emit paths, or partial install states can hang/crash the control lane.
3. stabilize Fun Line startup/open lifecycle, remove white/black flicker, improve animation/graphics quality, and align to current UX direction.
4. audit and fix Bridge Spotify hit reliability and related code-path defects; align bridge overlay UX.
5. stabilize Tuner renderer startup, improve turn performance, smooth needle movement, and remove visible jumps/sprints; align tuner UX.
6. preserve the existing code baseline in a separate directory/release/archive-equivalent retained path before destructive replacement.
7. ensure autostart-capable plugins install cleanly on the Pi and investigate/fix the post-install middle-state enable toggle problem on Tuner and Fun Line.
8. produce a Codex-owned canonical execution/distribution manifest if work must fan out across multiple target branches/components.

## required governance updates
1. update affected component truth files/journals/streams for hardware/frontpanel, fun-line, bridge, tuner, and SI where operational reality changes.
2. after handoff, update ChatGPT exchange governance docs so `ship to codex` write-path ambiguity is removed and `integration/chatgpt` is explicit for ChatGPT-authored exchange writes.
3. document the chosen preservation mechanism for legacy/current code baseline.

## risks
1. duplicate execution risk from accidentally created issue-based intake artifacts (#160, #163, #164 and related escalation artifacts) unless Codex treats this exchange package as canonical.
2. cross-component startup/render lifecycle defects may require shared root-cause analysis rather than isolated patching.
3. hardware/frontpanel refactor can introduce wiring/resource conflicts if HiFiBerry constraints are not checked first.
4. install/autostart failures may span plugin packaging, postinstall, UI state sync, and runtime enable-state logic.

## non-loss requirements
1. `ship to codex` for ChatGPT-authored exchange writes must use `integration/chatgpt`.
2. the current code baseline must be preserved separately.
3. HiFiBerry conflicts must be explicitly avoided.
4. the autostart/enable toggle problem after install must be treated as a real defect.
5. Fun Line, Bridge, and Tuner must align to the current UX direction.

## execution request for Codex
- execution branch: codex-owned sequential target execution from this exchange package; ChatGPT-authored handoff artifacts were written on `integration/chatgpt`
- required output: target branch plan/manifest + PR(s) to `main` + decision-ready packet(s) + rollback command(s) + next owner click

## execution gate
- execution_gate: now
- execution_gate_label: gate:now
- why_now: owner explicitly requested immediate handoff so Codex can start development on current defects and replacement work without more friction.
- why_not_now: waiting increases drift and preserves known unstable control/render/install behavior.
- promotion_trigger: owner requested governed handoff via `ship to codex` behavior.
- safe_to_attach_to_current_package: yes
- related_files_outputs: exchange/chatgpt/sessions/appliance-control-overlay-and-install-stabilization__live_v1.md; exchange/chatgpt/protocol-main/appliance-control-overlay-and-install-stabilization__protocol_v1.md; exchange/chatgpt/inbox-main/20260417T191939Z__appliance-control-overlay-and-install-stabilization__intake_snapshot_v1.md
- impacted_portfolio_component: system-integration, hardware, fun-line, bridge, tuner

## label index (query/routing)
- expected_labels:
  - gate:now
  - state:ready-for-agent
  - component:system-integration
  - agent:system-integration
- label_truth_rule: labels route/query only; repo sections in this file remain canonical detailed truth

## lifecycle tracking
- codex_trigger: ship-to-codex
- materialized_protocol: exchange/chatgpt/protocol-main/appliance-control-overlay-and-install-stabilization__protocol_v1.md
- main_inbox_snapshot: exchange/chatgpt/inbox-main/20260417T191939Z__appliance-control-overlay-and-install-stabilization__intake_snapshot_v1.md
- source_pr_url:
- source_branch: integration/chatgpt
- review_target_artifacts:
- chatgpt_review_result: pending
- owner_review_override: no
- owner_override_note:
- governance_closeout_status: pending
- next_owner_click: wait for Codex execution output and review the resulting decision-ready PR packet(s)
