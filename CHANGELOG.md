# Changelog

All notable changes to this project are documented in this file.

## [0.1.2] - 2026-03-04

### Release
- Promote release candidate `0.1.2rc2` to stable `0.1.2`.
- No additional code changes beyond the `0.1.2rc2` tested baseline.

### Post-0.1.2 (main branch, unreleased)

#### Added
- JSON file persistence adapter (`sim_framework.adapters.persistence.JsonFilePersistence`) implementing `PersistencePort` save/load for run manifests and snapshots.
- Adapter-level tests covering protocol conformance, round-trip integrity, serialized bundle contract, and missing-run errors.
- New `drone_patrol` scenario with registry integration and dedicated scenario/integration tests.
- R5 drone reproducibility bundle in `Plans/` with adapter-backed save/load artifacts and scenario-aware ON/OFF benchmark outputs.
- R4 physics reproducibility bundle in `Plans/` demonstrating boundary mode impact (`clamp` vs `wrap`) with deterministic artifacts.
- R3 headless configuration path via `--agent-spec-json` with scenario-level schema validation and reproducibility artifacts.

#### Changed
- Public CLI now supports persistence flows:
  - `--save-run-id` to persist a run bundle.
  - `--load-run-id` to load and summarize a persisted run.
  - `--persistence-root` to control storage location.
- App CLI tests extended with save/load success paths and persistence-specific argument/error coverage.
- Benchmark tooling is now scenario-aware (`--scenario`) for both `benchmark_headless.py` and `run_perf_snapshot_toggle.py`.
- CLI scenario initialization now dispatches agent-count parameter by scenario signature (`num_ants` / `num_drones` / `num_agents`) to support multi-scenario execution.
- CLI now exposes `--boundary-mode` (`clamp`/`wrap`) and passes physics mode into scenario behavior runners.
- CLI now supports scenario-compatible custom `StateMachineAgentSchemaSpec` payloads through `--agent-spec-json`.

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
- `scripts/check_import_flow.py` to enforce layer direction: `contracts <- core <- scenarios <- app`.
