from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict

from sim_framework.core.engine import SimulationEngine


class RuntimeMode(str, Enum):
    INTERACTIVE = "interactive"
    HEADLESS = "headless"


class RuntimeConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    mode: RuntimeMode = RuntimeMode.INTERACTIVE
    emit_snapshot_events: bool | None = None

    def resolved_emit_snapshot_events(self) -> bool:
        if self.emit_snapshot_events is not None:
            return self.emit_snapshot_events
        return self.mode is RuntimeMode.INTERACTIVE


def create_engine(seed: int, runtime: RuntimeConfig | None = None) -> SimulationEngine:
    config = runtime or RuntimeConfig()
    return SimulationEngine(
        seed=seed,
        emit_snapshot_events=config.resolved_emit_snapshot_events(),
    )
