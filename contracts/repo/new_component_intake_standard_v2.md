# NEW COMPONENT INTAKE STANDARD V2

Status: supersedes `contracts/repo/new_component_intake_standard_v1.md` as the canonical new-component intake standard.

## Purpose
This document defines the standard way to introduce a new component into the repository.

## Core rule
- `main` stays the protected truth branch
- a new component should normally enter through one bootstrap PR to `main`
- ongoing component work then continues on `dev/<component-suffix>`

## Tokens used in this standard
### Canonical component name
Use the full governed component name:
- `scale-radio-<component-suffix>`

Example:
- `scale-radio-bridge`

### Component suffix
Use the short suffix token taken from the canonical component name:
- `bridge`
- `tuner`
- `starter`

## Naming and path rule
For a new component:
- component root path uses the canonical component name
- journal path uses the canonical component name
- branch path uses the component suffix

Example:
- canonical component name: `scale-radio-bridge`
- component root: `components/scale-radio-bridge/`
- journals: `journals/scale-radio-bridge/`
- work branch: `dev/bridge`

## Minimum bootstrap files
Add at least:
- `components/scale-radio-<component-suffix>/README.md`
- `journals/scale-radio-<component-suffix>/current_state_v1.md`
- `journals/scale-radio-<component-suffix>/stream_v1.md`

## Minimum README content
- purpose
- boundaries
- non-goals
- journal links

## Minimum current-state content
- what exists now
- what works
- what is untested
- next step

## Minimum stream content
- bootstrap created
- payload imported
- deploy tested
- rollback tested
- branch realigned to `main`

## Branch pattern
Use:
- `dev/<component-suffix>`

## Process
1. define the canonical component name as `scale-radio-<component-suffix>`
2. define the boundary
3. prepare the bootstrap files in a dedicated branch
4. open one bundled PR to `main`
5. after merge, use `dev/<component-suffix>` as the long-lived work lane

## Communication rule
Use concise repo-facing communication.
Provide exact filenames, paths, and branch names.
Bundle related setup changes together.

## Decision rule
Escalate only when naming, boundaries, branch placement, or governance would change.

## Success condition
The component is ready when:
- one bootstrap PR was enough
- `main` stayed protected
- the component has a clear root and journals in canonical paths
- future work can continue from `dev/<component-suffix>`
