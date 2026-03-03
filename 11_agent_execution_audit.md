# Agent Execution Audit

**Auditor:** PAI (independent review)
**Date started:** 2026-03-03
**Last updated:** 2026-03-03
**Scope:** Continuous audit of the coding agent's execution against `10_execution_kit/01_first_10_commits_checklist.md` and `08_final_report.md`

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

**Test suite:** 62 passed, 0 failed (as of commit 16)
**End-of-Commit-10 Acceptance:** ALL 4 CRITERIA MET
**Post-Checklist Phase:** Commits 11-16 address audit findings I-14, I-15, I-12, I-7, I-9

---

## Current Truth Snapshot

This section reflects the current project state after checklist completion:

1. Project runtime is now Python 3.11.11 in `.venv` (policy-compliant environment).
2. Editable install works in `.venv`: `uv pip install --python .venv/bin/python -e .` succeeds.
3. Full test suite passes in `.venv`: `62 passed, 0 failed`.
4. System Python is still 3.10.9, but it is no longer the project execution environment.
5. Packaging discovery issue (I-8) is resolved.
6. ~~Remaining structural concern: schema split (`AgentSchemaSpec` vs `AntBehaviorSpec`, I-14).~~ **RESOLVED** by commit 11 — unified `StateMachineAgentSchemaSpec` in contracts layer.
7. Gradient sensing moved to framework API (`SignalGrid.sense_gradient()`) by commit 12 — resolves I-15.
8. Speed multiplier now consumed by engine for step batching by commit 13 — resolves I-12.
9. Package metadata now points to `README.md` (commit 15) — resolves I-7.
10. Port contract tests now validate method signatures and type hints against protocol definitions (commit 16) — resolves I-9.

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

---

## Environment Snapshot

| Property | Value | Expected | Status |
|----------|-------|----------|--------|
| System Python | 3.10.9 | >=3.11 (per pyproject.toml) | MISMATCH — mitigated by `.venv` runtime |
| Project Python (`.venv`) | 3.11.11 | >=3.11 (per pyproject.toml) | OK — policy-compliant runtime |
| Pydantic version | 2.8.2 | >=2.7 | OK |
| pytest version (system) | 7.1.2 | >=8.0 (per pyproject.toml dev) | MISMATCH — use `.venv` pytest |
| pytest version (`.venv`) | 9.0.2 | >=8.0 (per pyproject.toml dev) | OK |
| Editable install in `.venv` | SUCCEEDS | Should succeed | OK — discovery fixed and Python policy satisfied |
| Tests passing | 62/62 | All green | OK |
| Git commits | 18 | 10 checklist + post-checklist maintenance sequence | COMPLETE (audit ongoing) |
| Import rule violations | 0 | 0 | OK — `contracts ← core ← scenarios`, 13 imports all flow correctly |
| End-of-commit-10 acceptance | ALL 4 MET | All 4 criteria | COMPLETE |
| Post-checklist improvements | 6 commits | Address audit findings I-12, I-14, I-15, I-7, I-9 + audit consistency pass | ALL COMPLETED |

---

## Issue Tracker

| ID | Severity | Commit | Description | Status |
|----|----------|--------|-------------|--------|
| I-1 | MEDIUM | 1 | Commit message deviates from checklist convention | OPEN |
| I-2 | LOW | 1 | `__pycache__` committed to git history | OPEN (fixed going forward) |
| I-3 | MEDIUM | 1 | System interpreter is 3.10.9 while project policy is `>=3.11`; mitigated by `.venv` Python 3.11.11 | MITIGATED |
| I-4 | LOW | 2 | Frozen `Vector2` creates GC pressure at scale | DEFERRED (per D13) |
| I-5 | MEDIUM | 2 | `SignalField` is config-only, needs runtime state class | **RESOLVED** by commit 6 (`SignalGrid` dataclass) |
| I-6 | MEDIUM | 2 | 8 of 9 field validators untested | **RESOLVED** by commit 5 (retroactive test additions) |
| I-7 | LOW | 2 | `pyproject.toml` readme points to 590-line audit report | **RESOLVED** by commit 15 (`README.md` + metadata fix) |
| I-8 | CRITICAL | 2 | `pip install -e .` fails: setuptools autodiscovery finds `MEMORY` + `sim_framework` | **RESOLVED** by commit 2.5 (package find constraint) |
| I-9 | LOW | 3 | Port stubs lack return type annotations, `runtime_checkable` only checks method names | **RESOLVED** by commit 16 (signature and type-hint conformance tests) |
| I-10 | MEDIUM | 4-5 | Validator schema uses flat `behavior_chain`, not state machine from `08_final_report.md` | **SUPERSEDED** by I-14 — scenario bypassed validators entirely |
| I-11 | LOW | 6 | `sample()` reads point value, not gradient — ant pheromone-following will need extension | **RESOLVED** by commit 12 (`SignalGrid.sense_gradient()` framework API; commit 10 provided the interim scenario-local fix) |
| I-12 | LOW | 8 | `speed_multiplier` stored but never consumed by engine — speed control is external | **RESOLVED** by commit 13 (step batching via multiplier) |
| I-13 | LOW | 9 | `SpatialHash` built to spec but unused by ants scenario — unit-tested only | OPEN |
| I-14 | MEDIUM | 10 | Two coexisting schema systems — `AgentSchemaSpec` (validators.py) is dead code, `AntBehaviorSpec` (spec.py) is active | **RESOLVED** by commit 11 (unified `StateMachineAgentSchemaSpec` in contracts) |
| I-15 | LOW | 10 | Pheromone gradient logic in scenario, not framework — `_best_pheromone_direction()` is not reusable | **RESOLVED** by commit 12 (`SignalGrid.sense_gradient()` framework API) |

**CRITICAL:** 0 | **MEDIUM:** 2 (I-1, I-3) | **LOW:** 3 | **RESOLVED:** 9 | **MITIGATED:** 1 | **SUPERSEDED:** 1

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

---

## Audit Methodology

Each commit is assessed on:

1. **Checklist compliance** — Does it match `10_execution_kit/01_first_10_commits_checklist.md` exactly?
2. **Code quality** — Is the code clean, well-typed, following Python/Pydantic idioms?
3. **Test depth** — Do tests exercise the meaningful behaviors, not just happy paths?
4. **Alignment with final report** — Does the implementation follow `08_final_report.md`'s crystallized proposal (D1-D18, G1-G8)?
5. **Forward compatibility** — Will this commit cause problems for later commits?

---

*All 10 checklist commits completed. Post-checklist commits 11-16 address audit findings and documentation/test hardening. Audit ongoing.*
