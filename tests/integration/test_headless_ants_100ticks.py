from __future__ import annotations

from sim_framework.core.engine import SimulationEngine
from sim_framework.core.environment import SignalGrid
from sim_framework.core.physics import WorldBounds
from sim_framework.scenarios.ants_foraging import build_initial_state, create_ant_behavior_runner


def test_headless_ants_scout_release_cycle_runs_and_emits_signal() -> None:
    state = build_initial_state(num_ants=40, width=30, height=30, seed=42)
    initial_food_total = sum(source.amount for source in state.food_sources)
    bounds = WorldBounds(width=30.0, height=30.0)
    signal_grid = SignalGrid.from_config(state.signal_fields[0])

    engine = SimulationEngine(seed=state.seed)
    runner = create_ant_behavior_runner(bounds=bounds, signal_grid=signal_grid)

    saw_carrying = False
    for _ in range(120):
        state = engine.tick(state, runner)
        if any(agent.carrying > 0 for agent in state.agents):
            saw_carrying = True

    assert state.tick == 120
    assert len(state.agents) > 0
    assert saw_carrying
    assert signal_grid.total_signal() > 0.0
    assert state.delivered_food > 0
    assert state.food_discovered is True
    assert state.released_agents == len(state.agents)
    assert sum(source.amount for source in state.food_sources) < initial_food_total
    assert all(agent.state_label in {"searching", "carrying", "waiting"} for agent in state.agents)
