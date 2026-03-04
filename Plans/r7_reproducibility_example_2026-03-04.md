# R7 Reproducibility Example (Adapter-Backed Save/Load)

Date: 2026-03-04
Milestone tag: `milestone-persistence-cli-2026-03-04`
Base commit for this example: `0d7e7ca`

## Goal

Provide a concrete, adapter-backed R7 example using the public CLI to:
1. Run a deterministic headless simulation.
2. Persist snapshots + manifest with `--save-run-id`.
3. Reload persisted data with `--load-run-id`.
4. Export machine-readable summaries with `--json-out`.

## Save Command

```bash
.venv/bin/python -m sim_framework.app.cli \
  --scenario ants_foraging \
  --ticks 5 \
  --ants 10 \
  --seed 42 \
  --runtime-mode headless \
  --save-run-id r7-repro-20260304 \
  --persistence-root Plans/runs \
  --json-out Plans/r7_repro_save_2026-03-04.json
```

Key expected values:
- `run.ticks_completed = 5`
- `persistence.saved_run_id = "r7-repro-20260304"`
- `persistence.snapshots_saved = 6` (initial snapshot + 5 ticks)

## Load Command

```bash
.venv/bin/python -m sim_framework.app.cli \
  --load-run-id r7-repro-20260304 \
  --persistence-root Plans/runs \
  --json-out Plans/r7_repro_load_2026-03-04.json
```

Key expected values:
- `mode = "loaded"`
- `persistence.run_id = "r7-repro-20260304"`
- `persistence.snapshots = 6`
- `persistence.last_tick = 5`

## Produced Artifacts

- `Plans/runs/r7-repro-20260304/run.json`
- `Plans/r7_repro_save_2026-03-04.json`
- `Plans/r7_repro_load_2026-03-04.json`

## Artifact Hashes (SHA-256)

- `6704f7e75bd113c4832d2c0b93f022b4a89663e77e1af0ba59eb24dde87d19a0`  `Plans/runs/r7-repro-20260304/run.json`
- `cf341afabc560431eb5280b289ea58a02c456e1e59895e9b22a957ab5486ac81`  `Plans/r7_repro_save_2026-03-04.json`
- `46dca5e84127fdae3fcdec0c61618d866f959fd6ae5a621de9a2f2a3bf1428b9`  `Plans/r7_repro_load_2026-03-04.json`

## Notes

- This example demonstrates R7 backend scope (`save/load` and replayable state snapshots).
- UI-level playback controls remain part of the pending frontend scope.
