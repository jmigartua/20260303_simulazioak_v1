from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from sim_framework.contracts.models import (
    AgentState,
    Colony,
    ErrorEvent,
    LifecycleEvent,
    MetricEvent,
    PauseCommand,
    PlayCommand,
    ResetCommand,
    RunManifest,
    SeekCommand,
    SetSpeedCommand,
    SimulationState,
    SnapshotEvent,
    StepCommand,
    Vector2,
)
from sim_framework.contracts.ports import HistoryPort, PersistencePort, RendererPort


class StubRenderer:
    def render(self, snapshot: SimulationState) -> None:
        _ = snapshot

    def capture_screenshot(self, path: str | Path) -> Path:
        return Path(path)


class StubPersistence:
    def save_run(self, manifest: RunManifest, snapshots: list[SimulationState]) -> str:
        _ = (manifest, snapshots)
        return "run-1"

    def load_run(self, run_id: str):
        _ = run_id
        raise NotImplementedError


class StubHistory:
    def snapshot(self, state: SimulationState, tick: int) -> None:
        _ = (state, tick)

    def nearest_snapshot_before(self, tick: int):
        _ = tick
        return None

    def rewind(self, target_tick: int, current_state: SimulationState) -> SimulationState:
        _ = target_tick
        return current_state


def _state() -> SimulationState:
    return SimulationState(
        tick=0,
        agents=[AgentState(id="a1", position=Vector2(x=0.0, y=0.0))],
        food_sources=[],
        colony=Colony(id="c1", position=Vector2(x=1.0, y=1.0)),
        signal_fields=[],
        seed=42,
    )


def test_protocol_runtime_conformance() -> None:
    assert isinstance(StubRenderer(), RendererPort)
    assert isinstance(StubPersistence(), PersistencePort)
    assert isinstance(StubHistory(), HistoryPort)


def test_command_models() -> None:
    assert PlayCommand().kind == "play"
    assert PauseCommand().kind == "pause"
    assert ResetCommand().kind == "reset"
    assert StepCommand(steps=3).steps == 3
    assert SeekCommand(tick=10).tick == 10
    assert SetSpeedCommand(speed_multiplier=1.5).speed_multiplier == 1.5

    with pytest.raises(ValidationError):
        StepCommand(steps=0)

    with pytest.raises(ValidationError):
        SeekCommand(tick=-1)

    with pytest.raises(ValidationError):
        SetSpeedCommand(speed_multiplier=0.0)


def test_event_models() -> None:
    state = _state()
    snap = SnapshotEvent(tick=state.tick, state=state)
    metric = MetricEvent(tick=0, name="agents_count", value=1.0)
    err = ErrorEvent(tick=2, message="agent crash", agent_id="a1")
    life = LifecycleEvent(status="started", tick=0)

    assert snap.kind == "snapshot"
    assert metric.kind == "metric"
    assert err.kind == "error"
    assert life.kind == "lifecycle"
