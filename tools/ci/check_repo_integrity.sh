#!/usr/bin/env bash
set -euo pipefail

fail() { echo "CI: $1"; exit 1; }

if find . \( -name '__pycache__' -o -name '*.pyc' \) | grep -q .; then
  find . \( -name '__pycache__' -o -name '*.pyc' \)
  fail "Python cache artifacts are not allowed"
fi

for path in \
  contracts/repo/release_intake_and_delivery_status_v1.md \
  contracts/repo/component_journal_policy_v1.md \
  contracts/repo/repository_language_standard_v1.md
 do
  if [[ -f "$path" ]] && grep -Eq '^# placeholder$' "$path"; then
    fail "Placeholder governance doc still present: $path"
  fi
done

for path in \
  contracts/repo/release_intake_and_delivery_status_v2.md \
  contracts/repo/component_journal_policy_v2.md \
  contracts/repo/repository_language_standard_v2.md \
  journals/system-integration-normalization/STATUS_system_integration_normalization_v1.md \
  journals/system-integration-normalization/DECISIONS_system_integration_normalization_v1.md \
  .github/workflows/component-test-deploy-v6.yml \
  .github/workflows/component-test-rollback-v6.yml
 do
  [[ -f "$path" ]] || fail "Missing required file: $path"
done

for path in \
  .github/workflows/component-test-deploy-v3.yml \
  .github/workflows/component-test-deploy-v4.yml \
  .github/workflows/component-test-deploy-v5.yml \
  .github/workflows/component-test-rollback-v3.yml \
  .github/workflows/component-test-rollback-v4.yml \
  .github/workflows/component-test-rollback-v5.yml
 do
  [[ ! -f "$path" ]] || fail "Obsolete workflow still present: $path"
done

echo "CI: repo integrity checks passed"
