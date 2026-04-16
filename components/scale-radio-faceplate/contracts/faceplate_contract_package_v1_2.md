# Scale Radio Faceplate contract package v1.2

Status note: this file is the repo-normalized contract bundle for the first governed bootstrap of `scale-radio-faceplate`.
It consolidates the Stage-B faceplate doctrine, blueprint lock, state rules, token rules, and renderer handoff notes from the transferred package.

## 1. Purpose
Define one canonical, governed front-face contract for the visible Scale Radio appliance surface so consumer components use shared visual truth instead of local reinterpretation.

## 2. Leading rules
- analog scale first
- scale remains the primary hero element in normal playback
- metadata stays subordinate to the scale
- Bridge lives inside the right metadata column and does not become the dominant visual owner
- Sing Along is a full-screen replacement mode, not a sidecar overlay
- only a small, tightly-governed set of visible controls may appear on-screen
- marker distribution and magnetic snap behavior are part of the faceplate contract

## 3. Scope
This contract owns:
- visible front-face doctrine
- station-marker grammar
- needle-visible behavior
- metadata column hierarchy
- faceplate-side Bridge placement and Sing Along transition rule
- visual states
- theme, color, and typography tokens
- layer/export expectations for renderer owners

This contract does not own:
- source logic
- GPIO/input logic
- Bridge runtime/business logic
- lyrics lookup logic
- Spotify API logic
- deployment/rollback behavior of runtime components

## 4. Blueprint lock
### Surface framing
- the faceplate is a wide, low appliance surface centered on the analog scale
- the visible hierarchy is: chassis/backlight -> scale -> needle -> right metadata/Bridge column -> minimal controls
- front-face composition must preserve a hardware-like appliance impression, not a generic media app

### Metadata column
- metadata belongs to a controlled right-side column
- station identity may appear there, but the analog scale remains the main truth source
- Bridge content lives below or within the metadata stack without breaking the scale-first hierarchy
- the right column must not become a second hero area

### Controls
Visible controls are deliberately restricted.
No uncontrolled button ribbons, oversized transport bars, or generic web-app chrome are allowed.

## 5. Visual doctrine
### Chassis and backlight
- dark chassis/background with subtle vignette and light grain
- warm backlight glow behind the scale, brighter toward the center and darker at the edges
- physical-appliance feeling is preferred over flat UI minimalism

### Scale print
- off-white / ivory printed markings
- slight print softness is allowed
- micro-imperfections, mild print texture, and restrained brightness variance are acceptable when they increase realism

### Glass layer
- subtle vertical highlight
- light bottom counter-reflection
- faint side darkening
- optional dust/hairline imperfection, only if restrained

## 6. Station-marker grammar
- markers may use multi-row distribution where necessary
- station labels sit under numeric ticks with small square or restrained marker anchors
- marker placement should avoid mechanically even, lifeless distribution when realism benefits from controlled irregularity
- active station emphasis must remain visually consistent with the needle/snap rule
- logo usage, if present, is subdued and must not overpower the scale

## 7. Needle behavior contract
- normal movement should feel mechanically believable
- magnetic snap behavior is a governed UX rule
- the visual definition of “snap” belongs here even when implementation lives elsewhere
- snap emphasis must feel deliberate but not cartoonish
- unresolved runtime details such as jitter reduction remain consumer-component work, not a reason to redefine the visual contract

## 8. Modes and overlays
### Normal playback mode
- analog scale dominates
- metadata/Bridge stays subordinate
- Fun Line or other overlays must respect the protected faceplate occupancy

### Bridge
- Bridge is visually integrated in the right column
- Bridge must not flatten the faceplate into a generic overlay app
- Bridge placement, margins, and hierarchy are governed by the faceplate contract; Bridge runtime remains owned by `scale-radio-bridge`

### Sing Along
- Sing Along is full-screen replacement mode
- entry may be triggered from the right-column interaction grammar
- Sing Along does not share the screen as a half-overlay when active

### Fun Line
- Fun Line may occupy governed overlay space only
- it must not destroy the readability or premium-appliance impression of the faceplate
- runtime animation ownership stays with `scale-radio-fun-line`

## 9. Construction grid
- designs should target the wide panel layout used by the project
- normal working assumption remains the existing appliance-wide display format used in current project truth
- the construction grid must preserve:
  - dominant horizontal scale band
  - controlled right metadata column
  - minimal safe areas for overlay coexistence
  - predictable alignment anchors for scale print, markers, and needle pivot

## 10. Layer/export expectations
Renderer-facing packages should separate at least:
- chassis/background layer
- backlight/glow layer
- scale print layer
- marker layer
- needle layer
- glass/reflection layer
- right-column metadata/Bridge framing layer
- mode-specific replacement backgrounds where needed

Export posture for v1:
- documentation-first
- no authoritative binary assets are committed yet
- when assets later land, they should preserve the same layer separation and naming discipline

## 11. State sheets
The governed visible states are:

### State A — idle / browsing-compatible face
- faceplate present
- no aggressive motion
- restrained metadata

### State B — normal tuned playback
- faceplate active
- marker/needle relationship readable
- metadata/Bridge subordinate

### State C — Bridge engaged
- right-column interaction visible
- scale remains dominant

### State D — Sing Along active
- full-screen replacement mode
- normal faceplate hierarchy suspended for this state only

### State E — overlay coexistence
- controlled overlay occupancy only
- faceplate remains protected as upstream truth

## 12. Theme pack
Allowed theme evolution must preserve:
- analog-scale-first hierarchy
- premium appliance mood
- subdued logo/art treatment
- no generic bright app-chrome takeover

Theme variants may change:
- warmth of backlight
- subtle tonal palette
- print aging character
- reflection restraint
- controlled typography styling

## 13. Typography tokens
Typography must serve the appliance metaphor.
Use restrained, legible roles such as:
- scale numerics
- station markers
- metadata primary
- metadata secondary
- reminder strip / helper labels

Typography must not:
- become oversized dashboard chrome
- compete with the analog scale for dominance
- introduce generic mobile-app styling

## 14. Color tokens
Core token families:
- chassis darks
- warm backlight ambers
- scale-print ivories
- restrained accent tones for active states
- subdued metadata neutrals

Color rules:
- saturation remains controlled
- active emphasis is scarce and intentional
- the faceplate should read as premium hardware, not a neon software skin

## 15. Metadata and reminder grammar
- metadata is subordinate to the scale
- reminders/help text must remain sparse and appliance-like
- right-column copy should support the interaction model without becoming explanatory clutter
- any reminder strip must behave like a hardware-memory aid, not an app tutorial

## 16. Sync note locked into this bundle
Marker distribution and magnetic snap behavior are synchronized into this governed bundle.
Consumer components must treat both as upstream faceplate truth rather than redefining them locally.

## 17. Consumer rule
- `scale-radio-tuner` consumes this contract for scale, marker, and needle-visible behavior
- `scale-radio-bridge` consumes this contract for right-column placement and Sing Along trigger framing
- `scale-radio-fun-line` consumes this contract for protected occupancy and coexistence boundaries
- `scale-radio-starter` consumes this contract for startup-facing visual identity alignment

## 18. Asset posture
This bootstrap is intentionally asset-light and documentation-first.
Authoritative visual binaries may be added later without changing the ownership model established here.
