from __future__ import annotations

import pytest

from sim_framework.contracts.models import AgentState, Vector2
from sim_framework.core.physics import WorldBounds, apply_movement


def _agent(x: float, y: float, vx: float, vy: float) -> AgentState:
    return AgentState(
        id="a1",
        position=Vector2(x=x, y=y),
        velocity=Vector2(x=vx, y=vy),
        energy=1.0,
        carrying=0,
        state_label="searching",
    )


def test_apply_movement_updates_position() -> None:
    agent = _agent(1.0, 1.0, 2.0, -1.0)
    moved = apply_movement(agent, dt=0.5, bounds=WorldBounds(width=10.0, height=10.0))

    assert moved.position == Vector2(x=2.0, y=0.5)
    assert agent.position == Vector2(x=1.0, y=1.0)


def test_clamp_boundary_mode() -> None:
    agent = _agent(9.5, 0.5, 2.0, -2.0)
    moved = apply_movement(
        agent,
        dt=1.0,
        bounds=WorldBounds(width=10.0, height=10.0),
        mode="clamp",
    )

    assert moved.position == Vector2(x=10.0, y=0.0)


def test_wrap_boundary_mode() -> None:
    agent = _agent(9.5, 0.5, 2.0, -2.0)
    moved = apply_movement(
        agent,
        dt=1.0,
        bounds=WorldBounds(width=10.0, height=10.0),
        mode="wrap",
    )

    assert moved.position == Vector2(x=1.5, y=8.5)


def test_invalid_time_step_rejected() -> None:
    agent = _agent(1.0, 1.0, 1.0, 1.0)

    with pytest.raises(ValueError):
        apply_movement(agent, dt=0.0, bounds=WorldBounds(width=10.0, height=10.0))


def test_invalid_bounds_rejected() -> None:
    with pytest.raises(ValueError):
        WorldBounds(width=0.0, height=10.0)
