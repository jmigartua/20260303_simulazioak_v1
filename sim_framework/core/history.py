from __future__ import annotations

from collections import deque
from collections.abc import Callable

from sim_framework.contracts.models import SimulationState

ReplayFn = Callable[[SimulationState, int, int], SimulationState]


class SnapshotHistory:
    def __init__(
        self,
        max_snapshots: int = 1000,
        snapshot_every: int = 1,
        replay_fn: ReplayFn | None = None,
    ) -> None:
        if max_snapshots <= 0:
            raise ValueError("max_snapshots must be > 0")
        if snapshot_every <= 0:
            raise ValueError("snapshot_every must be > 0")

        self._snapshots: deque[tuple[int, SimulationState]] = deque(maxlen=max_snapshots)
        self.snapshot_every = snapshot_every
        self._replay_fn = replay_fn

    def snapshot(self, state: SimulationState, tick: int) -> None:
        if tick < 0:
            raise ValueError("tick must be >= 0")
        if tick % self.snapshot_every != 0:
            return
        self._snapshots.append((tick, state.model_copy(deep=True)))

    def nearest_snapshot_before(self, tick: int) -> tuple[int, SimulationState] | None:
        if tick < 0:
            raise ValueError("tick must be >= 0")

        for saved_tick, saved_state in reversed(self._snapshots):
            if saved_tick <= tick:
                return saved_tick, saved_state.model_copy(deep=True)
        return None

    def rewind(self, target_tick: int, current_state: SimulationState) -> SimulationState:
        if target_tick < 0:
            raise ValueError("target_tick must be >= 0")

        nearest = self.nearest_snapshot_before(target_tick)
        if nearest is None:
            return current_state.model_copy(deep=True)

        snapshot_tick, snapshot_state = nearest
        if snapshot_tick == target_tick:
            return snapshot_state

        if self._replay_fn is None:
            raise RuntimeError(
                "replay_fn is required to rewind to non-snapshot ticks"
            )

        replayed = self._replay_fn(snapshot_state, snapshot_tick, target_tick)
        return replayed.model_copy(deep=True)

    def count(self) -> int:
        return len(self._snapshots)

    def last_tick(self) -> int | None:
        if not self._snapshots:
            return None
        return self._snapshots[-1][0]
