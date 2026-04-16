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
