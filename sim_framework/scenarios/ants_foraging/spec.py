from __future__ import annotations

import random
from math import sqrt

from sim_framework.contracts.behaviors import BehaviorProtocol, BehaviorRegistry
from sim_framework.contracts.models import AgentState, Colony, FoodSource, SignalField, SimulationState, Vector2
from sim_framework.contracts.validators import (
    AgentAttributesSpec,
    BehaviorStepSpec,
    StateMachineAgentSchemaSpec,
    StateSpec,
    validate_known_behavior_names,
)
from sim_framework.core.environment import SignalGrid
from sim_framework.core.physics import (
    BoundaryMode,
    SpatialHash,
    WorldBounds,
    apply_movement,
    normalize_vector,
)
from sim_framework.scenarios.state_machine import behavior_params

ANT_WORKER_SPEC = StateMachineAgentSchemaSpec(
    agent_type="ant_worker",
    attributes=AgentAttributesSpec(max_speed=1.0, sensor_radius=4.0, carry_capacity=1),
    states={
        "searching": StateSpec(
            behaviors=[
                BehaviorStepSpec(name="sense_pheromone", params={"follow_weight": 0.7}),
                BehaviorStepSpec(name="wander_or_follow", params={"wander_sigma": 0.4}),
                BehaviorStepSpec(name="check_food", params={"pickup_radius": 1.0}),
            ],
            transitions={"has_food": "carrying"},
        ),
        "carrying": StateSpec(
            behaviors=[
                BehaviorStepSpec(name="deposit_pheromone", params={"amount": 1.0}),
                BehaviorStepSpec(name="move_to_colony", params={"arrival_radius": 1.0}),
                BehaviorStepSpec(name="drop_food", params={}),
            ],
            transitions={"food_dropped": "searching"},
        ),
    },
    initial_state="searching",
)

validate_known_behavior_names(
    ANT_WORKER_SPEC,
    {
        "sense_pheromone",
        "wander_or_follow",
        "check_food",
        "deposit_pheromone",
        "move_to_colony",
        "drop_food",
    },
)

ANT_KNOWN_BEHAVIOR_NAMES = {
    "sense_pheromone",
    "wander_or_follow",
    "check_food",
    "deposit_pheromone",
    "move_to_colony",
    "drop_food",
}
ANT_REQUIRED_STATES = {"searching", "carrying"}
ANT_REQUIRED_BEHAVIORS_BY_STATE = {
    "searching": {"sense_pheromone", "wander_or_follow", "check_food"},
    "carrying": {"deposit_pheromone", "move_to_colony", "drop_food"},
}


def validate_ant_agent_spec(spec: StateMachineAgentSchemaSpec) -> StateMachineAgentSchemaSpec:
    validate_known_behavior_names(spec, ANT_KNOWN_BEHAVIOR_NAMES)
    missing_states = ANT_REQUIRED_STATES - set(spec.states.keys())
    if missing_states:
        raise ValueError(
            f"Ant spec missing required states: {', '.join(sorted(missing_states))}"
        )

    for state_name, required_names in ANT_REQUIRED_BEHAVIORS_BY_STATE.items():
        state_spec = spec.states[state_name]
        present_names = {step.name for step in state_spec.behaviors}
        missing = required_names - present_names
        if missing:
            raise ValueError(
                f"Ant spec state '{state_name}' missing required behaviors: "
                f"{', '.join(sorted(missing))}"
            )
    return spec


def _effective_ant_spec(
    agent_spec: StateMachineAgentSchemaSpec | None,
) -> StateMachineAgentSchemaSpec:
    return validate_ant_agent_spec(agent_spec or ANT_WORKER_SPEC)


def build_initial_state(
    num_ants: int = 20,
    width: int = 30,
    height: int = 30,
    seed: int = 42,
    agent_spec: StateMachineAgentSchemaSpec | None = None,
) -> SimulationState:
    spec = _effective_ant_spec(agent_spec)
    rng = random.Random(seed)
    colony_pos = Vector2(x=width / 2.0, y=height / 2.0)

    agents: list[AgentState] = []
    for i in range(num_ants):
        jitter_x = rng.uniform(-0.4, 0.4)
        jitter_y = rng.uniform(-0.4, 0.4)
        agents.append(
            AgentState(
                id=f"ant-{i}",
                position=Vector2(x=colony_pos.x + jitter_x, y=colony_pos.y + jitter_y),
                velocity=Vector2(x=0.0, y=0.0),
                energy=1.0,
                carrying=0,
                state_label=spec.initial_state,
            )
        )

    # One food source close to colony guarantees early pickup for deterministic tests.
    food_sources = [
        FoodSource(id="food-near", position=Vector2(x=colony_pos.x + 0.8, y=colony_pos.y), amount=500.0),
        FoodSource(id="food-far-1", position=Vector2(x=2.0, y=2.0), amount=500.0),
        FoodSource(id="food-far-2", position=Vector2(x=width - 2.0, y=height - 2.0), amount=500.0),
    ]

    return SimulationState(
        tick=0,
        agents=agents,
        food_sources=food_sources,
        colony=Colony(id="colony-1", position=colony_pos),
        signal_fields=[SignalField(kind="pheromone", width=width, height=height, decay=0.98, diffusion=0.2)],
        seed=seed,
    )


def _dist(a: Vector2, b: Vector2) -> float:
    dx = a.x - b.x
    dy = a.y - b.y
    return sqrt(dx * dx + dy * dy)

def create_ant_behavior_runner(
    bounds: WorldBounds,
    signal_grid: SignalGrid,
    *,
    boundary_mode: BoundaryMode = "clamp",
    agent_spec: StateMachineAgentSchemaSpec | None = None,
):
    if boundary_mode not in {"clamp", "wrap"}:
        raise ValueError("boundary_mode must be 'clamp' or 'wrap'")
    spec = _effective_ant_spec(agent_spec)

    max_speed = spec.attributes.max_speed
    sensor_radius = spec.attributes.sensor_radius
    pickup_radius = behavior_params(
        spec,
        state_name="searching",
        behavior_name="check_food",
    )["pickup_radius"]
    drop_radius = behavior_params(
        spec,
        state_name="carrying",
        behavior_name="move_to_colony",
    )["arrival_radius"]
    deposit_amount = behavior_params(
        spec,
        state_name="carrying",
        behavior_name="deposit_pheromone",
    )["amount"]
    neighbor_radius = 1.5
    avoid_weight = 0.35
    spatial_hash = SpatialHash(cell_size=neighbor_radius)
    indexed_tick: int | None = None

    def _neighbor_avoidance(agent: AgentState, state: SimulationState) -> tuple[float, float]:
        nonlocal indexed_tick
        if indexed_tick != state.tick:
            spatial_hash.build(state.agents)
            indexed_tick = state.tick

        ax = 0.0
        ay = 0.0
        agent_pos = agent.position
        agent_x = agent_pos.x
        agent_y = agent_pos.y
        nearby = spatial_hash.query_radius(agent.position, neighbor_radius)
        for other in nearby:
            if other is agent:
                continue
            other_pos = other.position
            dx = agent_x - other_pos.x
            dy = agent_y - other_pos.y
            dist_sq = dx * dx + dy * dy
            if dist_sq == 0.0:
                continue
            inv_dist_sq = 1.0 / dist_sq
            ax += dx * inv_dist_sq
            ay += dy * inv_dist_sq
        return normalize_vector(ax, ay)

    class AntStateMachineBehavior(BehaviorProtocol):
        def sense(self, agent: AgentState, state: SimulationState) -> dict[str, object]:
            return {"agent": agent, "state": state}

        def decide(
            self,
            perception: dict[str, object],
            rng: random.Random,
        ) -> dict[str, object]:
            agent = perception["agent"]
            state = perception["state"]
            if not isinstance(agent, AgentState) or not isinstance(state, SimulationState):
                raise TypeError("Invalid ant behavior perception payload")

            carrying = agent.carrying
            label = agent.state_label
            picked_this_tick = False

            # Transition: searching -> carrying when food is close.
            if label != "carrying":
                for food in state.food_sources:
                    if food.amount > 0 and _dist(agent.position, food.position) <= float(pickup_radius):
                        carrying = 1
                        food.amount = max(0.0, food.amount - 1.0)
                        label = "carrying"
                        picked_this_tick = True
                        break

            if label == "carrying":
                signal_grid.deposit(agent.position, float(deposit_amount))
                dx = state.colony.position.x - agent.position.x
                dy = state.colony.position.y - agent.position.y

                if (not picked_this_tick) and _dist(agent.position, state.colony.position) <= float(drop_radius):
                    carrying = 0
                    label = "searching"
            else:
                direction = signal_grid.sense_gradient(agent.position, sensor_radius)
                if direction is None:
                    direction = normalize_vector(rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0))
                dx, dy = direction

            avoid_dx, avoid_dy = _neighbor_avoidance(agent, state)
            dx += avoid_dx * avoid_weight
            dy += avoid_dy * avoid_weight

            ux, uy = normalize_vector(dx, dy)
            next_agent = agent.model_copy(
                update={
                    "carrying": carrying,
                    "state_label": label,
                    "velocity": Vector2(x=ux * max_speed, y=uy * max_speed),
                }
            )
            return {"next_agent": next_agent}

        def act(
            self,
            agent: AgentState,
            decision: dict[str, object],
            state: SimulationState,
        ) -> AgentState:
            _ = state
            next_agent = decision.get("next_agent")
            if not isinstance(next_agent, AgentState):
                raise TypeError("Invalid ant behavior decision payload")
            return apply_movement(next_agent, dt=1.0, bounds=bounds, mode=boundary_mode)

    registry = BehaviorRegistry()
    registry.register("ant_state_machine", AntStateMachineBehavior)
    behavior = registry.create("ant_state_machine")

    def run(agent: AgentState, state: SimulationState, rng: random.Random) -> AgentState:
        perception = behavior.sense(agent, state)
        decision = behavior.decide(perception, rng)
        return behavior.act(agent, decision, state)

    return run
