# Changelog

All notable changes to this project are documented in this file.

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
