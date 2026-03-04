# Performance Comparison: Snapshot Events ON vs OFF (2026-03-04)

Comparison baseline:
- With snapshot events: `Plans/perf_baseline_2026-03-04_post_opt.json`
- Without snapshot events: `Plans/perf_baseline_2026-03-04_no_snapshots.json`

Run config: agents=[100,300], ticks=50, repeats=2, width=30, height=30, seed=42

| Agents | Elapsed ON (s) | Elapsed OFF (s) | Elapsed Δ | TPS ON | TPS OFF | TPS Δ | us/agent-tick ON | us/agent-tick OFF | us/agent-tick Δ | Peak Mem ON (MB) | Peak Mem OFF (MB) | Peak Mem Δ |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 4.9404 | 4.0938 | -17.14% | 10.1214 | 12.2164 | +20.70% | 988.08 | 818.75 | -17.14% | 9.6892 | 0.5855 | -93.96% |
| 300 | 36.5832 | 31.4911 | -13.92% | 1.3668 | 1.5878 | +16.17% | 2438.88 | 2099.41 | -13.92% | 28.4804 | 1.7489 | -93.86% |

## Interpretation

- Disabling SnapshotEvent emission improves throughput and substantially reduces memory pressure in headless benchmark mode.
- This confirms the profiler finding: deep-copy/model-copy in snapshot event path was a dominant runtime and memory cost.
- For UI/observer modes, keep snapshot events enabled (default). For pure headless perf runs, use `--no-snapshot-events`.
