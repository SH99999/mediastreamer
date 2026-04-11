# HARDWARE CONFIG CONTRACT V1

Status: authoritative integration standard.

## Purpose

This contract defines the currently normalized hardware interaction rules that all component chats must respect.

## Leading rule

No component may independently redefine GPIO ownership, input mappings, or hardware-critical pin usage.
Any change to normalized hardware mappings requires an integration decision.

## Current normalized input mappings

### Rotary Encoder II validated mappings

Encoder 0:
- pinA: GPIO 5
- pinB: GPIO 6
- push: GPIO 13

Encoder 1:
- pinA: GPIO 17
- pinB: GPIO 27
- push: GPIO 22

## Operational rule

These mappings are the leading hardware baseline unless explicitly superseded by a later integration contract.

## Hardware safety rule

Component chats must not silently repurpose pins that may conflict with:
- the normalized encoder mappings above,
- the HiFiBerry DAC+ ADC Pro stack,
- other already normalized hardware ownership.

## Required component behavior

Each hardware-touching component must document:
- which normalized inputs it consumes,
- which hardware resources it expects,
- whether it is only reading inputs or also driving hardware,
- whether any service or boot-time hardware configuration is required.

## Non-goal

This contract does not invent new pin assignments for yet-unsettled hardware topics.
Unknown or unnormalized hardware details remain outside the contract until explicitly integrated.
