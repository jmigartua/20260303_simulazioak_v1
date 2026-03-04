from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def _load_module(rel_path: str, module_name: str):
    root = Path(__file__).resolve().parents[2]
    script_path = root / rel_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _payload(*, emit_snapshot_events: bool, agents: int, us: float, mem: float) -> dict:
    return {
        "config": {
            "ticks": 10,
            "repeats": 1,
            "emit_snapshot_events": emit_snapshot_events,
        },
        "runs": [
            {
                "state_tick": 10,
                "carrying_agents": 4,
                "signal_total": 123.0,
            }
        ],
        "summaries": [
            {
                "agents": agents,
                "us_per_agent_tick_mean": us,
                "peak_mem_mb_mean": mem,
            }
        ],
    }


def test_parse_agents_valid_and_invalid_inputs() -> None:
    mod = _load_module("scripts/run_perf_snapshot_toggle.py", "run_perf_snapshot_toggle")

    assert mod._parse_agents("100,300") == [100, 300]
    assert mod._parse_agents(" 40 , 80 ") == [40, 80]
    with pytest.raises(Exception):
        mod._parse_agents("")
    with pytest.raises(Exception):
        mod._parse_agents("10,abc")
    with pytest.raises(Exception):
        mod._parse_agents("10,0")


def test_determinism_pair_counting() -> None:
    mod = _load_module("scripts/run_perf_snapshot_toggle.py", "run_perf_snapshot_toggle")
    on_payload = _payload(emit_snapshot_events=True, agents=100, us=1000.0, mem=10.0)
    off_payload = _payload(emit_snapshot_events=False, agents=100, us=900.0, mem=1.0)

    matched, compared = mod._determinism_pairs(on_payload, off_payload)
    assert (matched, compared) == (1, 1)

    off_payload["runs"][0]["carrying_agents"] = 5
    matched, compared = mod._determinism_pairs(on_payload, off_payload)
    assert (matched, compared) == (0, 1)


def test_write_comparison_generates_expected_markdown(tmp_path: Path) -> None:
    mod = _load_module("scripts/run_perf_snapshot_toggle.py", "run_perf_snapshot_toggle")
    on_payload = _payload(emit_snapshot_events=True, agents=100, us=1000.0, mem=10.0)
    off_payload = _payload(emit_snapshot_events=False, agents=100, us=900.0, mem=1.0)
    out = tmp_path / "comparison.md"

    mod._write_comparison(on_payload, off_payload, out)
    text = out.read_text(encoding="utf-8")

    assert "# Snapshot ON vs OFF Benchmark Comparison" in text
    assert "Throughput gain OFF vs ON" in text
    assert "| 100 | 1000.000 | 900.000 | +10.00% | 10.00 MB | 1.00 MB | +90.00% |" in text
    assert "Determinism cross-check (run-pairs): 1/1" in text
