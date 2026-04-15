# SCALE RADIO GOVERNANCE & DELIVERY — VIEW TABLE V1

Target project: `https://github.com/users/SH99999/projects/1`

Status: table-rendered view definition for quick owner review in Git.

| View | Type | Filters | Grouping / Fields | Purpose |
|---|---|---|---|---|
| Owner Decision Queue | Table | `label:state:needs-decision`, `-label:state:done` | Fields: Title, Labels, Repository, Updated, Assignees (optional) | Single clickpoint for pending owner decisions. |
| Component Intake Triage | Board (or Table fallback) | (`label:agent:ux` OR `label:agent:bridge` OR `label:agent:tuner` OR `label:agent:starter` OR `label:agent:autoswitch` OR `label:agent:fun-line` OR `label:agent:hardware`), `-label:state:done` | Grouping (board): `state:needs-triage`, `state:ready-for-agent`, `state:needs-decision`, `state:awaiting-owner`; Fields: Title, Labels, Repository, Updated, Assignees (optional) | Isolates component intake and progression across UI/UX and runtime lanes from generic governance noise. |
| SI Escalations | Table | `label:agent:system-integration`, (`label:impact:cross-component` OR `label:impact:system-wide`), `-label:state:done` | Fields: Title, Labels, Updated, Repository | Keeps cross-component/system-wide escalations visible. |
| PR Approval Queue | Table | `is:pr`, `label:state:awaiting-owner`, `-label:state:done` | Fields: Checks, Review status, Labels, Updated | Owner-ready PR gate. |
| Governance Closeout | Table | `label:state:docs-update-required`, `-label:state:done` | Fields: Title, Labels, Updated, Repository | Verifies governance-truth closeout before done state. |
| Component Delivery Readiness | Table | (`label:type:release-readiness` OR `label:type:defect` OR `label:type:integration-risk`), (`label:component:bridge` OR `label:component:tuner` OR `label:component:starter` OR `label:component:autoswitch` OR `label:component:fun-line` OR `label:component:hardware`), `-label:state:done` | Fields: Title, Labels, Repository, Updated, Milestone (optional) | Tracks deploy/test/rollback readiness across all governed components. |

## Canonical source chain
- Narrative canonical blueprint: `tools/governance/scale_radio_governance_delivery_views_v1.md`
- Kanban-rendered companion: `tools/governance/scale_radio_governance_delivery_views_kanban_v1.md`
