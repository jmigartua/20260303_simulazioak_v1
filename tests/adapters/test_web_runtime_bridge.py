from __future__ import annotations

import pytest

from sim_framework.adapters.web.runtime_bridge import BridgeConfig, WebRuntimeBridge


def test_bridge_starts_paused_with_initial_state() -> None:
    bridge = WebRuntimeBridge(
        BridgeConfig(
            scenario_name="ants_foraging",
            agents=8,
            width=20,
            height=20,
            seed=42,
        )
    )
    payload = bridge.state_payload()

    assert payload["scenario"] == "ants_foraging"
    assert payload["tick"] == 0
    assert payload["paused"] is True
    assert payload["metrics"]["agent_count"] == 8


def test_play_pause_step_commands_control_progression() -> None:
    bridge = WebRuntimeBridge(
        BridgeConfig(
            scenario_name="ants_foraging",
            agents=6,
            width=20,
            height=20,
            seed=7,
        )
    )

    bridge.apply_command({"kind": "play"})
    bridge.tick_once()
    tick_after_play = bridge.state_payload()["tick"]
    assert tick_after_play == 1

    bridge.apply_command({"kind": "pause"})
    bridge.tick_once()
    assert bridge.state_payload()["tick"] == tick_after_play

    bridge.apply_command({"kind": "step", "steps": 1})
    bridge.tick_once()
    assert bridge.state_payload()["tick"] == tick_after_play + 1


def test_reset_rebuilds_session_to_tick_zero() -> None:
    bridge = WebRuntimeBridge(
        BridgeConfig(
            scenario_name="drone_patrol",
            agents=4,
            width=18,
            height=18,
            seed=11,
        )
    )
    bridge.apply_command({"kind": "play"})
    bridge.tick_once()
    bridge.tick_once()
    assert bridge.state_payload()["tick"] >= 2

    bridge.apply_command({"kind": "reset"})
    payload = bridge.state_payload()

    assert payload["tick"] == 0
    assert payload["paused"] is True
    assert payload["metrics"]["agent_count"] == 4


def test_seek_command_rewinds_to_previous_tick() -> None:
    bridge = WebRuntimeBridge(BridgeConfig(scenario_name="ants_foraging", agents=6, seed=5))
    bridge.apply_command({"kind": "play"})
    for _ in range(4):
        bridge.tick_once()
    assert bridge.state_payload()["tick"] >= 4

    bridge.apply_command({"kind": "seek", "tick": 1})
    bridge.tick_once()
    assert bridge.state_payload()["tick"] == 1


def test_switch_scenario_rebuilds_without_restart() -> None:
    bridge = WebRuntimeBridge(BridgeConfig(scenario_name="ants_foraging", agents=5))
    assert bridge.state_payload()["scenario"] == "ants_foraging"

    bridge.switch_scenario("drone_patrol")
    payload = bridge.state_payload()
    assert payload["scenario"] == "drone_patrol"
    assert payload["tick"] == 0
    assert payload["metrics"]["agent_count"] == 5


def test_state_payload_exposes_signal_grid_for_overlay() -> None:
    bridge = WebRuntimeBridge(BridgeConfig(scenario_name="ants_foraging", width=12, height=10))
    payload = bridge.state_payload()
    signal = payload["signal"]
    assert signal["width"] == 12
    assert signal["height"] == 10
    assert len(signal["data"]) == 10
    assert len(signal["data"][0]) == 12


def test_meta_payload_exposes_tick_rate_contract() -> None:
    bridge = WebRuntimeBridge(
        BridgeConfig(
            scenario_name="ants_foraging",
            agents=9,
            step_interval_s=0.04,
        )
    )
    meta = bridge.meta_payload()
    assert meta["current_scenario"] == "ants_foraging"
    assert meta["agents"] == 9
    assert meta["step_interval_ms"] == 40
    assert meta["target_tick_hz"] == 25.0


def test_invalid_command_payload_is_rejected() -> None:
    bridge = WebRuntimeBridge(BridgeConfig())
    with pytest.raises(ValueError):
        bridge.apply_command({"kind": "step", "steps": 0})
