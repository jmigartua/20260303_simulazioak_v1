# TFG Evidence Matrix

**Date:** 2026-03-03  
**Purpose:** Provide thesis-defense traceability from requirement to architecture decision, implementation artifact, test evidence, and demo evidence.  
**Companion document:** `06_execution_blueprint.md`

---

## 1. How to Use This Matrix

For each requirement:

1. Confirm interpretation is correct.
2. Implement linked artifacts.
3. Produce the required test evidence.
4. Capture the listed demo/thesis evidence.
5. Mark status (`Not started`, `In progress`, `Done`).

---

## 2. Requirement Traceability Matrix

| Req ID | Requirement (Prompt) | Clarified Interpretation | Decisions | Implementation Artifacts | Test Evidence | Demo/Thesis Evidence | Status |
|---|---|---|---|---|---|---|---|
| R1 | Strict modularity via contracts | Module coupling only through typed contracts and validated models | D3, D4, D5, D10 | `contracts/models.py`, `contracts/ports.py`, package import policy | Contract conformance suite | Architecture diagram + dependency rule section | Not started |
| R2 | Per-module testing | Every module has unit tests; boundaries have contract tests | D14 | `tests/core/`, `tests/contracts/`, `tests/scenarios/`, `tests/adapters/` | CI report: unit + contract pass | Testing chapter with matrix of tests by module | Not started |
| R3 | Configurable agent attributes | UI edits validated attribute parameters | D6, D7, D15 | `contracts/validators.py`, agent schema handling in `core/agents.py` | Schema validation tests | UI screenshots of agent designer + rejected invalid config example | Not started |
| R3b | Configurable agent methods (user clarification) | Methods = selecting/composing known behavior methods, not code injection | D6, D7 | `contracts/behaviors.py`, curated behavior registry | Behavior chain validity tests | Section explaining "attributes + methods" interpretation | Not started |
| R4 | Configurable physics | Physics model parameters editable, model code remains curated | D6, D15 | `core/physics.py`, physics config models | Parameter boundary tests + invariant/property tests | Demo showing physics parameter impact | Not started |
| R5 | Multi-scenario generality | Ant and drone scenarios run on same core and contracts | D5, D15 | `scenarios/ants_foraging/`, `scenarios/drone_storm/`, `scenarios/registry.py` | Scenario contract tests + integration tests | Comparison table and live switch demo | Not started |
| R6 | Modern, performant UI | Web UI with clean controls, real-time rendering, stable frame pacing | D1, D13 | `adapters/web/static/`, PixiJS scene renderer | Render throughput measurements | UI walkthrough recording | Not started |
| R7 | Playback and capture controls incl. rewind | Play, pause, step, reset, seek, rewind, screenshot, save/load | D8, D9, D10 | `core/history.py`, `adapters/web/server.py`, persistence adapter | Rewind correctness and screenshot/save tests | Live rewind demo + exported artifact samples | Not started |
| R8 | Python implementation | Core system in Python 3.11+ | D2 | entire codebase | Environment and test run metadata | Toolchain section in thesis | Not started |
| R9 | Linux desktop + web-like app | Same backend; browser mode and pywebview desktop shell | D1 | `app/main.py`, pywebview launcher path | Smoke tests for web + desktop launch | Demo on Linux + browser | Not started |
| R10 | Orchestrator governance | Single composition root wires modules and enforces lifecycle | D5, D15 | `app/main.py` | Startup integration tests | Sequence diagram of startup and wiring | Not started |
| R11 | Robust runtime behavior | One faulty agent cannot crash full simulation | D11 | `core/engine.py` error isolation path | Fault-injection test around `agent.act()` | Error-report screenshot + log excerpt | Not started |
| R12 | Determinism and reproducibility | Same seed/scenario/commands must reproduce same state hashes | D12, D14 | RNG + manifest handling in core | Determinism test suite | Reproducibility appendix with run manifests | Not started |

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

