from __future__ import annotations

import json
import threading
import time
from urllib import error
from urllib import request

from sim_framework.adapters.web.runtime_bridge import BridgeConfig, WebRuntimeBridge
from sim_framework.app.web import WebShellServer


def _get_json(url: str) -> dict:
    with request.urlopen(url, timeout=2.0) as response:
        return json.loads(response.read().decode("utf-8"))


def _post_json(url: str, payload: dict) -> dict:
    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=2.0) as response:
        return json.loads(response.read().decode("utf-8"))


def _post_json_error(url: str, payload: dict) -> tuple[int, dict]:
    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=2.0):
            raise AssertionError("expected HTTPError")
    except error.HTTPError as exc:
        payload = json.loads(exc.read().decode("utf-8"))
        return exc.code, payload


def _wait_for_tick(base_url: str, *, at_least: int, timeout_s: float = 1.0) -> dict:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        payload = _get_json(f"{base_url}/api/state")
        if payload["tick"] >= at_least:
            return payload
        time.sleep(0.02)
    raise AssertionError(f"tick did not reach {at_least} within {timeout_s}s")


def test_web_shell_serves_html_and_state_and_accepts_commands() -> None:
    bridge = WebRuntimeBridge(
        BridgeConfig(
            scenario_name="ants_foraging",
            agents=8,
            width=20,
            height=20,
            seed=42,
            step_interval_s=0.01,
        )
    )
    server = WebShellServer(host="127.0.0.1", port=0, bridge=bridge)
    server.start()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        base_url = f"http://127.0.0.1:{server.port}"

        with request.urlopen(f"{base_url}/", timeout=2.0) as response:
            html = response.read().decode("utf-8")
        assert "sim-canvas" in html
        assert "Play" in html
        assert "Pause" in html
        assert "Step" in html
        assert "Reset" in html
        assert "Switch Scenario" in html
        assert "Signal overlay" in html
        assert "Renderer:" in html
        assert "Target tick Hz:" in html
        assert "Refresh Hz:" in html
        assert "API latency ms:" in html
        assert "Tick drift:" in html
        assert "pixi.min.js" in html

        meta = _get_json(f"{base_url}/api/meta")
        assert "ants_foraging" in meta["available_scenarios"]
        assert "drone_patrol" in meta["available_scenarios"]
        assert meta["current_scenario"] == "ants_foraging"
        assert meta["step_interval_ms"] == 10
        assert meta["target_tick_hz"] == 100.0

        state = _get_json(f"{base_url}/api/state")
        assert state["paused"] is True
        assert state["tick"] == 0
        assert "signal" in state
        assert "data" in state["signal"]

        _post_json(f"{base_url}/api/command", {"kind": "step", "steps": 1})
        progressed = _wait_for_tick(base_url, at_least=1, timeout_s=1.0)
        assert progressed["tick"] >= 1

        switched = _post_json(f"{base_url}/api/scenario", {"scenario": "drone_patrol"})
        assert switched["scenario"] == "drone_patrol"
        assert switched["tick"] == 0

        code, err = _post_json_error(
            f"{base_url}/api/scenario",
            {"scenario": "not_a_real_scenario"},
        )
        assert code == 400
        assert "Unknown scenario" in err["error"]

        code, err = _post_json_error(f"{base_url}/api/command", {"kind": "step", "steps": 0})
        assert code == 400
        assert "Invalid command payload" in err["error"]

        _post_json(f"{base_url}/api/command", {"kind": "step", "steps": 1})
        after_switch_step = _wait_for_tick(base_url, at_least=1, timeout_s=1.0)
        assert after_switch_step["scenario"] == "drone_patrol"
    finally:
        server.shutdown()
        thread.join(timeout=1.0)
