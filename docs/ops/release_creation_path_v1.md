# RELEASE CREATION PATH V1

## Goal
This path tells a specialist chat how to prepare a release that the operator can deploy from GitHub Actions.

## Steps
1. choose the correct `dev/<component>` branch
2. add the extracted release payload under `components/<component>/payload/<release_name>/`
3. make or update deploy candidate scripts so they can install, healthcheck, and remove that payload
4. keep repo-facing text in English
5. write or update the component journal stream/current state if the work changed agreements or status
6. run the deploy workflow from `main` against the `dev/<component>` branch
7. test on Pi
8. if the result is not acceptable, run the rollback workflow
9. only open a focused PR to `main` after the release is acceptable

## Required release contents
- extracted payload tree
- install path logic
- healthcheck logic
- remove/rollback logic
- any contract updates needed by the change

## PR rule
PRs to `main` should be focused and release-oriented. Do not use one giant component accumulation PR as the normal model.
