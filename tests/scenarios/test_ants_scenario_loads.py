from __future__ import annotations

import random

import pytest

from sim_framework.contracts.models import AgentState, Vector2
from sim_framework.contracts.behaviors import BehaviorRegistry
from sim_framework.contracts.validators import StateMachineAgentSchemaSpec
from sim_framework.core.environment import SignalGrid
from sim_framework.core.physics import SpatialHash, WorldBounds
from sim_framework.scenarios.ants_foraging import (
    ANT_WORKER_SPEC,
    build_initial_state,
    create_ant_behavior_runner,
    validate_ant_agent_spec,
)
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
    assert sum(1 for agent in state.agents if agent.state_label == "searching") == 4
    assert sum(1 for agent in state.agents if agent.state_label == "waiting") == 6
    assert state.delivered_food == 0
    assert state.food_discovered is False
    assert state.released_agents == 4
    assert len(state.obstacles) >= 1
    assert {zone.kind for zone in state.zones} >= {"nest", "forage"}


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


def test_ant_runner_respects_configured_boundary_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    seen_mode: dict[str, str] = {}

    def fake_apply_movement(agent, dt, bounds, mode="clamp"):
        _ = (dt, bounds)
        seen_mode["mode"] = mode
        return agent

    monkeypatch.setattr("sim_framework.scenarios.ants_foraging.spec.apply_movement", fake_apply_movement)

    state = build_initial_state(num_ants=2, width=20, height=20, seed=9)
    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    bounds = WorldBounds(width=20.0, height=20.0)
    runner = create_ant_behavior_runner(bounds=bounds, signal_grid=signal_grid, boundary_mode="wrap")
    rng = random.Random(state.seed)

    _ = runner(state.agents[0], state, rng)
    assert seen_mode["mode"] == "wrap"


def test_ant_spec_override_applies_initial_state_and_speed() -> None:
    spec = ANT_WORKER_SPEC.model_copy(deep=True)
    spec.initial_state = "carrying"
    spec.attributes.max_speed = 2.5
    validate_ant_agent_spec(spec)

    state = build_initial_state(num_ants=1, width=20, height=20, seed=13, agent_spec=spec)
    assert state.agents[0].state_label == "carrying"

    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    bounds = WorldBounds(width=20.0, height=20.0)
    runner = create_ant_behavior_runner(bounds=bounds, signal_grid=signal_grid, agent_spec=spec)
    rng = random.Random(state.seed)
    updated = runner(state.agents[0], state, rng)
    speed = (updated.velocity.x**2 + updated.velocity.y**2) ** 0.5
    assert pytest.approx(speed, rel=1e-6) == 2.5


def test_food_amount_decrements_on_pickup() -> None:
    state = build_initial_state(num_ants=1, width=20, height=20, seed=21)
    food_pos = state.food_sources[0].position
    forced_agent = state.agents[0].model_copy(
        update={"position": food_pos, "state_label": "searching", "carrying": 0}
    )
    state = state.model_copy(update={"agents": [forced_agent]})
    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    bounds = WorldBounds(width=20.0, height=20.0)
    runner = create_ant_behavior_runner(bounds=bounds, signal_grid=signal_grid)
    rng = random.Random(state.seed)

    initial_amount = state.food_sources[0].amount
    updated = runner(state.agents[0], state, rng)

    assert updated.carrying == 1
    assert state.food_sources[0].amount < initial_amount


def test_delivered_food_increments_when_ant_returns_to_colony() -> None:
    state = build_initial_state(num_ants=1, width=20, height=20, seed=24)
    forced_agent = state.agents[0].model_copy(
        update={
            "position": state.colony.position,
            "state_label": "carrying",
            "carrying": 1,
        }
    )
    state = state.model_copy(update={"agents": [forced_agent], "delivered_food": 0})
    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    bounds = WorldBounds(width=20.0, height=20.0)
    runner = create_ant_behavior_runner(bounds=bounds, signal_grid=signal_grid)
    rng = random.Random(state.seed)

    updated = runner(state.agents[0], state, rng)

    assert updated.carrying == 0
    assert updated.state_label == "searching"
    assert state.delivered_food == 1
    assert state.food_discovered is True
    assert state.released_agents == len(state.agents)


def test_waiting_workers_stay_idle_until_food_is_discovered() -> None:
    state = build_initial_state(num_ants=8, width=30, height=30, seed=25)
    waiting_agent = next(agent for agent in state.agents if agent.state_label == "waiting")
    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    bounds = WorldBounds(width=30.0, height=30.0)
    runner = create_ant_behavior_runner(bounds=bounds, signal_grid=signal_grid)
    rng = random.Random(state.seed)

    updated = runner(waiting_agent, state, rng)

    assert updated.state_label == "waiting"
    assert updated.velocity == Vector2(x=0.0, y=0.0)


def test_waiting_workers_are_released_after_food_discovery() -> None:
    state = build_initial_state(num_ants=8, width=30, height=30, seed=26)
    waiting_agent = next(agent for agent in state.agents if agent.state_label == "waiting")
    released_state = state.model_copy(update={"food_discovered": True, "released_agents": len(state.agents)})
    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    bounds = WorldBounds(width=30.0, height=30.0)
    runner = create_ant_behavior_runner(bounds=bounds, signal_grid=signal_grid)
    rng = random.Random(state.seed)

    updated = runner(waiting_agent, released_state, rng)

    assert updated.state_label in {"searching", "carrying"}


def test_ant_runner_does_not_require_forage_zone_hints() -> None:
    state = build_initial_state(num_ants=1, width=30, height=30, seed=30)
    state = state.model_copy(update={"zones": [zone for zone in state.zones if zone.kind == "nest"]})
    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    bounds = WorldBounds(width=30.0, height=30.0)
    runner = create_ant_behavior_runner(bounds=bounds, signal_grid=signal_grid)
    rng = random.Random(state.seed)

    updated = runner(state.agents[0], state, rng)

    assert updated.state_label in {"searching", "carrying"}
    assert updated.position != state.agents[0].position


def test_ant_runner_treats_obstacles_as_solid() -> None:
    state = build_initial_state(num_ants=1, width=30, height=30, seed=31)
    obstacle = state.obstacles[0]
    forced_agent = AgentState(
        id="ant-solid",
        position=Vector2(x=obstacle.position.x - 0.3, y=obstacle.position.y + (obstacle.height / 2.0)),
        velocity=Vector2(x=1.0, y=0.0),
        energy=1.0,
        carrying=1,
        state_label="carrying",
    )
    state = state.model_copy(update={"agents": [forced_agent]})
    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    bounds = WorldBounds(width=30.0, height=30.0)
    runner = create_ant_behavior_runner(bounds=bounds, signal_grid=signal_grid)
    rng = random.Random(state.seed)

    updated = runner(state.agents[0], state, rng)

    obstacle_left = obstacle.position.x
    assert updated.position.x <= obstacle_left


def test_ant_runner_uses_behavior_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {"register": 0, "create": 0}
    original_register = BehaviorRegistry.register
    original_create = BehaviorRegistry.create

    def register_spy(self: BehaviorRegistry, name, factory):
        calls["register"] += 1
        return original_register(self, name, factory)

    def create_spy(self: BehaviorRegistry, name):
        calls["create"] += 1
        return original_create(self, name)

    monkeypatch.setattr(BehaviorRegistry, "register", register_spy)
    monkeypatch.setattr(BehaviorRegistry, "create", create_spy)

    state = build_initial_state(num_ants=3, width=20, height=20, seed=22)
    signal_grid = SignalGrid.from_config(state.signal_fields[0])
    bounds = WorldBounds(width=20.0, height=20.0)
    runner = create_ant_behavior_runner(bounds=bounds, signal_grid=signal_grid)
    rng = random.Random(state.seed)
    _ = runner(state.agents[0], state, rng)

    assert calls["register"] >= 1
    assert calls["create"] >= 1
