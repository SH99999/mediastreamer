# ISSUE GOVERNANCE ROUTING STANDARD V1

## Purpose
This document defines how governance and delivery issues are classified, routed, and closed in this repository.

## Project model
Use one central GitHub Project for the repository.

Recommended project name:
- `Scale Radio Governance & Delivery`

Do not create one project per component.
Use labels and filtered views inside the single project instead.

## Core routing rule
Issues are routed by labels, not by GitHub assignee.

Reason:
- component chats and agent lanes may change over time
- labels are easy to automate
- human assignees remain optional

## Label groups
### Component labels
- `component:bridge`
- `component:tuner`
- `component:starter`
- `component:autoswitch`
- `component:fun-line`
- `component:hardware`
- `component:system-integration`

### Impact labels
- `impact:component-only`
- `impact:cross-component`
- `impact:system-wide`

### Type labels
- `type:decision`
- `type:governance-update`
- `type:branch-drift`
- `type:journal-gap`
- `type:release-readiness`
- `type:integration-risk`
- `type:defect`
- `type:follow-up`

### Agent routing labels
- `agent:system-integration`
- `agent:bridge`
- `agent:tuner`
- `agent:starter`
- `agent:autoswitch`
- `agent:fun-line`
- `agent:hardware`
- `agent:ux`
- `agent:governance`

### State labels
- `state:needs-triage`
- `state:needs-decision`
- `state:ready-for-agent`
- `state:blocked`
- `state:awaiting-owner`
- `state:docs-update-required`
- `state:done`

### Source labels
- `source:weekly-report`
- `source:decision-scan`
- `source:branch-monitor`
- `source:journal-monitor`
- `source:manual`
- `source:pr-review`

## Default routing logic
- `impact:system-wide` must also carry `agent:system-integration`
- `impact:cross-component` should also carry `agent:system-integration`
- `component:<x>` with only component-local impact should carry `agent:<x>`
- `type:decision` should carry `state:needs-decision`
- after owner decision, switch to `state:docs-update-required`
- after governance updates are merged, switch to `state:done`

## Human assignee rule
GitHub assignee is optional and reserved for human ownership only.
Do not depend on assignee for agent routing.

## Issue lifecycle
1. issue is created manually or by workflow
2. labels classify component, impact, type, source, and agent route
3. responsible lane reviews repo truth and points the owner to the required decision or action
4. owner decides if needed
5. governance docs and journals are updated in a PR
6. issue is marked `state:done` after merge

## Project usage
The single project should use filtered views by:
- component label
- agent label
- state label
- impact label

## Project auto-add guidance
Enable project auto-add for issues from this repository, or use a project filter based on labels such as:
- `label:governance`
- `label:type:decision`
- `label:type:branch-drift`
- `label:type:journal-gap`
- `label:weekly-governance-report`

## Governance source rule
Issue text is not the primary truth source.
The primary truth remains:
- contracts in `contracts/repo/`
- system integration journals in `journals/system-integration-normalization/`
- component journals in `journals/<component>/`

Issues are the operating queue built from that truth.
