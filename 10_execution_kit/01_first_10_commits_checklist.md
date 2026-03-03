# First 10 Commits Checklist

**Source of truth:** `06_execution_blueprint.md`, `07_tfg_evidence_matrix.md`, `08_final_report.md`  
**Goal:** get from zero code to a deterministic headless ant simulation core with rewind-ready structure.

## Commit 1
**Message:** `chore: scaffold sim_framework package layout`

Create in this order:
1. `sim_framework/__init__.py`
2. `sim_framework/contracts/__init__.py`
3. `sim_framework/core/__init__.py`
4. `sim_framework/scenarios/__init__.py`
5. `sim_framework/adapters/__init__.py`
6. `sim_framework/adapters/web/__init__.py`
7. `sim_framework/adapters/persistence/__init__.py`
8. `sim_framework/app/__init__.py`
9. `tests/__init__.py`
10. `pyproject.toml`

Test gate:
```bash
python -m pytest -q
```

## Commit 2
**Message:** `feat(contracts): add core pydantic domain models`

Create in this order:
1. `sim_framework/contracts/models.py`
2. `tests/contracts/test_models_basic.py`

Minimum models:
1. `Vector2`
2. `AgentState`
3. `FoodSource`
4. `Colony`
5. `SignalField`
6. `SimulationState`

Test gate:
```bash
python -m pytest -q tests/contracts/test_models_basic.py
```

## Commit 3
**Message:** `feat(contracts): define protocol ports and command/event types`

Create in this order:
1. `sim_framework/contracts/ports.py`
2. `tests/contracts/test_ports_contract_shape.py`

Minimum protocols:
1. `RendererPort`
2. `PersistencePort`
3. `HistoryPort`

Add command/event models for queue payloads in `models.py` if missing.

Test gate:
```bash
python -m pytest -q tests/contracts
```

## Commit 4
**Message:** `feat(contracts): add behavior protocol and registry skeleton`

Create in this order:
1. `sim_framework/contracts/behaviors.py`
2. `tests/contracts/test_behavior_registry.py`

Minimum:
1. `BehaviorProtocol` with `sense`, `decide`, `act`
2. registry dict with registration guard

Test gate:
```bash
python -m pytest -q tests/contracts/test_behavior_registry.py
```

## Commit 5
**Message:** `feat(contracts): add validators for schema and behavior spec`

Create in this order:
1. `sim_framework/contracts/validators.py`
2. `tests/contracts/test_validators_schema.py`

Validate:
1. attribute ranges
2. known behavior names only
3. no executable code payloads

Test gate:
```bash
python -m pytest -q tests/contracts
```

## Commit 6
**Message:** `feat(core): add environment signal grid with diffusion and decay`

Create in this order:
1. `sim_framework/core/environment.py`
2. `tests/core/test_environment_signals.py`

Minimum:
1. grid init
2. deposit
3. diffuse
4. decay
5. sample/sense method

Test gate:
```bash
python -m pytest -q tests/core/test_environment_signals.py
```

## Commit 7
**Message:** `feat(core): implement history snapshot buffer and replay hooks`

Create in this order:
1. `sim_framework/core/history.py`
2. `tests/core/test_history_buffer.py`

Minimum:
1. `deque(maxlen=N)` snapshot storage
2. `snapshot(state, tick)`
3. `nearest_snapshot_before(tick)`

Test gate:
```bash
python -m pytest -q tests/core/test_history_buffer.py
```

## Commit 8
**Message:** `feat(core): implement deterministic engine tick and command queue handling`

Create in this order:
1. `sim_framework/core/engine.py`
2. `tests/core/test_engine_determinism.py`
3. `tests/core/test_engine_error_isolation.py`

Minimum:
1. command drain at tick boundary
2. deterministic RNG with seed
3. per-agent try/except isolation
4. publish event emission stub

Test gate:
```bash
python -m pytest -q tests/core/test_engine_determinism.py tests/core/test_engine_error_isolation.py
```

## Commit 9
**Message:** `feat(core): add physics movement and boundary handling with simple spatial hash`

Create in this order:
1. `sim_framework/core/physics.py`
2. `tests/core/test_physics_movement.py`
3. `tests/core/test_spatial_hash_queries.py`

Minimum:
1. movement update
2. boundary clamp/wrap rule
3. grid spatial index build/query

Test gate:
```bash
python -m pytest -q tests/core/test_physics_movement.py tests/core/test_spatial_hash_queries.py
```

## Commit 10
**Message:** `feat(scenarios): add ants_foraging scenario with state-machine behavior spec`

Create in this order:
1. `sim_framework/scenarios/registry.py`
2. `sim_framework/scenarios/ants_foraging/__init__.py`
3. `sim_framework/scenarios/ants_foraging/spec.py`
4. `tests/scenarios/test_ants_scenario_loads.py`
5. `tests/integration/test_headless_ants_100ticks.py`

Minimum:
1. state machine with `searching` and `carrying`
2. pheromone-related behaviors present in spec
3. scenario can instantiate initial `SimulationState`

Test gate:
```bash
python -m pytest -q tests/scenarios tests/integration/test_headless_ants_100ticks.py
```

## End-of-Commit-10 Acceptance

All must pass:
```bash
python -m pytest -q
```

You should have:
1. deterministic core loop
2. signal environment for pheromones
3. rewind-capable history foundation
4. first ant scenario loading and running headless

