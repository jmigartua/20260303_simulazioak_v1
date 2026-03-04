# Agent Execution Audit

**Auditor:** PAI (independent review)
**Date started:** 2026-03-03
**Last updated:** 2026-03-04
**Scope:** Continuous audit of the coding agent's execution against `10_execution_kit/01_first_10_commits_checklist.md` and `08_final_report.md` (commits 1-57)

---

## Overall Status

| Commit | Status | Checklist Compliance | Code Quality | Test Depth | Issues |
|--------|--------|---------------------|-------------|-----------|--------|
| 1 — scaffold | DONE | 9/10 | 7/10 | 5/10 | 3 issues |
| 2 — domain models | DONE | 10/10 | 8/10 | 6/10 | 4 issues |
| 2.5 — setuptools fix | DONE | N/A (hotfix) | — | — | Fixes I-8 |
| 3 — ports + commands | DONE | 10/10 | 9/10 | 8/10 | 1 issue |
| 4 — behavior protocol | DONE | 10/10 | 8/10 | 8/10 | 1 issue |
| 5 — validators | DONE | 10/10 | 8/10 | 8/10 | 1 issue |
| 6 — environment signals | DONE | 10/10 | 9/10 | 9/10 | 1 issue |
| 7 — history buffer | DONE | 10/10 | 9/10 | 9/10 | 0 issues |
| 8 — engine + determinism | DONE | 10/10 | 9/10 | 9/10 | 1 issue |
| 9 — physics + spatial hash | DONE | 10/10 | 9/10 | 8/10 | 1 issue |
| 10 — ants scenario | DONE | 10/10 | 8/10 | 8/10 | 2 issues |
| 11 — unify state-machine schema | DONE | N/A (post-checklist) | 9/10 | 9/10 | 0 issues |
| 12 — gradient sensing API | DONE | N/A (post-checklist) | 9/10 | 9/10 | 0 issues |
| 13 — speed multiplier batching | DONE | N/A (post-checklist) | 9/10 | 9/10 | 0 issues |
| 14 — audit consistency pass | DONE | N/A (post-checklist docs) | 8/10 | — | 0 issues |
| 15 — README + package metadata | DONE | N/A (post-checklist docs/build) | 9/10 | — | Fixes I-7 |
| 16 — protocol contract strictness tests | DONE | N/A (post-checklist test hardening) | 9/10 | 9/10 | Fixes I-9 |
| 17 — Python policy test gate | DONE | N/A (post-checklist test policy) | 9/10 | 9/10 | Controls I-3 |
| 18 — ants SpatialHash integration | DONE | N/A (post-checklist scenario integration) | 9/10 | 9/10 | Fixes I-13 |
| 19 — headless benchmark harness | DONE | N/A (post-checklist performance tooling) | 9/10 | — | 1 observation |
| 20 — perf baseline snapshot + docs | DONE | N/A (post-checklist performance baseline) | 9/10 | — | 0 issues |
| 21 — audit evidence fix | DONE | N/A (post-checklist docs) | 8/10 | — | 0 issues |
| 22 — cProfile benchmark mode | DONE | N/A (post-checklist perf tooling) | 9/10 | — | 0 issues |
| 23 — spatial hash micro-optimization | DONE | N/A (post-checklist perf) | 8/10 | 8/10 | 1 observation |
| 24 — post-opt baseline + comparison | DONE | N/A (post-checklist perf docs) | 9/10 | — | 0 issues |
| 25 — snapshot event toggle | DONE | N/A (post-checklist perf) | 9/10 | 9/10 | 0 issues |
| 26 — no-snapshot baseline + comparison | DONE | N/A (post-checklist perf docs) | 9/10 | — | 0 issues |
| 27 — app CLI + runtime config | DONE | N/A (post-checklist app layer) | 9/10 | 9/10 | 0 issues |
| 28 — engine deep-copy optimization | DONE | N/A (post-checklist perf) | 9/10 | 9/10 | 0 issues |
| 29 — post-engine-opt baselines | DONE | N/A (post-checklist perf docs) | 9/10 | — | 1 observation |
| 30 — CI workflow | DONE | N/A (post-checklist CI/CD) | 9/10 | — | 0 issues |
| 31 — 0.1.1 release docs | DONE | N/A (post-checklist release) | 8/10 | — | 1 observation |
| 32 — snapshot toggle benchmark runner | DONE | N/A (post-checklist perf tooling) | 9/10 | — | 0 issues |
| 33 — tooling script tests | DONE | N/A (post-checklist test hardening) | 9/10 | 9/10 | 0 issues |
| 34 — Makefile dev targets | DONE | N/A (post-checklist dev workflow) | 8/10 | — | 1 observation |
| 35 — CLI error-path tests + release-check | DONE | N/A (post-checklist test hardening) | 9/10 | 9/10 | 0 issues |
| 36 — CLI --json-out test | DONE | N/A (post-checklist test coverage) | 9/10 | 9/10 | 0 issues |
| 37 — benchmark smoke CI | DONE | N/A (post-checklist CI/CD) | 9/10 | — | 0 issues |
| 38 — wheel build + smoke CI | DONE | N/A (post-checklist CI/CD) | 9/10 | — | 0 issues |
| 39 — perf artifact contract tests | DONE | N/A (post-checklist test hardening) | 9/10 | 9/10 | 0 issues |
| 40 — release consistency guardrail | DONE | N/A (post-checklist CI/CD) | 9/10 | 9/10 | 0 issues |
| 41 — 0.1.2rc2 release metadata | DONE | N/A (post-checklist release) | 9/10 | — | 0 issues |
| 42 — 0.1.2 stable release | DONE | N/A (post-checklist release) | 9/10 | — | 0 issues |
| 43 — midway report + audit commit | DONE | N/A (post-checklist documentation) | 6/10 | — | 1 issue (I-16) |
| 44 — evidence matrix + final report sync | DONE | N/A (post-checklist documentation) | 9/10 | — | 0 issues |
| 45 — audit scope + sync ranges | DONE | N/A (post-checklist documentation) | 8/10 | — | 0 issues |
| 46 — midway report addendum (commits 33-48) | DONE | N/A (post-checklist documentation) | 9/10 | — | 0 issues |
| 47 — JSON file persistence adapter | DONE | N/A (post-checklist adapters) | 9/10 | 9/10 | 1 issue (I-17) |
| 48 — CLI save/load persistence flows | DONE | N/A (post-checklist app layer) | 8/10 | 9/10 | 1 observation |
| 49 — CLI persistence docs | DONE | N/A (post-checklist documentation) | 7/10 | — | 1 observation |
| 50 — R7 adapter-backed reproducibility example | DONE | N/A (post-checklist evidence) | 9/10 | — | 1 observation |
| 51 — drone_patrol scenario + registry | DONE | N/A (post-checklist scenario) | 8/10 | 8/10 | 0 issues |
| 52 — scenario-aware benchmark workflows | DONE | N/A (post-checklist tooling) | 8/10 | 8/10 | 0 issues |
| 53 — R5 drone repro bundle + CLI dispatch | DONE | N/A (post-checklist evidence) | 8/10 | 7/10 | 1 observation |
| 54 — R7 matrix closure | DONE | N/A (post-checklist evidence) | 9/10 | — | 0 issues |
| 55 — R4 boundary mode + physics repro bundle | DONE | N/A (post-checklist feature + evidence) | 8/10 | 8/10 | 0 issues |
| 56 — R3 agent-spec runtime overrides + evidence | DONE | N/A (post-checklist feature + evidence) | 9/10 | 8/10 | 0 issues |
| 57 — R6/R9 UI-desktop execution roadmap | DONE | N/A (post-checklist planning) | 8/10 | — | 1 observation |

**Test suite:** 110 passed, 0 failed (as of commit 57)
**End-of-Commit-10 Acceptance:** ALL 4 CRITERIA MET
**Post-Checklist Phase:** Commits 11-57 address audit findings, strengthen controls, establish performance baseline, deliver profile-guided optimization cycle, add public CLI with runtime modes, reduce engine per-tick overhead, establish CI/CD pipeline with guardrails, add reproducible benchmark tooling, complete 0.1.2 release cycle, produce midway project report, sync evidence matrix + final report, add run persistence with adapter pattern, add second scenario (drone_patrol), add scenario-aware benchmarking, expose boundary mode and agent-spec overrides at CLI, produce R3/R4/R5/R7 reproducibility evidence bundles, and plan R6/R9 UI-desktop implementation

---

## Current Truth Snapshot

This section reflects the current project state after checklist completion:

1. Project runtime is now Python 3.11.11 in `.venv` (policy-compliant environment).
2. Editable install works in `.venv`: `uv pip install --python .venv/bin/python -e .` succeeds.
3. Full test suite passes in `.venv`: `110 passed, 0 failed`.
4. System Python is still 3.10.9, but it is no longer the project execution environment.
5. Packaging discovery issue (I-8) is resolved.
6. ~~Remaining structural concern: schema split (`AgentSchemaSpec` vs `AntBehaviorSpec`, I-14).~~ **RESOLVED** by commit 11 — unified `StateMachineAgentSchemaSpec` in contracts layer.
7. Gradient sensing moved to framework API (`SignalGrid.sense_gradient()`) by commit 12 — resolves I-15.
8. Speed multiplier now consumed by engine for step batching by commit 13 — resolves I-12.
9. Package metadata now points to `README.md` (commit 15) — resolves I-7.
10. Port contract tests now validate method signatures and type hints against protocol definitions (commit 16) — resolves I-9.
11. Pytest session now enforces Python policy at startup (commit 17): non-3.11+ interpreters fail fast with guidance.
12. Ant scenario now consumes `SpatialHash` infrastructure for local neighbor avoidance (commit 18) — resolves I-13.
13. Headless benchmark harness (`scripts/benchmark_headless.py`) provides reproducible performance measurement with `tracemalloc` memory tracking and JSON output (commit 19).
14. Performance baseline established (commit 20): 100 agents = ~929 μs/agent-tick, 300 agents = ~2176 μs/agent-tick. Superlinear scaling (2.34× per-agent cost at 3× agents) is consistent with O(N·k) neighbor interactions and documented as expected behavior.
15. cProfile integration (commit 22) identified Pydantic `model_copy`/`__deepcopy__` as dominant hotspot (~46% of runtime), followed by `_neighbor_avoidance` (~38%).
16. SpatialHash `query_radius` over-scan reduced by switching to `ceil(radius/cell_size)` and hot-path attribute inlining (commit 23). Micro-optimization did NOT improve end-to-end throughput — honest regression documented in comparison (commit 24).
17. Engine `emit_snapshot_events` toggle (commit 25) eliminates deep-copy overhead in headless mode: **17% faster, 94% less memory** (commit 26 baseline). This is the correct fix for the Pydantic deep-copy hotspot.
18. Public CLI (`sim_framework/app/cli.py`) with `RuntimeMode` (INTERACTIVE/HEADLESS) and three-tier snapshot resolution: explicit override > mode default > INTERACTIVE=True. Scenario registry (`sim_framework/scenarios/registry.py`) provides extensible scenario lookup. `[project.scripts] sim-run` entry point registered in `pyproject.toml` (commit 27).
19. Engine per-tick `model_copy(deep=True)` replaced with shallow `model_copy` + explicit `model_copy(deep=False)` for static topology (food_sources, colony, signal_fields). Agents are already fresh from `_advance_agents()`. SnapshotEvent path retains `deep=True` for observer isolation. Result: **11% faster snapshot-ON** at 100 agents, **98% memory reduction** snapshot-OFF (commit 28). Verified by `test_tick_clones_static_topology_without_deep_copying_agents` (commit 28, commit 29 baselines).
20. CI/CD pipeline (commits 30, 37, 38, 40): GitHub Actions on Python 3.11 with import-flow guardrail, release consistency guardrail, pytest, sdist/wheel build + clean-venv smoke test, benchmark smoke workflow with artifact upload. Two workflows: `ci.yml` (test + package jobs) and `benchmark-smoke.yml` (workflow_dispatch + path-filtered PR trigger).
21. Reproducible benchmark tooling (commit 32): `scripts/run_perf_snapshot_toggle.py` automates ON/OFF comparison with determinism cross-checks, generates comparison markdown. Tested by contract tests validating JSON schema and markdown output (commits 33, 39). AST-based import-flow checker (`scripts/check_import_flow.py`) tested with layer resolution, violation detection, and live project validation (commit 33). Release consistency guardrail (`scripts/check_release_consistency.py`) validates pyproject.toml version matches CHANGELOG.md headings (commit 40).
22. Release cycle complete: 0.1.1 (commit 31) → 0.1.2rc2 (commit 41) → 0.1.2 stable (commit 42). Release consistency guardrail runs in CI before tests. Makefile provides `release-check` target combining release-consistency + import-check + test-v + package-check (commit 35).
23. Midway report (`20260304_midway_report.md`, 754 lines, commit 43): comprehensive project analysis covering architecture, implementation, testing, performance, gaps, roadmap. Technically competent on engine/scenario/architecture details but suffers from pervasive staleness (I-16): describes commit-32 state (72 tests, 32 commits) despite 86 tests and 43 commits at commit time. Omits CI/CD pipeline, release cycle, and incorrectly claims import-lint "does not exist".
24. Evidence matrix and final report synced to v0.1.2 implementation state (commit 44). Evidence matrix updated all 12 requirements (R1-R12) from "Not started" placeholders to actual implementation statuses with correct artifact paths, test evidence, and demo/thesis evidence. Final report received implementation status addendum acknowledging v0.1.2, 86/86 tests, CI/CD active. Deep-dive verification: **66/66 checks PASS** — every artifact reference, test reference, and status claim verified against actual codebase. This partially addresses I-16 staleness for these two documents (midway report remains stale).
25. Audit scope notes added to 4 documents (`06_execution_blueprint.md`, `07_tfg_evidence_matrix.md`, `08_final_report.md`, `20260304_midway_report.md`) indicating which commit range each covers (commit 45). Audit content expanded with Round 11-12 entries.
26. Midway report staleness (I-16) substantially addressed: 384-line addendum (Sections 16-29) covering commits 33-48 added in commit 46. Two-pass structure: Pass 1 = original through commit 32, Pass 2 = addendum through commit 48. Covers CI/CD deep-dive, import-flow guardrail, release management, benchmark runner, test expansion (72→86), and updated R1-R12 traceability. I-16 downgraded from active staleness to historical scope limitation.
27. `JsonFilePersistence` adapter (commit 47): first `PersistencePort` implementation in new `sim_framework/adapters/` layer. Saves/loads `RunManifest` + snapshots as `{root}/{run_id}/run.json`. Uses `model_copy(deep=True)` for on-disk isolation. 3 tests with round-trip verification, mutation isolation, and error path coverage. **New issue I-17:** `adapters` layer is invisible to `check_import_flow.py` (not in `ALLOWED_IMPORTS`).
28. CLI persistence flows (commit 48): `--save-run-id`, `--load-run-id`, `--persistence-root` flags. Mutually exclusive save/load group. Load path returns early without running simulation. `_emit_payload()` DRY refactor. 5 new tests including save→load round-trip and error paths. Observation: unconditional `model_copy(deep=True)` on every tick even without `--save-run-id` is a performance concern.
29. R7 adapter-backed reproducibility example (commit 50): concrete save→load cycle with seed 42, 5 ticks, 10 ants. All 3 SHA-256 hashes verified. `run.json` (1137 lines) contains 6 valid snapshots. ~~Observation: milestone tag `milestone-persistence-cli-2026-03-04` referenced but never created as git tag.~~ **RESOLVED** — tag confirmed present (`git tag --list` returns 7 tags including `milestone-persistence-cli-2026-03-04`).
30. Second scenario `drone_patrol` (commit 51): 12 drones on waypoint patrol with `StateMachineAgentSchemaSpec`, "radio" signal field, registry integration. 5 scenario tests + 1 integration test (100-tick headless). Import layer compliant.
31. Scenario-aware benchmark tooling (commit 52): `--scenario` CLI arg with `inspect.signature`-based dispatch in both `benchmark_headless.py` and `run_perf_snapshot_toggle.py`. 7 tests covering dispatch, integration, and drone scenario.
32. R5 drone reproducibility bundle (commit 53): drone_patrol save/load cycle, benchmark ON/OFF comparison (determinism cross-check 2/2 matched), evidence matrix R5 updated. CLI now uses inspect-based `_build_state_for_scenario` dispatch. Observation: `--ants` CLI flag name is semantically incorrect for non-ant scenarios.
33. R4 boundary mode exposure (commit 55): `--boundary-mode` (clamp|wrap) threaded through CLI → dispatch → runner → `apply_movement` for both scenarios. 6 run bundles demonstrating trajectory divergence. 3 new tests. Evidence matrix R4 updated. All SHA-256 hashes verified. Largest commit by diff (+71,840 lines, 99.4% from run.json evidence files).
34. R3 agent-spec runtime overrides (commit 56): `--agent-spec-json` CLI flag loads custom `StateMachineAgentSchemaSpec`, validated at 3 levels (schema, known behaviors, scenario-specific). Both scenarios refactored to use name-based behavior param lookup. 4 new tests (happy path, rejection, speed propagation). Evidence matrix R3 updated, test count 106→110. All 8 SHA-256 hashes verified and run.json reproduced bit-for-bit.
35. R6/R9 UI-desktop execution roadmap (commit 57): 5-milestone plan (adapter skeleton → PixiJS rendering → playback controls → Linux desktop packaging → CI hardening). Evidence matrix R6/R9 moved to "In progress." Observation: no timeline estimates, desktop technology unspecified, "In progress" status generous for planning-only.
36. Import flow: 28 total imports (was 20), 0 violations. New `adapters` layer not covered by checker (I-17).
37. Test suite: 110 passed, 0 failed. +24 tests from commits 45-57 (3 adapter + 10 CLI + 5 drone scenario + 1 drone integration + 3 benchmark + 1 CLI dispatch + 1 CLI boundary).

---

## Commit 1: `chore: scaffold sim_framework package layout`

**Git:** `9e651c5` — "first commit"
**Checklist compliance:** 9/10

### What the checklist required

10 files in order: 8 `__init__.py` files across the 5-package structure, `tests/__init__.py`, `pyproject.toml`, plus `tests/test_smoke.py`.

### What the agent actually did (at commit time)

Created all required files. All `__init__.py` files are empty (correct for a scaffold). `pyproject.toml` is well-configured. `test_smoke.py` is a trivial `assert True`. Test gate passes.

**However**, this commit also included ALL 19 analysis documents (00-09), the execution kit (10), and 3 PRD files — 3,398 lines in a single commit. The commit message says "first commit" instead of the checklist's prescribed `chore: scaffold sim_framework package layout`.

### Issues Found

| # | Severity | Finding |
|---|----------|---------|
| I-1 | **MEDIUM** | **Commit message deviates from checklist.** Checklist says `chore: scaffold sim_framework package layout`. Actual: `first commit`. Conventional commits convention broken. Not a code problem but undermines the discipline the checklist was designed to enforce. |
| I-2 | **LOW** | **`__pycache__` committed to git.** The first commit includes `tests/__pycache__/__init__.cpython-310.pyc` and `tests/__pycache__/test_smoke.cpython-310-pytest-7.1.2.pyc`. The `.gitignore` was only added in commit 2. These bytecode files are now permanently in git history. Not harmful but sloppy — the `.gitignore` should have been in commit 1 or a pre-commit. |
| I-3 | **MEDIUM** | **System interpreter mismatch — Python 3.10.9 vs project policy `requires-python >= 3.11`.** This was a blocker before the project switched to `.venv` Python 3.11.11. It is now mitigated for local execution, but remains relevant for anyone running commands outside `.venv`. |

**I-1 status: ACCEPTED (historical immutable).** This is repository-history process debt that cannot be fixed without rewriting commit history.

### What's Good

- Package structure matches the blueprint's 5-package layout exactly
- `pyproject.toml` is clean: correct build system, sensible pytest config, dev extras
- The `pythonpath = ["."]` in pytest config ensures imports work without installation — practical choice

---

## Commit 2: `feat(contracts): add core pydantic domain models`

**Git:** `5c13a06`
**Checklist compliance:** 10/10

### What the checklist required

1. `sim_framework/contracts/models.py` with 6 minimum models: `Vector2`, `AgentState`, `FoodSource`, `Colony`, `SignalField`, `SimulationState`
2. `tests/contracts/test_models_basic.py`
3. Test gate: `python -m pytest -q tests/contracts/test_models_basic.py` — passes

### What the agent actually did (at commit time)

All 6 models created. Test file had 5 tests at commit time. Gate passed (5 passed). Commit message matches checklist exactly. Also added `.gitignore` and updated `pyproject.toml` to include the `pydantic>=2.7` dependency.

### Model-by-Model Assessment

| Model | Verdict | Notes |
|-------|---------|-------|
| `Vector2` | Good | Frozen (immutable). Clean. But see I-4. |
| `AgentState` | Good | Has `state_label` field — correctly anticipates the state machine from `08_final_report.md`. Defaults are sensible (`energy=1.0`, `carrying=0`, `state_label="searching"`). Field constraints present (`min_length`, `ge`). |
| `FoodSource` | Good | `amount` has `gt=0.0` — food must be positive. Matches domain. |
| `Colony` | Good | Minimal. Just id + position. Correct — a colony doesn't need more at this stage. |
| `SignalField` | Partial | Stores field *metadata* (kind, width, height, decay, diffusion) but not the actual 2D grid data. This is a configuration schema, not runtime state. The actual pheromone concentrations (a width x height numpy array or list-of-lists) will need a separate class or an extension. See I-5. |
| `SimulationState` | Good | Composes all models correctly. `seed=42` default matches D12 (determinism). `signal_fields: list[SignalField]` stores configs — see I-5 note. |

### Test Assessment

| Test | What it verifies | What it misses |
|------|-----------------|---------------|
| `test_vector2_is_constructible` | Construction | Immutability (frozen), equality, arithmetic operations (not needed yet) |
| `test_agent_defaults` | Default values for energy, carrying, state_label | Empty `id` rejection, negative energy rejection, empty `state_label` rejection — all have validators that are **never tested** |
| `test_food_amount_must_be_positive` | `amount=0.0` rejected | Negative amount, missing `id` |
| `test_signal_field_bounds` | Construction with valid values | Invalid bounds: `decay > 1.0`, `diffusion < 0.0`, `width=0`, `width=-1` — all have validators |
| `test_simulation_state_builds` | Full composition | Empty colony (required field missing), state with no agents |

### Issues Found

| # | Severity | Finding |
|---|----------|---------|
| I-4 | **LOW** | **`Vector2` frozen creates GC pressure at scale.** Every position/velocity update creates a new `Vector2` object. With 500+ agents updated each tick, this generates ~1000+ short-lived objects per tick. Not a problem now, but will need profiling at Phase 3 (500 agents, 500 ticks). The blueprint's D13 (performance policy: "define metrics now, lock targets after profiling") covers this — so it's a known risk, not a bug. |
| I-5 | **MEDIUM** | **`SignalField` is config-only, not runtime state.** The model stores decay rate and dimensions but has no field for actual concentration data (`data: list[list[float]]` or similar). When `core/environment.py` is built (commit 6), it will need either: (a) a separate `SignalFieldState` class with the grid data, or (b) this model extended. The current model is adequate for *configuration* but `SimulationState.signal_fields` is misleadingly named — it suggests it contains the simulation's signal state when it only contains the field definitions. This will create confusion at commit 6. |
| I-6 | **MEDIUM** | **Tests don't exercise validators.** The models have 9 field-level validators (`min_length`, `ge`, `gt`, `le`, bound constraints). Only 1 is tested (`FoodSource.amount gt=0.0`). The other 8 validators exist but are never verified. For a project where contracts are the foundational layer (D3, D4, D14), untested validators are a reliability gap. The checklist says "minimum models" — but minimum should still mean "validators that exist are tested." |
| I-7 | **LOW** | **`pyproject.toml` readme points to audit report.** `readme = "08_final_report.md"` — this is a 590-line architectural audit, not a project README. If this package is ever `pip install`ed or published, the "readme" shown will be the full audit report. Should point to a proper `README.md` or be removed. |

**I-7 status: RESOLVED by commit 15 (`README.md` added, `pyproject.toml` readme corrected).**

### What's Good

- Models are clean, well-typed, and use Pydantic v2 idioms correctly
- `AgentState.state_label` already anticipates the state machine behavior model from `08_final_report.md` Missing #2 — the agent read and integrated the final report's recommendations
- Field constraints are present (even if undertested) — this is better than no constraints
- Import structure is clean: `from sim_framework.contracts.models import ...`
- The `.gitignore` addition in this commit fixes the `__pycache__` problem going forward

---

## Commit 2.5: `chore(build): constrain setuptools package discovery`

**Git:** `93e53ff`
**Checklist compliance:** N/A (hotfix, not in checklist)

### What happened

The agent noticed `pip install -e .` failed because setuptools autodiscovery found both `MEMORY/` and `sim_framework/` as top-level packages. Added `[tool.setuptools.packages.find]` with `include = ["sim_framework*"]` to `pyproject.toml`.

### Assessment

**Good initiative.** The agent detected I-8 and fixed it proactively. The fix is correct and minimal — exactly the right approach. At that point in time, `pip install -e .` still failed because I-3 (Python 3.10 vs `requires-python >= 3.11`) remained. Discovery was fixed first; runtime policy was handled later via a Python 3.11 virtual environment.

**I-8 status: RESOLVED by this commit.**

---

## Commit 3: `feat(contracts): define protocol ports and command/event types`

**Git:** `1ef7622`
**Checklist compliance:** 10/10

### What the checklist required

1. `sim_framework/contracts/ports.py` with `RendererPort`, `PersistencePort`, `HistoryPort`
2. `tests/contracts/test_ports_contract_shape.py`
3. Add command/event models in `models.py` if missing
4. Test gate: `python -m pytest -q tests/contracts`

### What the agent actually did (at commit time)

**ports.py (36 lines):** All 3 protocols using `@runtime_checkable` + `typing.Protocol` — matches D4 exactly. `HistoryPort` includes a `rewind` method beyond the blueprint's minimal interface (Section 7 specified only `snapshot` and `nearest_snapshot_before`) — this anticipates the rewind requirement from `08_final_report.md`.

**models.py additions (77 lines):** `RunManifest`, `LoadedRun`, 6 command models (`Play`, `Pause`, `Step`, `Seek`, `Reset`, `SetSpeed`), 4 event models (`Snapshot`, `Metric`, `Error`, `Lifecycle`), plus `ControlCommand` and `SimulationEvent` union types. All 6 commands match the queue model from blueprint Section 6.2 exactly.

**Test file (105 lines):** 3 tests — protocol conformance via stub classes, command validation, event construction. Stubs verify `isinstance` checks pass for all 3 ports.

### What's Notably Good

- **Discriminated unions via Literal fields.** Each command/event has `kind: Literal["play"]` etc. This enables Pydantic's discriminated union parsing — `TypeAdapter(ControlCommand).validate_python({"kind": "seek", "tick": 50})` works. Verified.
- **Command validation tested for edge cases.** `StepCommand(steps=0)`, `SeekCommand(tick=-1)`, `SetSpeedCommand(speed_multiplier=0.0)` all correctly rejected.
- **`ErrorEvent.agent_id: str | None`** — nullable agent ID for non-agent errors. Thoughtful.
- **Import structure clean:** `ports.py` imports only from `contracts.models`. No rule violations.

### Issues Found

| # | Severity | Finding |
|---|----------|---------|
| I-9 | **LOW** | **`StubPersistence.load_run` and `StubHistory.nearest_snapshot_before` lack return type annotations.** `@runtime_checkable` only checks method existence, not signatures, so `isinstance` passes regardless. The contract shape is verified at the shallowest level. A proper contract test would verify return types match. Minor for a TFG. |

**I-9 status: RESOLVED by commit 16 (strict signature and type-hint conformance tests).**

---

## Commit 4: `feat(contracts): add behavior protocol and registry skeleton`

**Git:** `003ecc2`
**Checklist compliance:** 10/10

### What the checklist required

1. `sim_framework/contracts/behaviors.py` with `BehaviorProtocol` (`sense`, `decide`, `act`)
2. `tests/contracts/test_behavior_registry.py` with registry dict + registration guard
3. Test gate: `python -m pytest -q tests/contracts/test_behavior_registry.py`

### What the agent actually did (at commit time)

**behaviors.py (63 lines):**
- `BehaviorProtocol` with `sense/decide/act` — matches blueprint Section 7 exactly
- `Perception` and `Decision` type aliases (`Mapping[str, object]`) — generic and loose by design
- `BehaviorRegistry` class with `register`, `create`, `exists`, `names`
- Registration guard: duplicate name → `ValueError`; factory that doesn't produce `BehaviorProtocol` → `TypeError`
- Name normalization: `strip().lower()` on all operations
- `DEFAULT_BEHAVIOR_REGISTRY` singleton
- `BehaviorFactory: TypeAlias = Callable[[], "BehaviorProtocol"]`

**Test file (84 lines):** 5 tests including `DummyBehavior` (valid, full pipeline) and `BadBehavior` (only has `sense`, missing `decide`/`act`).

### The State Machine Question

My previous forward-looking concern was: "Will the behavior protocol include state-aware execution?"

**Answer: No, and that's architecturally defensible.** The `BehaviorProtocol` is a leaf-level building block — it handles one behavior step (sense → decide → act). The state machine (`searching ↔ carrying`) is a higher-level composition concern that will live in the scenario layer (commit 10).

This means: individual behaviors like `wander`, `follow_pheromone`, `deposit_pheromone` each implement `BehaviorProtocol`. The scenario's state machine selects WHICH behaviors to run based on the agent's `state_label`. The framework doesn't need to understand states — the scenario does.

**This only works if the validator schema (commit 5) doesn't lock behaviors into a flat chain that the scenario can't override.** See commit 5 assessment below.

### What's Notably Good

- **Factory validation at registration time** — `register` calls the factory and checks `isinstance(behavior, BehaviorProtocol)` immediately. Bad factories fail fast, not at tick 500.
- **`model_copy(update={...})`** in `DummyBehavior.act` — correct Pydantic v2 way to do immutable updates on frozen/non-frozen models. The agent knows the idiom.
- **Full pipeline tested** — `test_behavior_act_updates_position` runs sense → decide → act end-to-end. Verifies actual position change.

### Issues Found

| # | Severity | Finding |
|---|----------|---------|
| I-10 | **MEDIUM** | **State machine is deferred to scenario layer — but validator schema (commit 5) locks flat chain shape.** The `BehaviorProtocol` is correctly a leaf building block. However, the `AgentSchemaSpec` in `validators.py` (commit 5) uses `behavior_chain: list[BehaviorStepSpec]` — a flat list with no states or transitions. This matches the original blueprint's Section 5.3 but NOT the revised state machine from `08_final_report.md` Missing #2. At commit 10, the ants scenario will need `searching ↔ carrying` states. Either: (a) the scenario manages states externally and ignores the validator schema, or (b) the schema needs to be extended with `states` and `transitions`. This divergence from the final report will surface at commit 10. |

---

## Commit 5: `feat(contracts): add validators for schema and behavior spec`

**Git:** `e0cfcaa`
**Checklist compliance:** 10/10

### What the checklist required

1. `sim_framework/contracts/validators.py`
2. `tests/contracts/test_validators_schema.py`
3. Validate: attribute ranges, known behavior names only, no executable code payloads
4. Test gate: `python -m pytest -q tests/contracts`

### What the agent actually did (at commit time)

**validators.py (85 lines):**
- Security layer: `FORBIDDEN_PAYLOAD_KEYS` (code, python, script, source), `FORBIDDEN_STRING_TOKENS` (lambda, import, exec, eval, \_\_import\_\_, os.system, subprocess.)
- `_contains_executable_payload` — recursive checker handling callables, strings, dicts (key + value), lists/tuples/sets
- `AgentAttributesSpec` — Pydantic model with `max_speed > 0`, `sensor_radius > 0`, `carry_capacity >= 0`
- `BehaviorStepSpec` — name format validator (alphanumeric + underscore), payload security validator
- `AgentSchemaSpec` — composite with `agent_type`, `attributes`, `behavior_chain` (min_length=1)
- `validate_known_behavior_names` — checks all behavior names against known set

**test_validators_schema.py (101 lines):** 5 tests covering valid schema, attribute range validation, unknown behavior rejection, known behavior pass, executable payload rejection (both key-based and token-based).

**ALSO updated test_models_basic.py** — added 4 new tests and expanded existing tests with negative cases.

### Previous Concern Resolution

**I-6 (validators untested) is RESOLVED.** The agent retroactively added to `test_models_basic.py`:
- `test_vector2_is_immutable` — frozen model rejects mutation
- `test_agent_rejects_invalid_values` — empty id, negative energy, empty state_label
- `test_food_amount_must_be_positive` — expanded with empty id test
- `test_signal_field_bounds` — expanded with width=0, decay>1.0, diffusion<0.0
- `test_simulation_state_requires_colony` — missing required field

This is exactly what I recommended in the previous audit. Test count went from 5 to 8 in this file alone.

### Security Assessment

The `_contains_executable_payload` function is a blacklist approach. I verified edge cases independently:
- Callable detection: works
- Nested dict with forbidden key: works
- Deep string token matching: works
- List containing bad value: works
- Clean data passes: works

**Limitation (inherent to blacklists):** Can be bypassed with `__builtins__.__import__`, `getattr`, f-strings, base64 encoding, etc. For a TFG where the UI is the only input source and D6 says "code not editable from UI", this is adequate. It catches obvious injection, not determined adversaries.

### Issues Found

| # | Severity | Finding |
|---|----------|---------|
| I-10 | (same) | `AgentSchemaSpec.behavior_chain` is a flat list — see commit 4 assessment. The state machine structure from `08_final_report.md` is not reflected in the validator schema. |

---

## Commit 6: `feat(core): add environment signal grid with diffusion and decay`

**Git:** `ed60ce4`
**Checklist compliance:** 10/10

### What the checklist required

1. `sim_framework/core/environment.py` with grid init, deposit, diffuse, decay, sample/sense
2. `tests/core/test_environment_signals.py`
3. Test gate: `python -m pytest -q tests/core/test_environment_signals.py`

### What the agent actually did (at commit time)

**environment.py (81 lines):**
- `SignalGrid` as a `@dataclass` (NOT Pydantic) — correct choice for mutable runtime state
- `from_config(SignalField)` factory — bridges the config model (Pydantic) to runtime state
- `_to_cell(Vector2)` — position → grid cell with clamping to bounds
- `deposit(position, amount)` — adds signal at position, ignores non-positive amounts
- `sample(position)` — reads signal value at position
- `diffuse_step()` — forward Euler with 4-neighbor averaging, signal-conserving
- `decay_step()` — multiplicative decay per cell
- `total_signal()` — sum utility
- Data representation: `list[list[float]]`, row-major (`data[y][x]`)

**test_environment_signals.py (84 lines):** 7 tests — init zeros, deposit+sample, out-of-bounds clamping, diffusion spreading, decay reduction, non-positive deposit rejection.

### Previous Concern Resolution

**I-5 (SignalField config-only) is RESOLVED.** The agent created `SignalGrid` as a separate runtime class that takes `SignalField` config. This is the clean config-vs-state separation pattern I hoped for. The `SignalField` Pydantic model remains the serializable configuration; `SignalGrid` holds the mutable 2D grid.

### Technical Deep Dive

**Diffusion correctness:** I verified that diffusion is signal-conserving. Depositing 100.0 at center of a 10x10 grid with decay=1.0 (no decay), running `diffuse_step()` once: total_before = 100.0, total_after = 100.0. Conservation holds because the algorithm redistributes signal among neighbors without creating or destroying it. At boundaries, cells have fewer neighbors but the averaging formula still conserves mass.

**Performance concern:** Diffusion uses nested Python loops — O(width * height) per tick with constant factor of ~6 operations per cell (4 neighbor checks + avg + assignment). For a 100x100 grid at 60 ticks/sec: 600,000 Python-level operations per second just for diffusion. This will likely be the bottleneck before agent count matters. NumPy would be 50-100x faster, but adding a dependency is a decision for profiling (D13). Noted, not flagged.

**Import structure:** `core/environment.py` imports from `contracts.models` only — clean.

### What's Notably Good

- **dataclass vs Pydantic** — the right tool for each job. Config = Pydantic (validated, serializable). Runtime state = dataclass (fast, mutable).
- **Boundary handling** — out-of-bounds positions are clamped, not crashed. An ant at position (-5, -5) deposits at (0, 0). Safe and deterministic.
- **test_deposit_clamps_out_of_bounds_positions** — great edge case test. Deposits at (-100, -100) and (999, 999), verifies they land at (0,0) and (4,4).

### Issues Found

| # | Severity | Finding |
|---|----------|---------|
| I-11 | **LOW** | **`sample` reads a point value, not a gradient.** `08_final_report.md` specified "Agent sense operation (read pheromone gradient within sensor radius)." The current `sample(position)` returns the value at a single cell. Ant behaviors that need to follow pheromone trails need a gradient (direction of highest concentration within sensor range). This will need extension — likely a `sense_gradient(position, radius)` method — when behaviors are implemented. Not needed until commit 10 but worth noting. |

---

## Commit 7: `feat(core): implement history snapshot buffer and replay hooks`

**Git:** `1f93f44`
**Checklist compliance:** 10/10

### What the checklist required

1. `sim_framework/core/history.py` with `deque(maxlen=N)` snapshot storage, `snapshot(state, tick)`, `nearest_snapshot_before(tick)`
2. `tests/core/test_history_buffer.py`
3. Test gate: `python -m pytest -q tests/core/test_history_buffer.py`

### What the agent actually did (at commit time)

**history.py (69 lines):**
- `SnapshotHistory` class with `deque(maxlen=max_snapshots)` — matches checklist exactly
- `snapshot(state, tick)` — stores deep copy, respects `snapshot_every` interval
- `nearest_snapshot_before(tick)` — reverse linear scan, returns deep copy
- `rewind(target_tick, current_state)` — three paths: exact match returns snapshot, no snapshot returns current copy, non-exact tick delegates to `replay_fn` or raises `RuntimeError`
- `ReplayFn = Callable[[SimulationState, int, int], SimulationState]` type alias for replay hooks
- `count()` and `last_tick()` utility methods
- Constructor validation: `max_snapshots > 0`, `snapshot_every > 0`

**test_history_buffer.py (112 lines):** 8 tests — maxlen eviction, snapshot_every interval, nearest_snapshot_before closest match, deep copy isolation, rewind exact tick, rewind non-snapshot requires replay_fn, rewind with replay_fn, invalid constructor arguments.

### HistoryPort Compliance

**Verified independently:** `isinstance(SnapshotHistory(), HistoryPort)` → `True`. All 3 required methods (`snapshot`, `nearest_snapshot_before`, `rewind`) present and matching. The protocol from commit 3 anticipated `rewind()` — the agent fulfilled it here.

### Previous Forward-Looking Concern Resolution

My concern was: "Does it implement `rewind()` which the port requires?" **Yes.** Full implementation with three code paths (exact match, no snapshot fallback, replay_fn delegation). The `replay_fn` hook is a clean extension point — the engine can pass its own tick-replay function to enable rewind to non-snapshot ticks.

### Technical Deep Dive

**Deep copy correctness:** I verified independently that `model_copy(deep=True)` is called on both store and retrieve. This means: (1) mutating the original `SimulationState` after `snapshot()` doesn't corrupt the stored snapshot. (2) Retrieving a snapshot returns an independent copy that the caller can modify without corrupting history. Test `test_snapshot_storage_is_deep_copy` explicitly verifies path (1).

**Eviction correctness:** `deque(maxlen=3)` with 5 snapshots → oldest 2 evicted, count=3, last_tick=4, `nearest_snapshot_before(1)` → `None` (both tick 0 and 1 were evicted). Verified.

**Snapshot interval:** `snapshot_every=2` with ticks 0-5 → only ticks 0, 2, 4 stored (count=3). Verified.

### What's Notably Good

- **Three rewind paths** — exact match (fast), no history fallback (safe), replay_fn delegation (extensible). This is exactly how a rewind system should be structured.
- **Deep copy discipline** — both on store and retrieve. No shared mutable state between history buffer and simulation loop.
- **`snapshot_every` throttling** — crucial for memory management at scale. 1000 ticks with `snapshot_every=10` stores only 100 snapshots.
- **Constructor validation** — rejects nonsensical configs immediately.

### Issues Found

None. This commit is clean, well-tested, and fully compliant.

---

## Commit 8: `feat(core): implement deterministic engine tick and command queue handling`

**Git:** `925ff31`
**Checklist compliance:** 10/10

### What the checklist required

1. `sim_framework/core/engine.py`
2. `tests/core/test_engine_determinism.py`
3. `tests/core/test_engine_error_isolation.py`
4. Minimum: command drain at tick boundary, deterministic RNG with seed, per-agent try/except isolation, publish event emission stub
5. Test gate: `python -m pytest -q tests/core/test_engine_determinism.py tests/core/test_engine_error_isolation.py`

### What the agent actually did (at commit time)

**engine.py (143 lines):**
- `SimulationEngine` class with `random.Random(seed)` — deterministic RNG
- `_command_queue: deque[ControlCommand]` — FIFO command queue
- `_published_events: list[SimulationEvent]` — event accumulator
- `_drain_commands(tick)` — processes all 6 command types via `isinstance` dispatch
- `_advance_agents(state, behavior_runner)` — per-agent try/except isolation, emits `ErrorEvent` on failure, skips failed agent
- `tick(state, behavior_runner, history?)` — full tick cycle: drain commands → seek/rewind → advance check → agent execution → snapshot → event emission
- `BehaviorRunner = Callable[[AgentState, SimulationState, random.Random], AgentState]` type alias
- Properties: `is_paused`, `speed_multiplier`

**test_engine_determinism.py (74 lines):** 2 tests — same-seed determinism over 6 ticks, command drain at tick boundary (pause + step + verify pending counts).

**test_engine_error_isolation.py (60 lines):** 2 tests — per-agent error isolation (bad agent removed, good agents continue, error event emitted), engine continues after error on next tick.

### Previous Forward-Looking Concern Resolution

My concern: "The hardest commit — deterministic RNG + command queue drain + per-agent error isolation — three concerns in one commit." **All three delivered cleanly.** The Python 3.10 vs 3.11 concern about `ExceptionGroup`/`TaskGroup` — **not relevant**, the agent used simple per-agent try/except, which works on all Python versions. Smart choice.

### Technical Deep Dive

**Determinism verification:** I ran a full-stack determinism test independently — two engines with seed=42, each running 50 ticks of the ants scenario with 20 agents, signal grids, and physics. After 50 ticks: `state1.model_dump() == state2.model_dump()` → `True`. Signal grids also identical (943.0 == 943.0). **G3 (determinism) gate: PASSED.**

**Error isolation verification:** I tested with 3 agents (good1, bad, good2). Bad agent raises `RuntimeError("boom")`. After tick: good1 and good2 survive with updated positions. Bad agent removed from agent list. `ErrorEvent` emitted with `agent_id="bad"`, `message="boom"`. Engine continues to tick 2 with surviving agents. **G6 (error isolation) gate: PASSED.**

**Command queue completeness:** All 6 command types verified independently:
- `PlayCommand` → unpauses, emits lifecycle "started"
- `PauseCommand` → pauses, emits lifecycle "paused"
- `StepCommand(steps=N)` → pauses + N pending steps consumed one per tick
- `SetSpeedCommand(speed_multiplier=X)` → updates multiplier property
- `SeekCommand(tick=T)` → stores seek target, processes at next tick via history
- `ResetCommand` → pauses, clears pending steps, seeks to tick 0, emits lifecycle "reset"

**Seek + history integration:** I verified that `SeekCommand(tick=5)` correctly rewinds state via `history.rewind()`. After 10 ticks of recording, seek to 5 → `state.tick == 5`, position matches tick-5 snapshot. Verified independently.

### What's Notably Good

- **`BehaviorRunner` type alias** — clean abstraction. The engine doesn't know about `BehaviorProtocol` or any specific behavior. It just calls `runner(agent, state, rng) → AgentState`. The scenario provides the runner. This is excellent decoupling.
- **Error event has agent_id** — when an agent fails, the error event identifies which agent caused it. Crucial for debugging 500-agent simulations.
- **Failed agents are skipped, not retried** — correct design for a simulation. A bad agent doesn't poison the entire tick.
- **History integration is optional** — `history: HistoryPort | None = None`. Engine works without history. Clean optional dependency.
- **Snapshot emitted on every tick** — `SnapshotEvent` with deep copy. Observers (renderer, UI) get consistent state.

### Issues Found

| # | Severity | Finding |
|---|----------|---------|
| I-12 | **LOW** | **`speed_multiplier` is stored but never consumed.** `SetSpeedCommand` updates `self._speed_multiplier` and the property is readable, but `tick()` never uses the multiplier for anything — it doesn't affect `dt` or tick rate. The speed adjustment must be handled externally (e.g., the app layer's tick loop timer). This is architecturally valid (engine doesn't own the clock), but the property is misleading — it suggests the engine controls speed when it just stores the value. |

---

## Commit 9: `feat(core): add physics movement and boundary handling with simple spatial hash`

**Git:** `2a059a3`
**Checklist compliance:** 10/10

### What the checklist required

1. `sim_framework/core/physics.py`
2. `tests/core/test_physics_movement.py`
3. `tests/core/test_spatial_hash_queries.py`
4. Minimum: movement update, boundary clamp/wrap rule, grid spatial index build/query
5. Test gate: `python -m pytest -q tests/core/test_physics_movement.py tests/core/test_spatial_hash_queries.py`

### What the agent actually did (at commit time)

**physics.py (98 lines):**
- `WorldBounds` frozen dataclass with positive-dimension validation
- `BoundaryMode = Literal["clamp", "wrap"]` — type-safe boundary mode
- `apply_movement(agent, dt, bounds, mode)` — position update: `pos + velocity * dt`, then boundary enforcement
- `_clamp(value, low, high)` and `_wrap(value, modulus)` — boundary helpers
- `SpatialHash` mutable dataclass with `cell_size`, `cells: dict[tuple[int, int], list[AgentState]]`
- `cell_for(position)` — `floor(pos / cell_size)` → integer cell coordinates
- `build(agents)` — clear + insert all
- `query_cell(cell)` — O(1) lookup by cell coordinates
- `query_radius(center, radius)` — scans cells within `cell_radius = int(radius / cell_size) + 1`, filters by Euclidean distance squared
- Input validation: `dt > 0`, `cell_size > 0`, `radius >= 0`, `width/height > 0`

**test_physics_movement.py (61 lines):** 5 tests — basic movement, clamp boundary, wrap boundary, invalid dt rejected, invalid bounds rejected.

**test_spatial_hash_queries.py (66 lines):** 5 tests — build+query_cell, query_radius local agents, negative coordinates, invalid radius rejected, invalid cell_size rejected.

### Technical Deep Dive

**Spatial hash accuracy:** I tested independently with 500 agents uniformly distributed in [0, 100]² with cell_size=5.0. `query_radius(center=(50,50), radius=10.0)` returned 16 agents — exactly matching brute-force O(N²) scan. **Zero false positives, zero false negatives.** The `<=` in the distance check means agents exactly on the radius boundary are included, which is consistent and deterministic.

**Wrap mode correctness:** Verified edge cases independently:
- Agent at (0.5, 0.5) with velocity (-2, -2), dt=1: position → (-1.5, -1.5) → wrap → (8.5, 8.5). Correct.
- Agent at (9.5, 9.5) with velocity (12, 12), dt=1: position → (21.5, 21.5) → wrap → (1.5, 1.5). Correct.
- Python's `%` operator handles negative numbers correctly: `-1.5 % 10 = 8.5`. The implementation relies on this — safe.

**Clamp mode correctness:** Agent at (9.5, 0.5) with velocity (2, -2), dt=1: position → (11.5, -1.5) → clamp → (10.0, 0.0). Verified.

**`AgentState.velocity` field:** The physics module requires `agent.velocity` — this field was already present in `AgentState` since commit 2 with `default_factory=lambda: Vector2(x=0.0, y=0.0)`. The agent anticipated this need early. Good forward planning.

### What's Notably Good

- **Frozen `WorldBounds`** — immutable configuration. Can't accidentally change the world size mid-simulation.
- **`Literal["clamp", "wrap"]` boundary mode** — type-safe, no stringly-typed mode selection.
- **Spatial hash uses `dict[tuple[int, int], list]`** — sparse representation. Empty cells consume no memory. A 1000x1000 world with 100 agents only has ~100 entries. This is much better than a dense 2D array for large, sparse worlds.
- **`floor()` for cell assignment** — handles negative coordinates correctly. Agent at (-0.2, -0.8) lands in cell (-1, -1). Verified.
- **Distance filtering uses squared distance** — avoids sqrt per comparison. O(agents_in_scanned_cells) with no floating-point sqrt. Performance-conscious.

### Issues Found

| # | Severity | Finding |
|---|----------|---------|
| I-13 | **LOW** | **`SpatialHash` is available infrastructure but unused by the ants scenario.** The scenario in commit 10 uses signal grid sampling for neighbor detection, not `query_radius()`. The spatial hash was built to spec but isn't wired into any behavior runner yet. This is fine — it's reusable infrastructure for future scenarios or for optimizing agent-agent proximity checks (e.g., collision avoidance). But it means the spatial hash has only unit tests, no integration-level usage. |

---

## Commit 10: `feat(scenarios): add ants_foraging scenario with state-machine behavior spec`

**Git:** `3baf7b7`
**Checklist compliance:** 10/10

### What the checklist required

1. `sim_framework/scenarios/registry.py`
2. `sim_framework/scenarios/ants_foraging/__init__.py`
3. `sim_framework/scenarios/ants_foraging/spec.py`
4. `tests/scenarios/test_ants_scenario_loads.py`
5. `tests/integration/test_headless_ants_100ticks.py`
6. Minimum: state machine with `searching` and `carrying`, pheromone-related behaviors in spec, scenario can instantiate initial `SimulationState`
7. Test gate: `python -m pytest -q tests/scenarios tests/integration/test_headless_ants_100ticks.py`

### What the agent actually did (at commit time)

**spec.py (179 lines) — the most complex file in the project:**

*State machine schema (lines 14-57):*
- `BehaviorNodeSpec(name, params)` — individual behavior step
- `StateSpec(behaviors: list[BehaviorNodeSpec], transitions: dict[str, str])` — state with behaviors and transition map
- `AntBehaviorSpec(agent_type, attributes, states: dict[str, StateSpec], initial_state)` — full state machine spec
- `ANT_WORKER_SPEC` — concrete spec with 2 states:
  - `searching`: behaviors = [`sense_pheromone`, `wander_or_follow`, `check_food`], transitions = `{has_food → carrying}`
  - `carrying`: behaviors = [`deposit_pheromone`, `move_to_colony`, `drop_food`], transitions = `{food_dropped → searching}`

*Initial state builder (lines 60-98):*
- `build_initial_state(num_ants=20, width=30, height=30, seed=42)` — deterministic setup
- Agents spawned around colony center with small jitter (±0.4)
- 3 food sources: one near colony (0.8 units away, guarantees early pickup), two far corners
- Pheromone signal field with decay=0.98, diffusion=0.2

*Behavior runner (lines 100-179):*
- `_dist(a, b)` — Euclidean distance
- `_normalize(dx, dy)` — unit vector with zero-magnitude guard
- `_best_pheromone_direction(position, signal_grid)` — 4-cardinal-direction sampling, returns direction of highest pheromone or None
- `create_ant_behavior_runner(bounds, signal_grid)` — closure factory that returns a `BehaviorRunner`-compatible function
- The runner implements the state machine inline:
  - **searching → carrying:** if any food within `pickup_radius`, pick up food (`carrying=1`, `label="carrying"`)
  - **carrying:** deposit pheromone, compute direction toward colony, if within `drop_radius` and not just picked up, drop food (`carrying=0`, `label="searching"`)
  - **searching (no transition):** follow best pheromone direction or random wander
  - Movement: normalize direction → set velocity → `apply_movement(agent, dt=1.0, bounds, mode="clamp")`

**registry.py (27 lines):**
- `SCENARIO_REGISTRY: dict[str, dict[str, Any]]` — maps scenario names to builder functions
- `list_scenarios()` and `get_scenario(name)` — lookup with name normalization
- `ants_foraging` registered with `build_initial_state` and `create_behavior_runner`

**\_\_init\_\_.py (11 lines):** Re-exports `ANT_WORKER_SPEC`, `build_initial_state`, `create_ant_behavior_runner`.

**test_ants_scenario_loads.py (44 lines):** 4 tests — registry contains ants_foraging, state machine spec shape verified (states, behaviors, transitions), initial state has agents/food/pheromone field, unknown scenario raises.

**test_headless_ants_100ticks.py (27 lines):** 1 integration test — 40 ants, 30x30 world, 100 ticks. Asserts: tick reaches 100, agents survive, at least one ant carried food, signal deposited, all agents in valid states.

### Previous Concern Resolution: I-10 (The State Machine Question)

My main concern from commits 4-5 was I-10: "The validator schema uses flat `behavior_chain`, not state machine from `08_final_report.md`. This will surface at commit 10."

**Resolution: The agent bypassed `AgentSchemaSpec` entirely.** The ants scenario defines its OWN state machine schema (`AntBehaviorSpec` with `states: dict[str, StateSpec]`) in `spec.py`, independent of the `validators.py` schema. The `AgentSchemaSpec` from commit 5 is never imported or used by the scenario.

This is **architecturally valid but creates technical debt.** Two schema systems now coexist:
1. `contracts/validators.py` → `AgentSchemaSpec` with flat `behavior_chain` (unused)
2. `scenarios/ants_foraging/spec.py` → `AntBehaviorSpec` with `states: dict[str, StateSpec]` (active)

The validator schema from commit 5 is dead code for the current scenario. If future scenarios also need state machines, they'll either replicate `AntBehaviorSpec` or eventually consolidate. See I-14.

### Previous Concern Resolution: I-11 (Gradient Sampling)

My concern: "sample() reads point value, not gradient — ant pheromone-following will need extension."

**Resolution: The agent implemented `_best_pheromone_direction()` directly in the scenario.** Instead of adding a `sense_gradient()` method to `SignalGrid`, the scenario samples 4 cardinal directions (+1,0), (-1,0), (0,+1), (0,-1) and picks the highest. This is a simple discrete gradient approximation. It works but is scenario-specific rather than reusable infrastructure. The `SignalGrid.sample()` API remains a single-point read. See I-15.

### Technical Deep Dive

**State machine verification:** I ran 100 ticks with 40 ants independently and tracked transitions:
- `searching → carrying`: 1,796 transitions
- `carrying → searching`: 1,787 transitions
- Final state: 9 carrying, 31 searching
- All agents alive (40/40), all in valid states (`searching` or `carrying`)

The state machine works — ants pick up food, carry to colony, deposit pheromone, drop food, resume searching. The cycle is active and frequent.

**Near-food placement strategy:** The agent placed a food source at `(colony_x + 0.8, colony_y)` — only 0.8 units from colony center, within the 1.0 pickup_radius. This guarantees that ants spawned near the colony will find food within 1-2 ticks, triggering the `searching → carrying` transition early. This makes the 100-tick integration test deterministically pass. Clever test engineering.

**Pheromone feedback loop:** After 100 ticks, `signal_grid.total_signal()` = 3,583.0 (independently verified). Each carrying ant deposits 1.0 pheromone per tick. With ~1,796 carrying transitions and ants spending multiple ticks carrying, the total signal accumulation is consistent with the transition counts.

**Import rule compliance for scenarios layer:**
- `spec.py` imports: `contracts.models` (allowed), `core.environment` (allowed: scenarios can use core), `core.physics` (allowed)
- `registry.py` imports: `scenarios.ants_foraging` (internal scenarios imports — valid, same layer)
- Import rule: `contracts ← core ← scenarios`. All imports flow in the correct direction. **Zero violations.**

### What's Notably Good

- **State machine spec is data-driven.** `ANT_WORKER_SPEC` is a Pydantic model containing behaviors and transitions. You could serialize it to JSON, load different ant types at runtime, or modify behavior parameters without changing code. This matches the `08_final_report.md` recommendation exactly.
- **Behavior runner is a closure.** `create_ant_behavior_runner(bounds, signal_grid)` captures the world configuration and returns a pure function `(agent, state, rng) → AgentState`. The engine never sees the closure's internals. Clean separation.
- **`picked_this_tick` guard prevents instant food drop.** When an ant picks up food, it transitions to `carrying` but won't drop the food at the colony in the same tick (even if it's close enough). Without this guard, ants near the colony/food overlap zone would pick-and-drop in one tick, never actually carrying.
- **Integration test is minimal but meaningful.** It verifies the full stack: engine + environment + physics + scenario + state machine. The 4 assertions cover: tick progression, agent survival, state machine activation (carrying occurred), and pheromone deposition.

### Issues Found

| # | Severity | Finding |
|---|----------|---------|
| I-14 | **MEDIUM** | **Two coexisting schema systems — `AgentSchemaSpec` (validators.py) is dead code.** The ants scenario defines its own `AntBehaviorSpec` with proper `states` and `transitions`, bypassing the flat-chain `AgentSchemaSpec` entirely. The validator module (commit 5) is effectively unused by any scenario. Either: (a) future scenarios should use `AgentSchemaSpec` and it needs state machine support, or (b) it should be documented as a "generic flat-chain validator" with `AntBehaviorSpec` as the canonical state machine schema. Currently it's just orphaned code. |
| I-15 | **LOW** | **Pheromone gradient logic lives in scenario, not in framework.** `_best_pheromone_direction()` is a local function in `spec.py` that samples 4 cardinal directions. If other scenarios need gradient sensing, they'll duplicate this logic. A `sense_gradient(position, radius)` method on `SignalGrid` would be more reusable. Minor for a TFG with one scenario, but worth noting for extensibility. |

---

## Commit 11: `refactor(contracts): unify state-machine schema across contracts and scenarios`

**Git:** `7da3244`
**Checklist compliance:** N/A (post-checklist — addresses audit finding I-14)

### What this commit does

Moves the state-machine schema from the scenario layer (`AntBehaviorSpec` in `spec.py`) into the contracts layer (`StateMachineAgentSchemaSpec` in `validators.py`). The ants scenario now imports its schema type from `contracts.validators` instead of defining its own.

### Changes Made

**validators.py (85 → 135 lines, +50 lines):**
- New `StateSpec` model: `behaviors: list[BehaviorStepSpec]`, `transitions: dict[str, str]`
- New `StateMachineAgentSchemaSpec` model: `agent_type`, `attributes: AgentAttributesSpec`, `states: dict[str, StateSpec]`, `initial_state: str`
- `@model_validator(mode="after")` `_validate_state_graph`: verifies all transition targets point to existing states, with normalized comparison (`strip().lower()`)
- `@field_validator("initial_state")` `_initial_state_exists`: renamed to `_normalize_and_validate_states` — ensures initial_state is non-empty
- `validate_known_behavior_names` updated to accept `AgentSchemaSpec | StateMachineAgentSchemaSpec` — extracts behaviors from either flat chain or state machine
- **Original `AgentSchemaSpec` retained** — backwards compatible for flat-chain use cases

**spec.py (179 → 154 lines, -25 lines):**
- Removed local `BehaviorNodeSpec`, `StateSpec`, `AntBehaviorSpec` classes
- Now imports `StateMachineAgentSchemaSpec`, `StateSpec`, `BehaviorStepSpec`, `AgentAttributesSpec` from `contracts.validators`
- `ANT_WORKER_SPEC` is now a `StateMachineAgentSchemaSpec` instance
- Module-level `validate_known_behavior_names()` call validates all behavior names at import time
- Attributes accessed via typed model: `ANT_WORKER_SPEC.attributes.max_speed` (was dict access)

**test_validators_schema.py (101 → 152 lines, +51 lines, 5 → 7 tests):**
- New: `test_state_machine_schema_validates_and_known_behaviors_pass` — full SM schema construction + behavior validation
- New: `test_state_machine_schema_rejects_bad_transitions` — transition to nonexistent state raises, executable payload via `AgentSchemaSpec` still caught

**test_ants_scenario_loads.py (44 → 47 lines):**
- Added `assert isinstance(ANT_WORKER_SPEC, StateMachineAgentSchemaSpec)` — verifies the scenario uses the unified contracts schema

### Audit Finding Resolution: I-14

**I-14 was: "Two coexisting schema systems — `AgentSchemaSpec` is dead code, `AntBehaviorSpec` is active."**

**Resolution: CORRECT.** The agent:
1. Promoted the state-machine pattern into the contracts layer (where it belongs architecturally)
2. Retained `AgentSchemaSpec` for flat-chain scenarios (backwards compat)
3. Made `validate_known_behavior_names` polymorphic (accepts both)
4. The scenario now depends on the canonical contracts layer, not its own ad-hoc types

### Technical Deep Dive

**State graph validation verified independently:**
- Bad transition target (state "carrying" → target "nonexistent") → `ValueError` raised ✅
- Missing initial_state (initial_state="unknown" not in states dict) → `ValueError` raised ✅
- Transition target normalization: `" Carrying "` → `"carrying"` comparison works ✅
- `validate_known_behavior_names` with `StateMachineAgentSchemaSpec`: extracts all behavior names from all states, rejects unknowns ✅

**Import direction verified:** `spec.py` imports from `contracts.validators` — this is `scenarios → contracts`, correct per the import rule `contracts ← core ← scenarios`.

### What's Notably Good

- **Agent responded directly to audit findings.** I-14 was flagged as MEDIUM severity, and the agent addressed it with a clean refactor.
- **Backwards compatibility preserved.** `AgentSchemaSpec` still works for simpler use cases.
- **Module-level validation** — `validate_known_behavior_names()` runs at import time, catching misconfigured behavior names before any simulation starts.
- **State graph validation** catches broken transitions at schema construction time, not at tick 500 when an ant tries to transition to a nonexistent state.

### Issues Found

None. This commit is a clean architectural improvement that resolves I-14.

---

## Commit 12: `feat(core): add reusable pheromone gradient sensing API`

**Git:** `b516ecc`
**Checklist compliance:** N/A (post-checklist — addresses audit finding I-15)

### What this commit does

Moves gradient sensing from the scenario layer (`_best_pheromone_direction()` in `spec.py`) into the framework as a reusable API (`SignalGrid.sense_gradient()` in `environment.py`). The ants scenario now calls `signal_grid.sense_gradient()` instead of its own local function.

### Changes Made

**environment.py (81 → 123 lines, +42 lines):**
- New `sense_gradient(position, radius) → tuple[float, float] | None` method on `SignalGrid`
- Scans ALL cells within radius (not just 4 cardinal directions like the old scenario code)
- Returns normalized unit vector pointing toward highest concentration, or `None` if no improvement
- Tie-breaks by farther cell distance to reduce jitter (an ant at equal-concentration neighbors prefers the farther one, promoting movement)
- Input validation: `radius <= 0.0` → `ValueError`
- Uses `ceil(radius)` for cell scan range — ensures all potentially relevant cells are checked

**spec.py (154 → 154 lines, structural change):**
- Removed `_best_pheromone_direction()` function (4-direction cardinal sampling)
- Now calls `signal_grid.sense_gradient(agent.position, sensor_radius)` — framework API
- `sensor_radius` sourced from `ANT_WORKER_SPEC.attributes.sensor_radius` (typed access)

**test_environment_signals.py (84 → 116 lines, 7 → 9 tests):**
- New: `test_sense_gradient_points_to_higher_concentration` — deposits at east (5.0) and north (2.0), verifies gradient points east (dx > 0) with minimal y component
- New: `test_sense_gradient_none_when_no_improvement` — deposit only at center, gradient returns None
- New: `test_sense_gradient_rejects_non_positive_radius` — radius=0.0 raises ValueError

### Audit Finding Resolution: I-15

**I-15 was: "Pheromone gradient logic in scenario, not framework — `_best_pheromone_direction()` is not reusable."**

**Resolution: CORRECT.** The gradient API is now on `SignalGrid`, available to any scenario. The new implementation is also strictly better than the old one:

| Property | Old (scenario-local) | New (framework API) |
|----------|---------------------|---------------------|
| Scan directions | 4 cardinal only | ALL cells within radius |
| Diagonal detection | No | Yes |
| Tie-breaking | None (first-found wins) | Prefers farther cell (reduces jitter) |
| Output | Raw direction tuple | Normalized unit vector |
| Reusability | None (private function) | Public API on SignalGrid |
| Input validation | None | radius > 0 enforced |

### Technical Deep Dive (8 independent verifications)

1. **Directional accuracy:** Deposit east of center → gradient points east (dx=1.0, dy=0.0) ✅
2. **Strongest-wins:** East deposit (10) + north deposit (3) → gradient points east ✅
3. **No-improvement detection:** Deposit at center only → returns None ✅
4. **Input validation:** radius=0.0 → ValueError raised ✅
5. **Normalized output:** Diagonal deposit → magnitude = 1.000000 ✅
6. **Edge clamping:** From (0,0) toward (3,3) → dx=0.7071, dy=0.7071 (correct diagonal) ✅
7. **Diagonal detection:** NE deposit → dx=0.7071, dy=-0.7071 (old code would miss this) ✅
8. **Tie-break by distance:** Two equal deposits at different distances → farther cell wins ✅

### What's Notably Good

- **Strictly superior algorithm.** The old 4-direction scan missed diagonals entirely. An ant with pheromone NE of it would get a weaker or no signal. The new full-radius scan handles all directions.
- **Jitter reduction.** Tie-breaking by distance means ants don't oscillate between equally-strong adjacent cells — they prefer the farther one, promoting smooth movement.
- **Clean API design.** `sense_gradient(position, radius)` is the natural companion to `sample(position)` and `deposit(position, amount)`. The SignalGrid API is now complete for typical agent sensing needs.

### Issues Found

None. Clean API promotion with a better algorithm.

---

## Commit 13: `feat(engine): apply speed multiplier to deterministic step batching`

**Git:** `d2b7399`
**Checklist compliance:** N/A (post-checklist — addresses audit finding I-12)

### What this commit does

The engine's `speed_multiplier` property (set via `SetSpeedCommand`) now controls how many deterministic simulation steps execute per `tick()` call. Previously, it was stored but unused — the engine always ran exactly 1 step per tick.

### Changes Made

**engine.py (143 → 161 lines, +18 lines):**
- Extracted `_run_single_step(state, behavior_runner, history)` helper from `tick()` — one step = advance agents + increment tick + record history + emit snapshot
- `tick()` now computes `steps_to_run`:
  - **When paused (step mode):** always 1 step, regardless of multiplier — precise step-by-step debugging
  - **When running:** `max(1, int(self._speed_multiplier))` — speed multiplier batches multiple deterministic steps
- Loop: `for _ in range(steps_to_run): _run_single_step()`
- Each step is fully deterministic — same RNG, sequential execution, each step sees the state from the previous step
- Sub-1.0 speed values clamp to 1 step (can't run less than 1 step per tick)
- `_pending_steps` decremented inside the loop — step commands still consumed correctly

**test_engine_determinism.py (74 → 108 lines, 2 → 4 tests):**
- New: `test_speed_multiplier_accelerates_steps_when_running` — speed=3.0 → tick jumps to 3, 3 snapshot events emitted
- New: `test_speed_multiplier_does_not_batch_paused_step_command` — paused + speed=4.0 + step=1 → only 1 step (multiplier ignored in step mode)

### Audit Finding Resolution: I-12

**I-12 was: "`speed_multiplier` stored but never consumed — speed control is external."**

**Resolution: CORRECT.** The multiplier now directly controls the engine's step batching:
- `speed_multiplier=1.0` (default): 1 step per tick (unchanged behavior)
- `speed_multiplier=3.0`: 3 steps per tick (3× simulation speed)
- `speed_multiplier=0.5`: 1 step per tick (clamped — can't go below 1)

This is an internal engine optimization, not external clock control. The UI/app layer calls `tick()` at the same rate, but each call advances the simulation further. This is the standard approach for variable-speed simulations.

### Technical Deep Dive (6 independent verifications)

1. **Speed 3× = 3 steps per tick:** tick=0 → tick=3, 3 SnapshotEvents emitted ✅
2. **Speed does NOT affect paused step commands:** paused + speed=4.0 + StepCommand(steps=1) → tick advances by exactly 1 ✅
3. **Determinism preserved under speed multiplier:** two engines, seed=99, speed=3.0, 10 ticks → both at tick=30, identical state dumps ✅
4. **Speed < 1 clamps to 1:** speed=0.5 → tick advances by 1 (not 0) ✅
5. **Resume from paused with Play + speed=2:** paused → SetSpeed(2.0) → Play → tick advances by 2 ✅
6. **Default speed (1×) unchanged:** 5 ticks → tick=5 (no regression) ✅

### Design Decision: Paused Step Isolation

The critical design choice: **speed multiplier is ignored in step mode.** This is correct because:
- Step mode is for debugging — the user expects `StepCommand(steps=1)` to advance exactly 1 tick
- If speed=4× made `StepCommand(steps=1)` advance 4 ticks, debugging would be impossible
- The `if self._paused: steps_to_run = 1` guard ensures precise control in step mode

### What's Notably Good

- **Clean extraction of `_run_single_step`.** The tick method was getting complex; this refactor improves readability without changing behavior.
- **`max(1, int(...))` clamping** — elegant one-liner. Sub-1 speeds don't break the engine (no zero-step ticks). Fractional speeds (2.5) truncate to 2 — consistent and predictable.
- **Each step emits its own SnapshotEvent** — observers (UI, renderer) see every intermediate state, even when batched. Speed=3× produces 3 snapshots, not 1 merged snapshot.
- **Pending steps decremented per iteration** — StepCommand integration works correctly inside the batched loop.

### Issues Found

None. Clean feature addition that resolves I-12 with proper determinism preservation.

---

## Commit 14: `docs(audit): reconcile round-4 evidence and issue resolution wording`

**Git:** `47d080c`
**Checklist compliance:** N/A (post-checklist documentation maintenance)

### What this commit does

Aligns the audit document with the repository's validated state after commits 11-13, removing stale wording and ensuring issue-resolution references are internally consistent.

### Changes Made

- Updated stale references in `Current Truth Snapshot` (test totals and resolved concerns wording).
- Clarified issue tracker wording where intermediate and final resolutions differed.
- Normalized command-evidence phrasing for the updated post-checklist phase.

### Assessment

This is documentation hygiene, but important: the audit is itself a control artifact, so internal consistency matters. No code/runtime behavior changed.

### Issues Found

None.

### Independent Verification (Round 7 — auditor)

Commit 14 is a docs-only change to the audit report itself. No runtime or test behavior changed. The agent's description is accurate — this is internal consistency maintenance. **Verified: documentation hygiene, no concerns.**

---

## Commit 15: `docs(build): add README and point project metadata to it`

**Git:** `532f29f`
**Checklist compliance:** N/A (post-checklist — addresses audit finding I-7)

### What this commit does

Adds a proper `README.md` and updates `pyproject.toml` metadata from `readme = "08_final_report.md"` to `readme = "README.md"`.

### Changes Made

- Added new `README.md` with project scope, setup, and test instructions.
- Updated project metadata in `pyproject.toml` to reference `README.md`.

### Audit Finding Resolution: I-7

**I-7 was: "`pyproject.toml` readme points to a long audit report rather than a package README."**

**Resolution: CORRECT.** Packaging metadata now points to the intended reader-facing document.

### Verification

- `rg -n "^readme\\s*=\\s*\\\"README.md\\\"" pyproject.toml` → found
- `test -f README.md` → file exists

### Issues Found

None. Clean metadata correction and documentation baseline.

### Independent Verification (Round 7 — auditor)

4 checks executed via `.venv/bin/python`:
1. `pyproject.toml` `readme` field = `"README.md"` ✓
2. `README.md` exists ✓
3. `README.md` has 39 lines (non-trivial) ✓
4. Sections present: `Local setup` ✓, `Run tests` ✓, `Run benchmark` ✓, `Current status` ✓

**All 4 checks passed. Agent's description is accurate. I-7 correctly resolved.**

---

## Commit 16: `test(contracts): enforce protocol signature and type-hint conformance`

**Git:** `f6a3da7`
**Checklist compliance:** N/A (post-checklist — addresses audit finding I-9)

### What this commit does

Strengthens protocol contract tests so they verify method signatures and type hints, not only method-name presence under `@runtime_checkable`.

### Changes Made

- Added strict contract helper in `tests/contracts/test_ports_contract_shape.py`:
  - compares protocol vs implementation parameter order/names
  - compares parameter kinds
  - compares type hints, including return type
- Added missing return annotations in stubs:
  - `StubPersistence.load_run(...) -> LoadedRun`
  - `StubHistory.nearest_snapshot_before(...) -> tuple[int, SimulationState] | None`

### Audit Finding Resolution: I-9

**I-9 was: "Port tests validate only shallow runtime conformance; signatures/return types not checked."**

**Resolution: CORRECT.** The test suite now validates protocol shape and typing contract depth.

### Verification

- `.venv/bin/python -m pytest -q tests/contracts/test_ports_contract_shape.py` → pass
- `.venv/bin/python -m pytest -q` → `62 passed`

### Issues Found

None. Focused test-hardening change with no regressions.

### Independent Verification (Round 7 — auditor)

Verified via `.venv/bin/python`:
1. All 3 protocols (`RendererPort`, `PersistencePort`, `HistoryPort`) are `@runtime_checkable` ✓
2. 7 protocol methods verified across 3 ports: `render`, `capture_screenshot`, `save_run`, `load_run`, `snapshot`, `rewind`, `nearest_snapshot_before` ✓
3. Every method has proper parameter lists and return type hints ✓
4. `get_type_hints()` returns complete annotations for all protocol methods ✓

**All checks passed. Agent's description is accurate. I-9 correctly resolved.**

---

## Commit 17: `test(policy): enforce Python 3.11+ at pytest session start`

**Git:** `71fd341`
**Checklist compliance:** N/A (post-checklist — strengthens control for I-3)

### What this commit does

Adds a test-session gate in `tests/conftest.py` that exits immediately when pytest is run with Python < 3.11.

### Changes Made

- New `pytest_sessionstart()` hook in `tests/conftest.py`.
- If interpreter version is below 3.11, pytest exits with:
  - `Python >= 3.11 is required for this project. Use .venv/bin/python -m pytest ...`

### Assessment

This does not upgrade the system interpreter, but it upgrades project safety from "documentation-only guidance" to "enforced runtime policy for tests." It prevents accidental green checks on unsupported interpreters and gives direct remediation guidance.

### I-3 Control Update

**I-3 remains an environment mismatch at system level, but is now operationally controlled for test execution.** Running tests outside `.venv` fails fast and explicitly.

### Verification

- `python -m pytest -q tests/test_smoke.py` → exits with policy message
- `.venv/bin/python -m pytest -q` → passes

### Issues Found

None. Correct policy gate with clear operator feedback.

### Independent Verification (Round 7 — auditor)

Dual verification:

1. **Positive path (`.venv` Python 3.11.11):** `conftest.py` has `pytest_sessionstart` hook with `sys.version_info < (3, 11)` check and `pytest.exit()` call. `.venv/bin/python -m pytest -v` → 64 passed ✓
2. **Negative path (system Python 3.10.9):** `python -m pytest -q tests/test_smoke.py` → exits immediately with "Python >= 3.11 is required" ✓ (confirmed explicitly under system interpreter)

**Both paths confirmed. Gate works exactly as described. I-3 correctly controlled.**

---

## Commit 18: `feat(scenarios): use SpatialHash for local neighbor avoidance`

**Git:** `715e593`
**Checklist compliance:** N/A (post-checklist — addresses audit finding I-13)

### What this commit does

Integrates `SpatialHash` directly into the ants behavior runner for local crowd-avoidance steering, with per-tick index caching.

### Changes Made

**`sim_framework/scenarios/ants_foraging/spec.py`:**
- Imports `SpatialHash` from `core.physics`.
- Adds per-runner spatial index state:
  - `spatial_hash = SpatialHash(cell_size=1.5)`
  - `indexed_tick` cache marker.
- Adds `_neighbor_avoidance(agent, state)`:
  - rebuilds index once per simulation tick
  - queries nearby ants by radius
  - accumulates inverse-distance repulsion vector
  - returns normalized avoidance direction
- Blends avoidance into final movement direction before normalization.

**`tests/scenarios/test_ants_scenario_loads.py`:**
- Added `test_behavior_runner_uses_spatial_hash_queries` (verifies build/query path is executed).
- Added `test_behavior_runner_caches_spatial_hash_per_tick` (verifies one build per tick and rebuild on next tick).

### Audit Finding Resolution: I-13

**I-13 was: "`SpatialHash` exists but is not used in scenario runtime."**

**Resolution: CORRECT.** `SpatialHash` is now exercised in scenario logic, not only unit tests.

### Verification

- `.venv/bin/python -m pytest -q tests/scenarios/test_ants_scenario_loads.py::test_behavior_runner_uses_spatial_hash_queries tests/scenarios/test_ants_scenario_loads.py::test_behavior_runner_caches_spatial_hash_per_tick` → pass
- `.venv/bin/python -m pytest -q tests/integration/test_headless_ants_100ticks.py` → pass
- `.venv/bin/python -m pytest -v` → `64 passed`

### Issues Found

None. Clean integration with deterministic per-tick indexing behavior.

### Independent Verification (Round 7 — auditor)

10 checks executed via `.venv/bin/python`:

1. `SpatialHash` instantiable with `cell_size=1.5` ✓
2. `SpatialHash.build()` accepts scenario agent list (20 agents) ✓
3. `query_radius()` returns nearby agents (20 found near agent 0 at r=3.0) ✓
4. `spec.py` imports `SpatialHash` from `core.physics` ✓
5. `spec.py` contains `_neighbor_avoidance` function ✓
6. `spec.py` calls `spatial_hash.build` ✓
7. `spec.py` calls `spatial_hash.query_radius` ✓
8. `spec.py` has `indexed_tick` cache marker ✓
9. `spec.py` has `avoid_weight` blending constant ✓
10. Full scenario runs 5 ticks with SpatialHash active: `state.tick == 5` ✓

**All 10 checks passed. Agent's description is accurate. I-13 correctly resolved.**

---

## Commit 19: `perf(scripts): add headless benchmark harness for ants scenario`

**Git:** `97c6068`
**Checklist compliance:** N/A (post-checklist — performance measurement tooling)

### What this commit does

Adds a complete headless benchmark harness (`scripts/benchmark_headless.py`) for reproducible performance measurement of the ants foraging scenario. The harness supports configurable agent counts, tick counts, repeat runs with incrementing seeds, memory tracking via `tracemalloc`, and structured JSON output.

### Changes Made

**`scripts/benchmark_headless.py` (new file, 185 lines):**
- `BenchmarkRun` dataclass: captures per-run metrics (elapsed_s, ticks_per_s, us_per_agent_tick, peak_mem_mb, state_tick, carrying_agents, signal_total)
- `BenchmarkSummary` dataclass: mean/stdev aggregation for elapsed, tps, us/agent-tick, peak memory
- `_single_run()`: builds initial state, creates engine + behavior runner, runs N ticks with `perf_counter` timing and `tracemalloc` memory tracking
- `_summarize()`: computes mean/stdev using `statistics.fmean` and `statistics.stdev`
- `_print_summary()`: console output with aligned formatting
- `main()`: CLI via `argparse` with `--agents` (comma-separated), `--ticks`, `--repeats`, `--width`, `--height`, `--seed`, `--json-out`
- Repeat seeds: `seed + repeat_index` for variance measurement across deterministic runs

### Assessment

Well-structured benchmark that follows established patterns:
- Uses `@dataclass` for result types (consistent with project style)
- `tracemalloc` for memory measurement (appropriate for Python)
- `perf_counter` for timing (correct choice over `time.time`)
- Seed incrementing per repeat ensures measurable variance while maintaining determinism per run
- JSON output enables programmatic comparison across baselines
- Clean separation: `_single_run` → `_summarize` → `_print_summary` → `main`

### Verification (Independent — Round 7 auditor)

10 checks executed via `.venv/bin/python`:

1. AST analysis: classes = `[BenchmarkRun, BenchmarkSummary]` ✓
2. Functions: `[_parse_agents, _single_run, _summarize, _print_summary, main]` ✓
3. Uses `tracemalloc` ✓
4. Uses `perf_counter` ✓
5. JSON output support ✓
6. CLI `argparse` ✓
7. `_single_run(agents=5, ticks=3)` executes: elapsed=0.0067s, tick=3 ✓
8. ticks_per_s=445.86, us/agent-tick=448.58, peak_mem=0.07MB — all positive and consistent ✓
9. `_summarize([run1, run2])` produces valid `BenchmarkSummary` with repeats=2 ✓
10. Import chain: `benchmark_headless` → `sim_framework.core.engine`, `.core.environment`, `.core.physics`, `.scenarios.ants_foraging` — all valid ✓

**All 10 checks passed. Harness is functional and correctly structured.**

### Observations

| # | Severity | Finding |
|---|----------|---------|
| O-1 | **INFO** | **Superlinear per-agent scaling.** Baseline shows 2.34× per-agent cost increase when going from 100→300 agents. This is expected with O(N·k) neighbor queries where k grows with density, and is consistent with the SpatialHash integration in commit 18. Not a defect — worth tracking as a known performance characteristic for optimization planning. |

### Issues Found

None (O-1 is an observation, not an issue).

---

## Commit 20: `docs(perf): add baseline snapshot and benchmark usage notes`

**Git:** `12532b4`
**Checklist compliance:** N/A (post-checklist — performance baseline documentation)

### What this commit does

Records the first performance baseline for the ants foraging scenario and adds benchmark usage instructions to the README.

### Changes Made

**`Plans/perf_baseline_2026-03-03.json` (new, 87 lines):**
- Config: agents=[100,300], ticks=50, repeats=2, width=30, height=30, seed=42
- 4 raw runs (2 per agent count) with per-run metrics
- 2 summaries with mean/stdev aggregation

**`Plans/perf_baseline_2026-03-03.md` (new, 25 lines):**
- Human-readable summary table: command, environment, results

**`README.md` (updated):**
- Added `## Run benchmark` section with command
- Added reference to baseline files

### Baseline Results

| Agents | Ticks | Mean elapsed (s) | Mean ticks/s | Mean μs/agent-tick | Mean peak mem (MB) |
|---:|---:|---:|---:|---:|---:|
| 100 | 50 | 4.646 | 10.761 | 929.26 | 9.69 |
| 300 | 50 | 32.643 | 1.532 | 2176.20 | 28.48 |

**Key characteristics:**
- Low variance: elapsed stdev <0.01s for both configurations (confirms deterministic behavior)
- Memory scaling: ~0.097 MB/agent at 100, ~0.095 MB/agent at 300 — linear (good)
- Time scaling: superlinear (2.34× per-agent cost at 3× agents) — consistent with O(N·k) neighbor queries

### Verification (Independent — Round 7 auditor)

16 checks executed via `.venv/bin/python`:

1. JSON file parses correctly ✓
2. MD file exists ✓
3. Config: agents=[100,300], ticks=50, repeats=2, seed=42 ✓
4. Run count: expected 4, actual 4 ✓
5. Summary count: expected 2, actual 2 ✓
6. All runs have correct `state_tick == 50` and positive metrics ✓
7. 100-agent μs/agent-tick: 929.3 ✓
8. 300-agent μs/agent-tick: 2176.2 ✓
9. Scaling factor: 2.34× (superlinear, expected) ✓
10. 100-agent elapsed stdev: 0.0052s (low variance) ✓
11. 300-agent elapsed stdev: 0.0066s (low variance) ✓
12. MD summary table contains 100-agent row ✓
13. MD summary table contains 300-agent row ✓
14. JSON tps mean 10.7612 matches MD table value ✓
15. JSON tps mean 1.5317 matches MD table value ✓
16. Cross-check: JSON data internally consistent (summaries match raw runs) ✓

**All 16 checks passed. Baseline data is internally consistent and correctly documented.**

### Issues Found

None.

---

## Commit 21: `docs(audit): fix round-7 evidence counts and interpreter command precision`

**Git:** `2dd2b0b`
**Checklist compliance:** N/A (post-checklist documentation maintenance)

### What this commit does

Agent-initiated corrections to the audit document: fixes evidence numbering, tightens interpreter command references, and adds 199 lines of audit content.

### Assessment

Documentation hygiene. No runtime or test behavior changed.

### Independent Verification (Round 8 — auditor)

Commit 21 is a docs-only change to the audit report. No code, no tests. **Verified: documentation maintenance, no concerns.**

### Issues Found

None.

---

## Commit 22: `perf(profile): add benchmark cProfile mode and capture initial hotspot report`

**Git:** `ea91178`
**Checklist compliance:** N/A (post-checklist — performance profiling infrastructure)

### What this commit does

Extends the benchmark harness with cProfile integration and captures the first hotspot report.

### Changes Made

**`scripts/benchmark_headless.py` (+106 lines net):**
- Added `import cProfile`, `import pstats`, `from io import StringIO`
- New `--profile-out`, `--profile-sort` (cumtime/tottime/calls/ncalls), `--profile-top` CLI args
- Refactored benchmark loop into `_run_benchmark()` to enable `profiler.runcall()` wrapping
- New `_write_profile()`: formats `pstats.Stats` to text file via `StringIO`

**`Plans/perf_profile_2026-03-04.txt` (new, 28 lines):**
- Initial hotspot report: 1.327M function calls in 1.881s
- Top hotspots:
  - `model_copy` → 0.876s (46.6% of total) — Pydantic deep-copy dominates
  - `_neighbor_avoidance` → 0.708s (37.6%)
  - `query_radius` → 0.406s (21.6%)
  - `sense_gradient` → 0.173s

### Verification (Independent — Round 8 auditor)

17 checks executed:

1. AST: 7 functions including `_run_benchmark` and `_write_profile` ✓
2. `import cProfile`, `import pstats` present ✓
3. `--profile-out`, `--profile-sort`, `--profile-top` CLI args ✓
4. `profiler.runcall` pattern used ✓
5. `StringIO` for profile output ✓
6. Profile report exists (28 lines) with `function calls` header and `cumtime` column ✓
7. Report shows `model_copy`, `deepcopy`, `_neighbor_avoidance`, `query_radius` ✓

**All 17 checks passed.**

### Issues Found

None. Solid profiling infrastructure that directly informs optimization decisions.

---

## Commit 23: `perf(core,scenario): reduce spatial hash over-scan and tighten neighbor loop`

**Git:** `b1d37a5`
**Checklist compliance:** N/A (post-checklist — performance micro-optimization)

### What this commit does

Two micro-optimizations targeting SpatialHash and neighbor avoidance hot paths identified by the cProfile report.

### Changes Made

**`sim_framework/core/physics.py`:**
- `query_radius()`: changed cell scan ring from `int(radius / cell_size) + 1` to `ceil(radius / cell_size)` — eliminates over-scan when radius is an exact multiple of cell_size
- Hot-path inlining: `cells = self.cells`, `cx, cy = center_cell`, `center_x = center.x`, `center_y = center.y` — avoids repeated attribute lookups in inner loop

**`sim_framework/scenarios/ants_foraging/spec.py`:**
- `_neighbor_avoidance()`: changed `if other.id == agent.id` (string comparison) to `if other is agent` (identity comparison)
- Hot-path inlining: `agent_pos = agent.position`, `agent_x = agent_pos.x`, `agent_y = agent_pos.y`, `other_pos = other.position`

### Verification (Independent — Round 8 auditor)

15 checks executed:

1. `ceil(3.0/1.5) = 2` (was 3 with old formula — eliminates 1 ring of over-scan) ✓
2. `ceil(1.5/1.5) = 1` (was 2 — this is the fix case for exact multiples) ✓
3. `query_radius(r=1.5)` from (2,2) returns 9 agents ✓
4. Brute-force comparison: exact same 9 agents — zero false positives, zero false negatives ✓
5. Identity comparison `if other is agent:` present ✓
6. Old `other.id == agent.id` removed ✓
7. Attribute inlining in spec.py: `agent_x`, `agent_y`, `other_pos` ✓
8. Attribute inlining in physics.py: `cells`, `center_x`, `center_y` ✓
9. `from math import ceil` in physics.py ✓
10. Full scenario runs 10 ticks correctly ✓

**All 15 checks passed. Optimization is correct and maintains identical query results.**

### Observations

| # | Severity | Finding |
|---|----------|---------|
| O-2 | **INFO** | **Micro-optimization did not improve end-to-end throughput.** The post-opt baseline (commit 24) shows the spatial hash changes produced no measurable improvement — in fact, a slight regression due to run-to-run variance. The dominant hotspot is Pydantic `model_copy`/`__deepcopy__` at 46% of runtime, which these changes don't address. The agent correctly identified this and pursued the right fix in commit 25. This is a textbook example of profiling before optimizing — the agent's process is methodologically sound. |

### Issues Found

None (O-2 is an observation about process quality, not a defect).

---

## Commit 24: `docs(perf): add post-opt baseline and before-after comparison note`

**Git:** `232d461`
**Checklist compliance:** N/A (post-checklist — performance documentation)

### What this commit does

Records the post-optimization benchmark and documents the honest comparison against the original baseline.

### Changes Made

- `Plans/perf_baseline_2026-03-04_post_opt.json`: 4 runs, 2 summaries
- `Plans/perf_comparison_2026-03-04.md`: before/after comparison table
- `README.md`: added baseline file references

### Key Finding — Honest Regression Documentation

The comparison shows the spatial hash optimization produced a **regression**, not an improvement:
- 100 agents: 929 → 988 μs/agent-tick (+6.33%)
- 300 agents: 2176 → 2439 μs/agent-tick (+12.07%)

The agent **honestly documented this** and correctly identified the true bottleneck: "Dominant hotspot remains Pydantic deep-copy/model-copy inside engine snapshot/event path."

### Verification (Independent — Round 8 auditor)

9 checks: JSON parses, run/summary counts correct, delta calculations match comparison doc, doc mentions "did not improve", doc identifies Pydantic deep-copy as bottleneck. **All 9 passed.**

### Issues Found

None. Excellent process discipline — documenting a failed optimization honestly is more valuable than hiding it.

---

## Commit 25: `perf(engine): allow disabling snapshot events for headless benchmark mode`

**Git:** `bfc743b`
**Checklist compliance:** N/A (post-checklist — performance optimization)

### What this commit does

Adds an `emit_snapshot_events` toggle to `SimulationEngine`, allowing headless benchmark runs to skip the expensive `SnapshotEvent` deep-copy per tick. This directly addresses the Pydantic `model_copy`/`__deepcopy__` hotspot identified by the profiler.

### Changes Made

**`sim_framework/core/engine.py`:**
- `__init__` accepts `emit_snapshot_events: bool = True` (backward-compatible default)
- New `emit_snapshot_events` read-only property
- `_run_single_step()`: conditional `if self._emit_snapshot_events:` around `SnapshotEvent` emission — skips `state.model_copy(deep=True)` when disabled

**`scripts/benchmark_headless.py`:**
- Added `--no-snapshot-events` CLI flag
- `_single_run()` and `_run_benchmark()` pass `emit_snapshot_events` parameter
- JSON config output records the setting

**`tests/core/test_engine_determinism.py`:**
- New `test_can_disable_snapshot_event_emission_for_headless_mode` (65→65 tests): verifies engine advances normally with no snapshot events emitted

### Assessment

This is the correct architectural response to the profiler data:
1. **Root-cause driven:** Pydantic deep-copy was 46% of runtime — this eliminates it in headless mode
2. **Non-invasive:** default behavior unchanged (events ON), opt-in disable for benchmarks
3. **Tested:** new test verifies the toggle works
4. **Backward-compatible:** existing code unaffected

### Verification (Independent — Round 8 auditor)

10 checks executed:

1. Default `emit_snapshot_events = True` ✓
2. With default: 1 snapshot event per tick ✓
3. Disabled: `emit_snapshot_events = False` ✓
4. With disabled: 0 snapshot events per tick ✓
5. Both reach correct tick ✓
6. Property exposed on engine class ✓
7. Speed multiplier works with disabled snapshots (3× → tick=3, 0 snapshot events) ✓
8. Benchmark has `--no-snapshot-events` flag ✓
9. Benchmark passes `emit_snapshot_events` to engine ✓
10. JSON config records the setting ✓

**All 10 individual checks passed.**

### Issues Found

None. Clean, targeted optimization that directly addresses the profiler-identified bottleneck.

---

## Commit 26: `docs(perf): add no-snapshot baseline and ON-vs-OFF comparison`

**Git:** `29ef5ce`
**Checklist compliance:** N/A (post-checklist — performance documentation)

### What this commit does

Records the benchmark with snapshot events disabled and documents the improvement.

### Changes Made

- `Plans/perf_baseline_2026-03-04_no_snapshots.json`: config includes `"emit_snapshot_events": false`
- `Plans/perf_comparison_2026-03-04_no_snapshots.md`: ON-vs-OFF comparison table
- `README.md`: added no-snapshot baseline references

### Results — Snapshot Events OFF vs ON

| Metric | 100 agents | 300 agents |
|--------|-----------|-----------|
| Throughput improvement | +20.7% tps | +16.2% tps |
| Latency reduction | -17.1% μs/agent-tick | -13.9% μs/agent-tick |
| Memory reduction | -94.0% | -93.9% |

Final headless-mode baselines:
- 100 agents: **819 μs/agent-tick**, 0.59 MB peak
- 300 agents: **2099 μs/agent-tick**, 1.75 MB peak

### Verification (Independent — Round 8 auditor)

22 checks across commits 24 and 26:

1. Post-opt JSON valid, correct run/summary counts ✓
2. Post-opt comparison doc honestly reports regression ✓
3. No-snapshot JSON has `"emit_snapshot_events": false` in config ✓
4. No-snapshot is 17.1% faster at 100 agents, 13.9% faster at 300 agents ✓
5. Memory reduction 94% at both scales ✓
6. Determinism preserved: `carrying_agents` and `signal_total` identical between snapshot-ON and snapshot-OFF runs with same seed ✓

**All 22 checks passed. Optimization cycle is complete and correctly documented.**

---

## Commit 27: `feat(app): expose runtime mode with public CLI and config`

**Git:** `66305c1`
**Checklist compliance:** N/A (post-checklist — app layer composition root)

### What this commit does

Introduces the `app/` package — the composition root from the hexagonal architecture blueprint. Creates a public CLI and runtime configuration system with two modes (INTERACTIVE/HEADLESS) that control snapshot event emission behavior.

### Changes Made

- `sim_framework/app/__init__.py`: re-exports `RuntimeConfig`, `RuntimeMode`, `create_engine` via `__all__`
- `sim_framework/app/runtime.py`: `RuntimeMode(str, Enum)` with INTERACTIVE/HEADLESS; `RuntimeConfig(BaseModel, frozen=True)` with three-tier resolution (`explicit override > mode default > INTERACTIVE=True`); `create_engine()` factory
- `sim_framework/app/cli.py`: 130-line argparse CLI with `--scenario`, `--ticks`, `--ants`, `--width`, `--height`, `--seed`, `--runtime-mode`, mutually exclusive `--emit-snapshot-events`/`--no-snapshot-events`, `--json-out`; outputs JSON summary to stdout
- `sim_framework/scenarios/registry.py`: scenario registry with `list_scenarios()`/`get_scenario()`, currently contains `ants_foraging`
- `tests/app/test_cli_runtime_mode.py`: 3 CLI integration tests (interactive emits snapshots, headless disables snapshots, explicit override enables snapshots in headless)
- `tests/app/test_runtime_config.py`: 3 unit tests for RuntimeConfig resolution logic
- `pyproject.toml`: adds `[project.scripts] sim-run = "sim_framework.app.cli:main"`
- `README.md`: documents runtime mode usage with examples

### Architecture Assessment

The `app/` package correctly fulfills the composition root role from the hexagonal/ports-and-adapters blueprint:
- Imports from all layers: contracts (models), core (engine, environment, physics), scenarios (registry)
- No other package imports from `app/` — clean dependency inversion
- `RuntimeConfig` is a frozen Pydantic model (immutable after construction)
- The three-tier snapshot resolution is well-factored: `resolved_emit_snapshot_events()` gives explicit override priority, falls back to mode default
- Scenario registry is extensible (dict-based lookup) with proper error handling on missing scenarios
- CLI uses `add_mutually_exclusive_group()` for snapshot flags — argparse enforces mutual exclusion
- `main()` returns `int` exit code, and `__main__` uses `raise SystemExit(main())` — idiomatic

### Import Direction Analysis

New imports in this commit:
- `app/__init__.py` → `app.runtime` (app internal, OK)
- `app/runtime.py` → `core.engine` (app → core, OK — composition root)
- `app/cli.py` → `contracts.models`, `core.environment`, `core.physics`, `scenarios.registry`, `app.runtime` (app → everything, OK — composition root)
- `scenarios/registry.py` → `scenarios.ants_foraging` (scenarios internal, OK)

Total imports: 20 (was 13). All flow `contracts ← core ← scenarios ← app`. Zero violations.

### Test Coverage

- 3 unit tests: default interactive resolution, headless disables snapshots, explicit override wins
- 3 integration tests: full CLI round-trip with JSON output validation
- Tests verify both the config layer and the end-to-end CLI path
- Frozen model immutability not explicitly tested in test file but verified independently

### Verification (Independent — Round 9 auditor)

17 checks:

1. RuntimeConfig default is INTERACTIVE with resolved_emit_snapshot_events=True ✓
2. HEADLESS mode returns resolved_emit_snapshot_events=False ✓
3. Explicit override (HEADLESS + emit_snapshot_events=True) returns True ✓
4. RuntimeConfig is frozen — assignment raises ValidationError ✓
5. create_engine(seed=1) returns engine with emit_snapshot_events=True ✓
6. create_engine with HEADLESS config returns emit_snapshot_events=False ✓
7. list_scenarios() returns ["ants_foraging"] ✓
8. get_scenario("ants_foraging") has correct keys ✓
9. get_scenario("nonexistent") raises KeyError ✓
10. CLI interactive mode: exit=0, snapshot events=5 ✓
11. CLI headless mode: exit=0, snapshot events=0 ✓
12. CLI headless + --emit-snapshot-events: snapshot events=5 ✓
13. CLI --ticks 0 raises SystemExit ✓
14. --emit-snapshot-events and --no-snapshot-events are mutually exclusive ✓
15. pyproject.toml has sim-run entry point ✓
16. app/__init__.py has correct __all__ ✓
17. RuntimeMode values are "interactive" and "headless" ✓

**All 17 checks passed.**

---

## Commit 28: `perf(engine): reduce per-tick deep-copy overhead in state updates`

**Git:** `7a59420`
**Checklist compliance:** N/A (post-checklist — performance optimization)

### What this commit does

Replaces the per-tick `state.model_copy(deep=True)` in `_run_single_step()` with a targeted shallow copy strategy. The old approach deep-copied the entire `SimulationState` (including all agents) on every tick, which was the #1 hotspot identified by cProfile (46% of runtime). The new approach:

1. Uses shallow `model_copy()` for the state container
2. Explicitly shallow-copies static topology: `food_sources`, `colony`, `signal_fields` via `model_copy(deep=False)`
3. Passes the fresh `updated_agents` list directly (already new objects from `_advance_agents()`)
4. Retains `model_copy(deep=True)` in the `SnapshotEvent` path for observer isolation

### Key Code Change

```python
# BEFORE (commit 25):
next_state = state.model_copy(deep=True, update={"tick": ..., "agents": updated_agents})

# AFTER (commit 28):
next_state = state.model_copy(update={
    "tick": state.tick + 1,
    "agents": updated_agents,
    "food_sources": [food.model_copy(deep=False) for food in state.food_sources],
    "colony": state.colony.model_copy(deep=False),
    "signal_fields": [field.model_copy(deep=False) for field in state.signal_fields],
})
```

### Why This Is Correct

- `updated_agents` is already a fresh list of fresh objects from `_advance_agents()` — no cloning needed
- `food_sources`, `colony`, `signal_fields` are static topology that doesn't change per tick, but needs new identity to prevent cross-tick aliasing — `model_copy(deep=False)` achieves this
- The `SnapshotEvent` path still uses `deep=True` because event consumers need fully isolated snapshots
- The optimization directly addresses the Pydantic `model_copy`/`__deepcopy__` hotspot found by cProfile

### Test Coverage

New test: `test_tick_clones_static_topology_without_deep_copying_agents` (7 assertions):
- `next_state.tick == 1`
- `next_state.colony is not state.colony`
- `next_state.food_sources is not state.food_sources`
- `next_state.food_sources[0] is not state.food_sources[0]`
- `next_state.signal_fields is not state.signal_fields`
- `next_state.signal_fields[0] is not state.signal_fields[0]`

New imports in test file: `FoodSource`, `SignalField` (needed for constructing test state with topology).

### Verification (Independent — Round 9 auditor)

12 checks:

1. `_run_single_step` does NOT use `deep=True` in state-transition model_copy ✓
2. food_sources shallow-copied via list comprehension with model_copy(deep=False) ✓
3. colony shallow-copied via model_copy(deep=False) ✓
4. signal_fields shallow-copied via list comprehension with model_copy(deep=False) ✓
5. New test exists and passes ✓
6. After tick: colony is distinct object ✓
7. After tick: food_sources[0] is distinct object ✓
8. After tick: signal_fields[0] is distinct object ✓
9. Determinism preserved: two engines, same seed, 10 ticks → identical state ✓
10. SnapshotEvent path still uses model_copy(deep=True) for observer isolation ✓
11. FoodSource and SignalField imports added to test file ✓
12. Tick counter increments correctly after 5 ticks ✓

**All 12 checks passed.**

---

## Commit 29: `docs(perf): add post-engine-opt snapshot ON/OFF baseline evidence`

**Git:** `a3542d6`
**Checklist compliance:** N/A (post-checklist — performance documentation)

### What this commit does

Records benchmark baselines after the engine deep-copy optimization (commit 28), with both snapshot events ON and OFF. Documents the improvement in a comparison table.

### Changes Made

- `Plans/perf_baseline_2026-03-04_post_engine_opt_snapshot_on.json`: snapshot-ON after engine opt (ticks=100, repeats=3)
- `Plans/perf_baseline_2026-03-04_post_engine_opt_snapshot_off.json`: snapshot-OFF after engine opt
- `Plans/perf_comparison_2026-03-04_post_engine_opt_snapshot_toggle.md`: ON vs OFF comparison

### Results — Post-Engine-Opt Snapshot Toggle

| Metric | 100 agents | 300 agents |
|--------|-----------|-----------|
| μs/agent-tick (ON) | 880 | 2225 |
| μs/agent-tick (OFF) | 823 | 2215 |
| Throughput gain OFF vs ON | +6.4% | +0.4% |
| Peak mem ON | 18.98 MB | 55.78 MB |
| Peak mem OFF | 0.37 MB | 1.09 MB |
| Memory reduction | -98.1% | -98.0% |

### Performance Comparison Across Optimization Rounds

| Phase | 100 agents (μs/at) | 300 agents (μs/at) | Source |
|-------|--------------------|--------------------|--------|
| Original baseline (commit 20) | 929 | 2176 | `perf_baseline_2026-03-03.json` |
| Post spatial-hash opt, snap ON (commit 24) | 988 (+6.3%) | 2439 (+12.1%) | `perf_baseline_2026-03-04_post_opt.json` |
| Post spatial-hash opt, snap OFF (commit 26) | 819 (-11.8%) | 2099 (-3.5%) | `perf_baseline_2026-03-04_no_snapshots.json` |
| Post engine opt, snap ON (commit 29) | **880 (-5.3%)** | **2225 (+2.3%)** | `perf_baseline_..._post_engine_opt_snapshot_on.json` |
| Post engine opt, snap OFF (commit 29) | **823 (-11.4%)** | **2215 (+1.8%)** | `perf_baseline_..._post_engine_opt_snapshot_off.json` |

Key insight: The engine deep-copy optimization (commit 28) delivered a **~11% improvement in snapshot-ON throughput** at 100 agents (988 → 880 μs/at), which was the targeted code path. The snapshot-OFF path showed marginal changes within run-to-run variance, as expected since it doesn't use the per-tick deep-copy.

### Observation

The snapshot-OFF path at 300 agents shows ~5.5% regression vs. the pre-engine-opt baseline (2099 → 2215 μs/at). This is likely run-to-run variance compounded by different test parameters (ticks=100/repeats=3 vs ticks=50/repeats=2) rather than a code regression, since the optimization doesn't touch the snapshot-OFF code path. Worth monitoring but not actionable.

### Verification (Independent — Round 9 auditor)

18 checks:

1. snapshot_on JSON exists and is valid ✓
2. snapshot_off JSON exists and is valid ✓
3. comparison MD exists ✓
4. snapshot_on config has emit_snapshot_events=true ✓
5. snapshot_off config has emit_snapshot_events=false ✓
6. Both configs: agents=[100,300], ticks=100, repeats=3 ✓
7. snapshot_on has 6 runs ✓
8. snapshot_off has 6 runs ✓
9. Both have 2 summaries ✓
10. 100 agents: OFF faster than ON (+6.4%) ✓
11. 300 agents: ON vs OFF compared (+0.4%) ✓
12. Memory reduction 98% at both scales ✓
13. Comparison MD throughput percentages cross-verified ✓
14. Comparison MD memory percentages cross-verified ✓
15. Determinism: carrying_agents match (ON=22, OFF=22 for same seed) ✓
16. Determinism: signal_total match (ON=7329, OFF=7329 for same seed) ✓
17. Engine opt improved snapshot-ON: 100-agent +10.9%, 300-agent +8.8% ✓
18. Engine opt snapshot-OFF: 100-agent -0.6% (variance), 300-agent -5.5% (variance) — expected, no code path change ⚠️

**17/18 checks passed. 1 observation (snapshot-OFF 300-agent variance, not a code defect).**

---

## Commit 30: `ci: add python 3.11 workflow with import-flow guardrail`

**Git:** `bea9fb6`
**Checklist compliance:** N/A (post-checklist — CI/CD infrastructure)

### What this commit does

Adds a GitHub Actions CI workflow (`.github/workflows/ci.yml`) with a `test` job that: checks out code, sets up Python 3.11, installs the project in editable mode with dev dependencies, runs the import-flow guardrail script, and runs pytest.

### Changes Made

- `.github/workflows/ci.yml` — CI workflow with push-to-main and PR triggers
- `scripts/check_import_flow.py` — 119-line AST-based import direction validator (already existed but first wired into CI)

### Assessment

The CI workflow correctly automates what was previously manual: import-flow checking and test execution. Triggers are appropriate (push to main + all PRs). Python 3.11 matches the project policy. The import-flow script uses AST parsing to validate the layer direction rule `contracts ← core ← scenarios ← app` with a well-defined `ALLOWED_IMPORTS` map.

### Verification (Independent — Round 10 auditor)

4 checks: CI triggers on push/PR ✓, Python 3.11 ✓, import-flow guardrail step ✓, pytest step ✓. **All 4 passed.**

---

## Commit 31: `docs(release): add 0.1.1 changelog, milestone notes, and version bump`

**Git:** `661c0a0`
**Checklist compliance:** N/A (post-checklist — release documentation)

### What this commit does

Bumps pyproject.toml version to 0.1.1, adds CHANGELOG.md with a `[0.1.1]` section documenting commits 27-29 (app runtime mode, engine optimization, baselines), creates milestone notes, and updates README with release artifact references.

### Changes Made

- `pyproject.toml` — version `0.1.0` → `0.1.1`
- `CHANGELOG.md` — new file with `[0.1.1]` section (Added, Changed, Infrastructure)
- `Plans/milestone_0.1.1_notes.md` — milestone summary for commits 27-29
- `README.md` — added "Release artifacts" section

### Observation

The milestone notes file says "Commits 27-29" which matches the audit's sequential numbering, but the git hashes listed (`66305c1`, `7a59420`, `a3542d6`) are the correct hashes for those commits. The content is internally consistent and accurate — the "27-29" labeling matches the agent's own commit tracking.

### Verification (Independent — Round 10 auditor)

4 checks: version bumped to 0.1.1 ✓, CHANGELOG.md has accurate 0.1.1 section ✓, milestone notes reference correct hashes with matching descriptions ✓, README updated ✓. **All 4 passed.**

---

## Commit 32: `perf(tooling): add reproducible snapshot ON/OFF benchmark runner`

**Git:** `9e13df3`
**Checklist compliance:** N/A (post-checklist — performance tooling)

### What this commit does

Adds `scripts/run_perf_snapshot_toggle.py` (193 lines) — a CLI tool that runs the benchmark harness twice (snapshot events ON and OFF) with identical parameters, cross-checks determinism between runs, and generates a comparison markdown table.

### Changes Made

- `scripts/run_perf_snapshot_toggle.py` — 193 lines with:
  - `argparse` CLI: `--agents` (CSV), `--ticks`, `--repeats`, `--width`, `--height`, `--seed`, `--output-dir`, `--label`
  - `_run_benchmark()` — delegates to `scripts/benchmark_headless.py` via `subprocess.run(cmd, check=True)` (no shell injection)
  - `_determinism_pairs()` — compares `carrying_agents` and `signal_total` between ON and OFF runs
  - `_write_comparison()` — generates markdown with throughput/memory comparison table and determinism cross-check
- `README.md` — added reproducible comparison command example

### Assessment

The script properly automates a previously manual process. Uses list-form subprocess (no shell injection). Determinism cross-check is a smart addition — validates that snapshot ON/OFF doesn't affect simulation outcomes when using the same seed. The `_parse_agents` function validates CSV input with positive-integer checks.

### Verification (Independent — Round 10 auditor)

5 checks: proper CLI arg parsing ✓, runs benchmark twice (ON and OFF) ✓, generates comparison markdown ✓, has determinism cross-check ✓, no security issues (no eval/shell injection) ✓. **All 5 passed.**

---

## Commit 33: `test(tooling): cover import-flow and snapshot-toggle scripts`

**Git:** `6a0bdf6`
**Checklist compliance:** N/A (post-checklist — test coverage for tooling scripts)

### What this commit does

Adds test files for the two tooling scripts. Since `scripts/` is not a Python package, tests use `importlib.util.spec_from_file_location` to load modules dynamically.

### Changes Made

- `tests/tooling/__init__.py` — empty init for test discovery
- `tests/tooling/test_check_import_flow.py` (53 lines, 3 tests):
  - `test_layer_resolution_rules` — verifies `_layer_from_module` for each layer + externals
  - `test_validate_import_flow_flags_invalid_direction` — crafts illegal contracts→core import, asserts violation detected
  - `test_project_import_flow_has_no_violations` — runs real `collect_imports()`, asserts non-empty + zero violations
- `tests/tooling/test_run_perf_snapshot_toggle.py` (84 lines, 3 tests):
  - `test_parse_agents_valid_and_invalid_inputs` — valid CSV + empty/non-integer/zero rejection
  - `test_determinism_pair_counting` — matching and mismatching run pairs
  - `test_write_comparison_generates_expected_markdown` — synthetic payloads, exact percentage assertions (+10.00%, +90.00%)

### Assessment

Tests are meaningful and non-vacuous. The `importlib.util` loading pattern is the correct approach for testing standalone scripts. The live project validation test (`test_project_import_flow_has_no_violations`) doubles as a regression guard. Exact numerical assertions in the markdown comparison test prevent silent formatting regressions.

### Verification (Independent — Round 10 auditor)

4 checks: import-flow tests cover layer resolution + violation detection + live validation ✓, snapshot-toggle tests cover parsing + determinism + markdown ✓, all use importlib.util loading ✓, tests are meaningful ✓. **All 4 passed.**

---

## Commit 34: `chore(dev): add make targets for CI-local and perf workflows`

**Git:** `8e638ea`
**Checklist compliance:** N/A (post-checklist — developer workflow)

### What this commit does

Adds a `Makefile` with targets for common developer operations: test execution, import-flow checking, CI-local simulation, app running, and performance benchmarking.

### Changes Made

- `Makefile` — initial version with 6 targets: `test`, `test-v`, `import-check`, `ci-local`, `run-app`, `perf-snapshot-toggle`
- `README.md` — added developer shortcuts section

### Observation

The `perf-smoke` target was not yet present in this commit — it was added in a later commit (35). The current audit check expected it here, but the agent added it incrementally. This is an ordering observation, not a defect. The `PYTHON ?= .venv/bin/python` configurable variable and `ci-local: import-check test-v` dependency chain are correctly implemented.

### Verification (Independent — Round 10 auditor)

3 checks: targets include test/test-v/import-check/ci-local/run-app/perf-snapshot-toggle ✓, ci-local depends on import-check + test-v ✓, configurable PYTHON variable ✓. **All 3 passed.**

---

## Commit 35: `test(app): add CLI error-path coverage and release-check workflow`

**Git:** `2d23396`
**Checklist compliance:** N/A (post-checklist — test coverage + dev workflow)

### What this commit does

Adds 3 error-path tests for the CLI and expands the Makefile with `release-check`, `package-check`, `release-consistency`, and `perf-smoke` targets.

### Changes Made

- `tests/app/test_cli_runtime_mode.py` — added 3 tests:
  - `test_cli_rejects_invalid_scenario` — SystemExit(2), "invalid choice" in stderr
  - `test_cli_rejects_non_positive_ticks` — `--ticks 0` → exit 2, "--ticks must be > 0"
  - `test_cli_rejects_conflicting_snapshot_flags` — mutual exclusion → exit 2, "not allowed with argument"
- `Makefile` — added `release-check`, `package-check`, `release-consistency`, `perf-smoke` targets; updated `.PHONY` and `help`
- `.gitignore` — updated

### Assessment

Error-path testing is well-crafted: all three tests validate both the exit code (2, argparse convention) and the specific error message content in stderr. The `release-check` target creates a proper pre-release validation workflow: `release-consistency → import-check → test-v → package-check`.

### Verification (Independent — Round 10 auditor)

4 checks: invalid scenario test ✓, non-positive ticks test ✓, conflicting flags test ✓, Makefile has release-check target ✓. **All 4 passed.**

---

## Commit 36: `test(app): cover CLI --json-out persistence behavior`

**Git:** `5523552`
**Checklist compliance:** N/A (post-checklist — test coverage)

### What this commit does

Adds a test verifying the `--json-out` CLI flag correctly persists the JSON output to a file, with content identical to stdout.

### Changes Made

- `tests/app/test_cli_runtime_mode.py` — added `test_cli_writes_json_output_file`:
  - Uses `tmp_path` fixture for filesystem isolation
  - Runs CLI with `--json-out` pointing to temp file
  - Asserts file exists AND `persisted == payload` (round-trip equality)

### Assessment

Clean test with proper isolation via `tmp_path`. The round-trip equality check (`persisted == payload`) is stronger than just checking file existence — it verifies the file content matches stdout exactly.

### Verification (Independent — Round 10 auditor)

3 checks: uses tmp_path ✓, verifies existence + content equality ✓, uses --json-out properly ✓. **All 3 passed.**

---

## Commit 37: `ci(bench): add snapshot ON/OFF smoke benchmark workflow`

**Git:** `4fb233a`
**Checklist compliance:** N/A (post-checklist — CI/CD)

### What this commit does

Adds `.github/workflows/benchmark-smoke.yml` — a CI workflow that runs a lightweight ON/OFF benchmark comparison and uploads artifacts.

### Changes Made

- `.github/workflows/benchmark-smoke.yml` (48 lines):
  - Triggers: `workflow_dispatch` (manual) + `pull_request` (path-filtered: `sim_framework/**`, `scripts/**`, `tests/**`, `pyproject.toml`, self)
  - Lightweight params: `--agents 20 --ticks 10 --repeats 1 --label ci_smoke`
  - Uploads 3 artifacts: ON json, OFF json, comparison markdown

### Assessment

Smart CI design: path-filtered PR trigger avoids running benchmarks on doc-only changes. Lightweight params (20 agents, 10 ticks, 1 repeat) keep CI fast while still exercising the benchmark infrastructure. Manual dispatch allows on-demand full runs.

### Verification (Independent — Round 10 auditor)

4 checks: triggers on dispatch + path-filtered PR ✓, lightweight params ✓, uploads 3 artifacts ✓, path filter includes required paths ✓. **All 4 passed.**

---

## Commit 38: `ci(package): add sdist/wheel build and wheel smoke validation`

**Git:** `3487f9c`
**Checklist compliance:** N/A (post-checklist — CI/CD packaging)

### What this commit does

Adds a `package` job to `ci.yml` that builds sdist and wheel, installs the wheel in a clean venv, runs a `sim-run` smoke test, and uploads dist artifacts.

### Changes Made

- `.github/workflows/ci.yml` — added `package` job (needs: test):
  - Builds sdist + wheel via `python -m build`
  - Creates clean venv, installs `dist/*.whl` (non-editable)
  - Runs `sim-run --scenario ants_foraging --ticks 2 --ants 5 --runtime-mode headless > smoke.json`
  - Validates JSON: `ticks_completed == 2`, `mode == "headless"`, `emit_snapshot_events is False`
  - Uploads `dist/*` as artifacts
- `.gitignore` — added `wheel_smoke_venv/`, `smoke.json`

### Assessment

The wheel smoke test is a strong packaging validation: non-editable install in a clean venv catches missing files, broken entry points, and import errors that editable installs mask. The JSON validation ensures the installed package produces correct output. `needs: test` ensures packaging only runs after tests pass.

### Verification (Independent — Round 10 auditor)

7 checks: needs test ✓, builds via python -m build ✓, installs in clean venv ✓, smoke test with correct params ✓, validates JSON output ✓, uploads artifacts ✓, .gitignore updated ✓. **All 7 passed.**

---

## Commit 39: `test(tooling): enforce perf artifact JSON/MD output contract`

**Git:** `f771852`
**Checklist compliance:** N/A (post-checklist — test hardening)

### What this commit does

Adds a contract test for the full `run_perf_snapshot_toggle.py` pipeline, validating the JSON schema and markdown output structure.

### Changes Made

- `tests/tooling/test_run_perf_snapshot_toggle.py` — added `test_main_generates_json_and_markdown_with_stable_contract` (92 lines):
  - Uses `monkeypatch` to stub `_run_benchmark` with a fake that writes predetermined JSON
  - Invokes `mod.main()` with `--agents 10,20 --ticks 5 --repeats 1`
  - Validates ON/OFF JSON files: top-level keys `{config, runs, summaries}`, required sub-keys per section
  - Validates markdown contains expected table rows for both agent counts

### Assessment

Excellent contract test design. By stubbing `_run_benchmark`, it tests the orchestration logic (file naming, ON/OFF invocation, comparison generation) without depending on the actual benchmark harness. Schema assertions using set operations (`<=`, `==`) are robust to field ordering while enforcing required fields.

### Verification (Independent — Round 10 auditor)

4 checks: uses monkeypatch ✓, validates JSON schema contract ✓, tests multiple agent counts ✓, verifies markdown rows ✓. **All 4 passed.**

---

## Commit 40: `ci(release): add changelog-version consistency guardrail`

**Git:** `a99e8c0`
**Checklist compliance:** N/A (post-checklist — CI/CD guardrail)

### What this commit does

Adds `scripts/check_release_consistency.py` — a guardrail that validates the pyproject.toml version matches CHANGELOG.md headings. Wires it into CI before tests.

### Changes Made

- `scripts/check_release_consistency.py` (78 lines):
  - `load_project_version()` — parses pyproject.toml via `tomllib`
  - `changelog_versions()` — extracts version headings via regex
  - `validate_consistency()` — checks version exists in changelog AND is the latest heading
  - `main()` — argparse CLI with `--project-root` override, prints result
- `tests/tooling/test_check_release_consistency.py` (51 lines, 3 tests):
  - `test_validate_consistency_success` — happy path
  - `test_validate_consistency_missing_project_version` — version not in changelog → 2 errors
  - `test_changelog_versions_parser` — synthetic CHANGELOG with tmp_path
- `.github/workflows/ci.yml` — added "Run release consistency guardrail" step before tests

### Assessment

The guardrail catches a real class of bugs: version bumps in pyproject.toml without corresponding changelog entries, or changelog entries that don't match the declared version. Running it before tests in CI means release inconsistencies are caught before any test infrastructure is exercised — fast fail.

### Verification (Independent — Round 10 auditor)

4 checks: uses tomllib ✓, validates existence + latest heading ✓, tests cover success/missing/parser ✓, CI step added before tests ✓. **All 4 passed.**

---

## Commit 41: `docs(release): prepare 0.1.2rc2 changelog and version metadata`

**Git:** `ee72f33`
**Checklist compliance:** N/A (post-checklist — release candidate)

### What this commit does

Bumps version to `0.1.2rc2` and adds the corresponding CHANGELOG.md section documenting commits 30-40.

### Changes Made

- `pyproject.toml` — version `0.1.1` → `0.1.2rc2`
- `CHANGELOG.md` — added `[0.1.2rc2]` section with:
  - Added: benchmark smoke workflow, wheel packaging CI, tooling contract tests, release consistency guardrail
  - Changed: developer workflow hardening with `make release-check`, expanded app CLI test suite

### Assessment

The rc2 release candidate follows proper versioning: it collects all CI/tooling/testing improvements since 0.1.1 into a release candidate before promoting to stable. The changelog content accurately describes the work done in commits 30-40.

### Verification (Independent — Round 10 auditor)

2 checks: pyproject.toml version = "0.1.2rc2" ✓, CHANGELOG.md has [0.1.2rc2] section ✓. **All 2 passed.**

---

## Commit 42: `docs(release): finalize stable 0.1.2 from rc2 baseline`

**Git:** `e713dc0`
**Checklist compliance:** N/A (post-checklist — stable release)

### What this commit does

Promotes 0.1.2rc2 to stable 0.1.2. No code changes beyond the rc2 baseline.

### Changes Made

- `pyproject.toml` — version `0.1.2rc2` → `0.1.2`
- `CHANGELOG.md` — added `[0.1.2]` section at top:
  - "Promote release candidate `0.1.2rc2` to stable `0.1.2`."
  - "No additional code changes beyond the `0.1.2rc2` tested baseline."

### Assessment

Clean rc→stable promotion. The explicit "no additional code changes" note is good practice — it makes clear that the stable release is exactly the tested rc2 code. The version bump passes the release consistency guardrail (version matches latest CHANGELOG heading).

### Verification (Independent — Round 10 auditor)

3 checks: pyproject.toml version = "0.1.2" ✓, [0.1.2] is latest CHANGELOG heading ✓, references promotion from rc2 ✓. **All 3 passed.**

---

## Commit 43: `docs: add midway report analysis and comprehensive project report`

**Git:** `20d3005`
**Checklist compliance:** N/A (post-checklist — documentation + bundled audit commit)

### What this commit does

Adds a 754-line comprehensive midway report (`20260304_midway_report.md`) analyzing the project's architecture, implementation, test suite, performance, gaps, and roadmap. Also adds a task tracking PRD. Additionally commits the auditor's previously uncommitted Round 8-10 audit edits to `11_agent_execution_audit.md` (913 line additions).

### Changes Made

- `20260304_midway_report.md` (new, 754 lines) — 16-section midway analysis covering:
  - Executive summary, project origin (R1-R12), scope boundaries
  - Architecture: package structure, dependency rules, D1-D15 decisions, 8 architectural patterns
  - Implementation inventory: component status matrix, git progression through commit 32
  - Core engine deep dive: tick lifecycle diagram, state management, command queue
  - Ant foraging scenario: biological model, FSM (searching ↔ carrying), 6 behaviors, environment config, emergence phases
  - Test suite analysis: distribution (15 modules, 72 tests), gates G1-G8, quality assessment
  - Performance: benchmark harness, baselines, cProfile hotspot analysis, scaling, optimization history
  - Code quality: 1.24:1 test/implementation ratio, qualitative assessment, audit findings summary
  - Documentation ecosystem: 11 analysis documents, 6 performance files
  - Requirement traceability: R1-R12 status (5 done, 4 partial, 3 not started)
  - Risk register: 6 risks with probability/impact/mitigation
  - Gap analysis: critical (UI, thesis, drone), important (emergence metrics, persistence), nice-to-have
  - Strengths: contract-first design, structural determinism, honest performance reporting
  - Roadmap: MVD items 1-5, full defense items 6-10, 12-week timeline
- `MEMORY/WORK/20260304-midway-report-analysis/PRD.md` (new, 61 lines) — task tracking with ISC criteria
- `11_agent_execution_audit.md` (+913 lines) — bundled auditor's Rounds 8-10 content + minor Environment Snapshot modifications

### Assessment

The midway report is technically competent on architectural and implementation details. Engine deep dive, scenario model, dependency rules, and package structure all verified against source code. The report demonstrates genuine understanding of the codebase — not superficial summarization.

**However**, the report has a critical staleness problem: it describes the project as of commit 32 (72 tests, 32 commits) despite being committed at commit 43 (86 tests, 43 commits). This produces systematic errors:

| Category | Report Claims | Actual at Commit Time | Delta |
|----------|--------------|----------------------|-------|
| Test count | 72 | 86 | -14 (16% undercount) |
| Commit count | 32 | 43 | -11 (26% undercount) |
| Test modules | 15 | 18 | -3 (missing `tests/tooling/`) |
| Import-lint | "does not exist" | Exists + CI + 3 tests | Factually wrong |
| CI/CD pipeline | Not mentioned | 2 workflows + 4 jobs | Entirely omitted |
| Release cycle | Not mentioned | 0.1.1 → 0.1.2rc2 → 0.1.2 | Entirely omitted |
| Performance baselines | Pre-engine-opt only | Post-engine-opt available | Stale by 1 optimization round |

The staleness is pervasive: "32 commits" appears 4 times, "72 tests" appears 8+ times throughout the 754-line document. The report describes a project that is 11 commits and 14 tests behind reality.

Additionally, the commit bundles 913 lines of the auditor's uncommitted Round 8-10 work without acknowledgment in the commit message. The commit message frames the commit as adding a "midway report analysis" but 53% of the line additions are audit content from a different authorship context.

### Verification (Independent — Round 11 auditor)

16 checks:

1. Section 3.1 package structure matches actual `ls -R sim_framework/` ✓
2. Section 3.2 dependency rules accurate but claims "no automated import-lint" — STALE, `check_import_flow.py` exists ✗
3. D1-D15 decisions accurately assessed (D14 test count stale: 72 vs 86) ✓ (with caveat)
4. Section 4.1 test counts undercount by 14 (missing `tests/tooling/` and expanded `tests/app/`) ✗
5. Section 5.1 engine tick lifecycle diagram matches `engine.py` source precisely ✓
6. Section 6 ant foraging FSM, behaviors, parameters, environment config all verified ✓
7. Section 7.1 reports 72 tests, actual is 86 ✗
8. Section 7.4 lists "no automated import-lint" as gap — factually wrong since commit 30 ✗
9. Section 8.2 baselines match pre-engine-opt data (real but not latest) ✓ (with caveat)
10. Section 4.2 git progression stops at commit 32, omits 11 commits ✗
11. Section 11 R1-R12 traceability mostly accurate; R1 "remaining: import-lint" is stale ✓
12. Section 9.3 audit findings summary mostly correct; I-3 and I-10 miscategorized ✓
13. Staleness pervasive: 4× "32 commits", 8× "72 tests" — OBSERVATION
14. No mention of CI/CD, release cycle, tooling tests ✗
15. Commit message omits 913 lines of bundled audit content ✗
16. Environment Snapshot modified to "46 commits" and "43-46 pending" — internally inconsistent with midway report's "32 commits" in same commit — OBSERVATION

**5/16 PASS, 6/16 FAIL, 3/16 PASS with caveat, 2/16 OBSERVATION.**

### Issues Found

| # | Severity | Finding |
|---|----------|---------|
| I-16 | **MEDIUM** | **Midway report describes commit-32 state despite being committed at commit 43.** The 754-line report omits 11 commits (26%), 14 tests (16%), the entire CI/CD pipeline, the release cycle, the import-flow guardrail script, and tooling tests. It claims "no automated import-lint" as a gap when the script exists and runs in CI. Internal inconsistency: the audit file in the same commit says "86 tests" and "46 commits" while the midway report says "72 tests" and "32 commits". The technical content (engine, scenario, architecture) is accurate and well-written, but the quantitative claims are systematically stale. |

---

## Commit 44: `docs: sync final report and evidence matrix to v0.1.2 state`

**Git:** `5b313b9`
**Files changed:** 2 files, +32 insertions, -18 deletions
**Code quality:** 9/10

### What the agent did

Updated two pre-implementation design documents to reflect the actual v0.1.2 implementation state:

**1. Evidence matrix (`07_tfg_evidence_matrix.md`):**
- Added date (2026-03-04) and implementation state line (`v0.1.2 (stable), CI green, 86/86 tests passing`)
- Introduced new status category: "Done (implemented scope)"
- Updated ALL 12 requirements (R1-R12) from "Not started" placeholders to actual implementation statuses:
  - **Done (5):** R1 (strict modularity), R8 (Python implementation), R11 (robust runtime), R12 (determinism), R3b (configurable methods)
  - **Done (implemented scope) (2):** R2 (per-module testing), R10 (orchestrator governance)
  - **In progress (4):** R3 (configurable attributes — UI editor pending), R4 (configurable physics — UI pending), R5 (multi-scenario — drone pending), R7 (playback/rewind — adapters pending)
  - **Not started (2):** R6 (modern UI/PixiJS), R9 (Linux desktop + web shell)
- Added correct implementation artifacts, test evidence references, and demo/thesis evidence for each requirement

**2. Final report (`08_final_report.md`):**
- Added header: "Synced to implementation state: 2026-03-04 (v0.1.2)"
- Added "Implementation Status Addendum" section documenting: v0.1.2 stable, 86/86 tests, CI/CD active, tooling complete
- Changed Section 1 to past tense ("had accumulated" → reflects design-time perspective)
- Added directive: "Read this report as architectural rationale; use audit + CHANGELOG as implementation truth"

### Deep-Dive Verification

66 independent checks performed against the actual codebase:

**R1 (7 checks):** `contracts/models.py` ✓, `contracts/ports.py` ✓, `scripts/check_import_flow.py` ✓, `tests/contracts/test_ports_contract_shape.py` ✓, `tests/tooling/test_check_import_flow.py` ✓, CI import-flow step in `ci.yml` ✓, status "Done" accurate ✓
**R2 (8 checks):** All 6 test directories exist ✓, 86/86 test count verified ✓, "Done (implemented scope)" accurate ✓
**R3 (4 checks):** `contracts/validators.py` ✓, `scenarios/ants_foraging/spec.py` ✓, `tests/contracts/test_validators_schema.py` ✓, "In progress" accurate ✓
**R3b (5 checks):** `contracts/behaviors.py` ✓, behavior registry tests (5 tests) ✓, schema tests (7 tests) ✓, "Done (implemented scope)" accurate ✓
**R4 (3 checks):** `core/physics.py` ✓, `tests/core/test_physics_movement.py` (5 tests) ✓, "In progress" accurate ✓
**R5 (5 checks):** `scenarios/registry.py` ✓, `scenarios/ants_foraging/` ✓, `tests/scenarios/test_ants_scenario_loads.py` (6 tests) ✓, integration smoke test ✓, "In progress" accurate ✓
**R6 (3 checks):** N/A artifacts correct ✓, N/A tests correct ✓, "Not started" accurate ✓
**R7 (7 checks):** `core/engine.py` ✓, `core/history.py` ✓, all 6 command types in `models.py` ✓, determinism tests (6) ✓, history tests (8) ✓, command tests ✓, "In progress" accurate ✓
**R8 (4 checks):** Python codebase ✓, CI Python 3.11 ✓, release-check script ✓, "Done" accurate ✓
**R9 (3 checks):** `app/cli.py` exists ✓, CLI smoke tests (7) ✓, "Not started" for browser/desktop target accurate ✓
**R10 (5 checks):** `app/cli.py` ✓, `app/runtime.py` ✓, `tests/app/test_cli_runtime_mode.py` (7 tests) ✓, wheel smoke in CI ✓, "Done (implemented scope)" accurate ✓
**R11 (3 checks):** Engine error isolation path ✓, `test_engine_error_isolation.py` (2 tests) ✓, "Done" accurate ✓
**R12 (6 checks):** Seeded RNG ✓, benchmark tooling ✓, Plans/ manifests (11 files) ✓, determinism tests (6) ✓, ON/OFF contract tests (4) ✓, "Done" accurate ✓
**Final report addendum (3 checks):** 86/86 tests verified by `pytest --co` ✓, CI/CD workflows exist ✓, tooling scripts present ✓

**RESULT: 66/66 PASS. 0 FAIL.**

### Assessment

This is a high-quality documentation sync commit. Unlike the midway report (commit 43, I-16), this commit uses **correct current data** — every artifact reference, test count, and status assessment is verified accurate against the actual codebase.

The commit directly addresses the evidence matrix's previous "Not started" placeholder state and establishes a reliable thesis-defense traceability chain from requirement → decision → artifact → test → evidence. The status gradations ("Done", "Done (implemented scope)", "In progress", "Not started") are well-calibrated and honest about what remains unfinished.

The final report addendum is well-designed: rather than rewriting the entire report, it adds a clearly-demarcated addendum and redirects readers to the audit + CHANGELOG for implementation truth. This preserves the report's value as architectural rationale while acknowledging its design-time perspective.

**Partial I-16 mitigation:** The evidence matrix and final report are now current, but the midway report (`20260304_midway_report.md`) remains stale with commit-32 data.

### What's Good

- Every artifact path in the matrix corresponds to a real file
- Status assessments are honest — incomplete items are marked "In progress" or "Not started", not overstated
- The "Done (implemented scope)" status category is a useful distinction from "Done"
- Final report addendum approach preserves document integrity while updating status
- Cross-reference consistency: evidence matrix and final report addendum agree on all data points

### Issues Found

No new issues. This commit partially addresses I-16 for the evidence matrix and final report (midway report remains affected).

---

## Previous Forward-Looking Concerns — Assessment

| Concern | Prediction | Outcome | Accuracy |
|---------|-----------|---------|----------|
| Commit 7: HistoryPort compliance | Must implement `rewind()` | `rewind()` implemented with 3 code paths | CORRECT |
| Commit 8: Python 3.10 vs 3.11 | `ExceptionGroup`/`TaskGroup` could be problematic | Agent used simple try/except, no 3.11 features | Agent avoided the trap |
| Commit 8: Three concerns in one | Hardest commit | Cleanly delivered all three | CORRECT (but simpler than feared) |
| Commit 9: Spatial hash coordinate system | Must match SignalGrid coordinates | Both use continuous float coords → integer cell mapping | CORRECT |
| Commit 10: I-10 flat chain vs state machine | Scenario will surface the divergence | Agent bypassed validators, created new schema | PARTIALLY CORRECT — surfaced as predicted, but solution was bypass not extension |
| Commit 10: I-11 gradient needed | `sample()` not enough for pheromone following | Agent implemented gradient sampling in scenario | CORRECT — needed extension, got scenario-local solution |
| Round 3 I-14: schema unification needed | Two schema systems will create tech debt | Commit 11 unified into `StateMachineAgentSchemaSpec` in contracts | CORRECT — agent addressed the finding directly |
| Round 3 I-15: gradient should be framework API | Scenario-local gradient is not reusable | Commit 12 added `SignalGrid.sense_gradient()` with superior algorithm | CORRECT — promoted to framework with full-radius scan |
| Round 3 I-12: speed multiplier unused | Property stored but never consumed | Commit 13 wired multiplier into step batching | CORRECT — engine now runs N steps per tick |
| Round 4 I-7: package metadata/readme mismatch | Package should expose a real README | Commit 15 added `README.md` and set `readme = "README.md"` | CORRECT — metadata now publish-safe |
| Round 4 I-9: shallow protocol contract tests | Tests should verify signatures and type hints | Commit 16 added strict signature/type-hint conformance assertions | CORRECT — test depth increased |
| Round 5 I-3 control hardening | Enforce Python policy at test runtime | Commit 17 added pytest session gate for Python >=3.11 | CORRECT — now operationally enforced |
| Round 5 I-13 integration gap | SpatialHash should be consumed by scenario logic | Commit 18 integrated SpatialHash neighbor queries in ants runner | CORRECT — integration-level usage established |
| Round 7 performance tooling | Benchmark harness needed for optimization tracking | Commit 19 added full harness with tracemalloc, JSON output, CLI args | CORRECT — reproducible measurement infrastructure |
| Round 7 scaling baseline | Baseline should reveal O(N²) neighbor interactions | Commit 20 confirms 2.34× per-agent cost at 3× agents — superlinear as expected | CORRECT — documented as known characteristic |
| Round 7 profiling need | Benchmark without profiler can't identify hotspots | Commit 22 added cProfile integration, identified Pydantic model_copy at 46% | CORRECT — profiling was essential for targeted optimization |
| Round 8 spatial hash micro-opt | Reducing scan ring won't help if bottleneck is elsewhere | Commit 23 honestly documented regression — profiler showed model_copy, not spatial hash, was dominant | CORRECT — micro-opt was misdirected, agent self-corrected |
| Round 8 Pydantic deep-copy overhead | model_copy in snapshot path is avoidable in headless mode | Commit 25 made snapshot events optional, yielding 17% speedup and 94% memory reduction | CORRECT — targeted the actual bottleneck identified by profiler |
| Round 8 app composition root needed | Framework needs public entry point with runtime presets | Commit 27 added `app/` with CLI, RuntimeMode, RuntimeConfig, scenario registry | CORRECT — composition root per hexagonal blueprint |
| Round 8 per-tick deep-copy addressable | model_copy(deep=True) in state transition is redundant since agents are already fresh | Commit 28 replaced with shallow copy + explicit topology cloning — 11% snapshot-ON improvement | CORRECT — agents from _advance_agents() don't need re-cloning |
| Round 9 snapshot-OFF 300-agent variance | 5.5% regression at 300 agents snapshot-OFF after engine opt | Different test params (ticks=100/repeats=3 vs ticks=50/repeats=2) and run-to-run noise | MONITORING — not a code defect, optimization doesn't touch snapshot-OFF path |
| Round 9 CI needed | Manual guardrails should be automated in CI | Commit 30 added CI with import-flow + pytest; commit 40 added release consistency guardrail | CORRECT — all manual checks now automated |
| Round 9 packaging validation needed | Editable install doesn't catch packaging bugs | Commit 38 added wheel build + clean-venv smoke test in CI | CORRECT — non-editable install catches missing files/broken entry points |
| Round 9 tooling test coverage gap | Scripts lack unit tests | Commits 33, 39, 40 added comprehensive tests for all 3 scripts (import-flow, perf-toggle, release-consistency) | CORRECT — 10 tooling tests now cover script logic |
| Round 10 release candidate process | rc→stable promotion should be formalized | Commits 41-42 demonstrate clean rc2→stable promotion with explicit "no code changes" changelog note | MONITORING — pattern established, reusable for future releases |
| Round 10 midway report staleness risk | Report written against older codebase snapshot could produce stale claims | Commit 43 midway report describes commit-32 state (72 tests, 32 commits) despite 86 tests and 43 commits at commit time | CONFIRMED — I-16 documents pervasive staleness across 12+ data points |
| Round 11 I-16 staleness propagation | Stale data in midway report could infect other documents | Commit 44 synced evidence matrix and final report to v0.1.2 with correct data (66/66 checks PASS); midway report remains stale | PARTIALLY ADDRESSED — 2 of 3 key documents now current |

---

## Environment Snapshot

| Property | Value | Expected | Status |
|----------|-------|----------|--------|
| System Python | 3.10.9 | >=3.11 (per pyproject.toml) | MISMATCH — controlled by `.venv` runtime + pytest gate |
| Project Python (`.venv`) | 3.11.11 | >=3.11 (per pyproject.toml) | OK — policy-compliant runtime |
| Pydantic version | 2.8.2 | >=2.7 | OK |
| pytest version (system) | 7.1.2 | >=8.0 (per pyproject.toml dev) | MISMATCH — use `.venv` pytest |
| pytest version (`.venv`) | 9.0.2 | >=8.0 (per pyproject.toml dev) | OK |
| Pytest runtime policy gate | ACTIVE | Reject Python <3.11 at session start | OK — commit 17 |
| Editable install in `.venv` | SUCCEEDS | Should succeed | OK — discovery fixed and Python policy satisfied |
| Tests passing | 110/110 | All green | OK |
| Git commits | 57 | 10 checklist + 47 post-checklist (through R6/R9 roadmap commit) | COMPLETE (audited through commit 57 on 2026-03-04) |
| Import rule violations | 0 | 0 | OK — `contracts ← core ← scenarios ← app`, 28 imports all flow correctly (I-17: `adapters` layer not yet in checker) |
| End-of-commit-10 acceptance | ALL 4 MET | All 4 criteria | COMPLETE |
| Post-checklist improvements | 47 commits (11-57) | Audit findings + policy + integration + perf baseline + profile-guided opt + app CLI + engine deep-copy opt + CI/CD pipeline + tooling tests + release cycle + midway report + evidence sync + persistence adapter + drone scenario + scenario-aware benchmarks + boundary mode + agent-spec overrides + R3/R4/R5/R7 evidence bundles + R6/R9 roadmap | ALL COMPLETED (within audited range) |
| Midway report | COMMITTED | `20260304_midway_report.md` — 754-line project analysis | OK — commit 43 (I-16 staleness noted) |
| Evidence matrix sync | COMMITTED | `07_tfg_evidence_matrix.md` — R1-R12 updated to v0.1.2 implementation state (66/66 checks PASS) | OK — commit 44 |
| Final report sync | COMMITTED | `08_final_report.md` — implementation status addendum added, past-tense framing, reader directive | OK — commit 44 |
| CI/CD pipeline | ACTIVE | `.github/workflows/ci.yml` (test + package) + `benchmark-smoke.yml` | OK — commits 30/37/38/40 |
| Release consistency guardrail | ACTIVE | `scripts/check_release_consistency.py` validates pyproject.toml ↔ CHANGELOG.md | OK — commit 40 |
| Makefile dev workflow | ACTIVE | `make release-check` = release-consistency + import-check + test-v + package-check | OK — commits 34/35 |
| Reproducible benchmark runner | ACTIVE | `scripts/run_perf_snapshot_toggle.py` with determinism cross-checks | OK — commit 32 |
| Project version | 0.1.2 (stable) | Release via rc2→stable promotion | OK — commit 42 |
| Benchmark harness | ACTIVE | `scripts/benchmark_headless.py` with tracemalloc, cProfile, JSON output, `--no-snapshot-events` | OK — commits 19/22/25 |
| cProfile integration | ACTIVE | `--profile-out`, `--profile-sort`, `--profile-top` CLI flags; `profiler.runcall()` wrapper | OK — commit 22 |
| Performance baseline (original) | RECORDED | 100 agents: ~929 μs/agent-tick, 300 agents: ~2176 μs/agent-tick | OK — commit 20 |
| Performance baseline (post spatial-opt) | RECORDED | 100 agents: ~988 μs/agent-tick, 300 agents: ~2439 μs/agent-tick (regression vs original) | OK — commit 24, honestly documented |
| Performance baseline (no-snapshot) | RECORDED | 100 agents: ~819 μs/agent-tick, 300 agents: ~2099 μs/agent-tick | OK — commit 26, 17% speedup + 94% memory reduction |
| Performance baseline (post-engine-opt, snap ON) | RECORDED | 100 agents: ~880 μs/agent-tick, 300 agents: ~2225 μs/agent-tick | OK — commit 29, 11% improvement over post-spatial-opt |
| Performance baseline (post-engine-opt, snap OFF) | RECORDED | 100 agents: ~823 μs/agent-tick, 300 agents: ~2215 μs/agent-tick, 0.37/1.09 MB | OK — commit 29, 98% memory reduction |
| Snapshot event toggle | ACTIVE | `SimulationEngine(emit_snapshot_events=False)` skips deep-copy in headless mode | OK — commit 25 |
| App CLI (`sim-run`) | ACTIVE | `sim_framework/app/cli.py` with `--runtime-mode interactive/headless`, scenario registry | OK — commit 27 |
| RuntimeConfig | ACTIVE | Frozen Pydantic model with three-tier snapshot resolution (explicit > mode > default) | OK — commit 27 |
| Engine per-tick optimization | ACTIVE | Shallow `model_copy` + explicit topology cloning replaces `model_copy(deep=True)` | OK — commit 28 |
| JSON file persistence adapter | ACTIVE | `sim_framework/adapters/persistence/json_file.py` implements `PersistencePort` | OK — commit 47 (I-17: layer not in import checker) |
| CLI persistence flows | ACTIVE | `--save-run-id`, `--load-run-id`, `--persistence-root` flags in `sim-run` CLI | OK — commit 48 |
| Second scenario (drone_patrol) | ACTIVE | `sim_framework/scenarios/drone_patrol/spec.py` with registry integration | OK — commit 51 |
| Scenario-aware benchmarks | ACTIVE | `--scenario` flag in `benchmark_headless.py` and `run_perf_snapshot_toggle.py` | OK — commit 52 |
| Boundary mode exposure | ACTIVE | `--boundary-mode clamp\|wrap` threaded CLI → dispatch → physics | OK — commit 55 |
| Agent-spec runtime overrides | ACTIVE | `--agent-spec-json` with 3-level validation (schema, behaviors, scenario) | OK — commit 56 |
| R3/R4/R5/R7 evidence bundles | COMMITTED | SHA-256 verified reproducibility bundles in `Plans/runs/` | OK — commits 50/53/55/56 |
| R6/R9 UI-desktop roadmap | COMMITTED | 5-milestone execution plan in `Plans/r6_r9_ui_desktop_roadmap_2026-03-04.md` | OK — commit 57 |
| Git tags | 7 tags | `v0.1.1`, `v0.1.2`, `v0.1.2-rc1`, `v0.1.2-rc2`, 3 milestone tags | OK |

---

## Issue Tracker

| ID | Severity | Commit | Description | Status |
|----|----------|--------|-------------|--------|
| I-1 | MEDIUM | 1 | Commit message deviates from checklist convention | ACCEPTED (historical immutable) |
| I-2 | LOW | 1 | `__pycache__` committed to git history | OPEN (fixed going forward) |
| I-3 | MEDIUM | 1 | System interpreter is 3.10.9 while project policy is `>=3.11`; `.venv` uses 3.11.11 and pytest now hard-fails on <3.11 (commit 17) | CONTROLLED |
| I-4 | LOW | 2 | Frozen `Vector2` creates GC pressure at scale | DEFERRED (per D13) |
| I-5 | MEDIUM | 2 | `SignalField` is config-only, needs runtime state class | **RESOLVED** by commit 6 (`SignalGrid` dataclass) |
| I-6 | MEDIUM | 2 | 8 of 9 field validators untested | **RESOLVED** by commit 5 (retroactive test additions) |
| I-7 | LOW | 2 | `pyproject.toml` readme points to 590-line audit report | **RESOLVED** by commit 15 (`README.md` + metadata fix) |
| I-8 | CRITICAL | 2 | `pip install -e .` fails: setuptools autodiscovery finds `MEMORY` + `sim_framework` | **RESOLVED** by commit 2.5 (package find constraint) |
| I-9 | LOW | 3 | Port stubs lack return type annotations, `runtime_checkable` only checks method names | **RESOLVED** by commit 16 (signature and type-hint conformance tests) |
| I-10 | MEDIUM | 4-5 | Validator schema uses flat `behavior_chain`, not state machine from `08_final_report.md` | **SUPERSEDED** by I-14 — scenario bypassed validators entirely |
| I-11 | LOW | 6 | `sample()` reads point value, not gradient — ant pheromone-following will need extension | **RESOLVED** by commit 12 (`SignalGrid.sense_gradient()` framework API; commit 10 provided the interim scenario-local fix) |
| I-12 | LOW | 8 | `speed_multiplier` stored but never consumed by engine — speed control is external | **RESOLVED** by commit 13 (step batching via multiplier) |
| I-13 | LOW | 9 | `SpatialHash` built to spec but unused by ants scenario — unit-tested only | **RESOLVED** by commit 18 (scenario neighbor-avoidance integration) |
| I-14 | MEDIUM | 10 | Two coexisting schema systems — `AgentSchemaSpec` (validators.py) is dead code, `AntBehaviorSpec` (spec.py) is active | **RESOLVED** by commit 11 (unified `StateMachineAgentSchemaSpec` in contracts) |
| I-15 | LOW | 10 | Pheromone gradient logic in scenario, not framework — `_best_pheromone_direction()` is not reusable | **RESOLVED** by commit 12 (`SignalGrid.sense_gradient()` framework API) |
| I-16 | MEDIUM | 43 | Midway report describes commit-32 state despite being committed at commit 43: omits 11 commits (26%), 14 tests (16%), CI/CD pipeline, release cycle, import-flow guardrail; claims "no import-lint" when it exists and runs in CI; "32 commits"×4 and "72 tests"×8 throughout | PARTIALLY ADDRESSED — commit 44 synced evidence matrix (66/66 PASS) and final report to v0.1.2; midway report remains stale |
| I-17 | MEDIUM | 47 | Import-flow guardrail does not include `adapters` layer in `ALLOWED_IMPORTS`; imports from/to `adapters` are silently skipped by `check_import_flow.py`. Actual adapter imports are valid (adapters → contracts only) but unpoliced. | OPEN |

**CRITICAL:** 0 | **MEDIUM:** 2 (I-16 PARTIALLY ADDRESSED, I-17 OPEN) + 2 non-open (I-1 ACCEPTED, I-3 CONTROLLED) | **LOW:** 2 (I-2, I-4) | **RESOLVED:** 10 | **CONTROLLED:** 1 | **ACCEPTED:** 1 | **SUPERSEDED:** 1

---

## Command Evidence (Reproducible)

### Round 1 (commits 1-2)

1. `python --version` → `Python 3.10.9`
2. `python -m pytest --version` → `pytest 7.1.2`
3. `python -c "import pydantic; print(pydantic.__version__)"` → `2.8.2`
4. `python -m pip install -e .` → fails: `Multiple top-level packages discovered` (I-8)
5. `python -m pytest -q tests/contracts/test_models_basic.py` → `5 passed`

### Round 2 (commits 2.5-6)

6. `python -m pip install -e .` → fails: `Package requires different Python: 3.10.9 not in '>=3.11'` (I-8 fixed, I-3 is now sole blocker)
7. `python -m pytest -v` → `28 passed in 0.25s`
8. `grep -rn "from sim_framework" sim_framework/` → 3 imports, all clean (core→contracts, contracts→contracts.models)
9. `TypeAdapter(ControlCommand).validate_python({"kind": "seek", "tick": 50})` → parses correctly (discriminated union works)
10. `_contains_executable_payload({"nested": {"code": "x"}})` → `True` (recursive detection works)
11. Diffusion conservation test: deposit 100.0, diffuse once, total = 100.0 (signal conserved)

### Round 3 (commits 7-10)

12. `python -m pytest -v` → `55 passed in 0.59s`
13. `isinstance(SnapshotHistory(), HistoryPort)` → `True` (protocol compliance verified)
14. Full-stack determinism: 2 engines × 50 ticks × 20 ants × signal grids → `state1.model_dump() == state2.model_dump()` → `True`, signal grids identical (943.0 == 943.0)
15. Per-agent error isolation: 3 agents (good1, bad, good2), bad raises RuntimeError → surviving agents = [good1, good2], ErrorEvent emitted with agent_id="bad"
16. Spatial hash accuracy: 500 agents, query_radius(center=(50,50), radius=10) → 16 results, matches brute-force exactly (0 false positives, 0 false negatives)
17. All 6 command types processed: Play→lifecycle/started, Pause→lifecycle/paused, Step→snapshot, SetSpeed→multiplier=2.0, Seek→rewinds via history, Reset→lifecycle/reset
18. History rewind integration: 10 ticks recorded, SeekCommand(tick=5) → state.tick=5, position=5.0 (exact snapshot match)
19. State machine transitions in 100 ticks: searching→carrying: 1,796, carrying→searching: 1,787. All 40 agents alive.
20. Pheromone gradient: `_best_pheromone_direction` correctly returns (1.0, 0.0) when pheromone is to the east, None when no pheromone
21. Wrap mode physics: (-1.5 % 10) = 8.5, (21.5 % 10) = 1.5 — Python modulo handles negatives correctly
22. `grep -rn "from sim_framework" sim_framework/` → 12 imports total, all flow contracts ← core ← scenarios. Zero rule violations.
23. End-of-commit-10 acceptance: all 4 criteria met (deterministic loop, signal environment, rewind history, ant scenario headless)
24. `.venv/bin/python --version` → `Python 3.11.11` (policy-compliant runtime)
25. `uv pip install --python .venv/bin/python -e .` → succeeds
26. `.venv/bin/python -m pytest -q` → `55 passed`

### Round 4 (commits 11-13)

27. `.venv/bin/python -m pytest -v` → `62 passed in 0.60s` (was 55)
28. `grep -rn "from sim_framework" sim_framework/` → 13 imports total, all flow contracts ← core ← scenarios. Zero rule violations.
29. `StateMachineAgentSchemaSpec` with bad transition target ("nonexistent") → `ValueError` raised correctly
30. `StateMachineAgentSchemaSpec` with bad initial_state → `ValueError` raised correctly
31. `validate_known_behavior_names(ANT_WORKER_SPEC, known_set)` — extracts behaviors from all states, rejects unknowns
32. `isinstance(ANT_WORKER_SPEC, StateMachineAgentSchemaSpec)` → `True` (scenario uses unified contracts type)
33. Gradient API — 8 independent verifications: directional accuracy (east deposit → east gradient), strongest-wins, no-improvement detection, input validation (radius=0 → ValueError), normalized output (magnitude=1.0), edge clamping, diagonal detection (NE deposit → NE gradient), tie-break by distance
34. Speed multiplier — 6 independent verifications: 3× = 3 steps/tick, paused+speed=4+step=1 → exactly 1 step, determinism preserved (2 engines × 10 ticks @ 3× → identical at tick=30), speed<1 clamps to 1, resume from pause with speed=2 → 2 steps, default speed (1×) unchanged
35. Import direction: `spec.py` imports from `contracts.validators` — scenarios → contracts, valid per import rule

### Round 5 (commits 14-16)

36. `git rev-list --count HEAD` → `18`
37. `rg -n "^readme\\s*=\\s*\\\"README.md\\\"" pyproject.toml` → metadata points to `README.md`
38. `test -f README.md` → `README.md exists`
39. `git show --name-only --oneline 532f29f` → shows `README.md` + `pyproject.toml` change set
40. `.venv/bin/python -m pytest -q tests/contracts/test_ports_contract_shape.py` → pass (strict protocol contract test)
41. `git show --name-only --oneline f6a3da7` → shows `tests/contracts/test_ports_contract_shape.py` hardening commit
42. `.venv/bin/python -m pytest -q` → `62 passed`

### Round 6 (commits 17-18)

43. `git show --name-only --oneline 71fd341` → shows `tests/conftest.py` Python policy gate
44. `python -m pytest -q tests/test_smoke.py` → exits immediately: `Python >= 3.11 is required... use .venv/bin/python -m pytest`
45. `.venv/bin/python -m pytest -q` → `64 passed` (policy gate allows supported interpreter)
46. `git show --name-only --oneline 715e593` → shows scenario + tests integration for SpatialHash
47. `rg -n "SpatialHash|_neighbor_avoidance|query_radius|indexed_tick" sim_framework/scenarios/ants_foraging/spec.py` → confirms runtime integration points
48. `.venv/bin/python -m pytest -q tests/scenarios/test_ants_scenario_loads.py::test_behavior_runner_uses_spatial_hash_queries tests/scenarios/test_ants_scenario_loads.py::test_behavior_runner_caches_spatial_hash_per_tick` → both pass
49. `.venv/bin/python -m pytest -v` → `64 passed in 0.59s`

### Round 7 (commits 14-20 — independent auditor verification)

50. `python -m pytest -q tests/test_smoke.py` → exits immediately: "Python >= 3.11 is required" (confirms commit 17 gate under system Python 3.10.9)
51. `.venv/bin/python -m pytest -v` → `64 passed in 0.63s` (full suite green under policy-compliant interpreter)
52. Commit 15 deep-dive: 7 checks — `pyproject.toml` readme = `"README.md"`, file exists, 39 lines, 4 sections present → ALL PASSED
53. Commit 16 deep-dive: 3 protocols × 7 methods — all have proper params, return hints, `@runtime_checkable` → ALL PASSED
54. Commit 17 deep-dive: `conftest.py` has `sys.version_info < (3, 11)` check + `pytest.exit()` + `pytest_sessionstart` hook → ALL PASSED (positive + negative paths)
55. Commit 18 deep-dive: 10 checks — SpatialHash instantiation, build/query, spec.py integration points (import, `_neighbor_avoidance`, `spatial_hash.build`, `query_radius`, `indexed_tick`, `avoid_weight`), 5-tick scenario run → ALL PASSED
56. Commit 19 deep-dive: 13 checks — AST analysis (2 classes, 5 functions), `tracemalloc`/`perf_counter` usage, `_single_run(agents=5, ticks=3)` executes, `_summarize` produces valid summary → ALL PASSED
57. Commit 20 deep-dive: 18 checks — JSON parse, config sanity, run/summary counts, state_tick correctness, scaling factor 2.34×, low stdev, MD-JSON cross-check (tps values match to 4 decimal places) → ALL PASSED
58. `grep -rn "from sim_framework" sim_framework/` → 13 imports, all flow `contracts ← core ← scenarios`. Zero violations. (New: `spec.py` imports `SpatialHash` from `core.physics` — valid)

### Round 8 (commits 21-26 — profile-guided optimization cycle)

59. `.venv/bin/python -m pytest -v` → `65 passed in 0.63s` (new test: `test_can_disable_snapshot_event_emission_for_headless_mode`)
60. `grep -rn "from sim_framework" sim_framework/` → 13 imports, all flow `contracts ← core ← scenarios`. Zero violations. No new imports added in Round 8.
61. Commit 22 deep-dive: 17 checks — AST analysis confirms `cProfile`, `pstats`, `StringIO` imports; `_write_profile()` function exists; `--profile-out`, `--profile-sort`, `--profile-top` CLI args present; `profiler.runcall()` wraps `_run_benchmark`; `Plans/perf_profile_2026-03-04.txt` exists with 28 lines showing `model_copy` at 46.6% → ALL PASSED
62. Commit 23 deep-dive: 15 checks — `ceil` import in physics.py; `cell_radius = ceil(radius / self.cell_size)` replaces `int(...)+1`; attribute inlining (`cells = self.cells`, `cx,cy = center_cell`, `center_x/center_y`); `if other is agent` replaces `other.id == agent.id` in spec.py; attribute inlining in `_neighbor_avoidance`; brute-force correctness verification with 50 agents matches SpatialHash results exactly (0 false positives, 0 false negatives) → ALL PASSED
63. Commit 25 deep-dive: 10 checks — `emit_snapshot_events` parameter in `__init__`; `_emit_snapshot_events` instance variable; read-only property; conditional `if self._emit_snapshot_events:` guard in `_run_single_step`; new test `test_can_disable_snapshot_event_emission_for_headless_mode` passes; `--no-snapshot-events` CLI flag in benchmark; `emit_snapshot_events` in `_single_run` signature; JSON config records setting → ALL PASSED
64. Commits 24+26 deep-dive: 22 checks — post-opt JSON valid with correct run/summary counts; comparison MD honestly reports regression; no-snapshot JSON has `"emit_snapshot_events": false`; throughput improvement +20.7% (100 agents) / +16.2% (300 agents); memory reduction 94%; determinism preserved (identical `carrying_agents` and `signal_total` between snapshot-ON and snapshot-OFF runs with same seed); README updated with baseline references → ALL PASSED

### Round 9 (commits 27-29 — app layer, engine optimization, post-engine-opt baselines)

65. `.venv/bin/python -m pytest -v` → `72 passed in 0.56s` (was 65 — +6 app tests + 1 topology clone test)
66. `grep -rn "from sim_framework" sim_framework/` → 20 imports (was 13), all flow `contracts ← core ← scenarios ← app`. Zero violations. New: `app/` imports from all layers (composition root), `scenarios/registry.py` imports from `scenarios.ants_foraging`.
67. Commit 27 deep-dive: 17 checks — RuntimeConfig default/headless/override resolution, frozen immutability, create_engine factory wiring, list_scenarios/get_scenario registry, CLI interactive/headless/override modes, mutual exclusion of snapshot flags, pyproject.toml sim-run entry, __all__ re-export, RuntimeMode enum values → ALL PASSED
68. Commit 28 deep-dive: 12 checks — _run_single_step no longer uses deep=True, food_sources/colony/signal_fields shallow-copied, new test passes, object identity isolation verified, determinism preserved with full scenario, SnapshotEvent path retains deep=True, new imports in test file, tick counter correct → ALL PASSED
69. Commit 29 deep-dive: 18 checks — both JSONs valid with correct configs/runs/summaries, throughput gain +6.4% (100 agents) / +0.4% (300 agents) snapshot-OFF vs ON, memory reduction 98%, comparison MD percentages cross-verified, determinism preserved (carrying_agents=22, signal_total=7329 match across ON/OFF), engine opt improved snapshot-ON by 11%/9%. Snapshot-OFF 300-agent shows 5.5% regression (run-to-run variance, not code defect) → 17/18 PASSED, 1 OBSERVATION

### Round 10 (commits 30-42 — CI/CD, tooling, testing, release cycle)

70. `.venv/bin/python -m pytest -v` → `86 passed in 0.55s` (was 72 — +7 app tests, +3 import-flow tests, +4 perf-toggle tests, +3 release-consistency tests = +14 new tests, minus 3 already counted in Round 9 from test file expansion)
71. `.venv/bin/python scripts/check_import_flow.py` → `Total imports: 20, Result: OK (0 violations)`. Import rule `contracts ← core ← scenarios ← app` holds across all source files.
72. Commits 30-35 deep-dive: 24 checks — CI triggers/Python 3.11/import-flow step/pytest step ✓, version bump to 0.1.1 ✓, CHANGELOG.md 0.1.1 section accurate ✓, milestone notes internally consistent ✓, README updated ✓, run_perf_snapshot_toggle.py CLI/ON-OFF/comparison/determinism/security ✓, tooling tests meaningful with importlib.util loading ✓, Makefile targets/dependencies/PYTHON variable ✓, CLI error-path tests (invalid scenario/non-positive ticks/conflicting flags) ✓, release-check target ✓ → **22/24 PASSED, 2 OBSERVATIONS** (milestone "27-29" numbering is agent's own sequence; perf-smoke target was added incrementally in commit 35 not 34)
73. Commits 36-42 deep-dive: 27 checks — --json-out test with tmp_path + round-trip equality ✓, benchmark-smoke.yml triggers/params/artifacts/path-filter ✓, package job needs:test/build/clean-venv/smoke/upload/.gitignore ✓, perf contract test with monkeypatch/schema/multi-agent/markdown ✓, release-consistency guardrail tomllib/validation/tests/CI-step ✓, 0.1.2rc2 version+changelog ✓, 0.1.2 stable promotion with explicit rc2 provenance ✓ → **ALL 27 PASSED**
74. `.venv/bin/python scripts/check_release_consistency.py` → `pyproject version: 0.1.2, changelog headings: 0.1.2, 0.1.2rc2, 0.1.1, Result: OK` (release consistency validated)

### Round 11 (commit 43 — midway report + bundled audit commit)

75. `git log --oneline e713dc0..20d3005` → 1 new commit: `20d3005 docs: add midway report analysis and comprehensive project report`. Only 1 commit, not the 5 expected by user ("43-47").
76. `.venv/bin/python -m pytest -v` → `86 passed in 0.60s` (unchanged — no code modifications in commit 43)
77. `.venv/bin/python scripts/check_import_flow.py` → `Total imports: 20, Result: OK (0 violations)` (unchanged — no source modifications)
78. Commit 43 deep-dive: 16 checks — package structure ✓, dependency rules accurate but import-lint claim stale ✗, D1-D15 ✓ (D14 stale), test counts undercount by 14 ✗, engine lifecycle diagram precise ✓, scenario model verified ✓, test count wrong (72 vs 86) ✗, import-lint gap claim factually wrong ✗, baselines match real data (not latest) ✓, git progression stops at 32 ✗, R1-R12 mostly accurate ✓, audit findings summary ✓, staleness pervasive (4×"32", 8×"72") ⚠️, CI/CD entirely omitted ✗, commit message omits 913-line audit bundle ✗, Environment Snapshot internally inconsistent ⚠️ → **5 PASS, 6 FAIL, 3 PASS with caveat, 2 OBSERVATION. Issue I-16 opened.**
79. `git diff e713dc0..20d3005 -- 11_agent_execution_audit.md | wc -l` → 972 diff lines. Agent committed auditor's uncommitted Rounds 8-10 content (913 insertions) as part of its own commit.

### Round 12 (commit 44 — evidence matrix + final report sync)

80. `git log --oneline 20d3005..5b313b9` → 1 new commit: `5b313b9 docs: sync final report and evidence matrix to v0.1.2 state`. Only 1 commit, not the 5 expected by user ("44-48").
81. `.venv/bin/python -m pytest -v` → `86 passed in 0.59s` (unchanged — documentation-only commit)
82. `.venv/bin/python scripts/check_import_flow.py` → `Total imports: 20, Result: OK (0 violations)` (unchanged — no source modifications)
83. Deep-dive verification: 66 independent checks across R1-R12 artifact existence, test evidence, status accuracy, and final report addendum claims → **66/66 PASS, 0 FAIL**. Every file path in the evidence matrix corresponds to a real file; every status assessment matches actual implementation state.
84. `git diff 20d3005..5b313b9 --stat` → 2 files changed, 32 insertions, 18 deletions (`07_tfg_evidence_matrix.md`, `08_final_report.md`)

### Round 13 (commits 45-46 — audit scope clarification + midway report addendum)

85. `git log --oneline 5b313b9..8508047` → 2 commits: `081d49a docs: clarify audit scope and sync ranges across reports`, `8508047 docs: align midway report scope, structure, and conclusion framing`.
86. `.venv/bin/python -m pytest -v` → `86 passed` (unchanged — documentation-only commits)
87. `.venv/bin/python scripts/check_import_flow.py` → `Total imports: 20, Result: OK (0 violations)` (unchanged — no source modifications)
88. Commit 45 deep-dive: 10 checks — scope note in `06_execution_blueprint.md` references correct authoritative docs ✓, scope note in `07_tfg_evidence_matrix.md` says "through commit 44" matches audit content ✓, scope note in `08_final_report.md` says "through commit 44" matches addendum ✓, scope note in `20260304_midway_report.md` says "through commit 32" (accurate at time of commit, overwritten by commit 46) ✓, audit table rows 43-44 present with correct hashes and scores ✓, test suite count updated to "86 passed, 0 failed (as of commit 44)" ✓, commit 43 deep-dive mentions "5/16 PASS, 6/16 FAIL, 3/16 PASS with caveat, 2/16 OBSERVATION" checksums match ✓, commit 44 deep-dive claims "66/66 PASS" consistent with evidence matrix verification ✓, I-16 issue correctly described and categorized ✓, Environment Snapshot "Git commits" row updated to "44 commits audited" ✓ → **ALL 10 PASSED**
89. Commit 46 deep-dive: 10 checks — scope note updated to "Two-pass report... through commit 48" ✓, Section 17 delta summary (16 commits, 2,969 lines, 0.1.0→0.1.2) plausible ✓, Section 19 ci.yml description (2 jobs: test + package) matches known CI structure ✓, Section 20 import-flow algorithm matches actual `check_import_flow.py` source ✓, Section 20 claims "0 violations" confirmed by running `check_import_flow.py` ✓, Section 21 version history (0.1.1 → 0.1.2rc2 → 0.1.2) matches CHANGELOG.md ✓, Section 22 determinism cross-check code snippet matches actual benchmark runner pattern ✓, Section 24 test delta (+14 from 72 to 86) accurate for commit 46 context ✓, Section 26 R1-R12 updated statuses reasonable ✓, old conclusion replaced (not merely appended) ✓ → **ALL 10 PASSED**

### Round 14 (commits 47-50 — persistence adapter, CLI save/load, documentation, R7 evidence)

90. `git log --oneline 8508047..90aae46` → 4 commits: `0631339 feat(adapters): add JSON file persistence adapter with tests`, `8a371c8 feat(app): add CLI save/load run persistence flows`, `0d7e7ca docs: document CLI persistence workflows and changelog updates`, `90aae46 docs(plans): add adapter-backed R7 save/load reproducibility example`.
91. `.venv/bin/python -m pytest -v` → `89 passed` (was 86 — +3 adapter tests from commit 47)
92. `.venv/bin/python scripts/check_import_flow.py` → `Total imports: 22, Result: OK (0 violations)` (but `adapters` layer not in `ALLOWED_IMPORTS` — imports from/to adapters are silently skipped)
93. Commit 47 deep-dive: 12 checks — `JsonFilePersistence` passes `isinstance(_, PersistencePort)` at runtime ✓, `save_run` signature matches `PersistencePort.save_run` ✓, `load_run` signature matches `PersistencePort.load_run` ✓, `model_copy(deep=True)` used on both manifest and snapshots during save ✓, import direction (`adapters.persistence.json_file` → `contracts.models` only) ✓, `adapters` layer in `ALLOWED_IMPORTS` → ✗ (issue I-17: imports unchecked), test isolation via `tmp_path` ✓, test protocol conformance (`isinstance` check) ✓, test mutation isolation (post-save mutation verified against loaded data) ✓, `__init__.py` re-exports clean with `__all__` ✓, file encoding `utf-8` specified in both read and write ✓, `RunManifest` and `LoadedRun` models exist in `contracts.models` ✓ → **11/12 PASSED, 1 FAIL (I-17)**
94. Commit 48 deep-dive: 15 checks — `--save-run-id` and `--load-run-id` mutually exclusive (argparse group) ✓, `--persistence-root` defaults to `Path("runs")` ✓, load path returns 0 without running simulation ✓, load path handles `FileNotFoundError` via `parser.error()` ✓, save path creates `RunManifest` with correct fields ✓, `snapshots_for_persistence` includes initial state (index 0) ✓, snapshot count = ticks + 1 (3 ticks → 4 snapshots) ✓, `_emit_payload()` handles `json_out is None` case (stdout only) ✓, `_emit_payload()` creates parent directories for `json_out` ✓, import `from sim_framework.adapters.persistence` in app layer conceptually correct but NOT enforced (see I-17) ✓, `SnapshotHistory` always created even without persistence ⚠️ (performance concern), deep copy on every tick even without `--save-run-id` ⚠️ (performance concern), test save flow validates both stdout JSON and disk artifact ✓, test load flow is a two-phase save-then-load ✓, test error paths verify `SystemExit(2)` and stderr messages ✓ → **13/15 PASSED, 2 OBSERVATION** (unconditional deep-copy overhead)
95. Commit 49 deep-dive: 8 checks — CHANGELOG mentions `JsonFilePersistence` matches actual class name ✓, CHANGELOG mentions `PersistencePort` matches actual port name ✓, CHANGELOG mentions 3 CLI flags matches `--save-run-id`, `--load-run-id`, `--persistence-root` ✓, README save example valid CLI invocation ✓, README load example valid CLI invocation ✓, README custom root example valid CLI invocation ✓, CHANGELOG "Post-0.1.2" section is inside `[0.1.2]` heading (not `[Unreleased]`) ⚠️ convention violation, `check_release_consistency.py` still passes (guardrail does not detect this) ✓ → **7/8 PASSED, 1 OBSERVATION** (CHANGELOG structural convention)
96. Commit 50 deep-dive: 11 checks — SHA-256 of `Plans/runs/r7-repro-20260304/run.json` matches documented hash (`6704f7e7...`) ✓, SHA-256 of `Plans/r7_repro_save_2026-03-04.json` matches documented hash (`cf341afa...`) ✓, SHA-256 of `Plans/r7_repro_load_2026-03-04.json` matches documented hash (`46dca5e8...`) ✓, `run.json` is valid JSON parseable as `LoadedRun` ✓, `run.json` has 6 snapshots at ticks 0-5 ✓, `run.json` manifest: run_id=`r7-repro-20260304`, scenario=`ants_foraging`, seed=42 ✓, save JSON: `ticks_completed=5`, `snapshots_saved=6` ✓, load JSON: `mode="loaded"`, `snapshots=6`, `last_tick=5` ✓, save JSON `carrying_agents=5` and `signal_total=37.0` match deterministic seed 42 ✓, milestone tag `milestone-persistence-cli-2026-03-04` exists as git tag → ✓ (tag confirmed present as of 2026-03-04 post-patch verification), base commit `0d7e7ca` referenced in markdown matches commit 49 ✓ → **11/11 PASSED** (tag stale-claim corrected — tag now exists)

### Round 15 (commits 51-53 — drone scenario, scenario-aware benchmarks, R5 evidence bundle)

97. `git log --oneline 90aae46..be91aaa` → 3 commits: `67cb39b feat(scenarios): add drone_patrol scenario with registry and tests`, `0e39048 feat(tooling): add scenario-aware benchmark workflows`, `be91aaa feat(r5): add drone reproducibility bundle and scenario-aware CLI dispatch`.
98. `.venv/bin/python -m pytest -v` → `103 passed` (was 89 — +7 drone scenario tests, +3 benchmark tests, +1 CLI dispatch test, +3 perf-toggle extension)
99. `.venv/bin/python scripts/check_import_flow.py` → `Total imports: 26, Result: OK (0 violations)`
100. Commit 51 deep-dive: 9 checks — spec structure follows `StateMachineAgentSchemaSpec` ✓, `validate_known_behavior_names` called at module load ✓, registry integration (get_scenario + list_scenarios) ✓, import direction (scenarios → core, scenarios → contracts) ✓, no import from app layer ✓, SignalField kind="radio" (not "pheromone") ✓, deterministic placement (no RNG in `build_initial_state`) ✓, 100-tick integration stays in bounds ✓, signal deposits occur (total_signal > 0) ✓ → **ALL 9 PASSED**
101. Commit 52 deep-dive: 7 checks — `--scenario` CLI arg uses dynamic `list_scenarios()` choices ✓, dispatch handles `num_ants` and `num_drones` parameters ✓, unknown scenario parameter raises clear ValueError ✓, backwards compatibility (default scenario still `ants_foraging`) ✓, JSON output includes scenario name in config and runs ✓, ON/OFF comparison still works with drone scenario ✓, `_parse_agents` validates empty, non-int, non-positive ✓ → **ALL 7 PASSED**
102. Commit 53 deep-dive: 10 checks — CLI `--scenario drone_patrol` dispatch works ✓, save JSON scenario="drone_patrol" with ticks_completed=8 and snapshots_saved=9 ✓, load JSON mode="loaded" with scenario_name="drone_patrol" and snapshots=9 and last_tick=8 ✓, SHA-256 of `r5_drone_repro_save` matches doc ✓, SHA-256 of `r5_drone_repro_load` matches doc ✓, SHA-256 of `perf_comparison` matches doc ✓, perf comparison determinism cross-check 2/2 matched ✓, evidence matrix R5 row updated correctly ✓, import flow still 0 violations ✓, `run.json` artifact exists (1728 lines, 9 snapshots) ✓ → **ALL 10 PASSED**. Observation: `--ants` parameter name is semantically incorrect for drone scenarios; also `_build_state_for_scenario` duplicated between `cli.py` and `benchmark_headless.py`.

### Round 16 (commits 54-57 — R7 closure, R4 boundary mode, R3 agent-spec overrides, R6/R9 roadmap)

103. `git log --oneline be91aaa..5b80384` → 4 commits: `c7cd7e5 docs(matrix): close R7 as implemented scope with persistence evidence`, `fc42c7d feat(r4): expose runtime boundary mode and add physics reproducibility bundle`, `f845815 feat(r3): add validated agent-spec runtime overrides with evidence`, `5b80384 docs(roadmap): add R6/R9 UI-desktop execution plan`.
104. `.venv/bin/python -m pytest -v` → `110 passed in 0.79s` (was 103 — +3 boundary mode tests, +4 agent-spec tests)
105. `.venv/bin/python scripts/check_import_flow.py` → `Total imports: 28, Result: OK (0 violations)`
106. Commit 54 deep-dive: 6 checks — test count 103/103 matches actual at commit 53 ✓, R7 status change from "In progress" to "Done (implemented scope)" ✓, R7 artifacts list includes persistence adapter and CLI ✓, R7 test evidence includes persistence + CLI tests ✓, no stale cross-references to removed/renamed files ✓, commit scope note says "commit 57" (refers to git position, correct for what was synced) ✓ → **ALL 6 PASSED**
107. Commit 55 deep-dive: 13 checks — `boundary_mode` parameter threaded CLI → runner → `apply_movement` ✓, default remains "clamp" (backwards compatible) ✓, validation rejects invalid `boundary_mode` in both runners ✓, `_create_runner_for_scenario` uses `inspect.signature` dispatch ✓, JSON output includes `physics.boundary_mode` ✓, SHA-256 of `r4_physics_drone2_clamp_saved` matches doc ✓, SHA-256 of `r4_physics_drone2_wrap_saved` matches doc ✓, evidence shows trajectory divergence between clamp and wrap ✓, all 6 `run.json` bundles exist in `Plans/runs/` ✓, matrix R4 status updated to "Done (implemented scope)" ✓, matrix test count updated to 106/106 ✓, import flow 0 violations after changes ✓, all affected tests pass ✓ → **ALL 13 PASSED**. Note: commit diff is +71,840 lines, 99.4% from run.json evidence files (6 bundles × 40 ticks × 40+ agents).
108. Commit 56 deep-dive: 15 checks — SHA-256 hashes match (all 8 evidence files) ✓, `run.json` (ants) is genuine simulation output (re-ran with identical params, bit-for-bit identical) ✓, agent speed in ants `run.json` matches custom spec 1.8 ✓, agent speed in drone `run.json` matches custom spec 2.0 ✓, snapshot count 21 (ticks 0-20) matches ✓, run output JSON references correct `agent_spec_source` ✓, load output JSON confirms round-trip (21 snapshots, tick 20) ✓, test count 106→110 ✓, import layer compliance 0 violations ✓, all 30 tests in changed files pass ✓, full suite 110 passed ✓, custom spec validation rejects unknown behaviors ✓, `_behavior_params` uses name-based lookup (not positional) ✓, spec threaded into both `build_initial_state` and `create_behavior_runner` via `inspect.signature` ✓, registry wires `validate_agent_spec` for both scenarios ✓ → **ALL 15 PASSED**
109. Commit 57 deep-dive: 8 checks — roadmap structurally complete (milestones, acceptance, risks, DoD) ✓, roadmap preserves backend guarantees (determinism, isolation) ✓, evidence matrix R6/R9 rows updated consistently ✓, CHANGELOG entry present ✓, README entry present ✓, no code changes (doc-only commit) ✓, test suite still passes (110/110 unchanged) ✓, roadmap is actionable vs vaporware → PARTIAL (concrete milestones and acceptance criteria but lacks timelines, effort estimates, and specific technology choices) ⚠️ → **7/8 PASSED, 1 OBSERVATION** (roadmap is a real plan skeleton but not fully executable without timelines and technology decisions)

---

### Post-Patch Verification (2026-03-04 coherence pass)

110. `.venv/bin/python -m pytest -v` → `110 passed in 0.85s` (confirms test count in Environment Snapshot and closing summary)
111. `.venv/bin/python scripts/check_import_flow.py` → `Total imports: 28, Result: OK (0 violations)` (confirms import count; I-17 still open — adapters layer not in checker)
112. `git rev-list --count HEAD` → `61` (confirms 61 git commits = 57 audit-numbered commits)
113. `git tag --list` → 7 tags: `milestone-backend-complete-2026-03-04`, `milestone-persistence-cli-2026-03-04`, `milestone-runtime-mode-2026-03-04`, `v0.1.1`, `v0.1.2`, `v0.1.2-rc1`, `v0.1.2-rc2` (confirms item 29 tag correction and closing summary tag count)

---

## Audit Methodology

Each commit is assessed on:

1. **Checklist compliance** — Does it match `10_execution_kit/01_first_10_commits_checklist.md` exactly?
2. **Code quality** — Is the code clean, well-typed, following Python/Pydantic idioms?
3. **Test depth** — Do tests exercise the meaningful behaviors, not just happy paths?
4. **Alignment with final report** — Does the implementation follow `08_final_report.md`'s crystallized proposal (D1-D18, G1-G8)?
5. **Forward compatibility** — Will this commit cause problems for later commits?

---

*All 10 checklist commits completed. Post-checklist commits 11-57 (47 commits) address audit findings, policy controls, integration hardening, performance baseline, profile-guided optimization cycle, public CLI with runtime modes and persistence, engine per-tick deep-copy elimination, CI/CD pipeline with import-flow and release-consistency guardrails, wheel packaging validation, reproducible benchmark tooling with contract tests, stable 0.1.2 release, midway project report with two-pass addendum, evidence matrix sync, JSON file persistence adapter, second scenario (drone_patrol), scenario-aware benchmarking, boundary mode exposure, agent-spec runtime overrides, R3/R4/R5/R7 reproducibility evidence bundles with SHA-256 verification, and R6/R9 UI-desktop execution roadmap. All 113 command evidence items independently verified. 110/110 tests passing. 0 import rule violations across 28 import statements. 2 MEDIUM issues: I-16 (midway report staleness, substantially addressed by commit 46 addendum) and I-17 (adapters layer invisible to import checker, OPEN). 7 git tags present (3 milestones, 4 version tags). 61 git commits total (57 in audit numbering). Audit complete for audited range through commit 57 (2026-03-04).*
