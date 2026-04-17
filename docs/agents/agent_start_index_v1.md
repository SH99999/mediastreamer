# Agent Start Index v1

Quick owner-facing index for agent availability and startup instructions.

| agent | available | role summary | startup prompt path | bootstrap command |
|---|---|---|---|---|
| System Integration (`si`) | yes | governance control-plane + cross-component normalization | `docs/agents/agent_role_start_prompts_v1.md#si-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --role si --mode mode-b` |
| Dev Tuner (`dev-tuner`) | yes | tuner component developer lane | `docs/agents/agent_role_start_prompts_v1.md#dev-tuner-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --role tuner --mode mode-b` |
| Dev Bridge (`dev-bridge`) | yes | bridge component developer lane | `docs/agents/agent_role_start_prompts_v1.md#dev-bridge-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --role bridge --mode mode-b` |
| Dev Generic (`dev-generic`) | yes | governed implementation where role specialization is not required | `docs/agents/agent_role_start_prompts_v1.md#generic-developer-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --mode mode-b` |
| Dev Hardware (`dev-hardware`) | yes | hardware component developer lane | `docs/agents/agent_role_start_prompts_v1.md#dev-hardware-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --role hardware --mode mode-b` |
| Dev Fun Line (`dev-fun-line`) | no (planned) | fun-line specialist lane | `docs/agents/agent_role_start_prompts_v1.md#generic-developer-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --mode mode-b` |
| Dev Starter (`dev-starter`) | no (planned) | starter specialist lane | `docs/agents/agent_role_start_prompts_v1.md#generic-developer-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --mode mode-b` |
| Dev AutoSwitch (`dev-autoswitch`) | no (planned) | autoswitch specialist lane | `docs/agents/agent_role_start_prompts_v1.md#generic-developer-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --mode mode-b` |
| Dev UX (`dev-ux`) | no (planned) | UI/UX implementation lane | `docs/agents/agent_role_start_prompts_v1.md#generic-developer-role` | `bash tools/governance/agent_git_bootstrap_v1.sh --mode mode-b` |

Canonical registry source:
- `docs/agents/agent_registry_v1.md`
- `tools/governance/agent_registry_v1.json`
