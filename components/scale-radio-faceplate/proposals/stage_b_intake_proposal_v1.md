## 1) Proposal Markdown Document

# Stage-B Proposal — Intake of `scale-radio-faceplate` as a New Governed Component

## Problem statement
The repository already contains cross-component UI/UX truth for the visible Scale Radio appliance front, but that truth currently lives outside the governed component structure. This creates drift risk across tuner, bridge, fun-line, starter, and system-integration work because the front-face contract has no canonical component owner.

## Scope

### In-scope
- bootstrap a new governed component named `scale-radio-faceplate`
- define it as the canonical owner of front-face visual and interaction contracts
- place the existing UX/faceplate documents into a repo-native component structure
- establish journal truth for the new component
- define consumer relationship to tuner, bridge, fun-line, and starter

### Out-of-scope
- runtime renderer implementation
- source logic
- GPIO/input logic
- Spotify API logic
- lyrics fetching logic
- deploy/rollback workflow changes for existing runtime components
- final beauty-render approval as repo truth

## Affected component suffixes
- faceplate
- tuner
- bridge
- fun-line
- starter

## UX goals
- create one canonical home for the visible appliance front contract
- keep the analog scale as the visual truth source
- prevent UI drift across overlay and renderer consumers
- make front-face rules deterministic for Codex, chats, and future renderer work
- keep runtime components implementing against the contract instead of redefining it

## Constraints / assumptions
- `main` remains the protected truth branch
- intake must follow the existing issue/project routing model
- repository-facing output must remain English
- the new component should be contract-led in v1
- no direct mutation of protected truth should be assumed outside normal governed repo flow
- Bridge remains an overlay component and must keep its own runtime/business-logic ownership
- the faceplate component must not absorb tuner or bridge runtime responsibilities

## Proposed solution
Create a new governed component:

- canonical component name: `scale-radio-faceplate`
- branch suffix: `faceplate`
- work branch: `dev/faceplate`

Bootstrap it as a contract-heavy component with:
- `components/scale-radio-faceplate/README.md`
- `journals/scale-radio-faceplate/current_state_v1.md`
- `journals/scale-radio-faceplate/stream_v1.md`

Initial component contents should include the normalized front-face contract package:
- foundation contract
- blueprint lock
- visual master
- overlay and mode behavior
- scale artwork construction grid
- layer export spec
- state sheets
- theme pack
- typography tokens
- color tokens
- metadata and reminder grammar

Ownership model:
- `scale-radio-faceplate` owns visible appliance-front doctrine
- tuner owns tuning/source runtime behavior
- bridge owns overlay/runtime business logic
- fun-line owns character/animation behavior
- starter owns startup/runtime presentation path
- faceplate provides the visual and interaction contract all of them must respect

## Alternatives considered

### Option A
Create `scale-radio-faceplate` as a normal new component under `components/` with contract-heavy v1 contents.

### Option B
Keep the material outside components and place it in a repo-wide product-contract area.

### Option C
Distribute the front-face rules across existing component docs and journals without creating a dedicated component.

## Risks and mitigations

### Risk 1
Component boundary confusion with tuner and bridge.

**Mitigation:** lock ownership boundaries explicitly in the bootstrap README and current state.

### Risk 2
Front-face truth drifts again if not referenced by consuming components.

**Mitigation:** require tuner, bridge, fun-line, and starter journals to reference `scale-radio-faceplate` as upstream visual contract truth.

### Risk 3
The new component becomes a moodboard bucket instead of governed truth.

**Mitigation:** restrict v1 to contract, asset-reference, token, and handoff material only; exclude uncontrolled visual experimentation.

### Risk 4
Repo complexity increases without runtime value.

**Mitigation:** keep v1 contract-led and asset-light; no renderer implementation is required for intake.

## Acceptance criteria (testable)
- `scale-radio-faceplate` exists as a governed component root
- `dev/faceplate` is the canonical work branch for that component
- README, `current_state_v1.md`, and `stream_v1.md` exist
- the normalized front-face contract package is placed under the new component
- ownership boundaries are explicit and non-overlapping with tuner/bridge/fun-line/starter
- system-integration truth records the intake decision
- consumer components can reference the faceplate component as upstream contract truth
- no runtime component ownership is silently transferred into faceplate

## Rollback / fallback notes
If intake is rejected:
- keep the current UX package outside repo truth
- do not bootstrap `scale-radio-faceplate`
- continue using the material as pre-governed working documentation only

If intake is accepted but later superseded:
- mark the component as contract-only or superseded in journals
- keep runtime ownership with the existing components
- preserve the front-face contracts as historical truth rather than deleting them

## Governance/docs/journals that would need updates
- `contracts/repo/system_integration_governance_index_v8.md`
- `docs/agents/system_integration_recovery_onboarding_v8.md`
- `journals/system-integration-normalization/STATUS_system_integration_normalization_v9.md`
- `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v10.md`
- `journals/system-integration-normalization/stream_v7.md`
- `components/scale-radio-faceplate/README.md`
- `journals/scale-radio-faceplate/current_state_v1.md`
- `journals/scale-radio-faceplate/stream_v1.md`
- affected consumer journals for tuner, bridge, fun-line, and starter

## Recommended option (single clear recommendation)
**Recommend Option A:** bootstrap `scale-radio-faceplate` as a normal governed component under `components/`, contract-heavy in v1, with runtime components consuming it as upstream front-face truth.

---

## 2) Intake Fields (for GitHub template)

**demand_type:** new_component_intake  
**impact:** cross-component  
**components:** faceplate,tuner,bridge,fun-line,starter  
**summary:** Bootstrap `scale-radio-faceplate` as the governed front-face visual and interaction contract component for Scale Radio.  
**proposal_uri:** `components/scale-radio-faceplate/proposals/stage_b_intake_proposal_v1.md`  
**proposal_revision:** `stage-b-faceplate-intake-v1`  
**decision_need:** Yes — owner/SI decision required on classification and bootstrap of a new governed component.  
**decision_options:**  
- `OPT-A` — Create `scale-radio-faceplate` under `components/` as a normal governed component, contract-heavy in v1. **RECOMMENDED**  
- `OPT-B` — Store the same material in a repo-wide product-contract area without creating a component.  
- `OPT-C` — Do not create a new component; distribute the rules across existing component docs and journals.  

---

## 3) Owner Decision Packet

**decision_statement:** Decide whether `scale-radio-faceplate` should be bootstrapped as a new governed component that owns the visible front-face contract for Scale Radio.

**options:**
- `OPT-A` — New governed component under `components/scale-radio-faceplate/`, contract-heavy in v1
- `OPT-B` — Repo-wide product-contract area, no new component
- `OPT-C` — No new component; distribute ownership across existing components

**recommended_option:** `OPT-A`

**deployment_runtime_impact:** No immediate runtime deployment change in v1; this is a contract/journal/bootstrap change that reduces cross-component drift and prepares future renderer-facing work.

**specialist_distribution_map:**
- `agent:system-integration` — intake alignment, governance placement, journal/decision routing
- `agent:ux` — faceplate contract normalization, token pack, visual/state contract ownership
- `agent:tuner` — consume analog scale and snap behavior contract
- `agent:bridge` — consume right-column Bridge and Sing Along trigger contract
- `agent:fun-line` — consume overlay occupancy restrictions
- `agent:starter` — consume startup-facing visual identity constraints

**merge_gate:** owner approval required

---

## 4) Machine-readable decision output block

```yaml
decision_output_v1:
  issue: TBD
  decision_id: DEC-scale-radio-faceplate-intake-01
  selected_option: OPT-A
  owner_approval: true
  routed_agents:
    - agent:system-integration
    - agent:ux
  required_updates:
    - contracts/repo/system_integration_governance_index_v8.md
    - journals/system-integration-normalization/STATUS_system_integration_normalization_v9.md
    - journals/system-integration-normalization/DECISIONS_system_integration_normalization_v10.md
    - journals/system-integration-normalization/stream_v7.md
  followup_actions:
    - open_or_update_pr
    - update_labels_and_state
```
