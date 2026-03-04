from __future__ import annotations

from sim_framework.core.engine import SimulationEngine
from sim_framework.core.environment import SignalGrid
from sim_framework.core.physics import WorldBounds
from sim_framework.scenarios.drone_patrol import (
    build_drone_initial_state,
    create_drone_behavior_runner,
)


def test_headless_drone_100ticks_runs_and_patrols_in_bounds() -> None:
    state = build_drone_initial_state(num_drones=20, width=40, height=40, seed=42)
    bounds = WorldBounds(width=40.0, height=40.0)
    signal_grid = SignalGrid.from_config(state.signal_fields[0])

    engine = SimulationEngine(seed=state.seed)
    runner = create_drone_behavior_runner(bounds=bounds, signal_grid=signal_grid)

    for _ in range(100):
        state = engine.tick(state, runner)

    assert state.tick == 100
    assert len(state.agents) == 20
    assert all(agent.state_label == "patrolling" for agent in state.agents)
    assert all(0.0 <= agent.position.x <= bounds.width for agent in state.agents)
    assert all(0.0 <= agent.position.y <= bounds.height for agent in state.agents)
    assert signal_grid.total_signal() > 0.0

