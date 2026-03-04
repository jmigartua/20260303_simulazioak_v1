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


def test_invalid_command_payload_is_rejected() -> None:
    bridge = WebRuntimeBridge(BridgeConfig())
    with pytest.raises(ValueError):
        bridge.apply_command({"kind": "step", "steps": 0})
