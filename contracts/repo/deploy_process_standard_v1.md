# DEPLOY PROCESS STANDARD V1

## Purpose
This standard unifies manual and autonomous component deployment under one governed process.

## Core rules
- `main` remains protected truth.
- Execution happens from non-`main` branches.
- Promotion to `main` happens only via PR review and owner coordination.
- Deploy and rollback must respect target-slot exclusivity.

## Deploy process phases
1. **intake_ready**
   - payload path and component scope are explicit
2. **deploy_candidate_ready**
   - install, healthcheck, rollback candidate scripts exist
3. **manual_validation_ready**
   - repo-driven manual deploy and rollback are runnable
4. **validated_on_target**
   - deploy and rollback validated on target Pi
5. **autonomous_eligible**
   - component meets matrix criteria and has explicit SI decision
6. **accepted_for_main**
   - reviewed and merged through protected-`main` PR path

## Autonomous delivery eligibility
A component may be marked `auto_delivery_supported: true` only when all are true:
- manual deploy validated on target
- manual rollback validated on target
- healthcheck contract exists and is runnable
- rollback expectations are documented in component current-state
- SI decision log records the promotion decision
- lock-aware target-slot path has succeeded for deploy and rollback
- component current-state and stream journals are updated to the latest tested reality
- open runtime risks are explicitly assessed (accepted, mitigated, or escalated)

## Matrix synchronization rule
When deploy status changes materially:
- update current-state and stream journals
- update autonomous matrix in the same change set or explicitly state why deferred
- keep matrix workflow references aligned with active deploy/rollback workflows

## Failure and blocker handling
- if safe completion is blocked by tooling/access/runtime constraints, publish an explicit blocker
- do not imply deployment success without evidence
- prefer truthful negative status over fabricated progress
