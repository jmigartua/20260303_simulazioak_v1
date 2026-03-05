from __future__ import annotations

import inspect
from typing import Any


def build_state_for_scenario(
    build_fn,
    *,
    scenario_name: str,
    agents: int,
    width: int,
    height: int,
    seed: int,
    agent_spec: object | None = None,
):
    signature = inspect.signature(build_fn)
    kwargs: dict[str, Any] = {"width": width, "height": height, "seed": seed}

    if "num_ants" in signature.parameters:
        kwargs["num_ants"] = agents
    elif "num_drones" in signature.parameters:
        kwargs["num_drones"] = agents
    elif "num_agents" in signature.parameters:
        kwargs["num_agents"] = agents
    else:
        raise ValueError(
            f"Scenario '{scenario_name}' does not expose a supported agent-count parameter "
            "(expected one of: num_ants, num_drones, num_agents)."
        )

    if "agent_spec" in signature.parameters and agent_spec is not None:
        kwargs["agent_spec"] = agent_spec
    return build_fn(**kwargs)


def create_runner_for_scenario(
    runner_factory,
    *,
    bounds,
    signal_grid,
    boundary_mode: str,
    agent_spec: object | None = None,
):
    signature = inspect.signature(runner_factory)
    kwargs = {"bounds": bounds, "signal_grid": signal_grid}
    if "boundary_mode" in signature.parameters:
        kwargs["boundary_mode"] = boundary_mode
    if "agent_spec" in signature.parameters and agent_spec is not None:
        kwargs["agent_spec"] = agent_spec
    return runner_factory(**kwargs)
