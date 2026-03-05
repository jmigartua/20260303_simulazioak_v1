from __future__ import annotations

from sim_framework.contracts.validators import StateMachineAgentSchemaSpec


def behavior_params(
    spec: StateMachineAgentSchemaSpec,
    *,
    state_name: str,
    behavior_name: str,
) -> dict[str, object]:
    for step in spec.states[state_name].behaviors:
        if step.name == behavior_name:
            return step.params
    raise ValueError(f"Behavior '{behavior_name}' not found in state '{state_name}'")
