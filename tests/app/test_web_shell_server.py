from __future__ import annotations

import json
import threading
import time
from pathlib import Path
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


def _wait_for_exact_tick(base_url: str, *, tick: int, timeout_s: float = 1.0) -> dict:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        payload = _get_json(f"{base_url}/api/state")
        if payload["tick"] == tick:
            return payload
        time.sleep(0.02)
    raise AssertionError(f"tick did not reach exact value {tick} within {timeout_s}s")


def _wait_for_paused(base_url: str, *, paused: bool, timeout_s: float = 1.0) -> dict:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        payload = _get_json(f"{base_url}/api/state")
        if payload["paused"] is paused:
            return payload
        time.sleep(0.02)
    raise AssertionError(f"paused state did not reach {paused} within {timeout_s}s")


def test_web_shell_serves_html_and_state_and_accepts_commands(tmp_path) -> None:
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
    capture_root = tmp_path / "captures"
    server = WebShellServer(
        host="127.0.0.1",
        port=0,
        bridge=bridge,
        capture_root=capture_root,
    )
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
        assert "Last capture:" in html
        assert "Capture files:" in html
        assert "Capture JSON" in html
        assert "Refresh Captures" in html
        assert "Delete Capture" in html
        assert "Timeline" in html
        assert "Jump Latest" in html
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
        assert state["timeline"]["current_tick"] == 0
        assert state["timeline"]["max_tick_reached"] == 0

        _post_json(f"{base_url}/api/command", {"kind": "step", "steps": 1})
        progressed = _wait_for_tick(base_url, at_least=1, timeout_s=1.0)
        assert progressed["tick"] >= 1
        assert progressed["timeline"]["max_tick_reached"] >= progressed["tick"]

        _post_json(f"{base_url}/api/command", {"kind": "seek", "tick": 0})
        rewound = _wait_for_exact_tick(base_url, tick=0, timeout_s=1.0)
        assert rewound["timeline"]["max_tick_reached"] >= 1

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

        capture = _post_json(f"{base_url}/api/capture", {})
        capture_file = capture["capture_file"]
        capture_name = capture["capture_name"]
        assert capture["state"]["scenario"] == "drone_patrol"
        assert capture_file.startswith(str(capture_root))
        assert isinstance(capture["capture_digest"], str)
        assert len(capture["capture_digest"]) == 64

        capture_json = json.loads((capture_root / Path(capture_file).name).read_text(encoding="utf-8"))
        assert capture_json["state"]["scenario"] == "drone_patrol"
        assert "captured_at_utc" in capture_json
        assert capture_json["capture_digest"] == capture["capture_digest"]

        listing = _get_json(f"{base_url}/api/captures")
        assert len(listing["captures"]) == 1
        assert listing["captures"][0]["name"] == capture_name
        assert listing["captures"][0]["scenario"] == "drone_patrol"

        deleted = _post_json(f"{base_url}/api/capture/delete", {"name": capture_name})
        assert deleted["deleted"] == capture_name
        assert deleted["captures"] == []

        code, err = _post_json_error(f"{base_url}/api/capture/delete", {"name": "../bad.json"})
        assert code == 400
        assert "plain filename" in err["error"]
    finally:
        server.shutdown()
        thread.join(timeout=1.0)


def test_play_advances_ticks_and_pause_stabilizes_tick() -> None:
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
        initial = _get_json(f"{base_url}/api/state")
        assert initial["tick"] == 0
        assert initial["paused"] is True

        _post_json(f"{base_url}/api/command", {"kind": "play"})
        progressed = _wait_for_tick(base_url, at_least=5, timeout_s=1.0)
        assert progressed["paused"] is False
        start_tick = progressed["tick"]

        _post_json(f"{base_url}/api/command", {"kind": "pause"})
        paused_payload = _wait_for_paused(base_url, paused=True, timeout_s=1.0)
        paused_tick = paused_payload["tick"]

        time.sleep(0.12)
        after_sleep = _get_json(f"{base_url}/api/state")
        # Allow at most one residual tick if pause landed between loop iterations.
        assert after_sleep["tick"] - paused_tick <= 1
        assert after_sleep["tick"] >= start_tick
    finally:
        server.shutdown()
        thread.join(timeout=1.0)
