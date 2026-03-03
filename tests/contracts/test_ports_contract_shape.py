from __future__ import annotations

import inspect
from pathlib import Path
from typing import Protocol, get_type_hints

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
    LoadedRun,
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

    def load_run(self, run_id: str) -> LoadedRun:
        _ = run_id
        raise NotImplementedError


class StubHistory:
    def snapshot(self, state: SimulationState, tick: int) -> None:
        _ = (state, tick)

    def nearest_snapshot_before(self, tick: int) -> tuple[int, SimulationState] | None:
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


def _assert_method_signature_matches_protocol(
    protocol: type[Protocol], implementation: type[object], method_name: str
) -> None:
    protocol_method = getattr(protocol, method_name)
    implementation_method = getattr(implementation, method_name)
    protocol_sig = inspect.signature(protocol_method)
    implementation_sig = inspect.signature(implementation_method)

    assert tuple(protocol_sig.parameters) == tuple(implementation_sig.parameters)
    assert [p.kind for p in protocol_sig.parameters.values()] == [
        p.kind for p in implementation_sig.parameters.values()
    ]

    protocol_hints = get_type_hints(protocol_method)
    implementation_hints = get_type_hints(implementation_method)
    for param_name in protocol_sig.parameters:
        assert implementation_hints.get(param_name) == protocol_hints.get(param_name)
    assert implementation_hints.get("return") == protocol_hints.get("return")


def test_protocol_runtime_conformance() -> None:
    assert isinstance(StubRenderer(), RendererPort)
    assert isinstance(StubPersistence(), PersistencePort)
    assert isinstance(StubHistory(), HistoryPort)

    _assert_method_signature_matches_protocol(RendererPort, StubRenderer, "render")
    _assert_method_signature_matches_protocol(
        RendererPort, StubRenderer, "capture_screenshot"
    )
    _assert_method_signature_matches_protocol(
        PersistencePort, StubPersistence, "save_run"
    )
    _assert_method_signature_matches_protocol(
        PersistencePort, StubPersistence, "load_run"
    )
    _assert_method_signature_matches_protocol(HistoryPort, StubHistory, "snapshot")
    _assert_method_signature_matches_protocol(
        HistoryPort, StubHistory, "nearest_snapshot_before"
    )
    _assert_method_signature_matches_protocol(HistoryPort, StubHistory, "rewind")


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
