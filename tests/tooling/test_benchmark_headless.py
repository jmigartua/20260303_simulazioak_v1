import json
import sys
from pathlib import Path

from tests.tooling.helpers import load_module


def test_build_state_dispatch_supports_ants_and_drones() -> None:
    mod = load_module("scripts/benchmark_headless.py", "benchmark_headless_dispatch")
    scenarios_mod = load_module("sim_framework/scenarios/registry.py", "scenario_registry_for_bench")
    ants = scenarios_mod.get_scenario("ants_foraging")
    drones = scenarios_mod.get_scenario("drone_patrol")

    ants_state = mod._build_state_for_scenario(
        ants["build_initial_state"],
        scenario="ants_foraging",
        agents=7,
        width=20,
        height=20,
        seed=42,
    )
    drone_state = mod._build_state_for_scenario(
        drones["build_initial_state"],
        scenario="drone_patrol",
        agents=9,
        width=20,
        height=20,
        seed=42,
    )

    assert len(ants_state.agents) == 7
    assert len(drone_state.agents) == 9
    assert ants_state.signal_fields[0].kind == "pheromone"
    assert drone_state.signal_fields[0].kind == "radio"


def test_single_run_supports_drone_patrol() -> None:
    mod = load_module("scripts/benchmark_headless.py", "benchmark_headless_single_run")
    run = mod._single_run(
        scenario="drone_patrol",
        agents=10,
        ticks=3,
        width=20,
        height=20,
        seed=42,
        emit_snapshot_events=False,
    )

    assert run.scenario == "drone_patrol"
    assert run.agents == 10
    assert run.state_tick == 3
    assert run.signal_total >= 0.0


def test_main_writes_json_with_scenario_config(tmp_path: Path, monkeypatch) -> None:
    mod = load_module("scripts/benchmark_headless.py", "benchmark_headless_main")
    json_out = tmp_path / "bench.json"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "benchmark_headless.py",
            "--scenario",
            "drone_patrol",
            "--agents",
            "5",
            "--ticks",
            "2",
            "--repeats",
            "1",
            "--json-out",
            str(json_out),
            "--no-snapshot-events",
        ],
    )
    mod.main()

    payload = json.loads(json_out.read_text(encoding="utf-8"))
    assert payload["config"]["scenario"] == "drone_patrol"
    assert payload["config"]["emit_snapshot_events"] is False
    assert payload["runs"][0]["scenario"] == "drone_patrol"
    assert payload["summaries"][0]["scenario"] == "drone_patrol"
