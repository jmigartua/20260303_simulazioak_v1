from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from sim_framework.contracts.models import LoadedRun, RunManifest, SimulationState


@runtime_checkable
class RendererPort(Protocol):
    def render(self, snapshot: SimulationState) -> None:
        ...

    def capture_screenshot(self, path: str | Path) -> Path:
        ...


@runtime_checkable
class PersistencePort(Protocol):
    def save_run(self, manifest: RunManifest, snapshots: list[SimulationState]) -> str:
        ...

    def load_run(self, run_id: str) -> LoadedRun:
        ...


@runtime_checkable
class HistoryPort(Protocol):
    def snapshot(self, state: SimulationState, tick: int) -> None:
        ...

    def nearest_snapshot_before(self, tick: int) -> tuple[int, SimulationState] | None:
        ...

    def rewind(self, target_tick: int, current_state: SimulationState) -> SimulationState:
        ...
