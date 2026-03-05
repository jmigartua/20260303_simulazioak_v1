# M2 Rendering Readiness (Exit Gate)

**Date:** 2026-03-05  
**Scope:** M2 (PixiJS-based rendering + visual parity hardening for web shell)  
**Baseline commit:** `b091a20`

---

## 1. M2 Delivered Capabilities

1. PixiJS rendering path in web shell with automatic canvas fallback.
2. Visual layers for colony, food, agents, and signal overlay.
3. Scenario-specific visuals:
   - ants: carrying-state color differentiation
   - drone patrol: waypoint path + drone glyphs
4. Live controls:
   - play, pause, step, reset
   - speed set, seek tick, rewind 10
   - scenario switch without restart
5. Runtime telemetry:
   - refresh rate (`Refresh Hz`)
   - API latency (`API latency ms`)
   - tick drift (`Tick drift`)
   - target tick contract (`target_tick_hz` from `/api/meta`)

---

## 2. Acceptance Checklist (M2)

All checks below pass at baseline commit `b091a20`:

1. `python -m pytest -q` passes (120 tests).
2. Web shell HTTP smoke verifies:
   - HTML controls and telemetry labels
   - `/api/meta` contract fields
   - scenario switch endpoint
   - invalid scenario/command error paths (`400`)
3. Timing contract test verifies:
   - `play` advances ticks over wall-clock time
   - `pause` stabilizes ticks with race-tolerant bound
4. Import-flow guardrail passes (`0 violations`).
5. Release consistency guardrail passes.

---

## 3. Repro Steps

```bash
uv venv --python 3.11
source .venv/bin/activate
uv pip install -e .[dev]

# Run full validation gates
.venv/bin/python -m pytest -q
.venv/bin/python scripts/check_import_flow.py
.venv/bin/python scripts/check_release_consistency.py

# Launch web shell
.venv/bin/python -m sim_framework.app.web --scenario ants_foraging --agents 40 --width 30 --height 30
```

---

## 4. Residual M2 Risks (Accepted for M3 Transition)

1. PixiJS currently loaded from CDN (offline constraints unresolved).
2. No full browser automation suite yet (HTTP-level smoke + integration only).
3. Telemetry is informational; no alert thresholds enforced yet.

---

## 5. M3 Entry Criteria (Now Unblocked)

1. Keep existing control surface stable.
2. Add capture/export workflow (M3 target).
3. Add deeper replay timeline interactions.
4. Add stronger browser-level regression coverage.
