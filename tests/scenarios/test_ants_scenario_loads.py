from __future__ import annotations

import pytest

from sim_framework.scenarios.ants_foraging import ANT_WORKER_SPEC, build_initial_state
from sim_framework.scenarios.registry import get_scenario, list_scenarios


def test_registry_contains_ants_foraging() -> None:
    names = list_scenarios()
    assert "ants_foraging" in names

    scenario = get_scenario("ants_foraging")
    assert "build_initial_state" in scenario
    assert "create_behavior_runner" in scenario


def test_ants_state_machine_spec_shape() -> None:
    assert ANT_WORKER_SPEC.initial_state == "searching"
    assert set(ANT_WORKER_SPEC.states.keys()) == {"searching", "carrying"}

    searching_behaviors = [node.name for node in ANT_WORKER_SPEC.states["searching"].behaviors]
    carrying_behaviors = [node.name for node in ANT_WORKER_SPEC.states["carrying"].behaviors]

    assert "sense_pheromone" in searching_behaviors
    assert "deposit_pheromone" in carrying_behaviors
    assert ANT_WORKER_SPEC.states["searching"].transitions.get("has_food") == "carrying"
    assert ANT_WORKER_SPEC.states["carrying"].transitions.get("food_dropped") == "searching"


def test_build_initial_state_has_agents_food_and_pheromone_field() -> None:
    state = build_initial_state(num_ants=10, width=20, height=20, seed=7)

    assert state.tick == 0
    assert len(state.agents) == 10
    assert len(state.food_sources) >= 1
    assert state.signal_fields
    assert state.signal_fields[0].kind == "pheromone"
    assert all(agent.state_label == "searching" for agent in state.agents)


def test_unknown_scenario_raises() -> None:
    with pytest.raises(KeyError):
        get_scenario("does_not_exist")
