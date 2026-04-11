# DEV BRANCH FAST LOOP V1

## Purpose

Small component patches must no longer require a full integration funnel through main for every fix.

## Leading model

- `main` remains the promoted stable branch.
- component development happens on component-specific development branches.
- fast deployment from those branches happens automatically on the Pi through the self-hosted runner.
- if a deployment fails, the component is removed again under Rollback Contract V1.

## Initial component development branches

- `dev/tuner`
- `dev/bridge`

## Initial deployment behavior

- pushes to `dev/tuner` trigger Tuner fast-loop deployment
- pushes to `dev/bridge` trigger Bridge fast-loop deployment
- failed deployment triggers automatic clean-absent rollback of the affected component

## Promotion rule

When a component development branch becomes stable enough, it is promoted through one PR into `main`.

## Priority note

Tuner is already in better shape.
Bridge is the next higher-need component after the rollback baseline is in place.
