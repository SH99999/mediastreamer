#!/usr/bin/env python3
"""Render a human-readable owner decision packet from ChatGPT/Codex round inputs."""

from __future__ import annotations

import argparse
from pathlib import Path


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


def read_lines(path: Path, fallback: list[str]) -> list[str]:
    if not path.exists():
        return fallback
    lines = [line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()]
    items: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("- ", "1.", "2.", "3.")):
            items.append(stripped)
        if len(items) == 3:
            break
    return items or fallback


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--chatgpt-score", type=float, required=True)
    parser.add_argument("--codex-score", type=float, required=True)
    parser.add_argument(
        "--audit",
        default="exchange/chatgpt/audit_basis/current_audit_basis_v1.md",
    )
    parser.add_argument(
        "--response",
        default="exchange/chatgpt/outbox/TEMPLATE__response_v1.md",
    )
    parser.add_argument(
        "--out",
        default="",
        help="output markdown path (default derives from topic)",
    )
    args = parser.parse_args()

    avg = (args.chatgpt_score + args.codex_score) / 2.0
    gap = abs(args.chatgpt_score - args.codex_score)

    audit_items = read_lines(Path(args.audit), ["- audit finding extraction pending"])
    proposal_items = read_lines(Path(args.response), ["1. implementation proposal pending"])

    out_path = (
        Path(args.out)
        if args.out
        else Path(f"exchange/chatgpt/outbox/{args.topic}__owner_decision_packet_v1.md")
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# {args.topic} owner decision packet v1",
        "",
        "status: ready-for-owner",
        "actor: codex",
        "",
        "## decision summary",
        f"- recommendation: {recommendation(avg, gap)}",
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
        f"- branch: si/{args.topic}",
        "- follow-up branches (optional): dev/<component>",
        "",
        "## rollback",
        "- strategy: revert decision package commit",
        "- command: git revert <commit>",
        "",
        "## owner next click",
        "- accept | changes-requested | reject",
        "",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
