from __future__ import annotations

import random

import pytest

from sim_framework.contracts.behaviors import BehaviorProtocol, BehaviorRegistry
from sim_framework.contracts.models import AgentState, Colony, SimulationState, Vector2


class DummyBehavior:
    def sense(self, agent: AgentState, state: SimulationState):
        _ = (agent, state)
        return {"target": Vector2(x=1.0, y=1.0)}

    def decide(self, perception, rng: random.Random):
        _ = rng
        return {"move_to": perception["target"]}

    def act(self, agent: AgentState, decision, state: SimulationState) -> AgentState:
        _ = state
        target = decision["move_to"]
        return agent.model_copy(update={"position": target})


class BadBehavior:
    def sense(self, agent: AgentState, state: SimulationState):
        _ = (agent, state)
        return {}


def _state() -> SimulationState:
    return SimulationState(
        tick=0,
        agents=[AgentState(id="a1", position=Vector2(x=0.0, y=0.0))],
        food_sources=[],
        colony=Colony(id="c1", position=Vector2(x=2.0, y=2.0)),
        signal_fields=[],
        seed=42,
    )


def test_registry_register_and_create() -> None:
    registry = BehaviorRegistry()
    registry.register("move_dummy", DummyBehavior)

    created = registry.create("move_dummy")
    assert isinstance(created, BehaviorProtocol)
    assert registry.exists("move_dummy")
    assert registry.names() == ["move_dummy"]


def test_registry_duplicate_guard() -> None:
    registry = BehaviorRegistry()
    registry.register("move_dummy", DummyBehavior)

    with pytest.raises(ValueError):
        registry.register("move_dummy", DummyBehavior)


def test_registry_unknown_behavior() -> None:
    registry = BehaviorRegistry()

    with pytest.raises(KeyError):
        registry.create("missing")


def test_registry_rejects_invalid_behavior_factory() -> None:
    registry = BehaviorRegistry()

    with pytest.raises(TypeError):
        registry.register("bad", BadBehavior)


def test_behavior_act_updates_position() -> None:
    behavior = DummyBehavior()
    state = _state()
    agent = state.agents[0]

    perception = behavior.sense(agent, state)
    decision = behavior.decide(perception, random.Random(42))
    updated = behavior.act(agent, decision, state)

    assert updated.position == Vector2(x=1.0, y=1.0)
