# Agent Start Index v1

Quick owner-facing index for agent availability and startup instructions.

| agent | available | role summary | startup prompt path | bootstrap command |
|---|---|---|---|---|
| System Integration (`si`) | yes | governance control-plane + cross-component normalization | `docs/agents/agent_role_start_prompts_v1.md#si-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --role si --mode mode-b` |
| Dev Tuner (`dev-tuner`) | no (archived) | tuner component developer lane | `docs/agents/agent_role_start_prompts_v1.md#dev-tuner-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --role tuner --mode mode-b` |
| Dev Bridge (`dev-bridge`) | no (archived) | bridge component developer lane | `docs/agents/agent_role_start_prompts_v1.md#dev-bridge-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --role bridge --mode mode-b` |
| Dev Generic (`dev-generic`) | no (archived) | governed implementation where role specialization is not required | `docs/agents/agent_role_start_prompts_v1.md#generic-developer-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --mode mode-b` |
| Dev Hardware (`dev-hardware`) | no (archived) | hardware component developer lane | `docs/agents/agent_role_start_prompts_v1.md#dev-hardware-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --role hardware --mode mode-b` |
| Dev Fun Line (`dev-fun-line`) | no (archived) | fun-line specialist lane | `docs/agents/agent_role_start_prompts_v1.md#dev-fun-line-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --role fun-line --mode mode-b` |
| Dev Starter (`dev-starter`) | no (archived) | starter specialist lane | `docs/agents/agent_role_start_prompts_v1.md#generic-developer-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --mode mode-b` |
| Dev AutoSwitch (`dev-autoswitch`) | no (archived) | autoswitch specialist lane | `docs/agents/agent_role_start_prompts_v1.md#dev-autoswitch-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --role autoswitch --mode mode-b` |
| Dev UX (`dev-ux`) | no (archived) | UI/UX implementation lane (`dev/ux`) | `docs/agents/agent_role_start_prompts_v1.md#dev-ux-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --role ux --mode mode-b` |

Canonical registry source:
- `docs/agents/agent_registry_v1.md`
- `tools/governance/agent_registry_v1.json`

Codex startup helpers:
- list agents: `python3 tools/governance/agent_registry_helper_v1.py --list`
- print one start command: `python3 tools/governance/agent_registry_helper_v1.py --start-command <agent_id>`
- validate registry/startup alignment: `python3 tools/governance/agent_registry_helper_v1.py --validate`
