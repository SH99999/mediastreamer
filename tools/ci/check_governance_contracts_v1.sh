#!/usr/bin/env bash
set -euo pipefail

fail() { echo "CI: $1"; exit 1; }
require_file() { [[ -f "$1" ]] || fail "Missing required file: $1"; }
require_grep() { grep -Fq "$2" "$1" || fail "Missing required governance text in $1: $2"; }

# Required canonical governance files
for path in \
  contracts/repo/canonical_governance_sources_v1.md \
  contracts/repo/branch_strategy_v2.md \
  contracts/repo/component_artifact_model_v1.md \
  contracts/repo/overlay_component_contract_v1.md \
  contracts/repo/naming_and_release_numbering_standard_v1.md \
  contracts/repo/superseded_documents_index_v1.md \
  AGENTS.md \
  components/AGENTS.md \
  docs/agents/skill_volumio4_plugin_development_v1.md \
  docs/agents/skill_overlay_component_governance_v1.md \
  docs/agents/reference_repositories_and_docs_v1.md
 do
  require_file "$path"
 done

# Canonical branch doctrine markers
require_grep contracts/repo/branch_strategy_v2.md 'main` = truth'
require_grep contracts/repo/branch_strategy_v2.md 'not a second truth branch'
require_grep contracts/repo/branch_strategy_v2.md 'multiple deployable artifacts or plugins'

# Artifact model markers
require_grep contracts/repo/component_artifact_model_v1.md 'A **component** is the functional delivery unit.'
require_grep contracts/repo/component_artifact_model_v1.md 'one plugin/artifact with the effective runtime logic'
require_grep contracts/repo/component_artifact_model_v1.md 'same component'

# Overlay contract markers
require_grep contracts/repo/overlay_component_contract_v1.md 'Bridge is explicitly governed under this overlay contract.'
require_grep contracts/repo/overlay_component_contract_v1.md 'opens an overlay'
require_grep contracts/repo/overlay_component_contract_v1.md 'renders an overlay'

# Naming and numbering markers
require_grep contracts/repo/naming_and_release_numbering_standard_v1.md 'current_dev'
require_grep contracts/repo/naming_and_release_numbering_standard_v1.md 'current'
require_grep contracts/repo/naming_and_release_numbering_standard_v1.md 'vMAJOR.MINOR.PATCH'
require_grep contracts/repo/naming_and_release_numbering_standard_v1.md 'semantic versioning'

# Canonical source precedence markers
require_grep contracts/repo/canonical_governance_sources_v1.md 'If `branch_strategy_v1.md` and `branch_strategy_v2.md` differ'
require_grep contracts/repo/canonical_governance_sources_v1.md 'component_artifact_model_v1.md'
require_grep contracts/repo/canonical_governance_sources_v1.md 'overlay_component_contract_v1.md'

echo 'CI: governance contract checks passed'
