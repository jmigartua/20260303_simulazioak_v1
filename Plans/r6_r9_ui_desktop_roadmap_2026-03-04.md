# R6/R9 UI + Desktop Roadmap (Post-v0.1.2)

**Date:** 2026-03-04  
**Scope:** Requirement R6 (modern performant UI) and R9 (Linux desktop + web-like app)  
**Baseline:** `v0.1.2` backend stable (`110/110` tests at planning time)

---

## 1. Objective

Deliver a visual simulation client that preserves current backend guarantees:

1. Deterministic replay for same seed/scenario/commands.
2. Runtime safety and isolation behavior.
3. Scenario portability (`ants_foraging`, `drone_patrol`).

---

## 2. Target Architecture

Use existing layered architecture and add adapter-facing UI packages:

1. `sim_framework/adapters/web/`
   - Browser-facing rendering and input adapter.
2. `sim_framework/adapters/desktop/`
   - Linux desktop shell adapter (web view + packaging glue).
3. `sim_framework/app/`
   - Keep `sim-run` as composition root; add app mode selector for headless/web/desktop.

Core, contracts, and scenarios remain UI-agnostic.

---

## 3. Milestones

### M1: UI adapter skeleton

1. Add adapter ports/events mapping for:
   - play/pause/step/reset/seek/rewind controls
   - snapshot stream subscription
2. Implement a minimal browser app shell that can connect to runtime events.

Acceptance:
1. App boots and renders placeholder scene.
2. Control actions reach engine command queue.

### M2: PixiJS simulation rendering

1. Render agents, resources, and pheromone/signal overlays.
2. Add scenario switch support (ants/drone) in UI.

Acceptance:
1. Visual state updates match headless tick progression.
2. UI can run both scenarios without backend code changes.

### M3: Playback + capture parity

1. Expose rewind/seek timeline controls in UI.
2. Implement frame/screenshot export path in web adapter.

Acceptance:
1. Rewind seeks to target tick and resumes correctly.
2. Screenshot export produces deterministic capture metadata bundle.

### M4: Linux desktop packaging

1. Wrap web client in Linux desktop shell.
2. Add packaging script (AppImage or equivalent) and smoke test.

Acceptance:
1. Desktop app launches on clean Linux environment.
2. Scenario run + control loop works without developer tooling.

### M5: CI + release hardening for UI line

1. Add frontend lint/test/build jobs and desktop smoke job.
2. Extend release consistency checks for UI/desktop artifacts.

Acceptance:
1. CI validates headless + UI stacks.
2. Release candidate includes backend + UI + desktop checks.

---

## 4. Test Strategy Additions

1. UI contract tests:
   - command dispatch mapping
   - event payload parsing
2. Integration tests:
   - runtime bridge (`sim-run` app mode -> UI adapter)
   - scenario switch + rewind control path
3. Desktop smoke tests:
   - launch + one scripted scenario run

---

## 5. Risks and Mitigations

1. Risk: UI frame loop breaks determinism assumptions.
   - Mitigation: Keep engine tick authoritative; UI only consumes snapshots/events.
2. Risk: Desktop packaging drift across Linux distros.
   - Mitigation: Pin packaging toolchain and run smoke on CI Linux image.
3. Risk: Performance regression with large agent counts.
   - Mitigation: Keep benchmark harness scenario-aware and compare UI-on/off overhead.

---

## 6. Definition of Done (R6/R9 implemented scope)

1. Browser UI supports both scenarios with stable controls.
2. Linux desktop package runs end-to-end on target environment.
3. Playback controls include rewind/seek and capture output.
4. CI includes UI/desktop guardrails alongside existing backend checks.
5. Evidence matrix rows R6/R9 can be promoted from `In progress` to `Done`.

---

## 7. Deliverables Checklist

1. Architecture diagram update with new adapters.
2. Demo script for ants + drone in UI and desktop shell.
3. Reproducibility bundle including command script, seed, and capture output.
4. Updated thesis evidence links (matrix + final report).
