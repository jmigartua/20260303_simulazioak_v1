from __future__ import annotations

import random
from math import sqrt

from sim_framework.contracts.behaviors import BehaviorProtocol, BehaviorRegistry
from sim_framework.contracts.models import (
    AgentState,
    Colony,
    FoodSource,
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
    colony_pos = Vector2(x=width * 0.1, y=height * 0.5)
    initial_scout_count = min(4, num_ants)

    agents: list[AgentState] = []
    for i in range(num_ants):
        jitter_x = rng.uniform(-0.4, 0.4)
        jitter_y = rng.uniform(-0.4, 0.4)
        is_scout = i < initial_scout_count
        agents.append(
            AgentState(
                id=f"ant-{i}",
                position=Vector2(x=colony_pos.x + jitter_x, y=colony_pos.y + jitter_y),
                velocity=(
                    Vector2(x=rng.uniform(0.1, 0.5), y=rng.uniform(-0.25, 0.25))
                    if is_scout
                    else Vector2(x=0.0, y=0.0)
                ),
                energy=1.0,
                carrying=0,
                state_label=spec.initial_state if is_scout else "waiting",
            )
        )

    # Mirror the original default arena: colony on the left, food on the far right.
    food_sources = [
        FoodSource(id="food-main", position=Vector2(x=width * 0.875, y=height * 0.5), amount=50.0),
    ]

    obstacles = [
        TerrainObstacle(
            id="wall-1",
            kind="wall",
            position=Vector2(x=width * (10.0 / 30.0), y=height * (2.0 / 30.0)),
            width=width * (1.2 / 30.0),
            height=height * (9.0 / 30.0),
        ),
        TerrainObstacle(
            id="wall-2",
            kind="wall",
            position=Vector2(x=width * (10.0 / 30.0), y=height * (19.0 / 30.0)),
            width=width * (1.2 / 30.0),
            height=height * (9.0 / 30.0),
        ),
        TerrainObstacle(
            id="wall-3",
            kind="wall",
            position=Vector2(x=width * (18.0 / 30.0), y=height * (4.0 / 30.0)),
            width=width * (1.2 / 30.0),
            height=height * (8.0 / 30.0),
        ),
        TerrainObstacle(
            id="wall-4",
            kind="wall",
            position=Vector2(x=width * (18.0 / 30.0), y=height * (18.0 / 30.0)),
            width=width * (1.2 / 30.0),
            height=height * (8.0 / 30.0),
        ),
    ]
    zones = [
        WorldZone(
            id="nest-core",
            kind="nest",
            position=Vector2(
                x=max(0.0, colony_pos.x - (width * 0.05)),
                y=max(0.0, colony_pos.y - (height * 0.08)),
            ),
            width=width * 0.1,
            height=height * 0.16,
            label="Colony",
        ),
        WorldZone(
            id="forage-main",
            kind="forage",
            position=Vector2(x=width * 0.84, y=height * 0.43),
            width=width * 0.07,
            height=height * 0.14,
            label="Food",
        ),
    ]

    return SimulationState(
        tick=0,
        agents=agents,
        food_sources=food_sources,
        colony=Colony(id="colony-1", position=colony_pos),
        obstacles=obstacles,
        zones=zones,
        signal_fields=[SignalField(kind="pheromone", width=width, height=height, decay=0.98, diffusion=0.2)],
        delivered_food=0,
        food_discovered=False,
        released_agents=initial_scout_count,
        seed=seed,
    )


def _dist(a: Vector2, b: Vector2) -> float:
    dx = a.x - b.x
    dy = a.y - b.y
    return sqrt(dx * dx + dy * dy)


def _agent_index(agent_id: str) -> int:
    suffix = agent_id.rsplit("-", maxsplit=1)[-1]
    try:
        return int(suffix)
    except ValueError:
        return 0


def _obstacle_bounds(obstacle: TerrainObstacle) -> tuple[float, float, float, float]:
    min_x = obstacle.position.x
    min_y = obstacle.position.y
    return min_x, min_y, min_x + obstacle.width, min_y + obstacle.height


def _inside_rect(x: float, y: float, rect: tuple[float, float, float, float]) -> bool:
    min_x, min_y, max_x, max_y = rect
    return min_x <= x <= max_x and min_y <= y <= max_y


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _rect_avoidance(
    *,
    point: Vector2,
    rect: tuple[float, float, float, float],
    radius: float,
    strength: float,
    target: tuple[float, float] | None,
) -> tuple[float, float]:
    min_x, min_y, max_x, max_y = rect
    closest_x = _clamp(point.x, min_x, max_x)
    closest_y = _clamp(point.y, min_y, max_y)
    dx = point.x - closest_x
    dy = point.y - closest_y
    dist = sqrt(dx * dx + dy * dy)
    if dist >= radius:
        return 0.0, 0.0

    if dist > 0.01:
        repel = strength * (1.0 - (dist / radius))
        nx = dx / dist
        ny = dy / dist
        fx = nx * repel
        fy = ny * repel
    else:
        center_x = (min_x + max_x) / 2.0
        center_y = (min_y + max_y) / 2.0
        nx, ny = normalize_vector(point.x - center_x, point.y - center_y)
        if nx == 0.0 and ny == 0.0:
            nx, ny = 1.0, 0.0
        fx = nx * strength
        fy = ny * strength
        dist = 0.0

    if target is not None:
        tx, ty = target
        desired_x = tx - point.x
        desired_y = ty - point.y
        left_tangent = (-ny, nx)
        right_tangent = (ny, -nx)
        if (left_tangent[0] * desired_x) + (left_tangent[1] * desired_y) >= (
            (right_tangent[0] * desired_x) + (right_tangent[1] * desired_y)
        ):
            tangent_x, tangent_y = left_tangent
        else:
            tangent_x, tangent_y = right_tangent
        tangent_gain = 0.8 * (1.0 - (dist / radius if radius > 0 else 0.0))
        fx += tangent_x * strength * tangent_gain
        fy += tangent_y * strength * tangent_gain

    return fx, fy


def _resolve_static_collision(
    previous: AgentState,
    candidate: AgentState,
    *,
    bounds: WorldBounds,
    obstacles: list[TerrainObstacle],
    radius: float,
) -> AgentState:
    x = _clamp(candidate.position.x, radius, bounds.width - radius)
    y = _clamp(candidate.position.y, radius, bounds.height - radius)
    vx = candidate.velocity.x
    vy = candidate.velocity.y

    for obstacle in obstacles:
        min_x, min_y, max_x, max_y = _obstacle_bounds(obstacle)
        expanded = (min_x - radius, min_y - radius, max_x + radius, max_y + radius)
        if not _inside_rect(x, y, expanded):
            continue

        prev_x = previous.position.x
        prev_y = previous.position.y
        candidates: list[tuple[float, str]] = []
        if prev_x <= min_x - radius:
            candidates.append((abs(x - (min_x - radius)), "left"))
        if prev_x >= max_x + radius:
            candidates.append((abs((max_x + radius) - x), "right"))
        if prev_y <= min_y - radius:
            candidates.append((abs(y - (min_y - radius)), "top"))
        if prev_y >= max_y + radius:
            candidates.append((abs((max_y + radius) - y), "bottom"))
        if not candidates:
            candidates = [
                (abs(x - (min_x - radius)), "left"),
                (abs((max_x + radius) - x), "right"),
                (abs(y - (min_y - radius)), "top"),
                (abs((max_y + radius) - y), "bottom"),
            ]

        _, side = min(candidates, key=lambda item: item[0])
        if side == "left":
            x = min_x - radius
            vx = min(0.0, vx)
        elif side == "right":
            x = max_x + radius
            vx = max(0.0, vx)
        elif side == "top":
            y = min_y - radius
            vy = min(0.0, vy)
        else:
            y = max_y + radius
            vy = max(0.0, vy)

    return candidate.model_copy(
        update={"position": Vector2(x=x, y=y), "velocity": Vector2(x=vx, y=vy)}
    )


def _segment_intersects_rect(
    start: Vector2,
    end: Vector2,
    rect: tuple[float, float, float, float],
) -> bool:
    min_x, min_y, max_x, max_y = rect
    if _inside_rect(start.x, start.y, rect) or _inside_rect(end.x, end.y, rect):
        return True

    dx = end.x - start.x
    dy = end.y - start.y
    t0 = 0.0
    t1 = 1.0
    for p, q in (
        (-dx, start.x - min_x),
        (dx, max_x - start.x),
        (-dy, start.y - min_y),
        (dy, max_y - start.y),
    ):
        if p == 0.0:
            if q < 0.0:
                return False
            continue
        t = q / p
        if p < 0.0:
            if t > t1:
                return False
            t0 = max(t0, t)
        else:
            if t < t0:
                return False
            t1 = min(t1, t)
    return True


def _blocking_obstacle(
    start: Vector2,
    end: Vector2,
    obstacles: list[TerrainObstacle],
    radius: float,
) -> TerrainObstacle | None:
    blockers: list[tuple[float, TerrainObstacle]] = []
    for obstacle in obstacles:
        min_x, min_y, max_x, max_y = _obstacle_bounds(obstacle)
        expanded = (min_x - radius, min_y - radius, max_x + radius, max_y + radius)
        if _segment_intersects_rect(start, end, expanded):
            center_x = (min_x + max_x) / 2.0
            center_y = (min_y + max_y) / 2.0
            blockers.append((_dist(start, Vector2(x=center_x, y=center_y)), obstacle))
    if not blockers:
        return None
    blockers.sort(key=lambda item: item[0])
    return blockers[0][1]


def _detour_waypoint(
    start: Vector2,
    target: Vector2,
    obstacle: TerrainObstacle,
    radius: float,
) -> Vector2:
    min_x, min_y, max_x, max_y = _obstacle_bounds(obstacle)
    if target.x < min_x:
        waypoints = [
            Vector2(x=min_x - radius, y=min_y - radius),
            Vector2(x=min_x - radius, y=max_y + radius),
        ]
    elif target.x > max_x:
        waypoints = [
            Vector2(x=max_x + radius, y=min_y - radius),
            Vector2(x=max_x + radius, y=max_y + radius),
        ]
    elif target.y < min_y:
        waypoints = [
            Vector2(x=min_x - radius, y=min_y - radius),
            Vector2(x=max_x + radius, y=min_y - radius),
        ]
    else:
        waypoints = [
            Vector2(x=min_x - radius, y=max_y + radius),
            Vector2(x=max_x + radius, y=max_y + radius),
        ]
    return min(
        waypoints,
        key=lambda waypoint: _dist(start, waypoint) + _dist(waypoint, target),
    )

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
    explore_bias_weight = 0.85
    gradient_follow_weight = 1.1
    wander_weight = 0.55
    neighbor_radius = 1.5
    avoid_weight = 0.35
    wall_avoid_radius = max(1.2, sensor_radius * 0.4)
    wall_avoid_force = 1.0
    outbound_weight = 0.9
    inertia_weight = 0.8
    agent_radius = 0.45
    exploration_trail_amount = 0.06
    scout_lane_offsets = (-0.2, -0.05, 0.05, 0.2)
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

    def _static_avoidance(
        agent: AgentState,
        state: SimulationState,
        *,
        target: tuple[float, float] | None,
    ) -> tuple[float, float]:
        px = agent.position.x
        py = agent.position.y
        fx = 0.0
        fy = 0.0

        if px < wall_avoid_radius:
            fx += wall_avoid_force * (1.0 - (px / wall_avoid_radius))
        if px > bounds.width - wall_avoid_radius:
            fx -= wall_avoid_force * (1.0 - ((bounds.width - px) / wall_avoid_radius))
        if py < wall_avoid_radius:
            fy += wall_avoid_force * (1.0 - (py / wall_avoid_radius))
        if py > bounds.height - wall_avoid_radius:
            fy -= wall_avoid_force * (1.0 - ((bounds.height - py) / wall_avoid_radius))

        for obstacle in state.obstacles:
            rx, ry = _rect_avoidance(
                point=agent.position,
                rect=_obstacle_bounds(obstacle),
                radius=wall_avoid_radius,
                strength=wall_avoid_force,
                target=target,
            )
            fx += rx
            fy += ry

        return fx, fy

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
            agent_idx = _agent_index(agent.id)

            if label == "waiting":
                if agent_idx < state.released_agents:
                    label = "searching"
                else:
                    next_agent = agent.model_copy(
                        update={
                            "velocity": Vector2(x=0.0, y=0.0),
                            "state_label": "waiting",
                        }
                    )
                    return {"next_agent": next_agent}

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
                target = state.colony.position
                blocking = _blocking_obstacle(agent.position, target, state.obstacles, agent_radius)
                if blocking is not None:
                    target = _detour_waypoint(agent.position, target, blocking, agent_radius)
                dx = target.x - agent.position.x
                dy = target.y - agent.position.y

                if (not picked_this_tick) and _dist(agent.position, state.colony.position) <= float(drop_radius):
                    carrying = 0
                    label = "searching"
                    state.delivered_food += 1
                    if not state.food_discovered:
                        state.food_discovered = True
                        state.released_agents = len(state.agents)
            else:
                signal_grid.deposit(agent.position, exploration_trail_amount)
                direction = signal_grid.sense_gradient(agent.position, sensor_radius)
                prev_dx, prev_dy = normalize_vector(agent.velocity.x, agent.velocity.y)
                if prev_dx == 0.0 and prev_dy == 0.0:
                    prev_dx, prev_dy = normalize_vector(1.0, rng.uniform(-0.4, 0.4))

                if (not state.food_discovered) and agent_idx < len(scout_lane_offsets):
                    outbound_dx, outbound_dy = normalize_vector(1.0, scout_lane_offsets[agent_idx])
                    outbound_mix = 1.75
                    wander_mix = 0.12
                    inertia_mix = 1.0
                else:
                    outbound_dx, outbound_dy = normalize_vector(
                        1.0,
                        (_agent_index(agent.id) % 7 - 3) * 0.2,
                    )
                    outbound_mix = outbound_weight
                    wander_mix = wander_weight
                    inertia_mix = inertia_weight
                grad_dx, grad_dy = direction or (0.0, 0.0)
                rand_dx, rand_dy = normalize_vector(rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0))
                colony_dist = _dist(agent.position, state.colony.position)
                outbound_multiplier = explore_bias_weight if colony_dist < sensor_radius * 2.0 else 0.35
                dx = (
                    (outbound_dx * outbound_mix * outbound_multiplier)
                    + (prev_dx * inertia_mix)
                    + (grad_dx * gradient_follow_weight)
                    + (rand_dx * wander_mix)
                )
                dy = (
                    (outbound_dy * outbound_mix * outbound_multiplier)
                    + (prev_dy * inertia_mix)
                    + (grad_dy * gradient_follow_weight)
                    + (rand_dy * wander_mix)
                )

            avoid_dx, avoid_dy = _neighbor_avoidance(agent, state)
            target = (state.colony.position.x, state.colony.position.y) if label == "carrying" else None
            static_dx, static_dy = _static_avoidance(agent, state, target=target)
            dx += avoid_dx * avoid_weight
            dy += avoid_dy * avoid_weight
            dx += static_dx
            dy += static_dy

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
            next_agent = decision.get("next_agent")
            if not isinstance(next_agent, AgentState):
                raise TypeError("Invalid ant behavior decision payload")
            moved = apply_movement(next_agent, dt=1.0, bounds=bounds, mode=boundary_mode)
            return _resolve_static_collision(
                agent,
                moved,
                bounds=bounds,
                obstacles=state.obstacles,
                radius=agent_radius,
            )

    registry = BehaviorRegistry()
    registry.register("ant_state_machine", AntStateMachineBehavior)
    behavior = registry.create("ant_state_machine")

    def run(agent: AgentState, state: SimulationState, rng: random.Random) -> AgentState:
        perception = behavior.sense(agent, state)
        decision = behavior.decide(perception, rng)
        return behavior.act(agent, decision, state)

    return run
