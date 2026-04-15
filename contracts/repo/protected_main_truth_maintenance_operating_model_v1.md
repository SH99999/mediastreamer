# PROTECTED MAIN TRUTH MAINTENANCE OPERATING MODEL V1

## Purpose
This document defines the standard operating model for maintaining protected-`main` repo truth when an agent or connector cannot safely mutate an existing truth file directly.

## Leading rule
Do not improvise, fake completion, or silently create partial truth when safe mutation is blocked.

If the normal branch-plus-PR path cannot safely update an existing truth file end-to-end, the agent must use the controlled replacement-file path and inform the owner.

## Standard operating model
### Default path
Use the normal path whenever possible:
1. update the target truth file on a working branch
2. open a packaged PR to `main`
3. owner reviews and merges

### Replacement-file exception path
If the connector or tool cannot safely mutate the existing truth file:
1. create the intended replacement content on the working branch as a clearly named replacement file
2. use a deterministic naming pattern such as:
   - `ag_new.txt` for `AGENTS.md`
   - `<target_basename>_new.txt` for similar truth-file replacements when appropriate
3. explain in the PR body which protected truth file the replacement is for
4. the owner manually applies the replacement to the protected truth file on `main`
5. relevant journals and decision logs must record the operating-model use when it changes repo-truth maintenance behavior materially

## Safety rule
The replacement-file path is an exception path.
It exists to preserve truth quality under tool limitations, not to bypass protected-`main` governance.

## Communication rule
When this path is used, the agent must state clearly:
- what file could not be safely mutated
- why the normal safe path was blocked
- what replacement file was created
- what owner action is required

## Examples
- top-level `AGENTS.md` cannot be safely updated through the current connector surface -> create `ag_new.txt` on the working branch and instruct the owner to apply it on `main`
- another protected truth file cannot be safely mutated -> create a clearly named replacement artifact and document the required manual apply step

## What not to do
- do not claim the source truth file was updated when only a replacement artifact exists
- do not open a PR that hides the fact that owner action is still required
- do not fork a parallel governance chain just because a direct mutation path is awkward
