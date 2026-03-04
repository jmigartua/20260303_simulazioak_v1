from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from sim_framework.adapters.persistence import JsonFilePersistence
from sim_framework.contracts.models import RunManifest, SnapshotEvent
from sim_framework.core.environment import SignalGrid
from sim_framework.core.history import SnapshotHistory
from sim_framework.core.physics import WorldBounds
from sim_framework.scenarios.registry import get_scenario, list_scenarios

from sim_framework.app.runtime import RuntimeConfig, RuntimeMode, create_engine


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a simulation scenario with a public runtime mode."
    )
    parser.add_argument("--scenario", type=str, default="ants_foraging", choices=list_scenarios())
    parser.add_argument("--ticks", type=int, default=100)
    parser.add_argument("--ants", type=int, default=40)
    parser.add_argument("--width", type=int, default=30)
    parser.add_argument("--height", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--runtime-mode",
        type=str,
        choices=[mode.value for mode in RuntimeMode],
        default=RuntimeMode.INTERACTIVE.value,
        help="Runtime behavior preset. 'headless' disables snapshot events by default.",
    )

    snapshot_group = parser.add_mutually_exclusive_group()
    snapshot_group.add_argument(
        "--emit-snapshot-events",
        action="store_true",
        help="Force SnapshotEvent emission regardless of runtime mode.",
    )
    snapshot_group.add_argument(
        "--no-snapshot-events",
        action="store_true",
        help="Disable SnapshotEvent emission regardless of runtime mode.",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Optional path for writing the same JSON summary emitted to stdout.",
    )
    parser.add_argument(
        "--persistence-root",
        type=Path,
        default=Path("runs"),
        help="Root directory used by --save-run-id / --load-run-id.",
    )
    persistence_group = parser.add_mutually_exclusive_group()
    persistence_group.add_argument(
        "--save-run-id",
        type=str,
        default=None,
        help="Persist manifest + snapshots to persistence root under this run id.",
    )
    persistence_group.add_argument(
        "--load-run-id",
        type=str,
        default=None,
        help="Load a previously persisted run id and print a JSON summary.",
    )
    return parser


def _snapshot_override(args: argparse.Namespace) -> bool | None:
    if args.emit_snapshot_events:
        return True
    if args.no_snapshot_events:
        return False
    return None


def _validate_positive(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if args.ticks <= 0:
        parser.error("--ticks must be > 0")
    if args.ants <= 0:
        parser.error("--ants must be > 0")
    if args.width <= 0 or args.height <= 0:
        parser.error("--width/--height must be > 0")


def _emit_payload(payload: dict, json_out: Path | None) -> None:
    encoded = json.dumps(payload, indent=2)
    print(encoded)
    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(encoded + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    persistence = JsonFilePersistence(args.persistence_root)
    if args.load_run_id is not None:
        try:
            loaded = persistence.load_run(args.load_run_id)
        except FileNotFoundError as exc:
            parser.error(str(exc))

        payload = {
            "mode": "loaded",
            "persistence": {
                "root": str(args.persistence_root),
                "run_id": loaded.manifest.run_id,
                "scenario_name": loaded.manifest.scenario_name,
                "seed": loaded.manifest.seed,
                "snapshots": len(loaded.snapshots),
                "last_tick": loaded.snapshots[-1].tick if loaded.snapshots else None,
            },
        }
        _emit_payload(payload, args.json_out)
        return 0

    _validate_positive(args, parser)

    runtime = RuntimeConfig(
        mode=RuntimeMode(args.runtime_mode),
        emit_snapshot_events=_snapshot_override(args),
    )

    scenario = get_scenario(args.scenario)
    state = scenario["build_initial_state"](
        num_ants=args.ants,
        width=args.width,
        height=args.height,
        seed=args.seed,
    )
    bounds = WorldBounds(width=float(args.width), height=float(args.height))
    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    runner = scenario["create_behavior_runner"](bounds=bounds, signal_grid=signal_grid)
    engine = create_engine(seed=state.seed, runtime=runtime)
    history = SnapshotHistory(snapshot_every=1)
    snapshots_for_persistence = [state.model_copy(deep=True)]

    for _ in range(args.ticks):
        state = engine.tick(state, runner, history=history)
        snapshots_for_persistence.append(state.model_copy(deep=True))

    events = engine.drain_published_events()
    snapshot_events = sum(1 for event in events if isinstance(event, SnapshotEvent))
    result = {
        "scenario": args.scenario,
        "runtime": {
            "mode": runtime.mode.value,
            "emit_snapshot_events": engine.emit_snapshot_events,
        },
        "run": {
            "ticks_requested": args.ticks,
            "ticks_completed": state.tick,
            "ants": len(state.agents),
            "seed": state.seed,
            "world": {"width": args.width, "height": args.height},
        },
        "events": {
            "published": len(events),
            "snapshot": snapshot_events,
        },
        "metrics": {
            "carrying_agents": sum(1 for agent in state.agents if agent.carrying > 0),
            "signal_total": signal_grid.total_signal(),
        },
    }
    if args.save_run_id is not None:
        manifest = RunManifest(
            run_id=args.save_run_id,
            scenario_name=args.scenario,
            seed=args.seed,
        )
        persisted_run_id = persistence.save_run(manifest, snapshots_for_persistence)
        result["persistence"] = {
            "root": str(args.persistence_root),
            "saved_run_id": persisted_run_id,
            "snapshots_saved": len(snapshots_for_persistence),
        }
    _emit_payload(result, args.json_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
