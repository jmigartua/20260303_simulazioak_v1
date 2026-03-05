from __future__ import annotations

import random

from sim_framework.contracts.models import AgentState, Colony, SimulationState, Vector2
from sim_framework.core.engine import SimulationEngine


def _state() -> SimulationState:
    return SimulationState(
        tick=0,
        agents=[
            AgentState(id="good", position=Vector2(x=0.0, y=0.0)),
            AgentState(id="bad", position=Vector2(x=1.0, y=0.0)),
        ],
        food_sources=[],
        colony=Colony(id="c1", position=Vector2(x=0.0, y=0.0)),
        signal_fields=[],
        seed=42,
    )


def _runner(agent: AgentState, state: SimulationState, rng: random.Random) -> AgentState:
    _ = (state, rng)
    if agent.id == "bad":
        raise RuntimeError("boom")

    return agent.model_copy(update={"position": Vector2(x=agent.position.x + 1.0, y=0.0)})


def test_per_agent_error_isolation_keeps_loop_alive() -> None:
    engine = SimulationEngine(seed=99)
    state = _state()

    next_state = engine.tick(state, _runner)

    assert next_state.tick == 1
    assert [agent.id for agent in next_state.agents] == ["good"]
    assert next_state.agents[0].position.x == 1.0

    events = engine.drain_published_events()
    error_events = [event for event in events if event.kind == "error"]
    snapshot_events = [event for event in events if event.kind == "snapshot"]
    metric_events = [event for event in events if event.kind == "metric"]

    assert len(error_events) == 1
    assert error_events[0].agent_id == "bad"
    assert len(snapshot_events) == 1
    assert len(metric_events) == 1
    assert metric_events[0].name == "agents_count"
    assert metric_events[0].value == 1.0


def test_engine_continues_after_error_on_next_tick() -> None:
    engine = SimulationEngine(seed=99)
    state = _state()

    state = engine.tick(state, _runner)
    engine.drain_published_events()

    state = engine.tick(state, _runner)
    assert state.tick == 2
    assert [agent.id for agent in state.agents] == ["good"]
    assert state.agents[0].position.x == 2.0
