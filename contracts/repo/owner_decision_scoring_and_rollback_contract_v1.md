# OWNER DECISION SCORING AND ROLLBACK CONTRACT V1

## Purpose
Define deterministic decision-quality scoring and rollback one-click action fields for owner-facing decision packets.

## Required scoring fields
- `evidence_quality` (`0..3`)
- `rollback_readiness` (`0..3`)
- `blast_radius` (`low | medium | high`)
- `confidence` (`0..100`)

## Required rollback action fields
- `rollback_action.enabled` (boolean)
- `rollback_action.command` (exact rollback/revert command)
- `rollback_action.verification` (non-empty post-rollback check list)

## Canonical packet alignment
Scoring and rollback fields must be embedded in `status_packet_v1` payloads and visible in owner-facing markdown report sections.

## Rollback toggle
- scoring validation feature flag: `OWNER_DECISION_SCORING_ENABLED=false`
- when disabled, packets may omit scoring validation checks but must keep manual owner fallback path available

## Safety
If scoring or rollback fields are missing:
- do not claim decision packet is fully compliant
- provide explicit blocker with missing keys
- keep manual owner decision path available
