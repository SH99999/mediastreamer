# Agent Registry v1

## Purpose
Canonical registry of defined agent roles and current availability for SI delegation and owner inspection.

## Canonical source
- Machine-readable source: `tools/governance/agent_registry_v1.json`
- This markdown file is the human-readable companion.

## Registry fields (contract)
Each agent entry must provide:
- `agent_id`
- `display_name`
- `status` (`available | unavailable | planned`)
- `role`
- `branch_hint`
- `scope`
- `owned_components`
- `startup_prompt_path`
- `bootstrap_command`
- `escalates_to`
- `can_receive_work_from_si` (`yes | no`)

Required baseline agent ids:
- `si`
- `dev-tuner`
- `dev-bridge`
- `dev-generic`
- `dev-hardware`
- `dev-fun-line`
- `dev-autoswitch`
- `dev-ux`

## Active registry table
| agent_id | status | role | branch_hint | owned_components | startup_prompt_path | bootstrap_command | can_receive_work_from_si |
|---|---|---|---|---|---|---|---|
| si | available | system-integration | si/<topic> | system-integration | docs/agents/agent_role_start_prompts_v1.md#si-role | bash tools/governance/agent_git_bootstrap_v1.sh --role si --mode mode-b | no |
| dev-tuner | available | component-developer | dev/tuner | tuner | docs/agents/agent_role_start_prompts_v1.md#dev-tuner-role | bash tools/governance/agent_git_bootstrap_v1.sh --role tuner --mode mode-b | yes |
| dev-bridge | available | component-developer | dev/bridge | bridge | docs/agents/agent_role_start_prompts_v1.md#dev-bridge-role | bash tools/governance/agent_git_bootstrap_v1.sh --role bridge --mode mode-b | yes |
| dev-generic | available | generic-developer | dev/<component> or si/<topic> | - | docs/agents/agent_role_start_prompts_v1.md#generic-developer-role | bash tools/governance/agent_git_bootstrap_v1.sh --mode mode-b | yes |
| dev-hardware | available | hardware-developer | dev/hardware | hardware | docs/agents/agent_role_start_prompts_v1.md#dev-hardware-role | bash tools/governance/agent_git_bootstrap_v1.sh --role hardware --mode mode-b | yes |
| dev-fun-line | planned | component-developer | dev/fun-line | fun-line | docs/agents/agent_role_start_prompts_v1.md#dev-fun-line-role | bash tools/governance/agent_git_bootstrap_v1.sh --role fun-line --mode mode-b | no |
| dev-starter | planned | component-developer | dev/starter | starter | docs/agents/agent_role_start_prompts_v1.md#generic-developer-role | bash tools/governance/agent_git_bootstrap_v1.sh --mode mode-b | no |
| dev-autoswitch | planned | component-developer | dev/autoswitch | autoswitch | docs/agents/agent_role_start_prompts_v1.md#dev-autoswitch-role | bash tools/governance/agent_git_bootstrap_v1.sh --role autoswitch --mode mode-b | no |
| dev-ux | planned | ux-developer | si/<topic> or dev/<component> | ui | docs/agents/agent_role_start_prompts_v1.md#dev-ux-role | bash tools/governance/agent_git_bootstrap_v1.sh --role ux --mode mode-b | no |

## SI delegation rule
SI must consult this registry before delegation and only delegate direct work to agents with:
- `status: available`
- `can_receive_work_from_si: yes`

If required role is unavailable/planned:
- suggest `startup_prompt_path`
- suggest `bootstrap_command`
- keep ownership with SI until role becomes available.

## Registry helper commands
- list: `python3 tools/governance/agent_registry_helper_v1.py --list`
- one start command: `python3 tools/governance/agent_registry_helper_v1.py --start-command <agent_id>`
- validation: `python3 tools/governance/agent_registry_helper_v1.py --validate`
  - validates required baseline ids, required fields, startup prompt anchor existence, bootstrap command format, and role-profile markers for available agents
