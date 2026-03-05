from __future__ import annotations

import argparse


def parse_agents_csv(raw: str) -> list[int]:
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        raise argparse.ArgumentTypeError("agents list cannot be empty")
    try:
        values = [int(p) for p in parts]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("agents must be comma-separated integers") from exc
    if any(v <= 0 for v in values):
        raise argparse.ArgumentTypeError("all agents values must be > 0")
    return values
