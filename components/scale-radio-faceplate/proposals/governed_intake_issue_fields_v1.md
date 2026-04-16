# Governed intake issue fields — scale-radio-faceplate v1

Status note: GitHub issue creation/update is not exposed in the current connector lane, so this file is the issue-ready artifact prepared for manual issue creation or later agent replay.

## Intended issue title
`[Demand] Bootstrap scale-radio-faceplate as governed front-face contract component`

## Intended labels
- `governance`
- `source:manual`
- `impact:cross-component`
- `type:decision`
- `state:needs-decision`
- `agent:system-integration`
- `agent:ux`

Component labels to add once available:
- `component:tuner`
- `component:bridge`
- `component:fun-line`
- `component:starter`

## Governed demand intake fields
- Demand type: `Decision`
- Impact: `cross-component`
- Primary component suffix: `faceplate`
- Preferred agent lane: `system-integration`
- Summary: `Bootstrap scale-radio-faceplate as the governed front-face visual and interaction contract component for Scale Radio so tuner, bridge, fun-line, and starter consume one canonical visible-appliance truth instead of redefining it locally.`
- Known repo truth or affected docs:
  - `contracts/repo/system_integration_governance_index_v8.md`
  - `docs/agents/system_integration_recovery_onboarding_v8.md`
  - `journals/system-integration-normalization/STATUS_system_integration_normalization_v9.md`
  - `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v10.md`
  - `journals/system-integration-normalization/stream_v7.md`
  - `journals/system-integration-normalization/ui_gui_stream_v2.md`
  - `journals/scale-radio-bridge/current_state_v2.md`
  - `journals/scale-radio-tuner/current_state_v3.md`
  - `journals/scale-radio-fun-line/current_state_v2.md`
  - `journals/scale-radio-starter/current_state_v2.md`
- Proposal markdown URI or repo path: `components/scale-radio-faceplate/proposals/stage_b_intake_proposal_v1.md`
- Proposal revision or digest: `scale_radio_faceplate_transfer_v1.zip / review-normalized on 2026-04-15`
- Owner decision needed: `Decide whether scale-radio-faceplate should be bootstrapped as the canonical governed front-face contract component for Scale Radio.`
- Decision options:
  - `OPT-A` — Create `scale-radio-faceplate` under `components/` as a normal governed component, contract-heavy in v1. **RECOMMENDED**
  - `OPT-B` — Store the same material in a repo-wide product-contract area without creating a component.
  - `OPT-C` — Do not create a new component; distribute the rules across existing component docs and journals.

## Owner decision packet
- decision statement: `Decide whether scale-radio-faceplate should be bootstrapped as a new governed component that owns the visible front-face contract for Scale Radio.`
- allowed options:
  - `OPT-A`
  - `OPT-B`
  - `OPT-C`
- recommended option: `OPT-A`
- deployment/runtime impact: `No immediate runtime deployment change in v1; this is a contract/journal/bootstrap change that reduces cross-component drift and prepares future renderer-facing work.`
- specialist distribution map:
  - `agent:system-integration`
  - `agent:ux`
  - `agent:tuner`
  - `agent:bridge`
  - `agent:fun-line`
  - `agent:starter`
- merge gate: `owner approval required`

## decision_output_v1
```yaml
decision_output_v1:
  issue: not-created-in-current-connector-lane
  decision_id: DEC-scale-radio-faceplate-intake-01
  selected_option: OPT-A
  owner_approval: true
  routed_agents:
    - agent:system-integration
    - agent:ux
    - agent:tuner
    - agent:bridge
    - agent:fun-line
    - agent:starter
  required_updates:
    - contracts/repo/system_integration_governance_index_v8.md
    - docs/agents/system_integration_recovery_onboarding_v8.md
    - journals/system-integration-normalization/STATUS_system_integration_normalization_v9.md
    - journals/system-integration-normalization/DECISIONS_system_integration_normalization_v10.md
    - journals/system-integration-normalization/stream_v7.md
    - journals/system-integration-normalization/ui_gui_stream_v2.md
    - journals/scale-radio-bridge/current_state_v2.md
    - journals/scale-radio-tuner/current_state_v3.md
    - journals/scale-radio-fun-line/current_state_v2.md
    - journals/scale-radio-starter/current_state_v2.md
  followup_actions:
    - open_pr_to_main
    - create_or_update_issue_when_tooling_allows
```
