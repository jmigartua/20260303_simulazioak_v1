# sim-framework

Modular multi-agent simulation framework for deterministic, headless experiments.

## What is included

- Contracts layer (`sim_framework/contracts`) with core domain models, ports, behavior protocol, and schema validators.
- Core runtime layer (`sim_framework/core`) with signal grid, history buffer, deterministic engine, and physics/spatial hash.
- Scenario layer (`sim_framework/scenarios`) with `ants_foraging` and `drone_patrol` state-machine behaviors.

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
make release-check
make perf-smoke
make perf-snapshot-toggle
```

`make release-check` runs release-version consistency, import-flow checks, full tests, and package install sanity.

## Run benchmark

```bash
.venv/bin/python scripts/benchmark_headless.py --agents 100,300 --ticks 50 --repeats 2 --json-out Plans/perf_baseline_$(date +%F).json
```

Reproducible ON/OFF snapshot comparison (runs both modes + writes comparison markdown):

```bash
.venv/bin/python scripts/run_perf_snapshot_toggle.py --agents 100,300 --ticks 100 --repeats 3
```

Scenario-aware benchmarking is supported:

```bash
.venv/bin/python scripts/benchmark_headless.py --scenario drone_patrol --agents 100 --ticks 50 --repeats 2
.venv/bin/python scripts/run_perf_snapshot_toggle.py --scenario drone_patrol --agents 100,300 --ticks 100 --repeats 3
```

## Run simulation (public runtime mode)

`sim-run` exposes a runtime preset:
- `interactive` (default): emits `SnapshotEvent` events.
- `headless`: disables `SnapshotEvent` emission by default for lower overhead.

```bash
.venv/bin/python -m sim_framework.app.cli --scenario ants_foraging --ticks 100 --runtime-mode interactive
.venv/bin/python -m sim_framework.app.cli --scenario ants_foraging --ticks 100 --runtime-mode headless
.venv/bin/python -m sim_framework.app.cli --scenario drone_patrol --ticks 100 --runtime-mode headless
.venv/bin/python -m sim_framework.app.cli --scenario drone_patrol --ticks 100 --runtime-mode headless --boundary-mode wrap
```

You can explicitly override snapshot behavior in either mode:

```bash
.venv/bin/python -m sim_framework.app.cli --scenario ants_foraging --ticks 100 --runtime-mode headless --emit-snapshot-events
```

Agent attributes/method parameters can be overridden in headless mode via JSON spec:

```bash
.venv/bin/python -m sim_framework.app.cli --scenario ants_foraging --ticks 100 --agent-spec-json Plans/r3_agent_spec_ants_custom_2026-03-04.json
```

Run persistence workflows (save/load snapshots + manifest):

```bash
# Save a run bundle to runs/demo-run/run.json
.venv/bin/python -m sim_framework.app.cli --scenario ants_foraging --ticks 50 --runtime-mode headless --save-run-id demo-run

# Load a previously saved run and print metadata summary
.venv/bin/python -m sim_framework.app.cli --load-run-id demo-run

# Use a custom persistence root
.venv/bin/python -m sim_framework.app.cli --scenario ants_foraging --ticks 25 --save-run-id custom-run --persistence-root /tmp/sim-runs
```

Run the M1 visible app shell (browser + canvas + live controls):

```bash
.venv/bin/python -m sim_framework.app.web --scenario ants_foraging --agents 40 --width 30 --height 30
# or via console script:
sim-web --scenario drone_patrol --agents 20 --boundary-mode wrap
```

M1 controls currently available in the shell:
- `Play`, `Pause`, `Step`, `Reset`
- scenario switch without server restart (`ants_foraging` <-> `drone_patrol`)
- seek/rewind controls (`Seek tick`, `Rewind 10`)
- speed updates via `set_speed`
- signal overlay toggle for pheromone/radio field heat tint
- live state panel (`tick`, `paused`, `agent_count`, `carrying_agents`, `signal_total`)
- renderer backend: PixiJS shell (CDN) with automatic canvas fallback
- scenario-specific visuals (ants state colors, drone waypoint path and drone glyphs)
- refresh telemetry (`Refresh Hz`) for basic runtime smoothness sanity checks
- sync telemetry (`API latency ms`, `Tick drift`) to monitor polling responsiveness and state progression
- tick-rate contract from `/api/meta` (`step_interval_ms`, `target_tick_hz`) for render pacing sanity

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
- File-based persistence adapter implemented for run save/load (`JsonFilePersistence` + CLI flags).

## Release artifacts

- Changelog: `CHANGELOG.md`
- Milestone notes for commits 27-29: `Plans/milestone_0.1.1_notes.md`
- UI/Desktop execution roadmap (R6/R9): `Plans/r6_r9_ui_desktop_roadmap_2026-03-04.md`
