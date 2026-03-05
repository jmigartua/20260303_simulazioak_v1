# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Added
- JSON file persistence adapter (`sim_framework.adapters.persistence.JsonFilePersistence`) implementing `PersistencePort` save/load for run manifests and snapshots.
- Adapter-level tests covering protocol conformance, round-trip integrity, serialized bundle contract, and missing-run errors.
- New `drone_patrol` scenario with registry integration and dedicated scenario/integration tests.
- R5 drone reproducibility bundle in `Plans/` with adapter-backed save/load artifacts and scenario-aware ON/OFF benchmark outputs.
- R4 physics reproducibility bundle in `Plans/` demonstrating boundary mode impact (`clamp` vs `wrap`) with deterministic artifacts.
- R3 headless configuration path via `--agent-spec-json` with scenario-level schema validation and reproducibility artifacts.
- R6/R9 roadmap artifact in `Plans/r6_r9_ui_desktop_roadmap_2026-03-04.md` defining milestones for web UI, desktop packaging, and CI hardening.
- M1 visible app shell (`sim_framework.app.web`) with browser canvas, control API (`play/pause/step/reset/set_speed/seek`), scenario switching without restart, and live state polling.
- M2 step-1 renderer upgrade: PixiJS-backed drawing pipeline for the web shell with automatic canvas fallback.
- M2 rendering polish: scenario-specific visuals (drone waypoint path + glyphs, ant state coloring), signal-color mapping by field kind, and refresh-rate telemetry in UI.
- M2 runtime telemetry: API latency and tick-drift indicators added to web shell for render/state sync observability.
- M2 telemetry contract hardening: `/api/meta` now exposes `step_interval_ms` and `target_tick_hz`; HTTP smoke tests now cover invalid scenario and invalid command payload error paths.
- M2 timing-behavior contract tests: web shell now validates that `play` advances ticks over wall-clock time and `pause` stabilizes progression.
- M2 exit artifact: `Plans/m2_rendering_readiness_2026-03-05.md` documenting acceptance checklist, reproducibility commands, and M3 entry criteria.
- M3 slice-1 capture/export workflow: `/api/capture` endpoint + `Capture JSON` UI action writes timestamped JSON artifacts to `--capture-root`.
- M3 slice-2 replay timeline interactions: state payload now includes `timeline.max_tick_reached`; UI adds slider seek, rewind-50, and jump-to-latest controls.
- M3 slice-3 capture management parity: `/api/captures` index + `/api/capture/delete` endpoint, plus deterministic `capture_digest` metadata and UI refresh/delete actions.
- M3 slice-4 screenshot parity: `/api/capture/screenshot` accepts canvas PNG payloads, stores image + metadata bundle (`image_digest`, `bundle_digest`), and exposes `Capture PNG` in UI.
- Web runtime bridge (`sim_framework.adapters.web.runtime_bridge`) with scenario-aware composition and thread-safe command/state access.
- New console script entry point: `sim-web`.
- M1 tests for bridge command flow, scenario switching, and HTTP shell smoke behavior.

### Changed
- Public CLI now supports persistence flows:
  - `--save-run-id` to persist a run bundle.
  - `--load-run-id` to load and summarize a persisted run.
  - `--persistence-root` to control storage location.
- Scenario behavior runners now instantiate through `BehaviorRegistry`, making behavior contracts part of runtime execution (not test-only infrastructure).
- App CLI tests extended with save/load success paths and persistence-specific argument/error coverage.
- Benchmark tooling is now scenario-aware (`--scenario`) for both `benchmark_headless.py` and `run_perf_snapshot_toggle.py`.
- CLI scenario initialization now dispatches agent-count parameter by scenario signature (`num_ants` / `num_drones` / `num_agents`) to support multi-scenario execution.
- CLI now exposes `--boundary-mode` (`clamp`/`wrap`) and passes physics mode into scenario behavior runners.
- CLI now supports scenario-compatible custom `StateMachineAgentSchemaSpec` payloads through `--agent-spec-json`.
- CLI JSON output now standardizes on `run.agents`; legacy `run.ants` has been removed. Input alias `--ants` remains supported for backward compatibility.

## [0.1.2] - 2026-03-04

### Release
- Promote release candidate `0.1.2rc2` to stable `0.1.2`.
- No additional code changes beyond the `0.1.2rc2` tested baseline.

## [0.1.2rc2] - 2026-03-04

### Added
- Benchmark smoke workflow (`.github/workflows/benchmark-smoke.yml`) with artifact upload for snapshot ON/OFF outputs.
- Wheel packaging CI job in `.github/workflows/ci.yml` (build, clean install, `sim-run` smoke check).
- Tooling contract tests for benchmark artifact schema and markdown summary generation.
- Release consistency guardrail script (`scripts/check_release_consistency.py`) and tests.

### Changed
- Developer workflow hardening with `make release-check` now validating release consistency before tests/package checks.
- App CLI test suite expanded for `--json-out` persistence behavior and argument error paths.

## [0.1.1] - 2026-03-04

### Added
- Public app runtime mode with `RuntimeMode` (`interactive`/`headless`) and immutable `RuntimeConfig`.
- CLI composition root at `sim_framework.app.cli` with `sim-run` entry point.
- Post-engine optimization A/B benchmark evidence for snapshot events ON vs OFF.

### Changed
- Engine tick update path now avoids full per-tick deep-copy of state while preserving topology isolation semantics.
- Benchmark and docs now include explicit snapshot-toggle comparisons.

### Infrastructure
- CI workflow on Python 3.11 for editable install, test execution, and architectural import-flow checks.
- `scripts/check_import_flow.py` to enforce layer direction: `contracts <- core <- scenarios <- adapters <- app`.
