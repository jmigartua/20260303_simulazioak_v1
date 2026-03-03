import pytest
from pydantic import ValidationError

from sim_framework.contracts.models import (
    AgentState,
    Colony,
    FoodSource,
    SignalField,
    SimulationState,
    Vector2,
)


def test_vector2_is_constructible() -> None:
    point = Vector2(x=1.0, y=2.0)
    assert point.x == 1.0
    assert point.y == 2.0


def test_agent_defaults() -> None:
    agent = AgentState(id="a1", position=Vector2(x=0.0, y=0.0))
    assert agent.energy == 1.0
    assert agent.carrying == 0
    assert agent.state_label == "searching"


def test_food_amount_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        FoodSource(id="f1", position=Vector2(x=1.0, y=1.0), amount=0.0)


def test_signal_field_bounds() -> None:
    field = SignalField(kind="pheromone", width=10, height=12, decay=0.9, diffusion=0.3)
    assert field.width == 10
    assert field.decay == 0.9


def test_simulation_state_builds() -> None:
    state = SimulationState(
        tick=0,
        agents=[AgentState(id="a1", position=Vector2(x=0.0, y=0.0))],
        food_sources=[FoodSource(id="f1", position=Vector2(x=5.0, y=5.0), amount=10.0)],
        colony=Colony(id="c1", position=Vector2(x=2.0, y=2.0)),
        signal_fields=[SignalField(kind="pheromone", width=20, height=20)],
        seed=42,
    )
    assert state.tick == 0
    assert len(state.agents) == 1
    assert state.colony.id == "c1"
