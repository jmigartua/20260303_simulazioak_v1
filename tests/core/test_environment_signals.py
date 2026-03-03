from __future__ import annotations

import pytest

from sim_framework.contracts.models import SignalField, Vector2
from sim_framework.core.environment import SignalGrid


def _grid() -> SignalGrid:
    return SignalGrid.from_config(
        SignalField(kind="pheromone", width=5, height=5, decay=0.9, diffusion=0.2)
    )


def test_grid_initializes_with_zeros() -> None:
    grid = _grid()

    assert grid.width == 5
    assert grid.height == 5
    assert grid.total_signal() == 0.0


def test_deposit_and_sample() -> None:
    grid = _grid()
    pos = Vector2(x=2.0, y=2.0)

    grid.deposit(pos, 4.0)

    assert grid.sample(pos) == pytest.approx(4.0)


def test_deposit_clamps_out_of_bounds_positions() -> None:
    grid = _grid()

    grid.deposit(Vector2(x=-100.0, y=-100.0), 1.0)
    grid.deposit(Vector2(x=999.0, y=999.0), 2.0)

    assert grid.sample(Vector2(x=0.0, y=0.0)) == pytest.approx(1.0)
    assert grid.sample(Vector2(x=4.0, y=4.0)) == pytest.approx(2.0)


def test_diffusion_spreads_signal() -> None:
    grid = _grid()
    center = Vector2(x=2.0, y=2.0)

    grid.deposit(center, 10.0)
    before_center = grid.sample(center)

    grid.diffuse_step()

    after_center = grid.sample(center)
    north = grid.sample(Vector2(x=2.0, y=1.0))
    south = grid.sample(Vector2(x=2.0, y=3.0))
    east = grid.sample(Vector2(x=3.0, y=2.0))
    west = grid.sample(Vector2(x=1.0, y=2.0))

    assert after_center < before_center
    assert north > 0.0
    assert south > 0.0
    assert east > 0.0
    assert west > 0.0


def test_decay_reduces_signal_values() -> None:
    grid = _grid()
    pos = Vector2(x=2.0, y=2.0)

    grid.deposit(pos, 10.0)
    total_before = grid.total_signal()

    grid.decay_step()

    assert grid.sample(pos) == pytest.approx(9.0)
    assert grid.total_signal() < total_before


def test_non_positive_deposit_is_ignored() -> None:
    grid = _grid()
    pos = Vector2(x=1.0, y=1.0)

    grid.deposit(pos, 0.0)
    grid.deposit(pos, -1.0)

    assert grid.sample(pos) == pytest.approx(0.0)
