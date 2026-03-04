from __future__ import annotations

from typing import Any

from sim_framework.scenarios.ants_foraging import (
    build_initial_state as build_ants_initial_state,
    create_ant_behavior_runner,
    validate_ant_agent_spec,
)
from sim_framework.scenarios.drone_patrol import (
    build_drone_initial_state,
    create_drone_behavior_runner,
    validate_drone_agent_spec,
)


SCENARIO_REGISTRY: dict[str, dict[str, Any]] = {
    "ants_foraging": {
        "build_initial_state": build_ants_initial_state,
        "create_behavior_runner": create_ant_behavior_runner,
        "validate_agent_spec": validate_ant_agent_spec,
    },
    "drone_patrol": {
        "build_initial_state": build_drone_initial_state,
        "create_behavior_runner": create_drone_behavior_runner,
        "validate_agent_spec": validate_drone_agent_spec,
    }
}


def list_scenarios() -> list[str]:
    return sorted(SCENARIO_REGISTRY.keys())


def get_scenario(name: str) -> dict[str, Any]:
    key = name.strip().lower()
    if key not in SCENARIO_REGISTRY:
        raise KeyError(f"Unknown scenario '{name}'")
    return SCENARIO_REGISTRY[key]
