# TECHNOLOGY CHANGE PROCESS V1

## Purpose
This process governs component-level technology changes, such as replacing a bash/service implementation with a Volumio plugin, changing runtime language, changing deployment style, or moving a runtime responsibility between artifacts.

## Trigger
Use this process whenever a component changes one of these:
- implementation form
- runtime entrypoint
- deploy contract
- rollback contract
- ownership boundary
- branch/release structure

Examples:
- bash/service component -> Volumio plugin
- Volumio plugin -> service/helper split
- single artifact -> multi-artifact component
- polling runtime -> event-driven runtime

## Mandatory steps
### 1. State the proposed change clearly
The proposal must name:
- current technology shape
- proposed technology shape
- why the change is being made
- what stays the same
- what breaks if not handled carefully

### 2. Preserve component identity
A technology change does not automatically create a new component.
Default rule:
- keep the same component
- document the new artifact/runtime model inside that component

Only split into a new component if governance explicitly records a boundary change.

### 3. Protect rollback first
Before the change is treated as active work, define:
- rollback anchor
- rollback procedure
- what must be removed/unregistered on rollback
- what old artifact remains the safety baseline

### 4. Update repo truth before claiming migration
Before calling the migration active, update:
- component `current_state_v1.md`
- component `stream_v1.md`
- component README
- decision log if the technology change is binding

### 5. Keep naming and release discipline
During technology change:
- component name stays normalized
- artifact roles become explicit
- release numbering stays component-level unless governance explicitly splits it

### 6. Validate deploy contract again
A technology change reopens deploy validation.
At minimum re-check:
- install path
- activation behavior
- rollback behavior
- unregistration behavior if plugin-based
- target-Pi runtime behavior

## Decision rule
A technology change becomes active repo truth only when:
1. rollback is explicit
2. journals are updated
3. runtime/deploy impact is documented
4. the old authoritative baseline is still recoverable

## Autoswitch note
If `scale-radio-autoswitch` moves from bash/systemd toward a Volumio plugin, treat that as a technology change under this process. Do not silently replace the current service-based truth.
