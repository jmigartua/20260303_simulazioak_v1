from __future__ import annotations

import random

import pytest

from sim_framework.contracts.validators import StateMachineAgentSchemaSpec
from sim_framework.core.environment import SignalGrid
from sim_framework.core.physics import SpatialHash, WorldBounds
from sim_framework.scenarios.ants_foraging import ANT_WORKER_SPEC, build_initial_state, create_ant_behavior_runner
from sim_framework.scenarios.registry import get_scenario, list_scenarios


def test_registry_contains_ants_foraging() -> None:
    names = list_scenarios()
    assert "ants_foraging" in names

    scenario = get_scenario("ants_foraging")
    assert "build_initial_state" in scenario
    assert "create_behavior_runner" in scenario


def test_ants_state_machine_spec_shape() -> None:
    assert isinstance(ANT_WORKER_SPEC, StateMachineAgentSchemaSpec)
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


def test_behavior_runner_uses_spatial_hash_queries(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {"build": 0, "query": 0}

    original_build = SpatialHash.build
    original_query_radius = SpatialHash.query_radius

    def build_spy(self: SpatialHash, agents):
        calls["build"] += 1
        return original_build(self, agents)

    def query_spy(self: SpatialHash, center, radius):
        calls["query"] += 1
        return original_query_radius(self, center, radius)

    monkeypatch.setattr(SpatialHash, "build", build_spy)
    monkeypatch.setattr(SpatialHash, "query_radius", query_spy)

    state = build_initial_state(num_ants=5, width=20, height=20, seed=11)
    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    bounds = WorldBounds(width=20.0, height=20.0)
    runner = create_ant_behavior_runner(bounds=bounds, signal_grid=signal_grid)
    rng = random.Random(state.seed)

    _ = runner(state.agents[0], state, rng)

    assert calls["build"] >= 1
    assert calls["query"] >= 1


def test_behavior_runner_caches_spatial_hash_per_tick(monkeypatch: pytest.MonkeyPatch) -> None:
    build_calls = 0
    original_build = SpatialHash.build

    def build_spy(self: SpatialHash, agents):
        nonlocal build_calls
        build_calls += 1
        return original_build(self, agents)

    monkeypatch.setattr(SpatialHash, "build", build_spy)

    state = build_initial_state(num_ants=5, width=20, height=20, seed=12)
    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    bounds = WorldBounds(width=20.0, height=20.0)
    runner = create_ant_behavior_runner(bounds=bounds, signal_grid=signal_grid)
    rng = random.Random(state.seed)

    _ = runner(state.agents[0], state, rng)
    _ = runner(state.agents[1], state, rng)
    assert build_calls == 1

    next_tick_state = state.model_copy(update={"tick": state.tick + 1})
    _ = runner(next_tick_state.agents[0], next_tick_state, rng)
    assert build_calls == 2
