from __future__ import annotations

import pytest

from sim_framework.contracts.models import AgentState, Colony, SimulationState, Vector2
from sim_framework.core.history import SnapshotHistory


def _state(tick: int, x: float = 0.0) -> SimulationState:
    return SimulationState(
        tick=tick,
        agents=[AgentState(id="a1", position=Vector2(x=x, y=0.0))],
        food_sources=[],
        colony=Colony(id="c1", position=Vector2(x=0.0, y=0.0)),
        signal_fields=[],
        seed=42,
    )


def test_snapshot_buffer_maxlen_eviction() -> None:
    history = SnapshotHistory(max_snapshots=3)

    for tick in range(5):
        history.snapshot(_state(tick=tick, x=float(tick)), tick=tick)

    assert history.count() == 3
    assert history.last_tick() == 4

    nearest = history.nearest_snapshot_before(1)
    assert nearest is None


def test_snapshot_every_interval() -> None:
    history = SnapshotHistory(max_snapshots=10, snapshot_every=2)

    for tick in range(6):
        history.snapshot(_state(tick=tick), tick=tick)

    assert history.count() == 3
    assert history.last_tick() == 4


def test_nearest_snapshot_before_returns_closest() -> None:
    history = SnapshotHistory(max_snapshots=10)
    history.snapshot(_state(tick=0, x=0.0), tick=0)
    history.snapshot(_state(tick=5, x=5.0), tick=5)
    history.snapshot(_state(tick=10, x=10.0), tick=10)

    tick, state = history.nearest_snapshot_before(7) or (None, None)
    assert tick == 5
    assert state is not None
    assert state.tick == 5


def test_snapshot_storage_is_deep_copy() -> None:
    history = SnapshotHistory(max_snapshots=10)
    state = _state(tick=3, x=1.0)
    history.snapshot(state, tick=3)

    # mutate original state after snapshot; stored snapshot must not change
    state.agents[0].position = Vector2(x=99.0, y=0.0)

    _, snap = history.nearest_snapshot_before(3) or (None, None)
    assert snap is not None
    assert snap.agents[0].position.x == 1.0


def test_rewind_exact_tick_uses_snapshot() -> None:
    history = SnapshotHistory(max_snapshots=10)
    history.snapshot(_state(tick=4, x=4.0), tick=4)

    rewound = history.rewind(target_tick=4, current_state=_state(tick=9, x=9.0))
    assert rewound.tick == 4
    assert rewound.agents[0].position.x == 4.0


def test_rewind_non_snapshot_tick_requires_replay_fn() -> None:
    history = SnapshotHistory(max_snapshots=10)
    history.snapshot(_state(tick=4, x=4.0), tick=4)

    with pytest.raises(RuntimeError):
        history.rewind(target_tick=6, current_state=_state(tick=9, x=9.0))


def test_rewind_uses_replay_fn_when_needed() -> None:
    def replay(base_state: SimulationState, from_tick: int, to_tick: int) -> SimulationState:
        steps = to_tick - from_tick
        return base_state.model_copy(
            update={
                "tick": to_tick,
                "agents": [
                    base_state.agents[0].model_copy(
                        update={"position": Vector2(x=base_state.agents[0].position.x + steps, y=0.0)}
                    )
                ],
            }
        )

    history = SnapshotHistory(max_snapshots=10, replay_fn=replay)
    history.snapshot(_state(tick=4, x=4.0), tick=4)

    rewound = history.rewind(target_tick=6, current_state=_state(tick=9, x=9.0))
    assert rewound.tick == 6
    assert rewound.agents[0].position.x == 6.0


def test_invalid_constructor_arguments_fail() -> None:
    with pytest.raises(ValueError):
        SnapshotHistory(max_snapshots=0)

    with pytest.raises(ValueError):
        SnapshotHistory(snapshot_every=0)
