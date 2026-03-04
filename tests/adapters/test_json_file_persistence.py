from __future__ import annotations

import json
from pathlib import Path

import pytest

from sim_framework.adapters.persistence import JsonFilePersistence
from sim_framework.contracts.models import (
    AgentState,
    Colony,
    RunManifest,
    SignalField,
    SimulationState,
    Vector2,
)
from sim_framework.contracts.ports import PersistencePort


def _state(tick: int, *, energy: float = 1.0) -> SimulationState:
    return SimulationState(
        tick=tick,
        agents=[
            AgentState(
                id=f"a-{tick}",
                position=Vector2(x=float(tick), y=0.0),
                energy=energy,
            )
        ],
        food_sources=[],
        colony=Colony(id="c1", position=Vector2(x=0.0, y=0.0)),
        signal_fields=[SignalField(kind="pheromone", width=10, height=10)],
        seed=123,
    )


def test_persistence_round_trip_and_protocol_conformance(tmp_path: Path) -> None:
    persistence = JsonFilePersistence(tmp_path)
    assert isinstance(persistence, PersistencePort)

    manifest = RunManifest(run_id="run-1", scenario_name="ants_foraging", seed=123)
    snapshots = [_state(0, energy=1.0), _state(1, energy=0.9)]
    run_id = persistence.save_run(manifest, snapshots)

    # Mutate in-memory source after save to verify on-disk isolation.
    snapshots[0].agents[0].energy = 42.0

    loaded = persistence.load_run(run_id)
    assert loaded.manifest == manifest
    assert [snapshot.tick for snapshot in loaded.snapshots] == [0, 1]
    assert loaded.snapshots[0].agents[0].energy == 1.0


def test_save_writes_expected_json_bundle(tmp_path: Path) -> None:
    persistence = JsonFilePersistence(tmp_path)
    manifest = RunManifest(run_id="run-json", scenario_name="ants_foraging", seed=42)
    persistence.save_run(manifest, [_state(0)])

    run_file = tmp_path / "run-json" / "run.json"
    payload = json.loads(run_file.read_text(encoding="utf-8"))
    assert payload["manifest"]["run_id"] == "run-json"
    assert payload["manifest"]["scenario_name"] == "ants_foraging"
    assert payload["snapshots"][0]["tick"] == 0


def test_load_missing_run_raises_file_not_found(tmp_path: Path) -> None:
    persistence = JsonFilePersistence(tmp_path)
    with pytest.raises(FileNotFoundError, match="missing-run"):
        persistence.load_run("missing-run")
