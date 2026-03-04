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


def test_cli_drone_patrol_runs_headless(capsys) -> None:
    payload = _run_cli(
        [
            "--scenario",
            "drone_patrol",
            "--ticks",
            "5",
            "--ants",
            "10",
            "--runtime-mode",
            "headless",
        ],
        capsys,
    )

    assert payload["scenario"] == "drone_patrol"
    assert payload["runtime"]["mode"] == "headless"
    assert payload["run"]["ticks_completed"] == 5
    assert payload["run"]["ants"] == 10


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


def test_cli_writes_json_output_file(tmp_path, capsys) -> None:
    out_path = tmp_path / "run.json"
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
            "--json-out",
            str(out_path),
        ],
        capsys,
    )

    assert out_path.exists()
    persisted = json.loads(out_path.read_text(encoding="utf-8"))
    assert persisted == payload


def test_cli_save_run_persists_bundle(tmp_path, capsys) -> None:
    run_root = tmp_path / "runs"
    payload = _run_cli(
        [
            "--scenario",
            "ants_foraging",
            "--ticks",
            "3",
            "--ants",
            "8",
            "--runtime-mode",
            "headless",
            "--persistence-root",
            str(run_root),
            "--save-run-id",
            "run-save",
        ],
        capsys,
    )

    assert payload["persistence"]["saved_run_id"] == "run-save"
    assert payload["persistence"]["snapshots_saved"] == 4
    run_file = run_root / "run-save" / "run.json"
    assert run_file.exists()
    bundle = json.loads(run_file.read_text(encoding="utf-8"))
    assert bundle["manifest"]["run_id"] == "run-save"
    assert len(bundle["snapshots"]) == 4


def test_cli_save_run_persists_drone_bundle(tmp_path, capsys) -> None:
    run_root = tmp_path / "runs"
    payload = _run_cli(
        [
            "--scenario",
            "drone_patrol",
            "--ticks",
            "3",
            "--ants",
            "6",
            "--runtime-mode",
            "headless",
            "--persistence-root",
            str(run_root),
            "--save-run-id",
            "drone-save",
        ],
        capsys,
    )

    assert payload["scenario"] == "drone_patrol"
    assert payload["persistence"]["saved_run_id"] == "drone-save"
    run_file = run_root / "drone-save" / "run.json"
    bundle = json.loads(run_file.read_text(encoding="utf-8"))
    assert bundle["manifest"]["scenario_name"] == "drone_patrol"
    assert len(bundle["snapshots"]) == 4


def test_cli_load_run_prints_persistence_summary(tmp_path, capsys) -> None:
    run_root = tmp_path / "runs"
    _run_cli(
        [
            "--scenario",
            "ants_foraging",
            "--ticks",
            "2",
            "--ants",
            "6",
            "--runtime-mode",
            "headless",
            "--persistence-root",
            str(run_root),
            "--save-run-id",
            "run-load",
        ],
        capsys,
    )

    payload = _run_cli(
        [
            "--load-run-id",
            "run-load",
            "--persistence-root",
            str(run_root),
        ],
        capsys,
    )

    assert payload["mode"] == "loaded"
    assert payload["persistence"]["run_id"] == "run-load"
    assert payload["persistence"]["snapshots"] == 3
    assert payload["persistence"]["last_tick"] == 2


def test_cli_load_missing_run_raises_parser_error(tmp_path, capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        main(
            [
                "--load-run-id",
                "missing-run",
                "--persistence-root",
                str(tmp_path / "runs"),
            ]
        )

    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "Run not found: missing-run" in err


def test_cli_rejects_conflicting_persistence_flags(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--save-run-id", "run-1", "--load-run-id", "run-2"])

    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "not allowed with argument" in err
