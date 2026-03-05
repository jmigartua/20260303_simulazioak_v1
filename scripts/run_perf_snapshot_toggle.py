#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

from sim_framework.app.parsing import parse_agents_csv
from sim_framework.scenarios.registry import list_scenarios

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_SCRIPT = PROJECT_ROOT / "scripts" / "benchmark_headless.py"


def _parse_agents(raw: str) -> list[int]:
    return parse_agents_csv(raw)


def _run_benchmark(
    *,
    scenario: str,
    agents: list[int],
    ticks: int,
    repeats: int,
    width: int,
    height: int,
    seed: int,
    json_out: Path,
    snapshot_events: bool,
) -> None:
    cmd = [
        sys.executable,
        str(BENCHMARK_SCRIPT),
        "--scenario",
        str(scenario),
        "--agents",
        ",".join(str(v) for v in agents),
        "--ticks",
        str(ticks),
        "--repeats",
        str(repeats),
        "--width",
        str(width),
        "--height",
        str(height),
        "--seed",
        str(seed),
        "--json-out",
        str(json_out),
    ]
    if not snapshot_events:
        cmd.append("--no-snapshot-events")
    subprocess.run(cmd, check=True, cwd=PROJECT_ROOT)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _summary_map(payload: dict) -> dict[int, dict]:
    return {int(item["agents"]): item for item in payload["summaries"]}


def _determinism_pairs(on_payload: dict, off_payload: dict) -> tuple[int, int]:
    compared = 0
    matched = 0
    for on_run, off_run in zip(on_payload["runs"], off_payload["runs"], strict=False):
        compared += 1
        same_seed = on_run["state_tick"] == off_run["state_tick"]
        same_carrying = on_run["carrying_agents"] == off_run["carrying_agents"]
        same_signal = float(on_run["signal_total"]) == float(off_run["signal_total"])
        if same_seed and same_carrying and same_signal:
            matched += 1
    return matched, compared


def _write_comparison(on_payload: dict, off_payload: dict, out_path: Path) -> None:
    on_map = _summary_map(on_payload)
    off_map = _summary_map(off_payload)
    common_agents = sorted(set(on_map).intersection(off_map))

    lines: list[str] = []
    lines.append("# Snapshot ON vs OFF Benchmark Comparison")
    lines.append("")
    lines.append("- Source: `scripts/run_perf_snapshot_toggle.py`")
    lines.append(f"- Scenario: `{on_payload['config'].get('scenario', 'unknown')}`")
    lines.append(
        f"- ON config: ticks={on_payload['config']['ticks']}, repeats={on_payload['config']['repeats']}, "
        f"emit_snapshot_events={on_payload['config']['emit_snapshot_events']}"
    )
    lines.append(
        f"- OFF config: ticks={off_payload['config']['ticks']}, repeats={off_payload['config']['repeats']}, "
        f"emit_snapshot_events={off_payload['config']['emit_snapshot_events']}"
    )
    lines.append("")
    lines.append(
        "| Agents | us/agent-tick ON | us/agent-tick OFF | Throughput gain OFF vs ON | "
        "Peak mem ON | Peak mem OFF | Memory reduction OFF vs ON |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|")

    for agents in common_agents:
        on_summary = on_map[agents]
        off_summary = off_map[agents]
        on_uapt = float(on_summary["us_per_agent_tick_mean"])
        off_uapt = float(off_summary["us_per_agent_tick_mean"])
        on_mem = float(on_summary["peak_mem_mb_mean"])
        off_mem = float(off_summary["peak_mem_mb_mean"])

        gain = ((on_uapt - off_uapt) / on_uapt) * 100.0
        mem_drop = ((on_mem - off_mem) / on_mem) * 100.0 if on_mem > 0 else 0.0

        lines.append(
            f"| {agents} | {on_uapt:.3f} | {off_uapt:.3f} | {gain:+.2f}% | "
            f"{on_mem:.2f} MB | {off_mem:.2f} MB | {mem_drop:+.2f}% |"
        )

    matched, compared = _determinism_pairs(on_payload, off_payload)
    lines.append("")
    lines.append(f"- Determinism cross-check (run-pairs): {matched}/{compared} matched carrying/signal/tick.")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run ON/OFF snapshot baseline and generate a comparison markdown file."
    )
    parser.add_argument(
        "--scenario",
        type=str,
        choices=list_scenarios(),
        default="ants_foraging",
        help="Scenario to benchmark in ON/OFF mode.",
    )
    parser.add_argument("--agents", type=_parse_agents, default="100,300")
    parser.add_argument("--ticks", type=int, default=100)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--width", type=int, default=30)
    parser.add_argument("--height", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", type=Path, default=Path("Plans"))
    parser.add_argument(
        "--label",
        type=str,
        default=f"{date.today().isoformat()}_snapshot_toggle",
        help="Label used in generated output filenames.",
    )
    args = parser.parse_args()

    if args.ticks <= 0:
        raise ValueError("--ticks must be > 0")
    if args.repeats <= 0:
        raise ValueError("--repeats must be > 0")
    if args.width <= 0 or args.height <= 0:
        raise ValueError("--width/--height must be > 0")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    on_json = args.output_dir / f"perf_baseline_{args.label}_snapshot_on.json"
    off_json = args.output_dir / f"perf_baseline_{args.label}_snapshot_off.json"
    comparison_md = args.output_dir / f"perf_comparison_{args.label}.md"

    _run_benchmark(
        scenario=args.scenario,
        agents=args.agents,
        ticks=args.ticks,
        repeats=args.repeats,
        width=args.width,
        height=args.height,
        seed=args.seed,
        json_out=on_json,
        snapshot_events=True,
    )
    _run_benchmark(
        scenario=args.scenario,
        agents=args.agents,
        ticks=args.ticks,
        repeats=args.repeats,
        width=args.width,
        height=args.height,
        seed=args.seed,
        json_out=off_json,
        snapshot_events=False,
    )

    on_payload = _load_json(on_json)
    off_payload = _load_json(off_json)
    _write_comparison(on_payload, off_payload, comparison_md)

    print(f"Wrote: {on_json}")
    print(f"Wrote: {off_json}")
    print(f"Wrote: {comparison_md}")


if __name__ == "__main__":
    main()
