# TFG Evidence Matrix

**Date:** 2026-03-04  
**Purpose:** Provide thesis-defense traceability from requirement to architecture decision, implementation artifact, test evidence, and demo evidence.  
**Companion document:** `06_execution_blueprint.md`
**Current implementation state:** `v0.1.2` (stable), CI green, 86/86 tests passing
**Scope note:** Synced to audited range through commit 44 (2026-03-04). Re-validate matrix rows after newer commits.

---

## 1. How to Use This Matrix

For each requirement:

1. Confirm interpretation is correct.
2. Implement linked artifacts.
3. Produce the required test evidence.
4. Capture the listed demo/thesis evidence.
5. Mark status (`Not started`, `In progress`, `Done`, `Done (implemented scope)`).

---

## 2. Requirement Traceability Matrix

| Req ID | Requirement (Prompt) | Clarified Interpretation | Decisions | Implementation Artifacts | Test Evidence | Demo/Thesis Evidence | Status |
|---|---|---|---|---|---|---|---|
| R1 | Strict modularity via contracts | Module coupling only through typed contracts and validated models | D3, D4, D5, D10 | `sim_framework/contracts/models.py`, `sim_framework/contracts/ports.py`, `scripts/check_import_flow.py` | `tests/contracts/test_ports_contract_shape.py`, `tests/tooling/test_check_import_flow.py`, CI import-flow step | Import-flow report (`0 violations`) + layered dependency explanation | Done |
| R2 | Per-module testing | Every implemented module has unit tests; boundaries have contract tests | D14 | `tests/core/`, `tests/contracts/`, `tests/scenarios/`, `tests/app/`, `tests/tooling/`, `tests/integration/` | CI pytest (`86/86`) | Testing chapter matrix by package | Done (implemented scope) |
| R3 | Configurable agent attributes | Attribute config is validated at model/schema layer; UI editor pending | D6, D7, D15 | `sim_framework/contracts/validators.py`, `sim_framework/scenarios/ants_foraging/spec.py` | `tests/contracts/test_validators_schema.py` | Documented headless configuration flow | In progress |
| R3b | Configurable agent methods (user clarification) | Methods = selecting/composing known behavior methods, not code injection | D6, D7 | `sim_framework/contracts/behaviors.py`, `sim_framework/contracts/validators.py` | behavior registry + schema tests | Explicit thesis note clarifying "attributes + methods" | Done (implemented scope) |
| R4 | Configurable physics | Physics is parameterized in core/runtime; UI editing layer pending | D6, D15 | `sim_framework/core/physics.py`, runtime config in scenario/app | `tests/core/test_physics_movement.py` | Parameter-impact benchmark notes | In progress |
| R5 | Multi-scenario generality | Core supports registry-based scenarios; ants implemented, drone pending | D5, D15 | `sim_framework/scenarios/registry.py`, `sim_framework/scenarios/ants_foraging/` | `tests/scenarios/test_ants_scenario_loads.py`, integration smoke | Scenario extension plan section | In progress |
| R6 | Modern, performant UI | Web UI/PixiJS not yet implemented in this release line | D1, D13 | N/A (adapter placeholders only) | N/A | Deferred to next scope increment | Not started |
| R7 | Playback and capture controls incl. rewind | Play/pause/step/reset/seek/rewind implemented headlessly; screenshot/save-load adapters pending | D8, D9, D10 | `sim_framework/core/engine.py`, `sim_framework/core/history.py`, control commands in contracts | determinism + history + command tests | Headless replay/rewind evidence in audit logs | In progress |
| R8 | Python implementation | Core system implemented in Python 3.11+ | D2 | entire codebase | Python policy gate + CI runtime + release-check | Toolchain section with `.venv` + `uv` workflow | Done |
| R9 | Linux desktop + web-like app | Browser/desktop shell path remains pending | D1 | `sim_framework/app/cli.py` (headless composition root) | CLI smoke tests | Planned desktop/web adapter roadmap | Not started |
| R10 | Orchestrator governance | Composition root exists for runtime mode, scenario wiring, and lifecycle execution | D5, D15 | `sim_framework/app/cli.py`, `sim_framework/app/runtime.py` | `tests/app/test_cli_runtime_mode.py`, release wheel smoke (`sim-run`) | Sequence diagram (runtime mode + engine lifecycle) | Done (implemented scope) |
| R11 | Robust runtime behavior | One faulty agent cannot crash full simulation | D11 | `sim_framework/core/engine.py` error isolation path | `tests/core/test_engine_error_isolation.py` | Error-event evidence in audit/tests | Done |
| R12 | Determinism and reproducibility | Same seed/scenario/commands reproduce same state trajectories | D12, D14 | deterministic engine + benchmark tooling + manifests in `Plans/` | determinism tests + ON/OFF comparison contract tests | Reproducibility appendix with seed/config outputs | Done |

---

## 3. Decision-to-Test Coverage

| Decision | Verification Test | Acceptance Rule |
|---|---|---|
| D1 UI path | End-to-end web + pywebview smoke tests | Both launch and control simulation |
| D2 Python runtime | Environment lock + CI job | Python 3.11+ only |
| D3 Pydantic models | Model parsing/serialization tests | Invalid data rejected, valid data stable round-trip |
| D4 Protocol contracts | Static typing + runtime conformance tests | Each adapter satisfies required methods |
| D5 5-package structure | Import-lint/check script | No forbidden cross-layer imports |
| D6 Config boundary | UI payload contract tests | No arbitrary code field accepted |
| D7 Composition model | Agent assembly tests | Behavior chain composes without dynamic class generation |
| D8 Snapshot+replay | Rewind hash equivalence test | Replayed state hash equals canonical forward hash |
| D9 Queue concurrency | Queue throughput + race-condition tests | No deadlocks, no blocking API loop |
| D10 Minimal ports | Architecture review checklist | New port only when second implementation exists |
| D11 Error isolation | Fault-injection test | Crashed agent isolated, simulation continues |
| D12 Determinism | Seeded golden test at tick N | Stable hash across repeated runs |
| D13 Performance policy | Profiling runs after P2/P4 | Metrics captured and tracked |
| D14 Test minimum | CI gate policy | Merge blocked if mandatory suites fail |
| D15 Build order | Milestone checklist by phase | No out-of-order implementation unless justified |

---

## 4. ABM Verification and Validation (Thesis-Facing)

| Dimension | Question | Evidence Artifact |
|---|---|---|
| Software verification | Is code implementing intended rules correctly? | Unit/contract/determinism reports |
| Model validation | Does model behavior plausibly match domain expectations? | Scenario-level metrics and qualitative pattern checks |
| Replicability | Can another evaluator reproduce results? | Seeded manifests, environment lock, replay artifacts |

---

## 5. Mandatory Thesis Artifacts

1. Architecture diagram showing dependency direction and package boundaries.
2. Requirement-to-decision traceability table (this file, finalized).
3. Test evidence appendix with CI outputs and deterministic hash records.
4. Rewind mechanism explanation with complexity and memory bounds.
5. Two-scenario demonstration evidence (ants + at least one drone scenario).
6. Reproducibility package: config, seed, command script, and result hashes.

---

## 6. Defense Checklist (Go/No-Go)

All must be `Yes` before defense:

1. Are R1-R12 implemented with linked evidence?
2. Do mandatory tests pass in CI?
3. Does the demo include rewind and scenario switching?
4. Is there one reproducibility bundle that runs end-to-end on a clean machine?
5. Are deviations from locked decisions documented with rationale?
