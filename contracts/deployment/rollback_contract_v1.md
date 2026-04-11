# ROLLBACK CONTRACT V1

Status: authoritative integration decision for fast development loops on component branches.

## Purpose

Rollback Contract V1 defines the required system behavior when a deployed development version of a component fails.

## Leading rule

If a development deployment fails, the component must be removed again immediately and cleanly from the Pi until the next version of that component is deployed.

This is a clean-absent rollback model.

## Scope

Rollback Contract V1 is introduced first for:
- Tuner
- Bridge

It may later be extended to other components.

## Successful rollback outcome

A rollback is successful only if:
1. the component runtime services owned by that component are stopped or disabled as needed,
2. the component uninstall hook is executed,
3. component-owned deployed files are removed from `/opt/scale-radio/components/<component>`,
4. rollback state is written,
5. the component is left absent from the active runtime path.

## Explicit non-goal in V1

Rollback V1 does not yet restore the previous last-known-good version.

If a deployment fails under V1, the component must be removed and remain absent until a later version is deployed.

## Required repo artifacts for V1-managed components

Each V1-managed component must contain:
- `runtime_manifest.yaml`
- `install.sh`
- `configure.sh`
- `healthcheck.sh`
- `uninstall.sh`

## Failure handling rule

If install, configure or healthcheck fails:
- the deployment must stop,
- rollback must start automatically,
- the component state must be written as failed-then-removed,
- the global system must remain usable without that component.
