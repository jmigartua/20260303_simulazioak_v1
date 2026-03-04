#!/usr/bin/env python3
from __future__ import annotations

import argparse
import cProfile
import inspect
import json
import pstats
import statistics
import tracemalloc
from dataclasses import asdict, dataclass
from io import StringIO
from pathlib import Path
from time import perf_counter

from sim_framework.core.engine import SimulationEngine
from sim_framework.core.environment import SignalGrid
from sim_framework.core.physics import WorldBounds
from sim_framework.scenarios.registry import get_scenario, list_scenarios


@dataclass
class BenchmarkRun:
    scenario: str
    agents: int
    ticks: int
    elapsed_s: float
    ticks_per_s: float
    us_per_agent_tick: float
    peak_mem_mb: float
    state_tick: int
    carrying_agents: int
    signal_total: float


@dataclass
class BenchmarkSummary:
    scenario: str
    agents: int
    ticks: int
    repeats: int
    elapsed_s_mean: float
    elapsed_s_stdev: float
    ticks_per_s_mean: float
    ticks_per_s_stdev: float
    us_per_agent_tick_mean: float
    us_per_agent_tick_stdev: float
    peak_mem_mb_mean: float
    peak_mem_mb_stdev: float


def _parse_agents(raw: str) -> list[int]:
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        raise argparse.ArgumentTypeError("agents list cannot be empty")
    try:
        parsed = [int(p) for p in parts]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("agents must be comma-separated integers") from exc
    if any(v <= 0 for v in parsed):
        raise argparse.ArgumentTypeError("all agents values must be > 0")
    return parsed


def _build_state_for_scenario(
    build_fn,
    *,
    scenario: str,
    agents: int,
    width: int,
    height: int,
    seed: int,
):
    signature = inspect.signature(build_fn)
    kwargs = {"width": width, "height": height, "seed": seed}

    if "num_ants" in signature.parameters:
        kwargs["num_ants"] = agents
    elif "num_drones" in signature.parameters:
        kwargs["num_drones"] = agents
    elif "num_agents" in signature.parameters:
        kwargs["num_agents"] = agents
    else:
        raise ValueError(
            f"Scenario '{scenario}' does not expose a supported agent-count parameter "
            "(expected one of: num_ants, num_drones, num_agents)."
        )

    return build_fn(**kwargs)


def _single_run(
    scenario: str,
    agents: int,
    ticks: int,
    width: int,
    height: int,
    seed: int,
    *,
    emit_snapshot_events: bool,
) -> BenchmarkRun:
    scenario_impl = get_scenario(scenario)
    state = _build_state_for_scenario(
        scenario_impl["build_initial_state"],
        scenario=scenario,
        agents=agents,
        width=width,
        height=height,
        seed=seed,
    )
    bounds = WorldBounds(width=float(width), height=float(height))
    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    engine = SimulationEngine(
        seed=seed,
        emit_snapshot_events=emit_snapshot_events,
    )
    runner = scenario_impl["create_behavior_runner"](bounds=bounds, signal_grid=signal_grid)

    tracemalloc.start()
    start = perf_counter()
    for _ in range(ticks):
        state = engine.tick(state, runner)
    elapsed = perf_counter() - start
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    carrying_agents = sum(1 for agent in state.agents if agent.carrying > 0)
    tps = ticks / elapsed
    us_per_agent_tick = (elapsed * 1_000_000.0) / (agents * ticks)
    return BenchmarkRun(
        scenario=scenario,
        agents=agents,
        ticks=ticks,
        elapsed_s=elapsed,
        ticks_per_s=tps,
        us_per_agent_tick=us_per_agent_tick,
        peak_mem_mb=peak_bytes / (1024 * 1024),
        state_tick=state.tick,
        carrying_agents=carrying_agents,
        signal_total=signal_grid.total_signal(),
    )


def _summarize(runs: list[BenchmarkRun]) -> BenchmarkSummary:
    if not runs:
        raise ValueError("runs cannot be empty")
    agents = runs[0].agents
    scenario = runs[0].scenario
    ticks = runs[0].ticks
    elapsed = [r.elapsed_s for r in runs]
    tps = [r.ticks_per_s for r in runs]
    uapt = [r.us_per_agent_tick for r in runs]
    peak = [r.peak_mem_mb for r in runs]
    return BenchmarkSummary(
        scenario=scenario,
        agents=agents,
        ticks=ticks,
        repeats=len(runs),
        elapsed_s_mean=statistics.fmean(elapsed),
        elapsed_s_stdev=statistics.stdev(elapsed) if len(elapsed) > 1 else 0.0,
        ticks_per_s_mean=statistics.fmean(tps),
        ticks_per_s_stdev=statistics.stdev(tps) if len(tps) > 1 else 0.0,
        us_per_agent_tick_mean=statistics.fmean(uapt),
        us_per_agent_tick_stdev=statistics.stdev(uapt) if len(uapt) > 1 else 0.0,
        peak_mem_mb_mean=statistics.fmean(peak),
        peak_mem_mb_stdev=statistics.stdev(peak) if len(peak) > 1 else 0.0,
    )


def _print_summary(summary: BenchmarkSummary) -> None:
    print(
        (
            f"scenario={summary.scenario} agents={summary.agents:>4} ticks={summary.ticks:>4} "
            f"repeats={summary.repeats} | "
            f"elapsed={summary.elapsed_s_mean:.3f}s ±{summary.elapsed_s_stdev:.3f} | "
            f"tps={summary.ticks_per_s_mean:.2f} ±{summary.ticks_per_s_stdev:.2f} | "
            f"us/agent-tick={summary.us_per_agent_tick_mean:.3f} ±{summary.us_per_agent_tick_stdev:.3f} | "
            f"peak_mem={summary.peak_mem_mb_mean:.2f}MB ±{summary.peak_mem_mb_stdev:.2f}"
        )
    )


def _run_benchmark(
    *,
    scenario: str,
    agents: list[int],
    ticks: int,
    repeats: int,
    width: int,
    height: int,
    seed: int,
    emit_snapshot_events: bool,
) -> tuple[list[BenchmarkRun], list[BenchmarkSummary]]:
    all_runs: list[BenchmarkRun] = []
    summaries: list[BenchmarkSummary] = []

    for agent_count in agents:
        case_runs: list[BenchmarkRun] = []
        for repeat in range(repeats):
            run_seed = seed + repeat
            run = _single_run(
                scenario=scenario,
                agents=agent_count,
                ticks=ticks,
                width=width,
                height=height,
                seed=run_seed,
                emit_snapshot_events=emit_snapshot_events,
            )
            case_runs.append(run)
            all_runs.append(run)
        summary = _summarize(case_runs)
        summaries.append(summary)
        _print_summary(summary)

    return all_runs, summaries


def _write_profile(
    profile: cProfile.Profile,
    profile_out: Path,
    *,
    sort_key: str,
    top_n: int,
) -> None:
    stream = StringIO()
    stats = pstats.Stats(profile, stream=stream).sort_stats(sort_key)
    stats.print_stats(top_n)

    profile_out.parent.mkdir(parents=True, exist_ok=True)
    profile_out.write_text(stream.getvalue(), encoding="utf-8")
    print(f"Wrote profile report to: {profile_out}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Headless performance benchmark for registered simulation scenarios."
    )
    parser.add_argument(
        "--scenario",
        type=str,
        choices=list_scenarios(),
        default="ants_foraging",
        help="Scenario to benchmark.",
    )
    parser.add_argument("--agents", type=_parse_agents, default="100,500,1000")
    parser.add_argument("--ticks", type=int, default=200)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--width", type=int, default=30)
    parser.add_argument("--height", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument(
        "--profile-out",
        type=Path,
        default=None,
        help="Write cProfile text report to this path.",
    )
    parser.add_argument(
        "--profile-sort",
        type=str,
        default="cumtime",
        choices=["cumtime", "tottime", "calls", "ncalls"],
    )
    parser.add_argument(
        "--profile-top",
        type=int,
        default=30,
        help="Number of profiling rows to print.",
    )
    parser.add_argument(
        "--no-snapshot-events",
        action="store_true",
        help="Disable engine SnapshotEvent emission during benchmark runs.",
    )
    args = parser.parse_args()

    if args.ticks <= 0:
        raise ValueError("--ticks must be > 0")
    if args.repeats <= 0:
        raise ValueError("--repeats must be > 0")
    if args.width <= 0 or args.height <= 0:
        raise ValueError("--width/--height must be > 0")
    if args.profile_top <= 0:
        raise ValueError("--profile-top must be > 0")

    if args.profile_out is not None:
        profiler = cProfile.Profile()
        all_runs, summaries = profiler.runcall(
            _run_benchmark,
            scenario=args.scenario,
            agents=args.agents,
            ticks=args.ticks,
            repeats=args.repeats,
            width=args.width,
            height=args.height,
            seed=args.seed,
            emit_snapshot_events=not args.no_snapshot_events,
        )
        _write_profile(
            profiler,
            args.profile_out,
            sort_key=args.profile_sort,
            top_n=args.profile_top,
        )
    else:
        all_runs, summaries = _run_benchmark(
            scenario=args.scenario,
            agents=args.agents,
            ticks=args.ticks,
            repeats=args.repeats,
            width=args.width,
            height=args.height,
            seed=args.seed,
            emit_snapshot_events=not args.no_snapshot_events,
        )

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "config": {
                "scenario": args.scenario,
                "agents": args.agents,
                "ticks": args.ticks,
                "repeats": args.repeats,
                "width": args.width,
                "height": args.height,
                "seed": args.seed,
                "emit_snapshot_events": not args.no_snapshot_events,
            },
            "runs": [asdict(r) for r in all_runs],
            "summaries": [asdict(s) for s in summaries],
        }
        args.json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"\nWrote JSON results to: {args.json_out}")


if __name__ == "__main__":
    main()
