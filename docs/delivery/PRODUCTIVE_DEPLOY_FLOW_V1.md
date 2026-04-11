# Productive Deploy Flow v1

This document defines the first non-placeholder deployment path for Scale Radio.

## What is real in v1

- deployment is repo-driven, not release-asset-driven
- the Raspberry Pi updates or clones the central repository into `/opt/scale-radio/repo`
- deployment is executed by `deploy/v1/sr-deploy.sh`
- rollback is executed by `deploy/v1/sr-rollback.sh`
- GitHub can trigger a manual deployment through `.github/workflows/deploy-to-pi-v1.yml`

## Canonical commands

- `sr-deploy bundle latest`
- `sr-deploy starter latest`
- `sr-deploy tuner latest`
- `sr-deploy autoswitch latest`
- `sr-deploy bridge latest`
- `sr-deploy fun-line latest`
- `sr-rollback latest-good`

## Current limitation of v1

v1 synchronizes component directories into `/opt/scale-radio/components/<component>` and executes `install.sh` if a component-specific install hook exists.

That means v1 is already useful for rapid deployment orchestration and deterministic path handling, but full component installation depth still depends on future component-local install hooks.
