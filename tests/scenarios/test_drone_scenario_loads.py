from __future__ import annotations

import random

from sim_framework.contracts.validators import StateMachineAgentSchemaSpec
from sim_framework.core.environment import SignalGrid
from sim_framework.core.physics import WorldBounds
from sim_framework.scenarios.drone_patrol import (
    DRONE_SCOUT_SPEC,
    build_drone_initial_state,
    create_drone_behavior_runner,
)
from sim_framework.scenarios.registry import get_scenario, list_scenarios


def test_registry_contains_drone_patrol() -> None:
    names = list_scenarios()
    assert "drone_patrol" in names

    scenario = get_scenario("drone_patrol")
    assert "build_initial_state" in scenario
    assert "create_behavior_runner" in scenario


def test_drone_state_machine_spec_shape() -> None:
    assert isinstance(DRONE_SCOUT_SPEC, StateMachineAgentSchemaSpec)
    assert DRONE_SCOUT_SPEC.initial_state == "patrolling"
    assert set(DRONE_SCOUT_SPEC.states.keys()) == {"patrolling"}
    behavior_names = [step.name for step in DRONE_SCOUT_SPEC.states["patrolling"].behaviors]
    assert behavior_names == ["select_waypoint", "move_to_waypoint", "broadcast_beacon"]


def test_build_initial_state_has_drones_and_radio_field() -> None:
    state = build_drone_initial_state(num_drones=8, width=30, height=20, seed=5)
    assert state.tick == 0
    assert len(state.agents) == 8
    assert state.food_sources == []
    assert state.signal_fields
    assert state.signal_fields[0].kind == "radio"
    assert all(agent.state_label == "patrolling" for agent in state.agents)


def test_behavior_runner_keeps_agents_in_bounds_and_emits_signal() -> None:
    state = build_drone_initial_state(num_drones=4, width=20, height=20, seed=7)
    bounds = WorldBounds(width=20.0, height=20.0)
    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    runner = create_drone_behavior_runner(bounds=bounds, signal_grid=signal_grid)
    rng = random.Random(state.seed)

    next_agent = runner(state.agents[0], state, rng)
    assert 0.0 <= next_agent.position.x <= bounds.width
    assert 0.0 <= next_agent.position.y <= bounds.height
    assert next_agent.state_label == "patrolling"
    assert signal_grid.total_signal() > 0.0

