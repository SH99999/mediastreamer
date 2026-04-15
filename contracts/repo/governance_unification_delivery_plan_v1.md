# GOVERNANCE UNIFICATION DELIVERY PLAN V1

## Purpose
This plan splits governance normalization into small, reviewable bundles and defines where each topic should live in repository truth.

## Operating constraint
- Agents must work on non-`main` branches.
- Promotion into `main` happens through PR review and owner coordination.
- No direct ad-hoc mutation of `main`.

## Bundle structure

### Bundle 1 — Canonical entrypoint and source precedence
**Goal:** one unambiguous governance entrypoint and one precedence map.

**Scope:**
- align `AGENTS.md` read order with the active SI governance index
- keep `canonical_governance_sources` aligned with currently active contracts

**Primary home:**
- `AGENTS.md`
- `contracts/repo/system_integration_governance_index_v7.md`
- `contracts/repo/canonical_governance_sources_v1.md`

### Bundle 2 — Unified deploy process doctrine
**Goal:** one deploy process model for manual and autonomous lanes.

**Scope:**
- define deploy phases and required gates
- define lock/exclusivity behavior
- define autonomous support-matrix promotion criteria
- define matrix synchronization rule after validated deploy/rollback results

**Primary home:**
- `contracts/repo/deploy_process_standard_v1.md`
- `contracts/repo/deploy_target_exclusivity_standard_v1.md`
- `tools/governance/autonomous_delivery_matrix_v3.json`

### Bundle 3 — Naming, release numbering, and path normalization
**Goal:** unify release naming and path rules across components.

**Scope:**
- define canonical payload path and allowed mutable names
- define immutable release numbering and historical import handling
- define artifact role naming in docs/manifests

**Primary home:**
- `contracts/repo/naming_and_release_numbering_standard_v1.md`
- `contracts/repo/component_artifact_model_v1.md`
- `contracts/repo/new_component_intake_standard_v2.md`

### Bundle 4 — UI/GUI governance under same model
**Goal:** ensure UI/GUI work is governed exactly like runtime/deploy work.

**Scope:**
- define UI/GUI artifact roles (for example `ui_entry`, `renderer`, overlays)
- require UI/GUI changes to follow same branch, PR, release, journal, and rollback doctrine
- require UI/GUI intake and escalation through the same issue-routing model

**Primary home:**
- `contracts/repo/ui_gui_governance_standard_v1.md`
- `contracts/repo/issue_governance_routing_standard_v1.md`

### Bundle 5 — Status/decision/journal schema unification
**Goal:** remove duplicate vocabulary and ambiguous file naming.

**Scope:**
- unify lifecycle status vocabulary to one canonical set
- unify journal filename conventions
- define open-decision required metadata (owner, trigger, target review window, closing condition)

**Primary home:**
- `contracts/repo/release_intake_and_delivery_status_v2.md` (or v3 if needed)
- `contracts/repo/component_journal_policy_v2.md` (or v3 if needed)
- `contracts/repo/status_and_decision_review_cadence_v1.md`

## Delivery sequencing
1. Bundle 1 (entrypoint/preference cleanup)
2. Bundle 2 (deploy doctrine + autonomous line reliability)
3. Bundle 4 (UI/GUI governance inclusion)
4. Bundle 3 (naming/release/path normalization)
5. Bundle 5 (status/journal schema consolidation)

## Acceptance checks per bundle
- contract text is internally consistent
- SI governance index references the active source chain
- if a workflow/matrix behavior changed, docs and matrix are synchronized in same PR
- journal/decision updates reflect the new operational truth
