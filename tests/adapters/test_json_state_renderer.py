from __future__ import annotations

import json
from pathlib import Path

import pytest

from sim_framework.adapters.web import JsonStateRenderer
from sim_framework.contracts.models import AgentState, Colony, SimulationState, Vector2
from sim_framework.contracts.ports import RendererPort


def _state(tick: int = 0) -> SimulationState:
    return SimulationState(
        tick=tick,
        agents=[AgentState(id="a1", position=Vector2(x=1.0, y=2.0))],
        food_sources=[],
        colony=Colony(id="c1", position=Vector2(x=3.0, y=4.0)),
        signal_fields=[],
        seed=42,
    )


def test_json_state_renderer_conforms_to_renderer_port() -> None:
    renderer = JsonStateRenderer()
    assert isinstance(renderer, RendererPort)


def test_capture_requires_render_before_screenshot(tmp_path: Path) -> None:
    renderer = JsonStateRenderer()
    with pytest.raises(RuntimeError, match="Call render\\(\\) before capture_screenshot\\(\\)"):
        renderer.capture_screenshot(tmp_path / "capture.json")


def test_capture_screenshot_writes_latest_rendered_state(tmp_path: Path) -> None:
    renderer = JsonStateRenderer()
    renderer.render(_state(tick=3))

    out_path = renderer.capture_screenshot(tmp_path / "capture.json")
    assert out_path == tmp_path / "capture.json"
    assert out_path.exists()

    payload = json.loads(out_path.read_text(encoding="utf-8"))
    assert payload["tick"] == 3
    assert payload["state"]["tick"] == 3
    assert payload["state"]["agents"][0]["id"] == "a1"
