# R4 Physics Config Reproducibility Bundle

Date: 2026-03-04
Scope: configurable physics evidence in implemented backend scope (`clamp` vs `wrap`)

## 1) Commands

Clamp mode:

```bash
.venv/bin/python -m sim_framework.app.cli \
  --scenario drone_patrol \
  --ticks 40 \
  --ants 12 \
  --width 2 \
  --height 2 \
  --seed 42 \
  --runtime-mode headless \
  --boundary-mode clamp \
  --save-run-id r4-physics-drone2-clamp-20260304 \
  --persistence-root Plans/runs \
  --json-out Plans/r4_physics_drone2_clamp_saved_2026-03-04.json
```

Wrap mode:

```bash
.venv/bin/python -m sim_framework.app.cli \
  --scenario drone_patrol \
  --ticks 40 \
  --ants 12 \
  --width 2 \
  --height 2 \
  --seed 42 \
  --runtime-mode headless \
  --boundary-mode wrap \
  --save-run-id r4-physics-drone2-wrap-20260304 \
  --persistence-root Plans/runs \
  --json-out Plans/r4_physics_drone2_wrap_saved_2026-03-04.json
```

## 2) Observable Effect

Both runs use the same seed and scenario parameters; only `--boundary-mode` changes.

Trajectory diverges once boundary interaction starts:
- Tick 5, `agent-0` position
  - clamp: `(2.0, 2.0)`
  - wrap: `(1.242641, 1.242641)`
- Tick 40, `agent-0` position
  - clamp: `(2.0, 0.0)`
  - wrap: `(1.337225, 0.6562)`

This demonstrates that physics configuration is active and affects simulated trajectories.

## 3) Artifacts

- `Plans/r4_physics_drone2_clamp_saved_2026-03-04.json`
- `Plans/r4_physics_drone2_wrap_saved_2026-03-04.json`
- `Plans/runs/r4-physics-drone2-clamp-20260304/run.json`
- `Plans/runs/r4-physics-drone2-wrap-20260304/run.json`

## 4) SHA-256

- `29b5647a50e9aad998120a9c743343db952d168cc5933603b9d7c5ce91e978cf`  `Plans/r4_physics_drone2_clamp_saved_2026-03-04.json`
- `bbffd2b22f03c49c037c46ab0b3ba112b9ae7390a7bc4328de2d4e5a460b499a`  `Plans/r4_physics_drone2_wrap_saved_2026-03-04.json`
- `43643f9616120bde5554b91e433addb1538486fb990c9015523518700be01e21`  `Plans/runs/r4-physics-drone2-clamp-20260304/run.json`
- `ba5031c0455586593afc04efd120b32fe1eb5825eb26bac2f7d41d3e452c0a2f`  `Plans/runs/r4-physics-drone2-wrap-20260304/run.json`
