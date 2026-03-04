# R5 Drone Scenario Reproducibility Bundle

Date: 2026-03-04
Scope: Multi-scenario generality evidence for `drone_patrol` (backend scope)

## 1) Deterministic Save/Load Reproducibility (CLI + Persistence Adapter)

### Save run

```bash
.venv/bin/python -m sim_framework.app.cli \
  --scenario drone_patrol \
  --ticks 8 \
  --ants 12 \
  --seed 42 \
  --runtime-mode headless \
  --save-run-id r5-drone-repro-20260304 \
  --persistence-root Plans/runs \
  --json-out Plans/r5_drone_repro_save_2026-03-04.json
```

Expected checkpoints:
- `scenario = "drone_patrol"`
- `run.ticks_completed = 8`
- `persistence.saved_run_id = "r5-drone-repro-20260304"`
- `persistence.snapshots_saved = 9`

### Load run

```bash
.venv/bin/python -m sim_framework.app.cli \
  --load-run-id r5-drone-repro-20260304 \
  --persistence-root Plans/runs \
  --json-out Plans/r5_drone_repro_load_2026-03-04.json
```

Expected checkpoints:
- `mode = "loaded"`
- `persistence.scenario_name = "drone_patrol"`
- `persistence.snapshots = 9`
- `persistence.last_tick = 8`

## 2) Scenario-Aware Benchmark Evidence (ON/OFF Snapshot Toggle)

```bash
.venv/bin/python scripts/run_perf_snapshot_toggle.py \
  --scenario drone_patrol \
  --agents 20,40 \
  --ticks 20 \
  --repeats 1 \
  --label 2026-03-04_drone_patrol \
  --output-dir Plans
```

Generated:
- `Plans/perf_baseline_2026-03-04_drone_patrol_snapshot_on.json`
- `Plans/perf_baseline_2026-03-04_drone_patrol_snapshot_off.json`
- `Plans/perf_comparison_2026-03-04_drone_patrol.md`

## 3) Artifact List

- `Plans/r5_drone_repro_save_2026-03-04.json`
- `Plans/r5_drone_repro_load_2026-03-04.json`
- `Plans/runs/r5-drone-repro-20260304/run.json`
- `Plans/perf_baseline_2026-03-04_drone_patrol_snapshot_on.json`
- `Plans/perf_baseline_2026-03-04_drone_patrol_snapshot_off.json`
- `Plans/perf_comparison_2026-03-04_drone_patrol.md`

## 4) SHA-256 Hashes

- `234b2481f878fed0fde1c71ca4130d6af2f875dfc1ea44202ce7de78e44d9a0c`  `Plans/r5_drone_repro_save_2026-03-04.json`
- `87aae1fb116da6a88a45bf604148c4f3b69d589528656918868f41f60d8b66c4`  `Plans/r5_drone_repro_load_2026-03-04.json`
- `185874c2fee6dc47338fd8e04ea615144c21ec57bf95c785bb399a3822aa2e20`  `Plans/runs/r5-drone-repro-20260304/run.json`
- `67ea9bbfff2baa71dd373ae180f0b8bd6d7bcb223e5a2fd8855917282183c465`  `Plans/perf_baseline_2026-03-04_drone_patrol_snapshot_on.json`
- `8cdcb01b1fe14c3ebd4988f582478089237d900e5db53412aff5e40a817e7208`  `Plans/perf_baseline_2026-03-04_drone_patrol_snapshot_off.json`
- `f90253fff8961b7784e2876bb9d099b47ebca33c6e593e95f5f47e32b205c51c`  `Plans/perf_comparison_2026-03-04_drone_patrol.md`

## 5) Interpretation

This bundle demonstrates R5 in implemented backend scope:
- Scenario registry supports multiple scenarios (`ants_foraging`, `drone_patrol`).
- Public CLI executes and persists both scenario families.
- Benchmark tooling is scenario-aware and produces reproducible ON/OFF artifacts for the drone scenario.
