from __future__ import annotations

from dataclasses import dataclass
from math import ceil, sqrt

from sim_framework.contracts.models import SignalField, Vector2


def _clamp(value: int, low: int, high: int) -> int:
    return max(low, min(value, high))


@dataclass
class SignalGrid:
    kind: str
    width: int
    height: int
    decay: float
    diffusion: float
    data: list[list[float]]

    @classmethod
    def from_config(cls, config: SignalField) -> "SignalGrid":
        grid = [[0.0 for _ in range(config.width)] for _ in range(config.height)]
        return cls(
            kind=config.kind,
            width=config.width,
            height=config.height,
            decay=config.decay,
            diffusion=config.diffusion,
            data=grid,
        )

    def _to_cell(self, position: Vector2) -> tuple[int, int]:
        x = _clamp(int(round(position.x)), 0, self.width - 1)
        y = _clamp(int(round(position.y)), 0, self.height - 1)
        return x, y

    def deposit(self, position: Vector2, amount: float) -> None:
        if amount <= 0.0:
            return
        x, y = self._to_cell(position)
        self.data[y][x] += amount

    def sample(self, position: Vector2) -> float:
        x, y = self._to_cell(position)
        return self.data[y][x]

    def sense_gradient(self, position: Vector2, radius: float) -> tuple[float, float] | None:
        if radius <= 0.0:
            raise ValueError("radius must be > 0")

        cx, cy = self._to_cell(position)
        center_value = self.data[cy][cx]

        cell_radius = int(ceil(radius))
        best_dx = 0
        best_dy = 0
        best_value = center_value
        best_dist = 0.0

        for dy in range(-cell_radius, cell_radius + 1):
            for dx in range(-cell_radius, cell_radius + 1):
                if dx == 0 and dy == 0:
                    continue

                dist = sqrt(dx * dx + dy * dy)
                if dist > radius:
                    continue

                nx = _clamp(cx + dx, 0, self.width - 1)
                ny = _clamp(cy + dy, 0, self.height - 1)
                value = self.data[ny][nx]

                # Prefer higher concentration. Tie-break by farther cell to reduce jitter.
                if (value > best_value) or (value == best_value and dist > best_dist):
                    best_value = value
                    best_dx = dx
                    best_dy = dy
                    best_dist = dist

        if best_value <= center_value:
            return None

        norm = sqrt(best_dx * best_dx + best_dy * best_dy)
        if norm == 0.0:
            return None
        return best_dx / norm, best_dy / norm

    def diffuse_step(self) -> None:
        next_data = [[0.0 for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                center = self.data[y][x]
                neighbors: list[float] = []

                if x > 0:
                    neighbors.append(self.data[y][x - 1])
                if x < self.width - 1:
                    neighbors.append(self.data[y][x + 1])
                if y > 0:
                    neighbors.append(self.data[y - 1][x])
                if y < self.height - 1:
                    neighbors.append(self.data[y + 1][x])

                if neighbors:
                    neighbor_avg = sum(neighbors) / len(neighbors)
                else:
                    neighbor_avg = center

                next_data[y][x] = center + self.diffusion * (neighbor_avg - center)

        self.data = next_data

    def decay_step(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.data[y][x] *= self.decay

    def total_signal(self) -> float:
        return sum(sum(row) for row in self.data)
