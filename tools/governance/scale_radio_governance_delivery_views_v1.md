# SCALE RADIO GOVERNANCE & DELIVERY — PROJECT VIEW BLUEPRINT V1

Target project: `https://github.com/users/SH99999/projects/1`

Status: canonical view blueprint for owner decision readiness and stage-B multi-component routing (UI/UX + runtime + governance).

Companion renderings:
- Table rendering: `tools/governance/scale_radio_governance_delivery_views_table_v1.md`
- Kanban rendering: `tools/governance/scale_radio_governance_delivery_views_kanban_v1.md`

## View 1 — Owner Decision Queue
- Name: `Owner Decision Queue`
- Type: Table
- Filters:
  - `label:state:needs-decision`
  - `-label:state:done`
- Suggested fields:
  - Title
  - Labels
  - Repository
  - Updated
  - Assignees (optional)
- Purpose: single clickpoint for pending decisions.

## View 2 — Component Intake Triage
- Name: `Component Intake Triage`
- Type: Board (group by `state` label) or Table
- Filters:
  - (`label:agent:ux` OR `label:agent:bridge` OR `label:agent:tuner` OR `label:agent:starter` OR `label:agent:autoswitch` OR `label:agent:fun-line` OR `label:agent:hardware`)
  - `-label:state:done`
- Suggested grouping:
  - `state:needs-triage`
  - `state:ready-for-agent`
  - `state:needs-decision`
  - `state:awaiting-owner`
- Suggested fields:
  - Title
  - Labels
  - Repository
  - Updated
  - Assignees (optional)
- Purpose: isolate component delivery work across UI/UX and runtime lanes from generic governance noise.

## View 3 — Cross-Component Escalations
- Name: `SI Escalations`
- Type: Table
- Filters:
  - `label:agent:system-integration`
  - (`label:impact:cross-component` OR `label:impact:system-wide`)
  - `-label:state:done`
- Purpose: ensure SI-triggering work is always visible.

## View 4 — Owner Approval PR Queue
- Name: `PR Approval Queue`
- Type: Table
- Filters:
  - `is:pr`
  - `label:state:awaiting-owner`
  - `-label:state:done`
- Suggested fields:
  - Checks
  - Review status
  - Labels
  - Updated
- Purpose: owner-ready PR gate with minimal navigation.

## View 5 — Governance Closeout
- Name: `Governance Closeout`
- Type: Table
- Filters:
  - `label:state:docs-update-required`
  - `-label:state:done`
- Purpose: verify repo-truth updates are completed before closure.

## View 6 — Component Delivery Readiness
- Name: `Component Delivery Readiness`
- Type: Table
- Filters:
  - (`label:type:release-readiness` OR `label:type:defect` OR `label:type:integration-risk`)
  - (`label:component:bridge` OR `label:component:tuner` OR `label:component:starter` OR `label:component:autoswitch` OR `label:component:fun-line` OR `label:component:hardware`)
  - `-label:state:done`
- Suggested fields:
  - Title
  - Labels
  - Repository
  - Updated
  - Milestone (optional)
- Purpose: track deploy/test/rollback readiness work per component in one owner-facing queue.

## Minimum operational expectation
If direct API setup for project views is blocked in the execution environment, keep this blueprint in repo truth and apply once with owner credentials.
