# R8 End-to-End Reproducibility Bundle (CLI + Web Capture)

Date: 2026-03-05  
Scope: Adapter-backed reproducibility across `sim-run` and `sim-web` flows.

## 1) CLI Save/Load Reproducibility (`sim-run`)

### Save run

```bash
.venv/bin/python -m sim_framework.app.cli \
  --scenario ants_foraging \
  --ticks 6 \
  --agents 12 \
  --seed 42 \
  --runtime-mode headless \
  --save-run-id r8-e2e-20260305 \
  --persistence-root Plans/runs \
  --json-out Plans/r8_e2e_cli_save_2026-03-05.json
```

Expected checkpoints:
- `scenario = "ants_foraging"`
- `run.ticks_completed = 6`
- `run.agents = 12`
- `persistence.saved_run_id = "r8-e2e-20260305"`
- `persistence.snapshots_saved = 7`

### Load run

```bash
.venv/bin/python -m sim_framework.app.cli \
  --load-run-id r8-e2e-20260305 \
  --persistence-root Plans/runs \
  --json-out Plans/r8_e2e_cli_load_2026-03-05.json
```

Expected checkpoints:
- `mode = "loaded"`
- `persistence.run_id = "r8-e2e-20260305"`
- `persistence.snapshots = 7`
- `persistence.last_tick = 6`

## 2) Web Capture Reproducibility (`sim-web`)

### Start web shell

```bash
.venv/bin/python -m sim_framework.app.web \
  --host 127.0.0.1 \
  --port 8092 \
  --scenario drone_patrol \
  --agents 10 \
  --seed 42 \
  --capture-root Plans/captures_r8_2026-03-05
```

### Drive API and export artifacts

In another terminal:

```bash
curl -sS http://127.0.0.1:8092/api/meta > Plans/r8_e2e_web_meta_2026-03-05.json

cat <<'JSON' | curl -sS -X POST \
  -H "Content-Type: application/json" \
  --data-binary @- \
  http://127.0.0.1:8092/api/command \
  > Plans/r8_e2e_web_command_step_response_2026-03-05.json
{"kind":"step","steps":3}
JSON

curl -sS http://127.0.0.1:8092/api/state > Plans/r8_e2e_web_state_after_step_2026-03-05.json

cat <<'JSON' | curl -sS -X POST \
  -H "Content-Type: application/json" \
  --data-binary @- \
  http://127.0.0.1:8092/api/capture \
  > Plans/r8_e2e_web_capture_json_2026-03-05.json
{}
JSON

curl -sS http://127.0.0.1:8092/api/captures > Plans/r8_e2e_web_captures_index_2026-03-05.json

cat <<'JSON' | curl -sS -X POST \
  -H "Content-Type: application/json" \
  --data-binary @- \
  http://127.0.0.1:8092/api/capture/screenshot \
  > Plans/r8_e2e_web_capture_screenshot_2026-03-05.json
{"image_base64":"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO7nL8sAAAAASUVORK5CYII=","mime_type":"image/png"}
JSON

curl -sS http://127.0.0.1:8092/api/captures > Plans/r8_e2e_web_captures_index_after_screenshot_2026-03-05.json
```

Expected checkpoints:
- `/api/meta`: `current_scenario = "drone_patrol"`, `agents = 10`
- `/api/state` after step processing: `tick >= 3`
- First captures index length: `1`
- Second captures index length: `2`

## 3) Produced Artifacts

- `Plans/runs/r8-e2e-20260305/run.json`
- `Plans/r8_e2e_cli_save_2026-03-05.json`
- `Plans/r8_e2e_cli_load_2026-03-05.json`
- `Plans/r8_e2e_web_meta_2026-03-05.json`
- `Plans/r8_e2e_web_command_step_response_2026-03-05.json`
- `Plans/r8_e2e_web_state_after_step_2026-03-05.json`
- `Plans/r8_e2e_web_capture_json_2026-03-05.json`
- `Plans/r8_e2e_web_captures_index_2026-03-05.json`
- `Plans/r8_e2e_web_capture_screenshot_2026-03-05.json`
- `Plans/r8_e2e_web_captures_index_after_screenshot_2026-03-05.json`
- `Plans/captures_r8_2026-03-05/capture_drone_patrol_tick3_20260305T054103920828Z.json`
- `Plans/captures_r8_2026-03-05/capture_drone_patrol_tick3_20260305T054103925728Z.png`
- `Plans/captures_r8_2026-03-05/capture_drone_patrol_tick3_20260305T054103925728Z_screenshot.json`

## 4) SHA-256 Hashes

- `e349e092f06937d4312a628af580de7005c1aaf8302c1e34e380f8aab258ec3d`  `Plans/runs/r8-e2e-20260305/run.json`
- `b99f3bafc3d9e7e0d215d9bc7b2fafb80813409fe1437c47cfdb2e148141f745`  `Plans/r8_e2e_cli_save_2026-03-05.json`
- `5d3c8fe1b23d21c9200b687d7b01dfe8541c455c2ad505551d9f6e12c48ed164`  `Plans/r8_e2e_cli_load_2026-03-05.json`
- `4a3359059cce80b1786f2a7bc7ca2486cba0b9d66c51104035a00a9fe9dbe39f`  `Plans/r8_e2e_web_meta_2026-03-05.json`
- `d5fb76f1e7a24ea527ae5c6c6cb97600786221bfedf71f42de909e20abdefcf4`  `Plans/r8_e2e_web_command_step_response_2026-03-05.json`
- `90a8ba38462b0516e75506dc699272601ba8116aa9cfbae0f468c9e2dad3a1d5`  `Plans/r8_e2e_web_state_after_step_2026-03-05.json`
- `a88d3c0cf5da69dd3ea2e33b3e44c60745f0f6dace47345cfb9d92ee8df3b6ae`  `Plans/r8_e2e_web_capture_json_2026-03-05.json`
- `6c3c156f32eeeb02e12b446c5cbdd3696e24ae150046b960b5d515c7767bb59c`  `Plans/r8_e2e_web_captures_index_2026-03-05.json`
- `c1adff269850b716f42b2aac6ffedbf8b48b49e097c0dcc0d0afa142a9498cd1`  `Plans/r8_e2e_web_capture_screenshot_2026-03-05.json`
- `d4f3a0e0b6e5652a3b1731022f444cac1bc7441c1c63018722befd9a21adf79c`  `Plans/r8_e2e_web_captures_index_after_screenshot_2026-03-05.json`
- `7c91acf4af17e23e4b6ad431b9b265fff61da41f5b2b3a4f89cbd21aee8a1b8e`  `Plans/captures_r8_2026-03-05/capture_drone_patrol_tick3_20260305T054103920828Z.json`
- `e853151de645f9e72519e5f922c8ddf5eb61e228e7427efcece6d0a92321737a`  `Plans/captures_r8_2026-03-05/capture_drone_patrol_tick3_20260305T054103925728Z.png`
- `dd3b525ee336b0f9c3ba1bd7d4a8ae0ce36c7abb1e56ece759238b98b5ec0c1d`  `Plans/captures_r8_2026-03-05/capture_drone_patrol_tick3_20260305T054103925728Z_screenshot.json`

## 5) Notes

- The `/api/command` response can reflect pre-step state (`tick = 0`) because step execution is consumed asynchronously by the background loop.  
  Use `/api/state` polling for progression checks (`tick >= 3` in this bundle).
