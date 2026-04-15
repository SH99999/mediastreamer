# SCALE RADIO GOVERNANCE & DELIVERY — VIEW KANBAN MAP V1

Target project: `https://github.com/users/SH99999/projects/1`

Status: board-oriented rendering of canonical project views so owner can review lanes directly in Git.

## Lane: needs-triage
- **Component Intake Triage**
  - type: Board
  - filter anchor: (`label:agent:ux` OR `label:agent:bridge` OR `label:agent:tuner` OR `label:agent:starter` OR `label:agent:autoswitch` OR `label:agent:fun-line` OR `label:agent:hardware`), `-label:state:done`
  - grouping includes: `state:needs-triage`

## Lane: ready-for-agent
- **Component Intake Triage**
  - grouping includes: `state:ready-for-agent`

## Lane: needs-decision
- **Owner Decision Queue**
  - type: Table
  - filter anchor: `label:state:needs-decision`, `-label:state:done`
- **Component Intake Triage**
  - grouping includes: `state:needs-decision`

## Lane: awaiting-owner
- **PR Approval Queue**
  - type: Table
  - filter anchor: `is:pr`, `label:state:awaiting-owner`, `-label:state:done`
- **Component Intake Triage**
  - grouping includes: `state:awaiting-owner`

## Lane: escalated-to-si
- **SI Escalations**
  - type: Table
  - filter anchor: `label:agent:system-integration`, (`label:impact:cross-component` OR `label:impact:system-wide`), `-label:state:done`

## Lane: closeout-required
- **Governance Closeout**
  - type: Table
  - filter anchor: `label:state:docs-update-required`, `-label:state:done`

## Lane: delivery-readiness
- **Component Delivery Readiness**
  - type: Table
  - filter anchor: (`label:type:release-readiness` OR `label:type:defect` OR `label:type:integration-risk`), (`label:component:bridge` OR `label:component:tuner` OR `label:component:starter` OR `label:component:autoswitch` OR `label:component:fun-line` OR `label:component:hardware`), `-label:state:done`

## Canonical source chain
- Narrative canonical blueprint: `tools/governance/scale_radio_governance_delivery_views_v1.md`
- Table-rendered companion: `tools/governance/scale_radio_governance_delivery_views_table_v1.md`
