# Scale Radio Faceplate

## Purpose
Scale Radio Faceplate is the governed front-face contract component for the visible appliance surface of Scale Radio.

## Current role
- governed component: `scale-radio-faceplate`
- current work lane after bootstrap: `dev/faceplate`
- current bootstrap lane: `si/faceplate-intake-v1`
- artifact posture: contract-led, asset-light, no runtime deploy ownership in v1

## What this component owns
- front-face doctrine
- analog scale construction and behavior rules
- station-marker grammar
- visible needle behavior rules
- metadata column placement rules
- Bridge placement and Sing Along trigger rules from the faceplate side
- visual states, token packs, and renderer handoff contracts

## What this component does not own
- source logic
- GPIO logic
- Bridge runtime/business logic
- Fun Line runtime logic
- Starter runtime/deploy behavior
- tuner source/runtime implementation
- deployment and rollback workflows of consumer components

## Current contract package
- `components/scale-radio-faceplate/contracts/faceplate_contract_package_v1_2.md`
- `components/scale-radio-faceplate/proposals/stage_b_intake_proposal_v1.md`
- `components/scale-radio-faceplate/proposals/governed_intake_issue_fields_v1.md`
- `components/scale-radio-faceplate/reference/HANDOVER_scale-radio-faceplate_stage-b_v1.md`

## Asset posture
This bootstrap is documentation-only.
No authoritative visual binary assets are included yet.
Future authoritative assets should land under:
- `components/scale-radio-faceplate/assets/`
- `components/scale-radio-faceplate/reference/`

## Boundaries
This component owns the visible appliance contract.
Runtime components implement against it.

## See also
- `journals/scale-radio-faceplate/current_state_v1.md`
- `journals/scale-radio-faceplate/stream_v1.md`
- `contracts/repo/ui_ux_stage_b_autonomous_loop_standard_v1.md`
- `contracts/repo/system_integration_governance_index_v7.md`
