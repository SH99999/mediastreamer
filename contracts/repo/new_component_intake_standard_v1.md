# NEW COMPONENT INTAKE STANDARD V1

## Purpose
This document defines the standard way to introduce a new component into the repository.

## Core rule
- `main` stays the protected truth branch
- a new component should normally enter through one bootstrap PR to `main`
- ongoing work then continues on `dev/<component>`

## Naming
Use the format:
- `scale-radio-<component>`

## Minimum bootstrap files
Add at least:
- `components/<component>/README.md`
- `journals/<component>/current_state_v1.md`
- `journals/<component>/stream_v1.md`

## Branch pattern
Use:
- `dev/<component-suffix>`

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

## Process
1. define the canonical component name
2. define the boundary
3. prepare the bootstrap files in a dedicated branch
4. open one bundled PR to `main`
5. after merge, use `dev/<component>` as the long-lived work lane

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
- the component has a clear root and journals
- future work can continue from `dev/<component>`
