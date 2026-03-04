from __future__ import annotations

import json

from sim_framework.app.cli import main


def _run_cli(args: list[str], capsys) -> dict:
    exit_code = main(args)
    assert exit_code == 0
    out = capsys.readouterr().out
    return json.loads(out)


def test_cli_interactive_mode_emits_snapshot_events(capsys) -> None:
    payload = _run_cli(
        [
            "--scenario",
            "ants_foraging",
            "--ticks",
            "5",
            "--ants",
            "10",
            "--runtime-mode",
            "interactive",
        ],
        capsys,
    )

    assert payload["runtime"]["mode"] == "interactive"
    assert payload["runtime"]["emit_snapshot_events"] is True
    assert payload["run"]["ticks_completed"] == 5
    assert payload["events"]["snapshot"] == 5


def test_cli_headless_mode_disables_snapshot_events(capsys) -> None:
    payload = _run_cli(
        [
            "--scenario",
            "ants_foraging",
            "--ticks",
            "5",
            "--ants",
            "10",
            "--runtime-mode",
            "headless",
        ],
        capsys,
    )

    assert payload["runtime"]["mode"] == "headless"
    assert payload["runtime"]["emit_snapshot_events"] is False
    assert payload["run"]["ticks_completed"] == 5
    assert payload["events"]["snapshot"] == 0


def test_cli_explicit_override_can_enable_snapshot_events_in_headless_mode(capsys) -> None:
    payload = _run_cli(
        [
            "--scenario",
            "ants_foraging",
            "--ticks",
            "5",
            "--ants",
            "10",
            "--runtime-mode",
            "headless",
            "--emit-snapshot-events",
        ],
        capsys,
    )

    assert payload["runtime"]["mode"] == "headless"
    assert payload["runtime"]["emit_snapshot_events"] is True
    assert payload["events"]["snapshot"] == 5
