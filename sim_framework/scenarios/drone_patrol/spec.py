from __future__ import annotations

import random

from sim_framework.contracts.behaviors import BehaviorProtocol, BehaviorRegistry
from sim_framework.contracts.models import (
    AgentState,
    Colony,
    SignalField,
    SimulationState,
    TerrainObstacle,
    Vector2,
    WorldZone,
)
from sim_framework.contracts.validators import (
    AgentAttributesSpec,
    BehaviorStepSpec,
    StateMachineAgentSchemaSpec,
    StateSpec,
    validate_known_behavior_names,
)
from sim_framework.core.environment import SignalGrid
from sim_framework.core.physics import BoundaryMode, WorldBounds, apply_movement, normalize_vector
from sim_framework.scenarios.state_machine import behavior_params

DRONE_SCOUT_SPEC = StateMachineAgentSchemaSpec(
    agent_type="drone_scout",
    attributes=AgentAttributesSpec(max_speed=1.2, sensor_radius=6.0, carry_capacity=0),
    states={
        "patrolling": StateSpec(
            behaviors=[
                BehaviorStepSpec(name="select_waypoint", params={"segment_ticks": 10}),
                BehaviorStepSpec(name="move_to_waypoint", params={}),
                BehaviorStepSpec(name="broadcast_beacon", params={"amount": 0.15}),
            ],
            transitions={},
        )
    },
    initial_state="patrolling",
)

validate_known_behavior_names(
    DRONE_SCOUT_SPEC,
    {"select_waypoint", "move_to_waypoint", "broadcast_beacon"},
)

DRONE_KNOWN_BEHAVIOR_NAMES = {
    "select_waypoint",
    "move_to_waypoint",
    "broadcast_beacon",
}
DRONE_REQUIRED_STATES = {"patrolling"}
DRONE_REQUIRED_BEHAVIORS = {"select_waypoint", "move_to_waypoint", "broadcast_beacon"}


def validate_drone_agent_spec(spec: StateMachineAgentSchemaSpec) -> StateMachineAgentSchemaSpec:
    validate_known_behavior_names(spec, DRONE_KNOWN_BEHAVIOR_NAMES)
    missing_states = DRONE_REQUIRED_STATES - set(spec.states.keys())
    if missing_states:
        raise ValueError(
            f"Drone spec missing required states: {', '.join(sorted(missing_states))}"
        )
    present = {step.name for step in spec.states["patrolling"].behaviors}
    missing_behaviors = DRONE_REQUIRED_BEHAVIORS - present
    if missing_behaviors:
        raise ValueError(
            "Drone spec state 'patrolling' missing required behaviors: "
            + ", ".join(sorted(missing_behaviors))
        )
    return spec


def _effective_drone_spec(
    agent_spec: StateMachineAgentSchemaSpec | None,
) -> StateMachineAgentSchemaSpec:
    return validate_drone_agent_spec(agent_spec or DRONE_SCOUT_SPEC)


def build_initial_state(
    num_drones: int = 12,
    width: int = 40,
    height: int = 40,
    seed: int = 42,
    agent_spec: StateMachineAgentSchemaSpec | None = None,
) -> SimulationState:
    spec = _effective_drone_spec(agent_spec)
    center = Vector2(x=width / 2.0, y=height / 2.0)
    agents: list[AgentState] = []

    spacing = max(1.0, min(width, height) / (num_drones + 2))
    for idx in range(num_drones):
        x = 1.0 + (idx + 1) * spacing
        y = center.y
        agents.append(
            AgentState(
                id=f"drone-{idx}",
                position=Vector2(x=min(x, width - 1.0), y=y),
                velocity=Vector2(x=0.0, y=0.0),
                energy=1.0,
                carrying=0,
                state_label=spec.initial_state,
            )
        )

    return SimulationState(
        tick=0,
        agents=agents,
        food_sources=[],
        colony=Colony(id="base-1", position=center),
        obstacles=[
            TerrainObstacle(
                id="relay-pillar",
                kind="pillar",
                position=Vector2(x=max(1.0, center.x - 1.5), y=max(1.0, center.y - 1.5)),
                width=3.0,
                height=3.0,
            )
        ],
        zones=[
            WorldZone(
                id="patrol-ring",
                kind="patrol",
                position=Vector2(x=2.0, y=2.0),
                width=max(1.0, width - 4.0),
                height=max(1.0, height - 4.0),
                label="Patrol Loop",
            )
        ],
        signal_fields=[SignalField(kind="radio", width=width, height=height, decay=0.99, diffusion=0.05)],
        delivered_food=0,
        seed=seed,
    )

def _drone_index(agent_id: str) -> int:
    suffix = agent_id.rsplit("-", maxsplit=1)[-1]
    try:
        return int(suffix)
    except ValueError:
        return 0


def create_drone_behavior_runner(
    bounds: WorldBounds,
    signal_grid: SignalGrid,
    *,
    boundary_mode: BoundaryMode = "clamp",
    agent_spec: StateMachineAgentSchemaSpec | None = None,
):
    if boundary_mode not in {"clamp", "wrap"}:
        raise ValueError("boundary_mode must be 'clamp' or 'wrap'")
    spec = _effective_drone_spec(agent_spec)

    max_speed = spec.attributes.max_speed
    segment_ticks = int(
        behavior_params(
            spec,
            state_name="patrolling",
            behavior_name="select_waypoint",
        )["segment_ticks"]
    )
    beacon_amount = float(
        behavior_params(
            spec,
            state_name="patrolling",
            behavior_name="broadcast_beacon",
        )["amount"]
    )
    margin = 2.0
    waypoints = (
        Vector2(x=margin, y=margin),
        Vector2(x=bounds.width - margin, y=margin),
        Vector2(x=bounds.width - margin, y=bounds.height - margin),
        Vector2(x=margin, y=bounds.height - margin),
    )

    class DronePatrolBehavior(BehaviorProtocol):
        def sense(self, agent: AgentState, state: SimulationState) -> dict[str, object]:
            return {"agent": agent, "state": state}

        def decide(
            self,
            perception: dict[str, object],
            rng: random.Random,
        ) -> dict[str, object]:
            _ = rng
            agent = perception["agent"]
            state = perception["state"]
            if not isinstance(agent, AgentState) or not isinstance(state, SimulationState):
                raise TypeError("Invalid drone behavior perception payload")

            idx = _drone_index(agent.id)
            phase = ((state.tick // max(1, segment_ticks)) + idx) % len(waypoints)
            target = waypoints[phase]

            dx = target.x - agent.position.x
            dy = target.y - agent.position.y
            ux, uy = normalize_vector(dx, dy)

            next_agent = agent.model_copy(
                update={
                    "velocity": Vector2(x=ux * max_speed, y=uy * max_speed),
                    "state_label": "patrolling",
                }
            )
            return {"next_agent": next_agent}

        def act(
            self,
            agent: AgentState,
            decision: dict[str, object],
            state: SimulationState,
        ) -> AgentState:
            _ = (agent, state)
            next_agent = decision.get("next_agent")
            if not isinstance(next_agent, AgentState):
                raise TypeError("Invalid drone behavior decision payload")
            signal_grid.deposit(next_agent.position, beacon_amount)
            return apply_movement(next_agent, dt=1.0, bounds=bounds, mode=boundary_mode)

    registry = BehaviorRegistry()
    registry.register("drone_patrol", DronePatrolBehavior)
    behavior = registry.create("drone_patrol")

    def run(agent: AgentState, state: SimulationState, rng: random.Random) -> AgentState:
        perception = behavior.sense(agent, state)
        decision = behavior.decide(perception, rng)
        return behavior.act(agent, decision, state)

    return run
