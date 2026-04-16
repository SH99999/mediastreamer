#!/usr/bin/env python3
"""Render a human-readable owner decision packet from ChatGPT/Codex round inputs."""

from __future__ import annotations

import argparse
from pathlib import Path

REPO = "SH99999/mediastreamer"


def consensus_band(avg: float) -> str:
    if avg >= 80:
        return "high"
    if avg >= 60:
        return "medium"
    return "low"


def recommendation(avg: float, gap: float) -> str:
    if avg >= 80 and gap <= 20:
        return "accept"
    if avg >= 60:
        return "changes-requested"
    return "reject"


def is_placeholder(text: str) -> bool:
    lowered = text.strip().lower()
    if lowered in {"-", "1.", "2.", "3.", ""}:
        return True
    markers = ["<0..100>", "pending", "accept|modify|reject", "accept | changes-requested | reject", "agreement_score", "optional dev/<component>"]
    return any(token in lowered for token in markers)


def read_section_items(path: Path, headings: tuple[str, ...], fallback: list[str], max_items: int) -> list[str]:
    if not path.exists():
        return fallback

    lines = path.read_text(encoding="utf-8").splitlines()
    start = -1
    for i, line in enumerate(lines):
        normalized = line.strip().lower()
        if normalized in headings:
            start = i + 1
            break
    if start == -1:
        return fallback

    items: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if stripped.startswith(("- ", "1.", "2.", "3.", "4.", "5.")) and not is_placeholder(stripped):
            items.append(stripped)
        if len(items) >= max_items:
            break
    return items or fallback


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--chatgpt-score", type=float, required=True)
    parser.add_argument("--codex-score", type=float, required=True)
    parser.add_argument("--audit", default="exchange/chatgpt/audit_basis/current_audit_basis_v1.md")
    parser.add_argument("--response", default="exchange/chatgpt/outbox/TEMPLATE__response_v1.md")
    parser.add_argument("--out", default="", help="output markdown path (default derives from topic)")
    args = parser.parse_args()

    avg = (args.chatgpt_score + args.codex_score) / 2.0
    gap = abs(args.chatgpt_score - args.codex_score)
    owner_rec = recommendation(avg, gap)

    audit_fallback = [
        "- audit basis is incomplete; owner should require evidence update before acceptance",
        "- follow-up audit pull is required for unresolved components",
    ]
    proposal_fallback = [
        "1. Request a concrete ranked implementation proposal in `exchange/chatgpt/outbox/<topic>__response_v1.md`.",
        "2. Require branch name + exact files to change before approval.",
        "3. Defer merge until packet has non-placeholder evidence and rollback command.",
    ]

    audit_items = read_section_items(
        Path(args.audit),
        ("## current baseline findings", "## current baseline findings (condensed)", "## key findings considered"),
        audit_fallback,
        max_items=5,
    )
    proposal_items = read_section_items(
        Path(args.response),
        ("## implementation proposals (ranked)", "## implementation proposal (ranked)"),
        proposal_fallback,
        max_items=6,
    )

    degraded = audit_items == audit_fallback or proposal_items == proposal_fallback
    if degraded and owner_rec == 'accept':
        owner_rec = 'changes-requested'

    out_path = Path(args.out) if args.out else Path(f"exchange/chatgpt/outbox/{args.topic}__owner_decision_packet_v1.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    decision_issue_q = f"https://github.com/{REPO}/issues?q=is%3Aopen+is%3Aissue+label%3Astate%3Aneeds-decision"
    decision_pr_q = f"https://github.com/{REPO}/pulls?q=is%3Aopen+is%3Apr+label%3Astate%3Aneeds-decision"
    topic_branch = f"si/{args.topic}"
    branch_compare = f"https://github.com/{REPO}/compare/main...{topic_branch}"

    lines = [
        f"# {args.topic} owner decision packet v1",
        "",
        "status: ready-for-owner",
        "actor: codex",
        "",
        "## decision summary",
        f"- recommendation: {owner_rec}",
        f"- confidence_band: {consensus_band(avg)}",
        f"- agreement_score_chatgpt: {args.chatgpt_score:.1f}",
        f"- agreement_score_codex: {args.codex_score:.1f}",
        f"- agreement_gap: {gap:.1f}",
        "",
        "## key findings considered",
        *audit_items,
        "",
        "## implementation proposal (ranked)",
        *proposal_items,
        "",
        "## risks (essential)",
        "- scope drift",
        "- incomplete component normalization",
        "",
        "## execution path",
        f"- branch: {topic_branch}",
        "- follow-up branches (optional): dev/<component>",
        f"- compare link: {branch_compare}",
        "",
        "## rollback",
        "- strategy: revert decision package commit",
        "- command: git revert <commit>",
        "",
        "## where to click now",
        f"- decision issues queue: {decision_issue_q}",
        f"- decision PR queue: {decision_pr_q}",
        f"- topic branch compare: {branch_compare}",
        "",
        "## owner next click",
        f"- {owner_rec}",
        "",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
