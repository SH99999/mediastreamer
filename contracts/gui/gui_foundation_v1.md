# GUI FOUNDATION V1

Status: authoritative integration standard.

## Purpose

This document defines the global UI, layout and style language for Scale Radio on Volumio 4.
All component chats must respect this foundation.

## Leading design character

The product is:
- appliance-like
- analog-inspired
- calm
- high-end hi-fi oriented
- restrained rather than playful
- visually coherent across Tuner, Bridge, Starter and Fun Line

The product is not:
- mobile-app-like
- overly flat or game-like
- visually inconsistent between screens

## Primary screen zones

The canonical display layout is divided into these zones:

### Zone A — Main scale zone
The primary visual area.
Used for:
- radio scale
- pointer
- marker logic
- station or scale-related primary interaction feedback

### Zone B — Right info zone
The secondary information area on the right.
Used for:
- metadata
- bridge-related textual or logo content
- low-priority track or source information

### Zone C — Bottom hardware label zone
The bottom strip aligned to hardware button meaning.
Used for:
- current hardware button labels
- mode-dependent button hints

### Zone D — Overlay zone
Used only when an overlay owns the screen.
Must respect global ownership and must not visually break the underlying layout logic.

## Typography

### Leading rule
Typography must look like integrated hi-fi hardware, not default web UI.

### Global typography rules
- one primary UI font family for labels and metadata
- one optional numeric or scale-supporting style if required by the scale design
- avoid excessive font variety
- avoid decorative novelty fonts
- uppercase only where it strengthens device-like labeling
- metadata must remain readable at distance

### Hierarchy
- scale labels and primary tuner labels = primary hierarchy
- source and track metadata = secondary hierarchy
- hardware hint labels = tertiary hierarchy
- warning or temporary operational labels = temporary high contrast but visually controlled

## Color system

### Leading rule
Color must support the analog hi-fi identity and readability.

### Global token groups
- background base
- background elevated
- scale print primary
- scale print secondary
- marker accent
- active highlight
- metadata primary
- metadata secondary
- disabled text
- warning
- error
- fun accent

### Character
- backgrounds must avoid pure flat black where a richer device background is intended
- scale print should favor warm off-white or restrained light tones over harsh digital white
- accent usage must remain sparse
- metadata must stay visually subordinate to the main scale zone

## Buttons and controls

### Leading rule
Buttons and labels must read like hardware-linked UI, not generic web buttons.

### Control classes
- hardware label button state
- selected state
- inactive state
- temporary focus state
- warning state

### Rules
- bottom hardware labels must be aligned and consistently spaced
- mode changes may relabel buttons, but the zone itself remains stable
- button color changes must not overpower the main scale zone

## Positioning and spacing

### Leading rule
The layout must remain stable and appliance-like.

### Rules
- stable horizontal zoning is preferred over floating freeform placement
- right metadata zone remains right-aligned as canonical secondary area
- bottom hardware label zone remains bottom-aligned as canonical tertiary area
- spacing must prevent label collisions and keep scale readability intact
- overlay content must not randomly break grid or safe margins

## Motion and transitions

### Leading rule
Motion must feel deliberate and hardware-like.

### Allowed character
- pointer movement may be smooth but not excessive
- snap-on behavior is allowed and expected where station or marker logic requires it
- overlays may fade or slide in a restrained manner
- metadata transitions must be controlled and low-noise

### Forbidden character
- playful or chaotic motion in primary tuner mode
- unnecessary bouncing, zooming or flashing
- high-frequency motion that harms appliance feel or performance

## Fixed versus configurable

### Globally fixed
- primary screen zoning
- general hi-fi design character
- restrained motion character
- right-side metadata as secondary visual area
- bottom hardware label strip as tertiary area

### Component-configurable within limits
- selected font within approved list
- scale color within approved token family
- metadata visibility or content composition where explicitly supported
- some station label distribution logic where readability is preserved

### Forbidden local overrides
- moving the metadata area to arbitrary unrelated positions
- replacing the bottom hardware label logic with freeform controls
- introducing component-local color systems that conflict with the global tokens
- mobile-app-style button or card design in primary appliance screens

## Reference component priority

### Tuner
Defines the primary visual grammar.

### Bridge
Must integrate into the right info and metadata logic without taking over the primary visual hierarchy.

### Starter
Must inherit the same product identity and not look like a separate unrelated UI.

### Fun Line
May be more playful in content but must still respect the global visual system boundaries.
