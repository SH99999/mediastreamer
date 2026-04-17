# STATUS PACKET REPORTING CONTRACT V1

## Purpose
Define a canonical machine-readable status handoff payload for SI/governance and component-agent reporting.

## Canonical schema
- Schema file: `tools/governance/schemas/status_packet_v1.schema.json`
- Packet version marker: `schema: status_packet_v1`

## Required fields
- `component`
- `canonical_status`
- `evidence_links`
- `blockers`
- `recommended_owner_action`
- `next_owner_click`
- `decision_scoring`
- `rollback_action`
- `claim_classes`
- `component_claims`
- `timestamp`
- `source_commit`

## Owner-action routing contract
- `recommended_owner_action` enum:
  - `accept`
  - `changes-requested`
  - `defer`
  - `run_workflow`
- `next_owner_click` enum:
  - `approve_pr`
  - `request_changes`
  - `run_workflow`
  - `defer`

## Decision scoring contract
- `decision_scoring.evidence_quality`: `0..3`
- `decision_scoring.rollback_readiness`: `0..3`
- `decision_scoring.blast_radius`: `low | medium | high`
- `decision_scoring.confidence`: `0..100`

## Rollback one-click action contract
- `rollback_action.enabled`: boolean
- `rollback_action.command`: exact revert or rollback command
- `rollback_action.verification`: non-empty list of post-rollback checks

## Claim-class contract (mandatory separation)
Status packets and markdown views must keep these classes explicitly separate:
- `claim_classes.governance_docs`: `accepted | pending`
- `claim_classes.runtime_validation`: `not_claimed | validated`
- `claim_classes.autonomy_eligibility`: `not_claimed | eligible`

Evidence-gating scope rule:
- strict evidence requirements apply only to runtime/deploy/rollback/autonomy claims
- governance/docs-only packages may remain lightweight if they do not claim runtime/deploy/autonomy effects

Runtime/autonomy evidence requirements:
- if `claim_classes.runtime_validation=validated`, packet must include:
  - `runtime_claim.evidence_path`
  - `runtime_claim.tested_scope`
  - `runtime_claim.source_ref` (commit or packet path)
  - `runtime_claim.rollback_verification`
- if `claim_classes.autonomy_eligibility=eligible`, packet must include:
  - `autonomy_claim.evidence_path`
  - `autonomy_claim.tested_scope`
  - `autonomy_claim.source_ref` (commit or packet path)
  - `autonomy_claim.rollback_path`

Truthful degradation rule:
- if runtime/autonomy evidence is missing, packet/report output must degrade to `not_claimed` and must not present fully validated or eligible claims.

## Component claim ledger contract (mandatory)
Component-facing packets must expose one normalized claim ledger object:
- `component_claims.repo_ready_payload_present` (boolean)
- `component_claims.deploy_ready` (boolean)
- `component_claims.tested_on_target` (boolean)
- `component_claims.rollback_verified` (boolean)
- `component_claims.runtime_validated` (boolean)
- `component_claims.autonomy_eligible` (boolean)
- `component_claims.tested_scope` (string)
- `component_claims.evidence_path` (string)
- `component_claims.rollback_path` (string)
- `component_claims.source_ref` (string)

Alignment rule:
- `component_claims.autonomy_eligible=true` must not contradict `tools/governance/autonomous_delivery_matrix_v3.json`
- component claim fields must align with current-state/stream truth for the same component

## Canonical-status alignment
`canonical_status` must follow `contracts/repo/status_taxonomy_contract_v1.md` and must not invent new lifecycle labels.

## Report adapter contract
- markdown status pages are rendered from packet data and must include:
  - owner action contract block
  - `source_commit`
- packet JSON artifacts are generated under `reports/status/packets/`

## Rollback
- toggle: `STATUS_PACKET_V1_ENABLED=false` (workflow/process toggle path)
- scoring field toggle: `OWNER_DECISION_SCORING_ENABLED=false`
- revert path: revert schema + adapter commits; keep legacy markdown generation path available if toggle is disabled

## Safety
If required fields are missing:
- do not claim packet compliance
- publish explicit blocker with missing keys
- keep truthful fallback markdown output until packet compliance is restored
