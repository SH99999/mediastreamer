# BRANCH STRATEGY V1

Status: authoritative integration standard for day-to-day repository operation.

## Leading rule

Single-use topic branches are no longer the default working model.

The default model is:
- `main` for promoted stable states
- `integration/staging` for integration-owned repo changes
- persistent component development branches for fast loops

## Persistent branches

- `main`
- `integration/staging`
- `dev/tuner`
- `dev/bridge`
- `dev/autoswitch`
- `dev/fun-line`
- `dev/starter`
- `dev/hardware`

## Branch ownership

### main
- stable promotion branch
- protected
- no direct development

### integration/staging
- owned by the integration chat
- used for contracts, deploy logic, workflow logic, packaging, hardware standards and observability standards

### dev/tuner
- Tuner fast loop branch

### dev/bridge
- Bridge fast loop branch

### dev/autoswitch
- AutoSwitch development branch

### dev/fun-line
- Fun Line development branch

### dev/starter
- Starter development branch

### dev/hardware
- hardware integration branch
- used for AS5600, input abstraction changes, hardware-facing plugins and replacement input devices
- hardware changes must still respect the normalized hardware contract

## Promotion rule

Small development fixes stay on their component development branch until the block is stable enough for promotion.
Promotion to `main` happens through a single PR created by the integration chat.
