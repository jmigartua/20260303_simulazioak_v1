from __future__ import annotations

from typing import Any

from sim_framework.scenarios.ants_foraging import (
    build_initial_state as build_ants_initial_state,
    create_ant_behavior_runner,
)


SCENARIO_REGISTRY: dict[str, dict[str, Any]] = {
    "ants_foraging": {
        "build_initial_state": build_ants_initial_state,
        "create_behavior_runner": create_ant_behavior_runner,
    }
}


def list_scenarios() -> list[str]:
    return sorted(SCENARIO_REGISTRY.keys())


def get_scenario(name: str) -> dict[str, Any]:
    key = name.strip().lower()
    if key not in SCENARIO_REGISTRY:
        raise KeyError(f"Unknown scenario '{name}'")
    return SCENARIO_REGISTRY[key]
