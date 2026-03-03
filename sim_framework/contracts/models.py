from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Vector2(BaseModel):
    model_config = ConfigDict(frozen=True)

    x: float
    y: float


class AgentState(BaseModel):
    id: str = Field(min_length=1)
    position: Vector2
    velocity: Vector2 = Field(default_factory=lambda: Vector2(x=0.0, y=0.0))
    energy: float = Field(default=1.0, ge=0.0)
    carrying: int = Field(default=0, ge=0)
    state_label: str = Field(default="searching", min_length=1)


class FoodSource(BaseModel):
    id: str = Field(min_length=1)
    position: Vector2
    amount: float = Field(gt=0.0)


class Colony(BaseModel):
    id: str = Field(min_length=1)
    position: Vector2


class SignalField(BaseModel):
    kind: Literal["pheromone", "radio", "thermal"] = "pheromone"
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    decay: float = Field(default=0.95, ge=0.0, le=1.0)
    diffusion: float = Field(default=0.1, ge=0.0, le=1.0)


class SimulationState(BaseModel):
    tick: int = Field(default=0, ge=0)
    agents: list[AgentState] = Field(default_factory=list)
    food_sources: list[FoodSource] = Field(default_factory=list)
    colony: Colony
    signal_fields: list[SignalField] = Field(default_factory=list)
    seed: int = Field(default=42)
