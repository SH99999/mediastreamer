# UI UX STAGE-B AUTONOMOUS LOOP STANDARD V1

## Purpose
This standard defines the full stage-B operating model for governed proposal intake so external chat proposals can enter repo truth with minimal owner clicks and deterministic SI routing.

## Goal state
The stage-B loop is:
1. external chat creates a proposal artifact (`.md`) outside or inside the repo
2. intake creates one governed issue with the proposal reference
3. labels + workflows classify and route the demand
4. owner receives one decision packet with explicit options and downstream impact
5. owner decision triggers governance updates and specialist distribution

## Input artifact rule
A proposal may be provided as:
- repository file path (preferred)
- immutable URL to external markdown artifact
- attached markdown content snapshot in the issue body

The intake issue must contain:
- proposal reference URI/path
- proposal digest (or immutable revision identifier when available)
- concise summary in repo-facing English

## Canonical intake object
Use a governed issue (`[UX/Asset]` or `[Demand]`) as the canonical intake object.

Scope note:
- UI/UX proposals and component/runtime proposals both use this same intake and decision contract.
- Specialist routing remains label-driven (for example `agent:ux`, `agent:tuner`, `agent:bridge`) and not chat-memory-driven.

Required fields for stage-B intake:
- demand type
- impact
- affected components
- proposal reference URI/path
- proposal digest/revision
- owner decision needed

## Owner decision packet rule
For issues with `state:needs-decision`, the owner packet must contain:
- decision statement (single sentence)
- allowed options (2-3 mutually exclusive)
- recommended option
- governance/doc files that must change if each option is chosen
- deployment/runtime impact summary
- specialist distribution map (`agent:*` labels)
- explicit merge gate statement (`owner approval required`)

## Decision output contract (machine-readable block)
Use this block in issue comments or PR descriptions:

```yaml
decision_output_v1:
  issue: <number>
  decision_id: <token>
  selected_option: <option-id>
  owner_approval: true
  routed_agents:
    - agent:system-integration
    - agent:ux
  required_updates:
    - contracts/repo/<file>.md
    - journals/system-integration-normalization/<file>.md
  followup_actions:
    - open_or_update_pr
    - update_labels_and_state
```


## Owner-to-agent input contract (no repeated copy/paste)
For external ChatGPT outputs, owner input to SI/agent should be a URI-based governed intake request, not repeated raw-text copy/paste.

Required owner input fields:
- `source_proposal_uri`
- `proposal_revision`
- `demand_type`
- `components`
- `decision_need`
- `decision_options` + `recommended_option`

Reference prompt and strict YAML format:
- `docs/agents/chatgpt_governed_intake_prompt_v1.md`

Agent execution expectation after receiving this input:
1. populate/update governed intake fields
2. produce `decision_output_v1`
3. commit on dedicated branch (`si/<topic>` for SI/governance scope)
4. push branch and open PR to `main`
5. report only final owner approval action (or exact blocker)

## Project-view readiness rule
The project `Scale Radio Governance & Delivery` must provide owner-facing views that separate:
- decisions waiting for owner approval
- component intake triage (UI/UX + runtime lanes)
- cross-component/system-wide escalations
- merge-ready governance PRs
- delivery readiness per component

The canonical view definitions are maintained in:
- `tools/governance/scale_radio_governance_delivery_views_v1.md`

## Automation boundary
- this standard defines deterministic inputs/outputs so automation can run without chat memory
- if direct project-view mutation is blocked by missing access token or connector scope, record the blocker in SI stream and keep the view blueprint in repo truth

## Non-goals
- replacing protected `main` review gates
- bypassing owner decisions for governance-impacting changes
