# Performance Comparison (2026-03-04)

Comparison baseline:
- Before optimization: `Plans/perf_baseline_2026-03-03.json`
- After optimization: `Plans/perf_baseline_2026-03-04_post_opt.json`

Run config (both): agents=[100,300], ticks=50, repeats=2, width=30, height=30, seed=42

| Agents | Elapsed Before (s) | Elapsed After (s) | Elapsed Δ | TPS Before | TPS After | TPS Δ | us/agent-tick Before | us/agent-tick After | us/agent-tick Δ | Peak Mem Before (MB) | Peak Mem After (MB) | Peak Mem Δ |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 4.6463 | 4.9404 | +6.33% | 10.7612 | 10.1214 | -5.95% | 929.26 | 988.08 | +6.33% | 9.6892 | 9.6892 | +0.00% |
| 300 | 32.6429 | 36.5832 | +12.07% | 1.5317 | 1.3668 | -10.77% | 2176.20 | 2438.88 | +12.07% | 28.4805 | 28.4804 | -0.00% |

## Interpretation

- This optimization pass reduced `SpatialHash` cell over-scan overhead in code, but end-to-end benchmark throughput did not improve in this run window.
- Dominant hotspot remains Pydantic deep-copy/model-copy inside engine snapshot/event path (see `Plans/perf_profile_2026-03-04.txt`).
- Next optimization candidate: make snapshot-event emission optional for pure headless benchmark runs, then re-baseline with equivalent mode settings.
