from __future__ import annotations

import pytest
from pydantic import ValidationError

from sim_framework.contracts.validators import (
    AgentSchemaSpec,
    StateMachineAgentSchemaSpec,
    validate_known_behavior_names,
)


def _valid_schema() -> AgentSchemaSpec:
    return AgentSchemaSpec(
        agent_type="ant_worker",
        attributes={
            "max_speed": 1.2,
            "sensor_radius": 8.0,
            "carry_capacity": 1,
        },
        behavior_chain=[
            {"name": "search_food", "params": {"wander_sigma": 0.4}},
            {"name": "move_to_target", "params": {"arrival_radius": 0.8}},
        ],
    )


def test_valid_schema_passes() -> None:
    spec = _valid_schema()
    assert spec.agent_type == "ant_worker"
    assert len(spec.behavior_chain) == 2


def test_attribute_ranges_are_validated() -> None:
    with pytest.raises(ValidationError):
        AgentSchemaSpec(
            agent_type="ant_worker",
            attributes={
                "max_speed": 0.0,
                "sensor_radius": 8.0,
                "carry_capacity": 1,
            },
            behavior_chain=[{"name": "search_food", "params": {}}],
        )

    with pytest.raises(ValidationError):
        AgentSchemaSpec(
            agent_type="ant_worker",
            attributes={
                "max_speed": 1.0,
                "sensor_radius": -1.0,
                "carry_capacity": 1,
            },
            behavior_chain=[{"name": "search_food", "params": {}}],
        )


def test_unknown_behavior_names_are_rejected() -> None:
    spec = _valid_schema()

    with pytest.raises(ValueError):
        validate_known_behavior_names(spec, {"search_food"})


def test_known_behavior_names_pass() -> None:
    spec = _valid_schema()
    validate_known_behavior_names(spec, {"search_food", "move_to_target"})


def test_executable_payload_is_rejected() -> None:
    with pytest.raises(ValidationError):
        AgentSchemaSpec(
            agent_type="ant_worker",
            attributes={
                "max_speed": 1.0,
                "sensor_radius": 8.0,
                "carry_capacity": 1,
            },
            behavior_chain=[
                {
                    "name": "search_food",
                    "params": {"script": "import os; os.system('rm -rf /')"},
                }
            ],
        )


def test_state_machine_schema_validates_and_known_behaviors_pass() -> None:
    spec = StateMachineAgentSchemaSpec(
        agent_type="ant_worker",
        attributes={
            "max_speed": 1.0,
            "sensor_radius": 4.0,
            "carry_capacity": 1,
        },
        states={
            "searching": {
                "behaviors": [
                    {"name": "sense_pheromone", "params": {}},
                    {"name": "check_food", "params": {}},
                ],
                "transitions": {"has_food": "carrying"},
            },
            "carrying": {
                "behaviors": [
                    {"name": "deposit_pheromone", "params": {"amount": 1.0}},
                    {"name": "drop_food", "params": {}},
                ],
                "transitions": {"food_dropped": "searching"},
            },
        },
        initial_state="searching",
    )
    validate_known_behavior_names(
        spec, {"sense_pheromone", "check_food", "deposit_pheromone", "drop_food"}
    )


def test_state_machine_schema_rejects_bad_transitions() -> None:
    with pytest.raises(ValidationError):
        StateMachineAgentSchemaSpec(
            agent_type="ant_worker",
            attributes={
                "max_speed": 1.0,
                "sensor_radius": 4.0,
                "carry_capacity": 1,
            },
            states={
                "searching": {
                    "behaviors": [{"name": "sense_pheromone", "params": {}}],
                    "transitions": {"has_food": "missing_state"},
                }
            },
            initial_state="searching",
        )

    with pytest.raises(ValidationError):
        AgentSchemaSpec(
            agent_type="ant_worker",
            attributes={
                "max_speed": 1.0,
                "sensor_radius": 8.0,
                "carry_capacity": 1,
            },
            behavior_chain=[
                {
                    "name": "search_food",
                    "params": {"expression": "eval('2+2')"},
                }
            ],
        )
