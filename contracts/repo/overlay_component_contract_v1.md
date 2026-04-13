# OVERLAY COMPONENT CONTRACT V1

## Purpose
This contract defines repository governance requirements for components that open, render, or arbitrate overlays.

## Leading rule
Overlay behavior is a governed runtime contract, not only a UI detail.

## Applies to
Any component that:
- opens an overlay
- renders an overlay
- shares visible display/runtime space with another overlay
- participates in overlay ownership or arbitration
- can force another overlay into hidden or idle behavior

## Required overlay fields
Every governed overlay component should document:
- component name
- artifact roles involved
- which artifact opens the overlay
- which artifact renders or maintains the overlay
- whether overlay ownership or arbitration is used
- what file, state, or process indicates active overlay control
- visible behavior
- hidden behavior
- deep-idle behavior, if any
- rollback behavior
- Volumio unregistration behavior, if applicable

## Artifact role pattern
Overlay components may include multiple artifacts, for example:
- `launcher`
- `runtime`
- `bridge`
- `renderer`
- `helper`

These remain one governed component unless explicitly split by governance.

## Deployment rule
Overlay deployment must preserve:
- clean-replace semantics
- explicit rollback path
- documented interaction with existing overlay state

## Rollback rule
Rollback must restore a stable operator-visible state.
If the overlay component includes a Volumio plugin artifact, rollback must also document whether plugin unregistration is required.

## Bridge note
Bridge is explicitly governed under this overlay contract.
Bridge documentation and journals must state:
- runtime overlay artifact
- launcher/open-entry artifact, if present
- how overlay control is established
- known interaction with other overlays
- accepted temporary activation quirks, if any
