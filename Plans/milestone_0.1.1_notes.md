# Milestone 0.1.1 Notes (Commits 27-29)

Date: 2026-03-04

## Scope

This milestone captures three post-checklist delivery commits:

1. `66305c1` - `feat(app): expose runtime mode with public CLI and config`
2. `7a59420` - `perf(engine): reduce per-tick deep-copy overhead in state updates`
3. `a3542d6` - `docs(perf): add post-engine-opt snapshot ON/OFF baseline evidence`

## Outcomes

- Runtime control is now first-class via `RuntimeMode` (`interactive`, `headless`) and `sim-run`.
- Engine transition path removes avoidable deep-copy pressure while keeping state isolation guarantees.
- Reproducible baseline evidence exists for snapshot-event ON/OFF modes under identical benchmark parameters.

## Validation Snapshot

- Test suite: `72/72` passing on Python 3.11.11.
- Import direction: `contracts <- core <- scenarios <- app`, zero violations.
- Performance evidence:
  - 100 agents: snapshot OFF vs ON -> `+6.43%` throughput, `~98.05%` lower peak memory.
  - 300 agents: snapshot OFF vs ON -> `+0.43%` throughput, `~98.04%` lower peak memory.

## Notes

- Snapshot-OFF throughput at 300 agents remains sensitive to run variance and should be interpreted as statistically narrow gain at current repeat counts.
