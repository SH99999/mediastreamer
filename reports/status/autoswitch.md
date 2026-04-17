# Status Autoswitch

_Generated: 2026-04-16T00:00:00+00:00_

## Quick summary
- `payload_complete`
- `deployment_candidate_started`
- `functional_acceptance_open`

## Main open points
- previous playback source restore is unresolved
- renderer-visible tape-state export is unresolved
- interaction with future overlay ownership signaling remains unresolved
- long-duration runtime validation is still open

## Next actions

## Sources
- [Current state](/workspace/mediastreamer/journals/scale-radio-autoswitch/current_state_v1.md)
- [Stream](/workspace/mediastreamer/journals/scale-radio-autoswitch/stream_v1.md)

## Owner action contract
- recommended owner action: `changes-requested`
- next_owner_click: `request_changes`
- claim_classes.governance_docs: `accepted`
- claim_classes.runtime_validation: `not_claimed`
- claim_classes.autonomy_eligibility: `not_claimed`
- component_claims.repo_ready_payload_present: `True`
- component_claims.deploy_ready: `False`
- component_claims.tested_on_target: `False`
- component_claims.rollback_verified: `False`
- component_claims.runtime_validated: `False`
- component_claims.autonomy_eligible: `False`
- runtime_claim.evidence_path: `n/a`
- runtime_claim.tested_scope: `n/a`
- autonomy_claim.evidence_path: `n/a`
- autonomy_claim.tested_scope: `n/a`
- decision_scoring.evidence_quality: `2`
- decision_scoring.rollback_readiness: `2`
- decision_scoring.blast_radius: `medium`
- decision_scoring.confidence: `68`
- rollback_action.command: `git revert <merge_commit_for_autoswitch>`
- source_commit: `c4ec33b112570bd8b52368e66e866a8c254c84bf`

## Visual snapshot
```mermaid
pie
    title Lifecycle snapshot
    "lifecycle entries" : 3
    "main gaps" : 4
    "next actions" : 0
```
