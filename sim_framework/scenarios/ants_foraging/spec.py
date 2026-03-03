from __future__ import annotations

import random
from math import sqrt

from sim_framework.contracts.models import AgentState, Colony, FoodSource, SignalField, SimulationState, Vector2
from sim_framework.contracts.validators import (
    AgentAttributesSpec,
    BehaviorStepSpec,
    StateMachineAgentSchemaSpec,
    StateSpec,
    validate_known_behavior_names,
)
from sim_framework.core.environment import SignalGrid
from sim_framework.core.physics import WorldBounds, apply_movement

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


def build_initial_state(
    num_ants: int = 20,
    width: int = 30,
    height: int = 30,
    seed: int = 42,
) -> SimulationState:
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
                state_label=ANT_WORKER_SPEC.initial_state,
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


def _normalize(dx: float, dy: float) -> tuple[float, float]:
    mag = sqrt(dx * dx + dy * dy)
    if mag == 0.0:
        return 0.0, 0.0
    return dx / mag, dy / mag


def _best_pheromone_direction(position: Vector2, signal_grid: SignalGrid) -> tuple[float, float] | None:
    samples = [
        (1.0, 0.0),
        (-1.0, 0.0),
        (0.0, 1.0),
        (0.0, -1.0),
    ]
    best = None
    best_value = -1.0

    for dx, dy in samples:
        value = signal_grid.sample(Vector2(x=position.x + dx, y=position.y + dy))
        if value > best_value:
            best_value = value
            best = (dx, dy)

    if best_value <= 0.0:
        return None
    return best


def create_ant_behavior_runner(bounds: WorldBounds, signal_grid: SignalGrid):
    max_speed = ANT_WORKER_SPEC.attributes.max_speed
    pickup_radius = ANT_WORKER_SPEC.states["searching"].behaviors[2].params["pickup_radius"]
    drop_radius = ANT_WORKER_SPEC.states["carrying"].behaviors[1].params["arrival_radius"]
    deposit_amount = ANT_WORKER_SPEC.states["carrying"].behaviors[0].params["amount"]

    def run(agent: AgentState, state: SimulationState, rng: random.Random) -> AgentState:
        carrying = agent.carrying
        label = agent.state_label
        picked_this_tick = False

        # Transition: searching -> carrying when food is close.
        if label != "carrying":
            for food in state.food_sources:
                if food.amount > 0 and _dist(agent.position, food.position) <= float(pickup_radius):
                    carrying = 1
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
            direction = _best_pheromone_direction(agent.position, signal_grid)
            if direction is None:
                direction = _normalize(rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0))
            dx, dy = direction

        ux, uy = _normalize(dx, dy)
        next_agent = agent.model_copy(
            update={
                "carrying": carrying,
                "state_label": label,
                "velocity": Vector2(x=ux * max_speed, y=uy * max_speed),
            }
        )
        return apply_movement(next_agent, dt=1.0, bounds=bounds, mode="clamp")

    return run
