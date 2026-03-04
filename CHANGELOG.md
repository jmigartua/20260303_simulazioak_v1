# Changelog

All notable changes to this project are documented in this file.

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
