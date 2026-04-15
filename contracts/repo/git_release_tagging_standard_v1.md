# GIT RELEASE TAGGING STANDARD V1

## Purpose
This document defines the governed Git tagging rule for accepted stable baselines and rollback anchors.

## Leading rule
Git tags are not used for every intermediate branch state.
Git tags are used only for accepted stable baselines and governed rollback anchors.

## Why this exists
This keeps repository history useful without turning tags into noise.
It also makes stable recovery points obvious for owner review, rollback, and future agent work.

## Tagging rule
Create a Git tag only when a component baseline is:
- accepted as stable after real validation, or
- explicitly locked as the governed rollback anchor

Do not create Git tags for:
- every candidate deploy
- every branch checkpoint
- every PR merge
- incomplete or unvalidated intermediate work

## Tag format
Use this format:
- `<component-suffix>-vMAJOR.MINOR.PATCH`

Examples:
- `bridge-v1.2.3`
- `tuner-v1.10.2`
- `autoswitch-v0.3.0`

## Relation to payload naming
This standard does not replace the payload pointer model.
The existing payload rules still apply:
- `current_dev`
- `current`
- immutable payload releases using `vMAJOR.MINOR.PATCH`

Git tags are the governed repository marker for accepted baselines, not the only naming mechanism.

## When to tag
Tag when all of these are true:
1. the component baseline has a clear release number
2. deploy/rollback contract is in governed repo truth
3. real validation evidence exists at the intended acceptance level
4. the baseline is accepted as stable or rollback-anchor truth
5. journals and decisions are updated to match

## What not to do
- do not tag every experimental state
- do not tag a baseline that has not been really validated at the intended level
- do not create parallel tag naming schemes
- do not use tags as a substitute for journals, decisions, or release handoff fields

## Practical rule
For most components, keep only the meaningful governed tags:
- current accepted stable baseline
- current rollback anchor when different from the stable baseline

Older tags may remain for historical recovery, but new tagging should stay conservative.
