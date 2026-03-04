from __future__ import annotations

from sim_framework.app.runtime import RuntimeConfig, RuntimeMode, create_engine


def test_runtime_default_is_interactive_with_snapshot_events() -> None:
    runtime = RuntimeConfig()

    assert runtime.mode is RuntimeMode.INTERACTIVE
    assert runtime.resolved_emit_snapshot_events() is True
    assert create_engine(seed=1, runtime=runtime).emit_snapshot_events is True


def test_headless_mode_disables_snapshot_events_by_default() -> None:
    runtime = RuntimeConfig(mode=RuntimeMode.HEADLESS)

    assert runtime.resolved_emit_snapshot_events() is False
    assert create_engine(seed=1, runtime=runtime).emit_snapshot_events is False


def test_explicit_snapshot_override_wins_over_mode() -> None:
    runtime = RuntimeConfig(
        mode=RuntimeMode.HEADLESS,
        emit_snapshot_events=True,
    )

    assert runtime.resolved_emit_snapshot_events() is True
    assert create_engine(seed=1, runtime=runtime).emit_snapshot_events is True
