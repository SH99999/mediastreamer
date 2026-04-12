# REPOSITORY LANGUAGE STANDARD V2

## Leading rule
Repository-facing content is English.

## Applies to
- contracts
- workflows
- README files
- journals
- release notes committed to Git
- commit messages where practical
- AGENTS/Codex guidance files

## Allowed exceptions
The following may remain non-English if they are payload-native artifacts:
- historical vendor/user payload files
- legacy notes preserved inside extracted payload trees
- UI strings where the payload intentionally ships multilingual content

## Chat-to-repo rule
A specialist chat may work in any language with the operator, but anything written into the repository must be normalized to English unless it is a payload-native exception.

## Naming rule
Use canonical component names in repo text:
- `scale-radio-tuner` instead of `scale fm`
- `scale-radio-fun-line`
- `scale-radio-autoswitch`
- `scale-radio-hardware`
- `scale-radio-starter`
- `scale-radio-bridge`

## Governance wording rule
Canonical wording is:
- `main` = truth for workflows, governance, and stable/current accepted artifacts
- `dev/<component>` = component work lane for evolving or not-yet-accepted artifacts

Other docs should follow this wording and not redefine it differently.
