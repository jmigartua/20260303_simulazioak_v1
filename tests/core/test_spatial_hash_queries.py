from __future__ import annotations

import pytest

from sim_framework.contracts.models import AgentState, Vector2
from sim_framework.core.physics import SpatialHash


def _agent(agent_id: str, x: float, y: float) -> AgentState:
    return AgentState(
        id=agent_id,
        position=Vector2(x=x, y=y),
        velocity=Vector2(x=0.0, y=0.0),
        energy=1.0,
        carrying=0,
        state_label="searching",
    )


def test_spatial_hash_build_and_query_cell() -> None:
    index = SpatialHash(cell_size=1.0)
    agents = [
        _agent("a", 0.1, 0.1),
        _agent("b", 0.9, 0.8),
        _agent("c", 2.2, 2.2),
    ]
    index.build(agents)

    cell_agents = index.query_cell((0, 0))
    assert sorted(a.id for a in cell_agents) == ["a", "b"]


def test_spatial_hash_query_radius_returns_local_agents() -> None:
    index = SpatialHash(cell_size=1.0)
    agents = [
        _agent("a", 0.0, 0.0),
        _agent("b", 0.7, 0.7),
        _agent("c", 4.0, 4.0),
    ]
    index.build(agents)

    near = index.query_radius(Vector2(x=0.0, y=0.0), radius=1.1)
    assert sorted(a.id for a in near) == ["a", "b"]

    far = index.query_radius(Vector2(x=0.0, y=0.0), radius=0.2)
    assert sorted(a.id for a in far) == ["a"]


def test_spatial_hash_handles_negative_coordinates() -> None:
    index = SpatialHash(cell_size=1.0)
    agent = _agent("neg", -0.2, -0.8)
    index.build([agent])

    queried = index.query_cell((-1, -1))
    assert [a.id for a in queried] == ["neg"]


def test_invalid_query_radius_rejected() -> None:
    index = SpatialHash(cell_size=1.0)
    with pytest.raises(ValueError):
        index.query_radius(Vector2(x=0.0, y=0.0), radius=-0.1)


def test_invalid_cell_size_rejected() -> None:
    with pytest.raises(ValueError):
        SpatialHash(cell_size=0.0)
