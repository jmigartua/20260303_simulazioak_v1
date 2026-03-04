# Snapshot ON vs OFF (Post Engine Optimization)

- Generated: 2026-03-04
- Config ON: ticks=100, repeats=3, emit_snapshot_events=True
- Config OFF: ticks=100, repeats=3, emit_snapshot_events=False

| Agents | us/agent-tick ON | us/agent-tick OFF | Throughput gain OFF vs ON | Peak mem ON | Peak mem OFF | Memory reduction OFF vs ON |
|---|---:|---:|---:|---:|---:|---:|
| 100 | 879.963 | 823.393 | +6.43% | 18.98 MB | 0.37 MB | +98.05% |
| 300 | 2224.903 | 2215.326 | +0.43% | 55.78 MB | 1.09 MB | +98.04% |
