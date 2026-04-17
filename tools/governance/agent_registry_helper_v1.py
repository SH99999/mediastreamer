#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


REQUIRED_FIELDS = [
    "agent_id",
    "display_name",
    "status",
    "role",
    "branch_hint",
    "scope",
    "owned_components",
    "startup_prompt_path",
    "bootstrap_command",
    "escalates_to",
    "can_receive_work_from_si",
]
REQUIRED_AGENT_IDS = {
    "si",
}
ALLOWED_STATUS = {"available", "unavailable", "planned"}
ALLOWED_DELEGATION = {"yes", "no"}
ROLE_MARKERS = {
    "si": "### system-integration / governance",
    "dev-tuner": "### tuner",
    "dev-bridge": "### bridge",
    "dev-starter": "### starter",
    "dev-generic": "### generic",
    "dev-hardware": "### hardware",
    "dev-fun-line": "### fun-line",
    "dev-autoswitch": "### autoswitch",
    "dev-ux": "### ux",
}


def slugify_anchor(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[`]+", "", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")


def load_registry(repo_root: Path) -> dict:
    path = repo_root / "tools" / "governance" / "agent_registry_v1.json"
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_prompt_anchor(repo_root: Path, startup_prompt_path: str) -> tuple[Path, str]:
    if "#" in startup_prompt_path:
        file_path, anchor = startup_prompt_path.split("#", 1)
    else:
        file_path, anchor = startup_prompt_path, ""
    return (repo_root / file_path, anchor)


def normalize_anchor(anchor: str) -> str:
    return anchor.lstrip("#").strip().lower()


def validate(repo_root: Path) -> int:
    registry = load_registry(repo_root)
    agents = registry.get("agents", [])
    prompt_doc = (repo_root / "docs" / "agents" / "agent_role_start_prompts_v1.md").read_text(encoding="utf-8")
    profile_doc = (repo_root / "docs" / "agents" / "role_bootstrap_profiles_v1.md").read_text(encoding="utf-8")
    errors: list[str] = []

    prompt_anchors = {f"#{slugify_anchor(h[3:].strip())}" for h in prompt_doc.splitlines() if h.startswith("## ")}
    seen_agent_ids = {str(agent.get("agent_id", "")).strip() for agent in agents}

    missing_required_agents = sorted(REQUIRED_AGENT_IDS - seen_agent_ids)
    if missing_required_agents:
        errors.append(f"missing_required_agents={','.join(missing_required_agents)}")

    for agent in agents:
        missing = [field for field in REQUIRED_FIELDS if field not in agent]
        if missing:
            errors.append(f"{agent.get('agent_id', '<unknown>')}:missing_fields={','.join(missing)}")
            continue

        if agent["status"] not in ALLOWED_STATUS:
            errors.append(f"{agent['agent_id']}:invalid_status={agent['status']}")
        if agent["can_receive_work_from_si"] not in ALLOWED_DELEGATION:
            errors.append(f"{agent['agent_id']}:invalid_delegation_value={agent['can_receive_work_from_si']}")
        if not str(agent["bootstrap_command"]).startswith("bash tools/governance/agent_git_bootstrap_v1.sh"):
            errors.append(f"{agent['agent_id']}:invalid_bootstrap_command")
        if not str(agent["startup_prompt_path"]).strip():
            errors.append(f"{agent['agent_id']}:empty_startup_prompt_path")
        if not str(agent["bootstrap_command"]).strip():
            errors.append(f"{agent['agent_id']}:empty_bootstrap_command")

        prompt_path, anchor = resolve_prompt_anchor(repo_root, str(agent["startup_prompt_path"]))
        if not prompt_path.exists():
            errors.append(f"{agent['agent_id']}:missing_start_prompt_file={prompt_path.relative_to(repo_root)}")
        elif anchor and f"#{slugify_anchor(normalize_anchor(anchor))}" not in prompt_anchors:
            errors.append(f"{agent['agent_id']}:missing_start_prompt_anchor=#{anchor}")

        if agent["status"] == "available":
            marker = ROLE_MARKERS.get(agent["agent_id"])
            if marker and marker not in profile_doc:
                errors.append(f"{agent['agent_id']}:missing_role_profile_marker={marker}")

    if errors:
        print("agent_registry_alignment=fail")
        for err in errors:
            print(f"error:{err}")
        return 1

    print("agent_registry_alignment=ok")
    print(f"agents_total={len(agents)}")
    print(f"agents_available={sum(1 for a in agents if a.get('status') == 'available')}")
    return 0


def list_agents(repo_root: Path) -> int:
    agents = load_registry(repo_root).get("agents", [])
    for agent in agents:
        print(f"{agent['agent_id']}\t{agent['status']}\t{agent['role']}\t{agent['bootstrap_command']}")
    return 0


def start_command(repo_root: Path, agent_id: str) -> int:
    agents = load_registry(repo_root).get("agents", [])
    for agent in agents:
        if agent.get("agent_id") == agent_id:
            print(agent["bootstrap_command"])
            return 0
    print(f"unknown_agent_id={agent_id}", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent registry helper (list/start-command/validate).")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--list", action="store_true", help="List agent registry entries.")
    parser.add_argument("--validate", action="store_true", help="Validate registry alignment.")
    parser.add_argument("--start-command", metavar="AGENT_ID", help="Print bootstrap command for AGENT_ID.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()

    if args.list:
        return list_agents(repo_root)
    if args.validate:
        return validate(repo_root)
    if args.start_command:
        return start_command(repo_root, args.start_command)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
