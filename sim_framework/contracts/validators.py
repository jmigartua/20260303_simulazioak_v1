from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


FORBIDDEN_PAYLOAD_KEYS = {"code", "python", "script", "source"}
FORBIDDEN_STRING_TOKENS = (
    "lambda ",
    "import ",
    "exec(",
    "eval(",
    "__import__",
    "os.system",
    "subprocess.",
)


def _contains_executable_payload(value: Any) -> bool:
    if callable(value):
        return True

    if isinstance(value, str):
        lowered = value.strip().lower()
        return any(token in lowered for token in FORBIDDEN_STRING_TOKENS)

    if isinstance(value, dict):
        for key, nested in value.items():
            if str(key).strip().lower() in FORBIDDEN_PAYLOAD_KEYS:
                return True
            if _contains_executable_payload(nested):
                return True
        return False

    if isinstance(value, (list, tuple, set)):
        return any(_contains_executable_payload(item) for item in value)

    return False


class AgentAttributesSpec(BaseModel):
    max_speed: float = Field(gt=0.0)
    sensor_radius: float = Field(gt=0.0)
    carry_capacity: int = Field(ge=0)


class BehaviorStepSpec(BaseModel):
    name: str = Field(min_length=1)
    params: dict[str, Any] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def _name_format(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not normalized.replace("_", "").isalnum():
            raise ValueError("Behavior name must be alphanumeric/underscore")
        return normalized

    @field_validator("params")
    @classmethod
    def _forbid_executable_payloads(cls, value: dict[str, Any]) -> dict[str, Any]:
        if _contains_executable_payload(value):
            raise ValueError("Executable payloads are not allowed in behavior params")
        return value


class StateSpec(BaseModel):
    behaviors: list[BehaviorStepSpec] = Field(min_length=1)
    transitions: dict[str, str] = Field(default_factory=dict)


class AgentSchemaSpec(BaseModel):
    agent_type: str = Field(min_length=1)
    attributes: AgentAttributesSpec
    behavior_chain: list[BehaviorStepSpec] = Field(min_length=1)


class StateMachineAgentSchemaSpec(BaseModel):
    agent_type: str = Field(min_length=1)
    attributes: AgentAttributesSpec
    states: dict[str, StateSpec] = Field(min_length=1)
    initial_state: str = Field(min_length=1)

    @field_validator("initial_state")
    @classmethod
    def _initial_state_exists(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("states")
    @classmethod
    def _normalize_and_validate_states(cls, value: dict[str, StateSpec]) -> dict[str, StateSpec]:
        normalized = {name.strip().lower(): spec for name, spec in value.items()}
        if any(not key for key in normalized):
            raise ValueError("State names must be non-empty")
        return normalized

    @model_validator(mode="after")
    def _validate_state_graph(self) -> "StateMachineAgentSchemaSpec":
        if self.initial_state not in self.states:
            raise ValueError("initial_state must reference an existing state")

        state_names = set(self.states.keys())
        for state_name, spec in self.states.items():
            for condition, target_state in spec.transitions.items():
                if not condition.strip():
                    raise ValueError(f"State '{state_name}' has an empty transition condition")
                normalized_target = target_state.strip().lower()
                if normalized_target not in state_names:
                    raise ValueError(
                        f"State '{state_name}' transition points to unknown state '{target_state}'"
                    )
                spec.transitions[condition] = normalized_target
        return self


def validate_known_behavior_names(
    spec: AgentSchemaSpec | StateMachineAgentSchemaSpec, known_behavior_names: set[str]
) -> None:
    if isinstance(spec, AgentSchemaSpec):
        behavior_names = [step.name for step in spec.behavior_chain]
    else:
        behavior_names = [
            step.name
            for state_spec in spec.states.values()
            for step in state_spec.behaviors
        ]

    unknown = [
        name for name in behavior_names if name.strip().lower() not in known_behavior_names
    ]
    if unknown:
        formatted = ", ".join(sorted(set(unknown)))
        raise ValueError(f"Unknown behavior names: {formatted}")
