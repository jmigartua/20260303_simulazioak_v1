from __future__ import annotations

import json

import pytest

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


def test_cli_rejects_invalid_scenario(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--scenario", "unknown_scenario"])

    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "invalid choice" in err


def test_cli_rejects_non_positive_ticks(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--ticks", "0"])

    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "--ticks must be > 0" in err


def test_cli_rejects_conflicting_snapshot_flags(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--emit-snapshot-events", "--no-snapshot-events"])

    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "not allowed with argument" in err
