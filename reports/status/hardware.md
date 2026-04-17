# Status Hardware

_Generated: 2026-04-16T00:00:00+00:00_

## Quick summary
- `payload_partial`
- `functional_acceptance_open`

## Main open points
- no confirmed repo-integrated Pi-validated baseline yet
- no confirmed production-ready install/rollback path in repo yet
- live AS5600 communication on target Pi remains unvalidated
- mechanical bracket/adapter dimensions remain open until real measurements are captured

## Next actions

## Sources
- [Current state](/workspace/mediastreamer/journals/scale-radio-hardware/current_state_v1.md)
- [Stream](/workspace/mediastreamer/journals/scale-radio-hardware/stream_v1.md)

## Owner action contract
- recommended owner action: `changes-requested`
- next_owner_click: `request_changes`
- claim_classes.governance_docs: `accepted`
- claim_classes.runtime_validation: `not_claimed`
- claim_classes.autonomy_eligibility: `not_claimed`
- component_claims.repo_ready_payload_present: `False`
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
- rollback_action.command: `git revert <merge_commit_for_hardware>`
- source_commit: `c4ec33b112570bd8b52368e66e866a8c254c84bf`

## Visual snapshot
```mermaid
pie
    title Lifecycle snapshot
    "lifecycle entries" : 2
    "main gaps" : 4
    "next actions" : 0
```
