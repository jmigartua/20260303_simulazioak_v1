# Headless Benchmark Baseline (2026-03-03)

## Command

```bash
.venv/bin/python scripts/benchmark_headless.py --agents 100,300 --ticks 50 --repeats 2 --json-out Plans/perf_baseline_2026-03-03.json
```

## Environment

- Runtime: Python 3.11.11 (`.venv`)
- Scenario: `sim_framework.scenarios.ants_foraging`
- World size: `30x30`
- Seed base: `42` (repeat seeds: `42`, `43`)

## Summary

| Agents | Ticks | Repeats | Mean elapsed (s) | Mean ticks/s | Mean us/agent-tick | Mean peak mem (MB) |
|---|---:|---:|---:|---:|---:|---:|
| 100 | 50 | 2 | 4.6463 | 10.7612 | 929.2613 | 9.6892 |
| 300 | 50 | 2 | 32.6429 | 1.5317 | 2176.1958 | 28.4805 |

Raw run-by-run data is stored in:
- `Plans/perf_baseline_2026-03-03.json`
