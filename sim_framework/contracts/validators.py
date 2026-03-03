from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


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


class AgentSchemaSpec(BaseModel):
    agent_type: str = Field(min_length=1)
    attributes: AgentAttributesSpec
    behavior_chain: list[BehaviorStepSpec] = Field(min_length=1)


def validate_known_behavior_names(
    spec: AgentSchemaSpec, known_behavior_names: set[str]
) -> None:
    unknown = [
        step.name
        for step in spec.behavior_chain
        if step.name.strip().lower() not in known_behavior_names
    ]
    if unknown:
        formatted = ", ".join(sorted(set(unknown)))
        raise ValueError(f"Unknown behavior names: {formatted}")

