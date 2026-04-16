# CURRENT STATE — scale-radio-faceplate

## Component
- normalized component name: `scale-radio-faceplate`
- governed role: front-face visual and interaction contract component
- active bootstrap lane: `si/faceplate-intake-v1`
- post-bootstrap work lane: `dev/faceplate`

## Repo truth
- component root is bootstrapped at `components/scale-radio-faceplate/`
- current v1 posture is contract-led and asset-light
- canonical proposal path: `components/scale-radio-faceplate/proposals/stage_b_intake_proposal_v1.md`
- canonical issue-ready intake artifact: `components/scale-radio-faceplate/proposals/governed_intake_issue_fields_v1.md`
- canonical contract bundle: `components/scale-radio-faceplate/contracts/faceplate_contract_package_v1_2.md`

## Lifecycle status
- `bootstrap_proposed`
- `contract_bundle_imported`
- `issue_ready_artifact_prepared`
- `owner_decision_pending`
- `runtime_not_owned`

## Current known truth
- one dedicated governed component now exists for front-face doctrine instead of leaving that truth outside repo structure
- v1 keeps ownership boundaries strict: faceplate owns visible contract truth; runtime consumers keep implementation ownership
- marker distribution and magnetic snap are locked as upstream faceplate rules
- no authoritative binary asset pack is committed yet
- no deploy/rollback runtime contract is introduced by this component in v1

## Current gaps
- GitHub issue creation/update could not be executed in the current connector lane and remains issue-ready only
- no authoritative visual export assets are committed yet
- consumer components still need explicit current-state references to the new upstream faceplate contract
- later renderer-support artifacts may still be needed once a runtime renderer owner requests them

## Repo-normalized next action
1. treat this component as the canonical visible-appliance contract truth after owner approval
2. create/update the governed intake issue from the prepared issue fields when issue tooling is available
3. keep binary visual assets out of truth until they are authoritative enough to govern
4. require consumer components to reference `scale-radio-faceplate` as upstream contract truth in their next active current-state files
