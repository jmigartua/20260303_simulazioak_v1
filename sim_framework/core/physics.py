from __future__ import annotations

from dataclasses import dataclass, field
from math import ceil, floor, sqrt
from typing import Literal

from sim_framework.contracts.models import AgentState, Vector2

BoundaryMode = Literal["clamp", "wrap"]


@dataclass(frozen=True)
class WorldBounds:
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("WorldBounds width/height must be > 0")


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(value, high))


def _wrap(value: float, modulus: float) -> float:
    return value % modulus


def normalize_vector(dx: float, dy: float) -> tuple[float, float]:
    mag = sqrt(dx * dx + dy * dy)
    if mag == 0.0:
        return 0.0, 0.0
    return dx / mag, dy / mag


def apply_movement(
    agent: AgentState,
    dt: float,
    bounds: WorldBounds,
    mode: BoundaryMode = "clamp",
) -> AgentState:
    if dt <= 0:
        raise ValueError("dt must be > 0")

    next_x = agent.position.x + agent.velocity.x * dt
    next_y = agent.position.y + agent.velocity.y * dt

    if mode == "clamp":
        next_x = _clamp(next_x, 0.0, bounds.width)
        next_y = _clamp(next_y, 0.0, bounds.height)
    elif mode == "wrap":
        next_x = _wrap(next_x, bounds.width)
        next_y = _wrap(next_y, bounds.height)
    else:
        raise ValueError(f"Unknown boundary mode: {mode}")

    return agent.model_copy(update={"position": Vector2(x=next_x, y=next_y)})


@dataclass
class SpatialHash:
    cell_size: float
    cells: dict[tuple[int, int], list[AgentState]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.cell_size <= 0:
            raise ValueError("cell_size must be > 0")

    def cell_for(self, position: Vector2) -> tuple[int, int]:
        return (int(floor(position.x / self.cell_size)), int(floor(position.y / self.cell_size)))

    def clear(self) -> None:
        self.cells.clear()

    def insert(self, agent: AgentState) -> None:
        cell = self.cell_for(agent.position)
        self.cells.setdefault(cell, []).append(agent)

    def build(self, agents: list[AgentState]) -> None:
        self.clear()
        for agent in agents:
            self.insert(agent)

    def query_cell(self, cell: tuple[int, int]) -> list[AgentState]:
        return list(self.cells.get(cell, []))

    def query_radius(self, center: Vector2, radius: float) -> list[AgentState]:
        if radius < 0:
            raise ValueError("radius must be >= 0")

        center_cell = self.cell_for(center)
        # ceil(radius / cell_size) is the minimal safe search ring.
        # The previous `int(...)+1` over-scanned when radius was an exact multiple.
        cell_radius = ceil(radius / self.cell_size)
        radius_sq = radius * radius

        result: list[AgentState] = []
        cells = self.cells
        cx, cy = center_cell
        center_x = center.x
        center_y = center.y
        for dx in range(-cell_radius, cell_radius + 1):
            for dy in range(-cell_radius, cell_radius + 1):
                cell = (cx + dx, cy + dy)
                for agent in cells.get(cell, []):
                    px = agent.position.x - center_x
                    py = agent.position.y - center_y
                    if (px * px + py * py) <= radius_sq:
                        result.append(agent)
        return result
