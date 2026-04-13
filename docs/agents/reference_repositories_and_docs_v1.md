# REFERENCE REPOSITORIES AND DOCS V1

## Purpose
This document gives coding agents a curated reference set for Volumio 4 and related overlay/plugin work.

## Primary sources
### Volumio developer documentation
Use for:
- plugin system concepts
- plugin command-line utility
- plugin publishing expectations
- API references

### Volumio GitHub organization
Use for:
- upstream code-reading
- official example structures
- plugin source references

Important repositories to inspect when relevant:
- `volumio/volumio-plugins-sources`
- `volumio/volumio3-backend`
- `volumio/Volumio2-UI`
- `volumio/volumio-developers-docs`

## Community/reference repos
### foonerd repositories
Use as implementation references for Bookworm-era Peppy and related display/runtime work.
Relevant repos include:
- `foonerd/peppy_screensaver`
- `foonerd/peppy_builds`
- `foonerd/peppy_remote`
- `foonerd/peppy_templates`

These are reference inputs, not automatic truth. Community repos may have support or maintenance limits.

## Reference usage rules
- prefer official Volumio docs for standards and APIs
- use community repos to study patterns, runtime behavior, and compatibility workarounds
- do not assume community code is store-ready or officially supported
- document when repo code intentionally depends on community-maintained behavior

## Current repository expectation
When in doubt:
1. read governance docs first
2. consult official Volumio docs second
3. consult reference repos third
4. encode repo decisions back into governance or journals when they become operational rules
