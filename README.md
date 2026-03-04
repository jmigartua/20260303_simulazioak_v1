# sim-framework

Modular multi-agent simulation framework for deterministic, headless experiments.

## What is included

- Contracts layer (`sim_framework/contracts`) with core domain models, ports, behavior protocol, and schema validators.
- Core runtime layer (`sim_framework/core`) with signal grid, history buffer, deterministic engine, and physics/spatial hash.
- Scenario layer (`sim_framework/scenarios`) with `ants_foraging` state-machine behavior.

## Local setup

```bash
uv venv --python 3.11
source .venv/bin/activate
uv pip install -e .[dev]
```

## Run tests

```bash
.venv/bin/python -m pytest -v
```

## Developer shortcuts

```bash
make ci-local
make perf-snapshot-toggle
```

## Run benchmark

```bash
.venv/bin/python scripts/benchmark_headless.py --agents 100,300 --ticks 50 --repeats 2 --json-out Plans/perf_baseline_$(date +%F).json
```

Reproducible ON/OFF snapshot comparison (runs both modes + writes comparison markdown):

```bash
.venv/bin/python scripts/run_perf_snapshot_toggle.py --agents 100,300 --ticks 100 --repeats 3
```

## Run simulation (public runtime mode)

`sim-run` exposes a runtime preset:
- `interactive` (default): emits `SnapshotEvent` events.
- `headless`: disables `SnapshotEvent` emission by default for lower overhead.

```bash
.venv/bin/python -m sim_framework.app.cli --scenario ants_foraging --ticks 100 --runtime-mode interactive
.venv/bin/python -m sim_framework.app.cli --scenario ants_foraging --ticks 100 --runtime-mode headless
```

You can explicitly override snapshot behavior in either mode:

```bash
.venv/bin/python -m sim_framework.app.cli --scenario ants_foraging --ticks 100 --runtime-mode headless --emit-snapshot-events
```

Latest baseline snapshot in this repository:
- `Plans/perf_baseline_2026-03-03.json`
- `Plans/perf_baseline_2026-03-03.md`
- `Plans/perf_baseline_2026-03-04_post_opt.json`
- `Plans/perf_comparison_2026-03-04.md`
- `Plans/perf_baseline_2026-03-04_no_snapshots.json` (headless mode, SnapshotEvent emission disabled)
- `Plans/perf_comparison_2026-03-04_no_snapshots.md`

## Current status

- Deterministic engine loop and command handling implemented.
- Rewind/history snapshot support implemented.
- Ant foraging scenario runs headless and is covered by integration tests.

## Release artifacts

- Changelog: `CHANGELOG.md`
- Milestone notes for commits 27-29: `Plans/milestone_0.1.1_notes.md`
