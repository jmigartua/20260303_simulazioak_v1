from __future__ import annotations

import json
from pathlib import Path

from sim_framework.contracts.models import SimulationState
from sim_framework.contracts.ports import RendererPort


class JsonStateRenderer(RendererPort):
    """Headless renderer that persists the latest rendered state as JSON."""

    def __init__(self) -> None:
        self._last_snapshot: SimulationState | None = None

    def render(self, snapshot: SimulationState) -> None:
        self._last_snapshot = snapshot.model_copy(deep=True)

    def capture_screenshot(self, path: str | Path) -> Path:
        if self._last_snapshot is None:
            raise RuntimeError("No rendered state available. Call render() before capture_screenshot().")

        out_path = Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "tick": self._last_snapshot.tick,
            "state": self._last_snapshot.model_dump(mode="json"),
        }
        out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return out_path
