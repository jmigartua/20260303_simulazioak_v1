# R3 Agent Spec Reproducibility Bundle

Date: 2026-03-04
Scope: headless runtime configurability of agent attributes + methods via validated JSON schema (`--agent-spec-json`)

## 1) Custom Spec Files

- `Plans/r3_agent_spec_ants_custom_2026-03-04.json`
  - Overrides: `max_speed=1.8`, `sensor_radius=6.0`, `wander_sigma=0.2`, `deposit amount=1.5`
- `Plans/r3_agent_spec_drone_custom_2026-03-04.json`
  - Overrides: `max_speed=2.0`, `segment_ticks=6`, `beacon amount=0.25`

## 2) Run Commands

Ants scenario with custom spec:

```bash
.venv/bin/python -m sim_framework.app.cli \
  --scenario ants_foraging \
  --ticks 20 \
  --ants 10 \
  --seed 42 \
  --runtime-mode headless \
  --agent-spec-json Plans/r3_agent_spec_ants_custom_2026-03-04.json \
  --save-run-id r3-ants-custom-20260304 \
  --persistence-root Plans/runs \
  --json-out Plans/r3_ants_custom_run_2026-03-04.json
```

Drone scenario with custom spec:

```bash
.venv/bin/python -m sim_framework.app.cli \
  --scenario drone_patrol \
  --ticks 20 \
  --ants 10 \
  --seed 42 \
  --runtime-mode headless \
  --agent-spec-json Plans/r3_agent_spec_drone_custom_2026-03-04.json \
  --save-run-id r3-drone-custom-20260304 \
  --persistence-root Plans/runs \
  --json-out Plans/r3_drone_custom_run_2026-03-04.json
```

## 3) Load/Verification Commands

```bash
.venv/bin/python -m sim_framework.app.cli --load-run-id r3-ants-custom-20260304 --persistence-root Plans/runs --json-out Plans/r3_ants_custom_load_2026-03-04.json
.venv/bin/python -m sim_framework.app.cli --load-run-id r3-drone-custom-20260304 --persistence-root Plans/runs --json-out Plans/r3_drone_custom_load_2026-03-04.json
```

Expected checkpoints:
- run JSON includes `scenario_config.agent_spec_source` pointing to the provided JSON file
- load JSON confirms saved scenario and snapshot count

## 4) Artifacts

- `Plans/r3_agent_spec_ants_custom_2026-03-04.json`
- `Plans/r3_agent_spec_drone_custom_2026-03-04.json`
- `Plans/r3_ants_custom_run_2026-03-04.json`
- `Plans/r3_drone_custom_run_2026-03-04.json`
- `Plans/r3_ants_custom_load_2026-03-04.json`
- `Plans/r3_drone_custom_load_2026-03-04.json`
- `Plans/runs/r3-ants-custom-20260304/run.json`
- `Plans/runs/r3-drone-custom-20260304/run.json`

## 5) SHA-256

- `842334663fcd73db260d9b267aedf7e8a0366efa0d56c2ebd1d1e48c35effb82`  `Plans/r3_agent_spec_ants_custom_2026-03-04.json`
- `b0e0221cdc39628d3f243ae4c27fb042b473aec27dc51c4dcdcc860ed70f045f`  `Plans/r3_agent_spec_drone_custom_2026-03-04.json`
- `cefde8a4b3f5c7409fee73eb84200dc914beeb87df130ffcc4d56a5d842fed97`  `Plans/r3_ants_custom_run_2026-03-04.json`
- `ea8f52c285c2a79c7aa3fd68f653bfb130b4bfab038dda28533fc85f419e5733`  `Plans/r3_drone_custom_run_2026-03-04.json`
- `1ddab5514c2b0ea1c5cb8bb256b24376fd97b8365900a6f5f5ec835b1c074e82`  `Plans/r3_ants_custom_load_2026-03-04.json`
- `ab14d5f385ab8ca353430c01ecaf2680d03fd506d7003aad84c537ecb8f6763f`  `Plans/r3_drone_custom_load_2026-03-04.json`
- `0e5edc4d96e97ea6d184b5fa812017b7d6cc49f2fe11566c21b32b7959d1c1ed`  `Plans/runs/r3-ants-custom-20260304/run.json`
- `e65a12349a9bc49be15203d13d4e625b228e5017920ea67a1e6a036e4b7c5408`  `Plans/runs/r3-drone-custom-20260304/run.json`
