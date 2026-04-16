#!/usr/bin/env python3
"""
Derive owner decision suggestion from ChatGPT/Codex agreement scores.
"""

from __future__ import annotations

import argparse


def band(avg: float) -> str:
    if avg >= 80:
        return "high"
    if avg >= 60:
        return "medium"
    return "low"


def decision(avg: float, max_gap: float) -> str:
    if avg >= 80 and max_gap <= 20:
        return "accept"
    if avg >= 60:
        return "changes-requested"
    return "reject"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--chatgpt-score", required=True, type=float)
    p.add_argument("--codex-score", required=True, type=float)
    args = p.parse_args()

    avg = (args.chatgpt_score + args.codex_score) / 2.0
    gap = abs(args.chatgpt_score - args.codex_score)
    print(f"consensus_band: {band(avg)}")
    print(f"average_score: {avg:.1f}")
    print(f"score_gap: {gap:.1f}")
    print(f"recommended_owner_decision: {decision(avg, gap)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
