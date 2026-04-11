# Scale Radio / MediaStreamer

Central monorepo for the Scale Radio project on Volumio 4 / RadioScaleOS Appliance Track.

## Canonical purpose

This repository is the leading location for:
- integration contracts
- component boundaries
- release baselines
- delivery manifests
- deployment scripts for Raspberry Pi targets
- pull-request-based component delivery

## Component roots

- `components/scale-radio-starter/`
- `components/scale-radio-tuner/`
- `components/scale-radio-autoswitch/`
- `components/scale-radio-bridge/`
- `components/scale-radio-fun-line/`

## Protected integration zones

- `contracts/`
- `packaging/`
- `deploy/`
- `.github/`
- `shared/`

## Deployment target

This repo is designed to support:
- `sr-deploy bundle latest`
- `sr-deploy starter latest`
- `sr-deploy tuner latest`
- `sr-deploy autoswitch latest`
- `sr-deploy bridge latest`
- `sr-deploy fun-line latest`
- `sr-rollback <tag|alias>`
