# DEPLOYMENT DECISIONS V1

## Leading rule
Deployment uses clean-replace semantics, not update-in-place semantics.

## Required deploy sequence
1. detect whether a live version is installed
2. move the currently active plugin runtime out of the active Volumio paths
3. move the currently active plugin configuration out of the active Volumio paths
4. copy the selected payload into the live plugin path
5. run the payload `install.sh`
6. restart Volumio
7. wait for Volumio recovery
8. run baseline recovery checks
9. run component-specific healthcheck
10. leave the component installed for functional testing

## Required rollback sequence
1. move the active plugin runtime out of the active Volumio path
2. move the active plugin configuration out of the active Volumio path
3. unregister the plugin from Volumio's enabled plugin state when applicable
4. restart Volumio
5. wait for recovery
6. verify baseline runtime recovery

## Baseline recovery checks
- `volumio` active
- `volumio-kiosk` active
- `Xorg` present
- `chromium` present

## Workflow rule
- workflows live on `main`
- workflows must accept a `git_ref` input
- workflows must accept component-specific release selectors where needed, for example `payload`
- workflows must be manually runnable by the operator from the Actions UI

## Payload rule
- payloads committed to Git must be extracted file trees, not only ZIP archives
- payloads live under `components/<component>/payload/<release_name>/`

## Current bridge rule
The Bridge deploy lane already proved:
- stable payload install works from `dev/bridge`
- overlay on `:5511` is reachable
- plugin may remain inactive after install and that is acceptable for now
