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
    amount: float = Field(ge=0.0)


class Colony(BaseModel):
    id: str = Field(min_length=1)
    position: Vector2


class TerrainObstacle(BaseModel):
    id: str = Field(min_length=1)
    kind: Literal["wall", "rock", "pillar"] = "wall"
    position: Vector2
    width: float = Field(gt=0.0)
    height: float = Field(gt=0.0)


class WorldZone(BaseModel):
    id: str = Field(min_length=1)
    kind: Literal["nest", "forage", "patrol", "corridor"] = "nest"
    position: Vector2
    width: float = Field(gt=0.0)
    height: float = Field(gt=0.0)
    label: str | None = None


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
    obstacles: list[TerrainObstacle] = Field(default_factory=list)
    zones: list[WorldZone] = Field(default_factory=list)
    signal_fields: list[SignalField] = Field(default_factory=list)
    delivered_food: int = Field(default=0, ge=0)
    food_discovered: bool = False
    released_agents: int = Field(default=4, ge=0)
    seed: int = Field(default=42)


class RunManifest(BaseModel):
    run_id: str = Field(min_length=1)
    scenario_name: str = Field(min_length=1)
    seed: int = Field(default=42)


class LoadedRun(BaseModel):
    manifest: RunManifest
    snapshots: list[SimulationState] = Field(default_factory=list)


class _StrictCommandModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PlayCommand(_StrictCommandModel):
    kind: Literal["play"] = "play"


class PauseCommand(_StrictCommandModel):
    kind: Literal["pause"] = "pause"


class StepCommand(_StrictCommandModel):
    kind: Literal["step"] = "step"
    steps: int = Field(default=1, ge=1)


class SeekCommand(_StrictCommandModel):
    kind: Literal["seek"] = "seek"
    tick: int = Field(ge=0)


class ResetCommand(_StrictCommandModel):
    kind: Literal["reset"] = "reset"


class SetSpeedCommand(_StrictCommandModel):
    kind: Literal["set_speed"] = "set_speed"
    speed_multiplier: float = Field(gt=0.0)


ControlCommand = (
    PlayCommand
    | PauseCommand
    | StepCommand
    | SeekCommand
    | ResetCommand
    | SetSpeedCommand
)


class SnapshotEvent(BaseModel):
    kind: Literal["snapshot"] = "snapshot"
    tick: int = Field(ge=0)
    state: SimulationState


class MetricEvent(BaseModel):
    kind: Literal["metric"] = "metric"
    tick: int = Field(ge=0)
    name: str = Field(min_length=1)
    value: float


class ErrorEvent(BaseModel):
    kind: Literal["error"] = "error"
    tick: int = Field(ge=0)
    message: str = Field(min_length=1)
    agent_id: str | None = None


class LifecycleEvent(BaseModel):
    kind: Literal["lifecycle"] = "lifecycle"
    status: Literal["started", "paused", "stopped", "reset"]
    tick: int = Field(default=0, ge=0)


SimulationEvent = SnapshotEvent | MetricEvent | ErrorEvent | LifecycleEvent
