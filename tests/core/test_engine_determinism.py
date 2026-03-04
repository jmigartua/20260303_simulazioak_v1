from __future__ import annotations

import random

from sim_framework.contracts.models import (
    AgentState,
    Colony,
    PauseCommand,
    SetSpeedCommand,
    SimulationState,
    StepCommand,
    Vector2,
)
from sim_framework.core.engine import SimulationEngine


def _state(num_agents: int = 3) -> SimulationState:
    agents = [
        AgentState(id=f"a{i}", position=Vector2(x=float(i), y=0.0))
        for i in range(num_agents)
    ]
    return SimulationState(
        tick=0,
        agents=agents,
        food_sources=[],
        colony=Colony(id="c1", position=Vector2(x=0.0, y=0.0)),
        signal_fields=[],
        seed=42,
    )


def _runner(agent: AgentState, state: SimulationState, rng: random.Random) -> AgentState:
    _ = state
    dx = rng.uniform(-0.5, 0.5)
    new_pos = Vector2(x=agent.position.x + dx, y=agent.position.y)
    return agent.model_copy(update={"position": new_pos})


def test_deterministic_rng_with_same_seed() -> None:
    engine_a = SimulationEngine(seed=123)
    engine_b = SimulationEngine(seed=123)

    state_a = _state()
    state_b = _state()

    for _ in range(6):
        state_a = engine_a.tick(state_a, _runner)
        state_b = engine_b.tick(state_b, _runner)

    assert state_a.model_dump() == state_b.model_dump()


def test_command_drain_happens_at_tick_boundary() -> None:
    engine = SimulationEngine(seed=7)
    state = _state(num_agents=1)

    engine.enqueue_command(PauseCommand())
    paused_state = engine.tick(state, _runner)
    assert paused_state.tick == 0

    events = engine.drain_published_events()
    assert any(event.kind == "lifecycle" and event.status == "paused" for event in events)

    engine.enqueue_command(StepCommand(steps=2))
    step1 = engine.tick(paused_state, _runner)
    step2 = engine.tick(step1, _runner)
    step3 = engine.tick(step2, _runner)

    assert step1.tick == 1
    assert step2.tick == 2
    assert step3.tick == 2

    later_events = engine.drain_published_events()
    snapshot_events = [event for event in later_events if event.kind == "snapshot"]
    assert len(snapshot_events) == 2


def test_speed_multiplier_accelerates_steps_when_running() -> None:
    engine = SimulationEngine(seed=7)
    state = _state(num_agents=1)

    engine.enqueue_command(SetSpeedCommand(speed_multiplier=3.0))
    state = engine.tick(state, _runner)

    assert state.tick == 3
    assert engine.speed_multiplier == 3.0

    events = engine.drain_published_events()
    snapshot_events = [event for event in events if event.kind == "snapshot"]
    assert len(snapshot_events) == 3


def test_speed_multiplier_does_not_batch_paused_step_command() -> None:
    engine = SimulationEngine(seed=7)
    state = _state(num_agents=1)

    engine.enqueue_command(PauseCommand())
    state = engine.tick(state, _runner)
    engine.drain_published_events()

    engine.enqueue_command(SetSpeedCommand(speed_multiplier=4.0))
    state = engine.tick(state, _runner)
    assert state.tick == 0

    engine.enqueue_command(StepCommand(steps=1))
    state = engine.tick(state, _runner)
    assert state.tick == 1


def test_can_disable_snapshot_event_emission_for_headless_mode() -> None:
    engine = SimulationEngine(seed=7, emit_snapshot_events=False)
    state = _state(num_agents=1)

    state = engine.tick(state, _runner)
    assert state.tick == 1
    assert engine.emit_snapshot_events is False

    events = engine.drain_published_events()
    snapshot_events = [event for event in events if event.kind == "snapshot"]
    assert not snapshot_events
