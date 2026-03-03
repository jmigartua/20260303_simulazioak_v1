# Execution Blueprint v1

**Date:** 2026-03-03  
**Project:** Modular multi-agent simulation framework (TFG)  
**Status:** Canonical implementation blueprint (reconciles 04 + 05 audit reports)

---

## 1. Purpose

This document is the single source of truth for implementation.

It resolves the main inconsistencies detected in earlier reports:

1. Module/package ambiguity (8 vs 9 modules) is replaced by a fixed 5-package structure.
2. Concurrency is locked as a design decision, not a later optional choice.
3. Configurability is precisely defined, including the user clarification that "functions" means class methods.
4. Traceability to tests and thesis evidence is made explicit.

---

## 2. Requirement Clarification (Attributes + Methods)

The prompt phrase "attributes and functions configurable" is interpreted as:

1. `Attributes` are UI-editable data parameters validated by schema.
2. `Methods` means behavior methods implemented in known Python behavior classes.
3. UI can select, order, and parameterize those behavior methods through a constrained behavior specification.
4. UI cannot inject arbitrary Python code.

This preserves safety, determinism, and testability while respecting the original intent.

---

## 3. Locked Decisions

| ID | Decision | Locked Value |
|---|---|---|
| D1 | v1 UI path | Web-first: FastAPI + WebSocket + PixiJS; desktop via pywebview |
| D2 | Language/runtime | Python 3.11+ |
| D3 | Data contracts | Pydantic v2 models in `contracts/models.py` |
| D4 | Interface contracts | Python `Protocol` in `contracts/ports.py` |
| D5 | Physical architecture | 5 packages: `contracts/`, `core/`, `scenarios/`, `adapters/`, `app/` |
| D6 | Configurability boundary | Parameters editable; behaviors selectable/composable; code not editable from UI |
| D7 | Agent design | Composition, not dynamic class generation |
| D8 | Rewind strategy | Snapshot + replay with bounded buffer (`deque(maxlen=N)`) |
| D9 | Concurrency model | Dedicated simulation thread + `cmd_queue` + `pub_queue` |
| D10 | Initial ports | Start with `RendererPort` and `PersistencePort`; add only when second implementation appears |
| D11 | Error isolation | Per-agent `try/except` in tick loop, structured error event to UI |
| D12 | Determinism | Seeded RNG, command application at tick boundaries only |
| D13 | Performance policy | Define metrics now, lock target numbers after profiling Phase 2/4 |
| D14 | Test minimum | Unit + contract + determinism + schema validation mandatory |
| D15 | Implementation order | Contracts first, then engine/history/physics, then scenarios, then adapters/UI |

---

## 4. Canonical Package Structure

```text
sim_framework/
├── contracts/
│   ├── models.py
│   ├── ports.py
│   ├── behaviors.py
│   └── validators.py
├── core/
│   ├── engine.py
│   ├── physics.py
│   ├── history.py
│   └── agents.py
├── scenarios/
│   ├── registry.py
│   ├── ants_foraging/
│   └── drone_storm/
├── adapters/
│   ├── web/
│   │   ├── server.py
│   │   └── static/
│   └── persistence/
│       └── storage.py
└── app/
    └── main.py
```

### Import Rule (must be enforced)

1. `contracts` imports nothing project-internal.
2. `core` imports only `contracts`.
3. `scenarios` imports `contracts` (and behavior registry interfaces), not adapters.
4. `adapters` import `contracts` and orchestration interfaces, never mutate core internals directly.
5. `app` is the only composition root allowed to know all concrete implementations.

---

## 5. Behavioral Configurability Model (Methods Included)

## 5.1 What UI can configure

1. Attribute values (speed, sensor radius, carry capacity, battery, etc.).
2. Method chain selection by behavior name from a curated registry.
3. Method parameters per behavior component.
4. Activation order for behavior chain.

## 5.2 What UI cannot configure

1. Raw Python code.
2. New executable method definitions at runtime.
3. Unregistered behavior names.

## 5.3 Behavior Spec (v1 DSL shape)

```json
{
  "agent_type": "ant_worker",
  "attributes": {
    "max_speed": 1.2,
    "sensor_radius": 8.0,
    "carry_capacity": 1
  },
  "behavior_chain": [
    {"name": "search_food", "params": {"wander_sigma": 0.4}},
    {"name": "move_to_target", "params": {"arrival_radius": 0.8}},
    {"name": "pickup_food", "params": {}},
    {"name": "return_to_base", "params": {"drop_radius": 1.2}}
  ]
}
```

---

## 6. Simulation and Concurrency Contracts

## 6.1 Engine loop contract

1. Drain `cmd_queue` at tick boundary.
2. Advance state by one deterministic tick.
3. Push snapshot or delta event to `pub_queue` according to stream cadence.
4. Send errors as structured events, not crashes.

## 6.2 Queue model

1. `cmd_queue`: UI/API to engine commands (`play`, `pause`, `step`, `seek`, `reset`, `set_speed`).
2. `pub_queue`: engine to adapter state events (`snapshot`, `metric`, `error`, `lifecycle`).

## 6.3 Rewind

1. Full snapshot every `N` ticks (default 10).
2. Bounded ring buffer capacity `K` snapshots (default 1000).
3. Rewind to tick `t` = nearest snapshot before `t` + deterministic replay.

Note: eviction is FIFO by time. LRU is not used because rewind is temporal.

---

## 7. Minimal Interface Baseline (v1)

`RendererPort`:

1. `render(snapshot) -> None`
2. `capture_screenshot(path) -> Path`

`PersistencePort`:

1. `save_run(manifest, snapshots) -> RunId`
2. `load_run(run_id) -> LoadedRun`

`BehaviorProtocol`:

1. `sense(agent, state) -> Perception`
2. `decide(perception, rng) -> Decision`
3. `act(agent, decision, state) -> AgentUpdate`

---

## 8. Testing and Quality Gates

| Gate | Required Test | Pass Condition |
|---|---|---|
| G1 | Unit tests (`core`, `contracts`, `scenarios`) | Core logic correctness for module internals |
| G2 | Contract conformance tests | Concrete adapters satisfy `Protocol` signatures/semantics |
| G3 | Determinism test | Same seed + same commands + same scenario = same state hash at tick N |
| G4 | Schema validation test | Invalid attribute/method specs rejected with actionable messages |
| G5 | Rewind correctness test | Rewound-then-replayed state hash matches forward-only run at same tick |
| G6 | Error isolation test | One crashing agent does not terminate simulation loop |

---

## 9. 12-Week Implementation Plan

| Phase | Weeks | Deliverables | Exit Criteria |
|---|---|---|---|
| P1 Foundation | 1-2 | contracts, validators, test harness | G1/G2 scaffolding green |
| P2 Core | 3-4 | engine, physics, history, deterministic tick loop | G1/G3/G5 green headless |
| P3 Ant Scenario | 5-6 | ants_foraging scenario + behavior library v1 | 100 ants, 500 ticks stable |
| P4 API + Rendering | 7-8 | FastAPI WS + PixiJS + basic controls | End-to-end demo ready (passing-grade line) |
| P5 Full UX | 9-10 | agent designer, rewind timeline, export | G4/G6 + operator workflow complete |
| P6 Packaging + Generality | 11-12 | pywebview desktop + drone scenario + thesis assets | second projection proven |

---

## 10. Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Over-design before runnable core | Medium | High | Freeze D1-D15 and defer new abstractions until second implementation exists |
| UI latency under load | Medium | High | Queue decoupling + stream throttling + profiling checkpoints |
| Nondeterminism regressions | Medium | High | Determinism test mandatory in CI |
| Schema complexity growth | Medium | Medium | Keep behavior DSL minimal and versioned |
| Time overrun in UX polish | High | Medium | Protect P4 milestone first |

---

## 11. Definition of Done (TFG-Ready v1)

Project is considered "ready for thesis defense" when all are true:

1. All mandatory gates G1-G6 pass.
2. Ant scenario runs headless and via UI with rewind.
3. One additional non-ant scenario runs with same core.
4. Desktop build (pywebview) and web mode both demonstrable.
5. Traceability matrix (see `07_tfg_evidence_matrix.md`) is complete with evidence links.

