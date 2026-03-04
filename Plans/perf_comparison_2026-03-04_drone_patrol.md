# Snapshot ON vs OFF Benchmark Comparison

- Source: `scripts/run_perf_snapshot_toggle.py`
- Scenario: `drone_patrol`
- ON config: ticks=20, repeats=1, emit_snapshot_events=True
- OFF config: ticks=20, repeats=1, emit_snapshot_events=False

| Agents | us/agent-tick ON | us/agent-tick OFF | Throughput gain OFF vs ON | Peak mem ON | Peak mem OFF | Memory reduction OFF vs ON |
|---|---:|---:|---:|---:|---:|---:|
| 20 | 118.113 | 49.608 | +58.00% | 0.86 MB | 0.08 MB | +90.77% |
| 40 | 110.724 | 50.310 | +54.56% | 1.66 MB | 0.15 MB | +90.86% |

- Determinism cross-check (run-pairs): 2/2 matched carrying/signal/tick.
