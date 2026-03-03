# Audit Report: Three Proposals for a Modular Multi-Agent Simulation Framework

**Date:** 2026-03-03
**Context:** Leire Goikoetxea's TFG — ant foraging simulation as first projection of a generic agent-based modelling platform
**Proposals audited:** 01_analysis_claude.md (Claude), 02_analysis_googlestudio.md (Google Studio), 03_analysis_chatgpt.md (ChatGPT)
**Method:** First Principles decomposition, IterativeDepth multi-angle audit (5 lenses), Council debate (4 experts, 3 rounds)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Original Requirements Recap](#2-original-requirements-recap)
3. [Individual Proposal Audits](#3-individual-proposal-audits)
   - 3.1 Proposal 01 — Claude
   - 3.2 Proposal 02 — Google Studio
   - 3.3 Proposal 03 — ChatGPT
4. [Cross-Comparison Matrix](#4-cross-comparison-matrix)
5. [What ALL Three Miss](#5-what-all-three-miss)
6. [The Unified Optimal Proposal](#6-the-unified-optimal-proposal)
7. [Recommended Development Roadmap](#7-recommended-development-roadmap)
8. [Conclusion](#8-conclusion)

---

## 1. Executive Summary

Three AI systems produced architectural proposals from the same prompt requesting a modular, multi-agent simulation framework in Python. Each brings genuine strengths and significant gaps:

- **Proposal 01 (Claude)** is the most pragmatic and implementable — clean layering, concrete tech stack, prioritized features, and an excellent scenario mapping table. But it lacks architectural formalism, ignores the rewind requirement, and underspecifies testing.
- **Proposal 02 (Google Studio)** is the most architecturally ambitious — ECS, Event Sourcing, Behavior Trees, Taichi GPU physics. Several genuinely valuable ideas, but the technology complexity (Tauri, Taichi, React, ECS) makes it impractical for a TFG. Module granularity is too coarse and testing is absent.
- **Proposal 03 (ChatGPT)** is the most academically rigorous — Hexagonal architecture, 4-type testing strategy, plugin system, Module Charters, academic references. But it suffers from analysis paralysis (3 tech options, no recommendation), over-specified governance, and lacks a concrete scenario mapping.

**The optimal path:** Take Proposal 01's practical skeleton, add Proposal 03's testing rigor and academic grounding, incorporate Proposal 02's snapshot-based rewind idea (simplified), and include the best unique innovations from each.

---

## 2. Original Requirements Recap

From `00_prompt.md`, the hard requirements (non-negotiable):

| # | Requirement | Source Quote |
|---|------------|-------------|
| R1 | **Strict modularity** — each module independent, contracts only | "this modular construction idea is compulsory" |
| R2 | **Per-module testing** | "tests should be done per module" |
| R3 | **Configurable agents** — class attributes and functions via UI | "classes should be completely configurable" |
| R4 | **Configurable physics** — movement and interaction parameters | "physics of the movements...completely configurable" |
| R5 | **Multiple scenarios** — ants, drones for storm/fire | "should not be the only one" |
| R6 | **Modern professional UI** with controls | "modern, professional and performant" |
| R7 | **Simulation controls** — stop, forward, backward, pause, reset, screenshots, save | Explicit list in prompt |
| R8 | **Python** | "I want python" |
| R9 | **Desktop (Linux) + Web** deployment | "app for linux-like os, and as a web-like app" |
| R10 | **Orchestrator** to manage modules and contracts | "orchestrator skill to keep track" |

---

## 3. Individual Proposal Audits

### 3.1 Proposal 01 — Claude

#### Architecture: Layered (6 layers)

```
Layer 0: Domain (Pydantic models)
Layer 1: Simulation Core (engine, physics, behaviors, signals, environment)
Layer 2: Scenario/Agent Configuration (agents factory, scenarios, swarm)
Layer 3: Infrastructure (persistence, api, events)
Layer 4: Presentation (renderer, ui)
Layer 5: Orchestrator (registry, wiring, lifecycle)
```

#### Strengths

| # | Strength | Why It Matters |
|---|----------|---------------|
| S1 | **Scenario mapping table** — most practically useful artifact across all three proposals | Immediately shows how ants/drones/fire map to the same abstractions (Agent→Ant/Drone, Colony→Anthill/Station, Signal→Pheromone/Radio). This is the clearest proof that the architecture supports multiple projections |
| S2 | **Prioritized feature list** (17 items, ordered) | The only proposal that acknowledges time constraints. "Must-have" vs "High value" vs "Advanced" categorization is essential for a TFG |
| S3 | **Concrete tech stack** — FastAPI + PixiJS + PyWebView | No ambiguity. One recommendation, well-justified. Smallest viable stack that satisfies all deployment requirements |
| S4 | **Sequential development roadmap** (9 steps) | Actionable: domain models → protocols → engine → API → renderer → scenario → UI → persistence → packaging |
| S5 | **Agent schema factory** — JSON/YAML → dynamic class generation | Elegant approach: the UI writes/reads schemas, the factory builds agent instances. Clean separation of configuration from implementation |
| S6 | **Event bus for decoupling** | Correct instinct — modules communicate via events, not direct calls |

#### Weaknesses

| # | Weakness | Impact |
|---|----------|--------|
| W1 | **Rewind/backward NOT addressed** | R7 explicitly requires "backwarding". This is an architectural decision (state storage strategy), not just a UI button. Critical gap |
| W2 | **Testing strategy underspecified** | "Test independently" is stated but no concrete strategy (what types of tests, how to test contracts, determinism) |
| W3 | **No formal dependency rule** | Layers imply direction but it's not stated that "lower layers must never import upper layers" |
| W4 | **Event bus not detailed** | Mentioned once, never specified. What events? What format? Sync or async? |
| W5 | **No academic references** | For a TFG thesis document, architectural decisions need citations |
| W6 | **12 modules may be too many for v1** | `domain`, `engine`, `physics`, `behaviors`, `signals`, `environment`, `agents`, `scenarios`, `swarm`, `persistence`, `api`, `events`, `renderer`, `ui`, `orchestrator` — 15 modules total. Ambitious for a first implementation |

#### Requirement Coverage: 9/10

Missing: R7 rewind/backward (not addressed at all)

#### TFG Feasibility: 7/10

Most implementable of the three. Reasonable tech stack, clear roadmap. Could deliver a working v1 within a term if the module count is reduced.

---

### 3.2 Proposal 02 — Google Studio

#### Architecture: Entity-Component-System (ECS) + Event Sourcing

```
Module A: Orchestrator (state & contract manager)
Module B: Simulation Engine (world, ECS loop, spatial environment)
Module C: Dynamic Agent Generator (metaprogramming from UI config)
Module D: Frontend GUI (renders shapes, no domain knowledge)
```

#### Strengths

| # | Strength | Why It Matters |
|---|----------|---------------|
| S1 | **ECS pattern for composable agents** | Entities = just IDs, Components = data, Systems = logic. This achieves maximum agent configurability — add/remove components without changing agent "classes" |
| S2 | **Event Sourcing for rewind** | Store state snapshots/deltas per tick → rewind is just scrubbing through an array. The only proposal that solves R7 architecturally from the start |
| S3 | **Behavior Trees for configurable logic** | Genuinely innovative: UI allows chaining logic nodes (`[If Sensing Food] → [Move to Food] → [Pick up Food]`). More powerful than simple parameter configuration |
| S4 | **Taichi for GPU-accelerated physics** | For very large agent populations (>10K), this would provide a real performance advantage |
| S5 | **Frontend knows nothing about domain** | "It only knows how to render shapes, colors, and coordinates" — this is the correct abstraction for a multi-scenario system |
| S6 | **"Skill" metaphor for development phases** | Aligns with the prompt's idea of "one skill per module" |

#### Weaknesses

| # | Weakness | Impact |
|---|----------|--------|
| W1 | **Tauri requires Rust toolchain** | Adding Rust to a Python TFG project is a massive complexity burden. PyWebView achieves the same desktop packaging with zero additional toolchain |
| W2 | **Only 4 macro-modules** — far too coarse | "Simulation Engine" bundles spatial environment, time-stepping, and ECS loop into one module. "Dynamic Agent Generator" conflates configuration parsing with metaprogramming. This violates the prompt's strict modularity |
| W3 | **No testing strategy at all** | R2 explicitly requires per-module testing. This proposal doesn't mention testing once |
| W4 | **ECS is from game dev, not ABM** | ECS optimizes for cache coherence with millions of entities. Python ABM with <10K agents doesn't need this. Standard OOP with component composition achieves the same configurability without the paradigm shift |
| W5 | **Metaprogramming in Dynamic Agent Generator** | "Dynamically generates Agent classes" via metaprogramming = runtime code generation. This makes debugging extremely difficult, type checking impossible, and IDE support broken |
| W6 | **No plugin system for scenarios** | Adding a new scenario requires understanding the entire system. No mechanism for discoverable, drop-in scenarios |
| W7 | **Taichi is a heavy dependency** | Requires GPU/CUDA setup. For a TFG, NumPy vectorization handles typical ABM scales |
| W8 | **React/Vue frontend = separate JS codebase** | The student must now maintain Python + Rust (Tauri) + JavaScript (React/Vue). Three ecosystems |
| W9 | **No feature prioritization** | No "must-have" vs "nice-to-have" distinction. Everything is presented as necessary |
| W10 | **No academic references** | Same gap as Proposal 01 |

#### Requirement Coverage: 7.5/10

Excellent on: R7 (rewind via Event Sourcing), R3 (agent configurability via ECS+BT)
Missing/Weak on: R2 (testing), R5 (scenario system underspecified), R1 (only 4 modules is not "strict modularity")

#### TFG Feasibility: 4/10

The technology stack alone (Python + Rust + JavaScript + Taichi + ECS paradigm) makes this impractical for a one-term TFG. Many genuinely good ideas, but the implementation complexity is prohibitive.

---

### 3.3 Proposal 03 — ChatGPT

#### Architecture: Hexagonal / Clean Architecture (Ports + Adapters)

```
Core (pure, headless):
  sim_state, sim_kernel, agent_model, environment_model, physics_rules, logging_observability

Ports (stable interfaces):
  RendererPort, PersistencePort, ScenarioPort, ControlPort, StreamingPort

Adapters (replaceable implementations):
  Desktop UI, Web UI, Storage, Export

Orchestrator (composition root):
  Selects adapters, loads plugins, validates configs, starts everything
```

#### Strengths

| # | Strength | Why It Matters |
|---|----------|---------------|
| S1 | **Most rigorous architectural formalism** | Hexagonal architecture with explicit dependency rule ("dependencies point inward"), named ports, and adapter swappability. The modularity is not just stated — it's enforced by the pattern |
| S2 | **4-type testing strategy** | Contract tests (does impl satisfy Protocol?), determinism tests (same seed → same result), property-based tests (invariants), performance regression tests. The only proposal that makes R2 concrete |
| S3 | **Plugin system via Python entry_points** | Real, standard mechanism for discoverable scenario packages. `scenario_ants_foraging/`, `scenario_drone_storm/` as separate installable packages |
| S4 | **Module Charter concept** | Per-module governance: purpose, ports, invariants, test obligations, performance budget. Excellent documentation discipline |
| S5 | **Hybrid rewind mechanism** | Checkpoints + replay, isolated in a `HistoryPort`. Storage strategy changeable without touching UI or kernel |
| S6 | **Academic references** | Parnas (information hiding), Clean Architecture, Mesa ABM, PEP 544 (Protocols), JSON Schema. Strengthens the TFG thesis |
| S7 | **Configuration validation** | Pydantic + JSON Schema for runtime validation. The only proposal that addresses "what happens when configuration is invalid" |
| S8 | **Logging/observability as core submodule** | Events, metrics, traces — essential for debugging simulations |
| S9 | **Concrete first milestone** | "Smallest vertical slice that still satisfies modularity doctrine" — contracts + kernel + one scenario + one UI + history + contract tests |

#### Weaknesses

| # | Weakness | Impact |
|---|----------|--------|
| W1 | **Three tech options, no firm recommendation** | Option A (FastAPI+JS), Option B (PySide6/QML), Option C (NiceGUI). The "pragmatic recommendation" paragraph hedges between all three. A TFG student needs ONE answer |
| W2 | **No scenario mapping table** | Unlike Proposal 01, there's no concrete visualization of how ants/drones/fire map to the same abstractions |
| W3 | **6 core submodules + 5 ports may be too many interfaces** | That's 11+ Protocol definitions to write and maintain before a single agent moves. Interface fatigue |
| W4 | **Module Charter is heavy governance for a TFG** | Writing a formal charter per module (purpose, non-goals, public ports, invariants, test obligations, perf budget, compatibility rules) for 8+ modules is weeks of work before coding starts |
| W5 | **entry_points requires packaging infrastructure** | `setup.py` or `pyproject.toml` with entry_point declarations, `importlib.metadata` for discovery. Additional complexity vs. a simple importable module registry |
| W6 | **No feature prioritization** | Like Proposal 02, everything is presented as equally important. No guidance on what to build first vs. defer |
| W7 | **Verbose** — 316 lines, 17 references | Academic thoroughness becomes information overload. The student must extract the actionable plan from dense prose |
| W8 | **No concrete agent configuration mechanism** | Mentions "component system" and "composition strategy" but doesn't specify how the UI drives agent creation (no schema factory, no BT, no concrete approach) |

#### Requirement Coverage: 10/10

The only proposal that addresses every requirement from the prompt, including rewind (HistoryPort), testing (4 types), and scenario extensibility (plugins).

#### TFG Feasibility: 5/10

Academically outstanding, but the governance overhead (Module Charters, entry_points, 5 ports, 6 core submodules) would consume significant time before any code runs. Needs simplification to be implementable in one term.

---

## 4. Cross-Comparison Matrix

### Architecture

| Dimension | P01 (Claude) | P02 (Google Studio) | P03 (ChatGPT) | Winner |
|-----------|:---:|:---:|:---:|:---:|
| Pattern | Layered (6) | ECS + Event Sourcing | Hexagonal (Ports+Adapters) | **P01** — simplest that works |
| Dependency rule | Implied by layers | Not stated | Explicit ("inward") | **P03** — formal is better |
| Module count | ~15 | 4 | ~11+ | **P01** — closest to right (needs reduction) |
| Contract mechanism | Python Protocols | Protocols/ABC | Python Protocols + Pydantic | **P03** — most complete |
| Scenario extensibility | Mapping table | Implied | Plugin entry_points | **P03** — real mechanism |

### Technology Stack

| Dimension | P01 (Claude) | P02 (Google Studio) | P03 (ChatGPT) | Winner |
|-----------|:---:|:---:|:---:|:---:|
| Backend | FastAPI + WebSocket | FastAPI + WebSocket | FastAPI + WebSocket | **Tie** — all agree |
| Frontend rendering | PixiJS | PixiJS/Three.js + React/Vue | Depends on option | **P01** — decisive |
| Desktop packaging | PyWebView | Tauri (Rust) | PyWebView or PySide6 | **P01** — simplest |
| Physics acceleration | Not specified | Taichi (GPU) | Not specified | **P02** — but overkill for TFG |
| Data validation | Pydantic | Pydantic | Pydantic + JSON Schema | **P03** — most rigorous |
| Languages required | Python + JS | Python + Rust + JS | Python + JS (Option A) | **P01** — minimal |

### Modularity & Testing

| Dimension | P01 (Claude) | P02 (Google Studio) | P03 (ChatGPT) | Winner |
|-----------|:---:|:---:|:---:|:---:|
| Testing strategy | "Test per module" (vague) | Not mentioned | 4-type strategy | **P03** — comprehensive |
| Contract enforcement | Protocols | Protocols/ABC | Protocols + conformance tests | **P03** — tested contracts |
| Determinism | Not addressed | Implied by Event Sourcing | Explicit (seed + hash) | **P03** — explicit |
| Configuration validation | Not addressed | Not addressed | Pydantic + JSON Schema | **P03** — only one |

### Agent Configuration

| Dimension | P01 (Claude) | P02 (Google Studio) | P03 (ChatGPT) | Winner |
|-----------|:---:|:---:|:---:|:---:|
| Mechanism | JSON schema → factory | ECS components + metaprogramming | Component system (vague) | **P01** — most concrete |
| Behavior configurability | Pluggable strategies | Behavior Trees (UI-chainable) | Not specified | **P02** — most powerful |
| UI integration | Schema = UI data | UI generates config JSON | Not specified | **P01/P02** — tie |

### Rewind/History

| Dimension | P01 (Claude) | P02 (Google Studio) | P03 (ChatGPT) | Winner |
|-----------|:---:|:---:|:---:|:---:|
| Strategy | Not addressed | Full Event Sourcing | Hybrid checkpoints + replay | **P03** — practical balance |
| Isolation | N/A | Part of engine | HistoryPort (swappable) | **P03** — modular |
| Memory management | N/A | Not addressed | Not addressed | **None** — all miss this |

### Practicality

| Dimension | P01 (Claude) | P02 (Google Studio) | P03 (ChatGPT) | Winner |
|-----------|:---:|:---:|:---:|:---:|
| Feature prioritization | 17 items, ordered | None | None | **P01** — essential for TFG |
| Development roadmap | 9 concrete steps | 5 phases (high level) | First milestone defined | **P01** — most actionable |
| Academic references | None | None | 11 references | **P03** — thesis value |
| TFG feasibility | 7/10 | 4/10 | 5/10 | **P01** — most buildable |

---

## 5. What ALL Three Miss

These gaps exist in every proposal and must be addressed in the unified version:

| # | Missing Element | Impact |
|---|----------------|--------|
| G1 | **Concurrency model** — how does the simulation tick loop coexist with the API server without blocking? | Will cause UI freezes when simulation is heavy. Needs: async event loop or separate process/thread for simulation |
| G2 | **Memory budget for state history** — rewind stores snapshots, but how many? What eviction policy? | Unbounded memory growth. Needs: max snapshot count or time window, LRU eviction |
| G3 | **Performance targets** — how many agents at what framerate? | No way to know if the architecture is adequate. Needs: target like "1000 agents at 30 fps rendering + 60 ticks/sec simulation" |
| G4 | **Error handling for user-configured behaviors** — what if a configured agent behavior crashes mid-tick? | Simulation crashes entirely. Needs: per-agent error isolation (try/except per agent step, log error, skip agent) |
| G5 | **UI accessibility** — keyboard navigation, color contrast, screen reader basics | Not critical for a TFG but worth noting as a professional gap |
| G6 | **Internationalization** — the prompt author writes in Basque/Spanish context | Not critical, but UI strings should be externalizable |

---

## 6. The Unified Optimal Proposal

### 6.1 Architectural Pattern

**Layered architecture with explicit dependency rule**, taking the practical layering from Proposal 01 and the formal dependency governance from Proposal 03.

**Rule:** Dependencies point inward. Core simulation modules never import infrastructure, API, or UI code. The orchestrator is the only module that knows all concrete implementations.

This is NOT full Hexagonal (no need for 5 named ports) and NOT ECS (unnecessary paradigm shift for Python ABM). It's clean layering with Python Protocol contracts at each module boundary — the simplest pattern that satisfies the strict modularity requirement.

### 6.2 Module Map (8 modules for v1)

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                              │
│         (composition root — the only module that             │
│          knows all concrete implementations)                 │
├─────────────────────────────────────────────────────────────┤
│  LAYER 3: PRESENTATION + INFRASTRUCTURE                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  api          │  │  renderer    │  │  persistence │      │
│  │  (FastAPI +   │  │  (PixiJS     │  │  (save/load  │      │
│  │   WebSocket)  │  │   frontend)  │  │   snapshots) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: SCENARIO + AGENT CONFIGURATION                    │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │  scenarios    │  │  agents      │                         │
│  │  (registry +  │  │  (schema     │                         │
│  │   projections)│  │   factory +  │                         │
│  │              │  │   behaviors) │                         │
│  └──────────────┘  └──────────────┘                         │
├─────────────────────────────────────────────────────────────┤
│  LAYER 1: SIMULATION CORE                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  engine       │  │  physics     │  │  history     │      │
│  │  (tick loop,  │  │  (movement,  │  │  (snapshots, │      │
│  │   scheduling, │  │   collision, │  │   rewind,    │      │
│  │   signals)    │  │   forces)    │  │   replay)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│  LAYER 0: DOMAIN (pure data, no logic)                      │
│  ┌──────────────────────────────────────────────────┐       │
│  │  domain                                           │       │
│  │  (Agent, Environment, Colony, Food, Signal,       │       │
│  │   SimulationState — all Pydantic models)          │       │
│  └──────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

**9 modules total** (including orchestrator). Each has:
- One Python Protocol defining its public interface
- One Pydantic model (or set of models) defining its data contracts
- A docstring charter: purpose, contract, invariants (lightweight version of P03's Module Charter)

### 6.3 Technology Stack

| Component | Choice | Justification |
|-----------|--------|---------------|
| **Language** | Python 3.11+ | Prompt requirement |
| **Data models** | Pydantic v2 | Runtime validation, serialization, schema generation (from P01/P03) |
| **Contracts** | Python `Protocol` (PEP 544) | Structural subtyping without inheritance coupling (all three agree) |
| **Backend API** | FastAPI + WebSocket | Real-time state streaming to frontend (all three agree) |
| **Frontend rendering** | PixiJS (WebGL/Canvas) | 60fps capable with thousands of agents (from P01/P02) |
| **Frontend UI** | Vanilla JS or lightweight framework | Simulation controls, agent config panels |
| **Desktop packaging** | PyWebView | Wraps the web UI as a native Linux/Mac/Windows app (from P01) |
| **Physics computation** | NumPy vectorization | Sufficient for <10K agents, no GPU dependency (practical choice) |
| **Testing** | pytest + hypothesis | Unit tests, contract conformance, property-based (from P03) |
| **Serialization** | JSON (config) + msgpack (snapshots) | Human-readable config, efficient binary snapshots |

### 6.4 Agent Configuration System

Synthesized from P01's schema factory and P02's composable behavior idea:

1. **Agent schemas** defined in JSON/YAML — attributes (speed, sensor_radius, carrying_capacity, etc.) and behavior assignment
2. **Agent factory** (from P01) reads schemas and constructs agent instances with the correct attributes and behavior objects
3. **Behaviors as pluggable strategy objects** — not full Behavior Trees (too complex for v1), but composable rule chains configurable via the UI:
   - Each behavior is a Python class implementing a `BehaviorProtocol` (sense → decide → act)
   - Behaviors can be chained: `[SearchFood, MoveToFood, PickupFood, ReturnToColony]`
   - The chain is configurable per agent type via the schema
4. **The UI's Agent Designer panel** reads/writes these schemas — it is literally editing the JSON that the factory consumes

### 6.5 Scenario System

Synthesized from P01's mapping table and P03's plugin concept (simplified):

**Scenario mapping table** (from P01 — the most useful artifact):

| Abstract Concept | Ants | Storm Drones | Fire Drones |
|-----------------|------|--------------|-------------|
| Agent | Ant | Drone | Drone |
| Base | Anthill | Ground station | Command post |
| Target | Food source | Storm cell | Fire front |
| Signal | Pheromone trail | Radio/telemetry | Thermal map |
| Task | Food pickup + return | Data collection + uplink | Observation + report |
| Obstacle | Rock, water | No-fly zone | Smoke, terrain |
| Emergent behavior | Trail formation | Swarm coverage | Fire perimeter mapping |

**Scenario as importable package** (simplified from P03):
- Each scenario is a Python module in `scenarios/` with a standard interface
- A `ScenarioRegistry` dict maps scenario names to their modules
- Adding a new scenario = adding a new module and registering it
- No `entry_points` complexity — just importable modules with a standard `ScenarioProtocol`

### 6.6 Rewind/History Mechanism

Synthesized from P02's Event Sourcing idea and P03's HistoryPort:

- **Periodic snapshots** — every N ticks (configurable, default: every 10 ticks), serialize the full `SimulationState` to a snapshot
- **Rewind** = load the nearest snapshot before the target tick, then replay forward to the exact tick
- **Memory management** — maximum snapshot buffer size (e.g., 1000 snapshots). Oldest snapshots evicted when buffer is full (addresses gap G2)
- **Isolated in the `history` module** — engine calls `history.snapshot(state)` at tick boundaries. Rewind goes through `history.rewind(target_tick)`. Storage strategy is changeable without touching engine or UI

### 6.7 Testing Strategy

Directly from P03, simplified to 3 mandatory types:

| Test Type | Purpose | Example |
|-----------|---------|---------|
| **Unit tests** | Internal module logic | `physics.apply_movement()` moves agent by velocity * dt |
| **Contract conformance tests** | Does implementation satisfy its Protocol? | `AntScenario` satisfies `ScenarioProtocol` — has all required methods with correct signatures |
| **Determinism tests** | Same seed → same result | Seed 42 + ant scenario + 100 ticks → state hash `0xABCDEF` |

Optional (time permitting):
- Property-based tests (hypothesis): "no agent moves outside boundaries", "food count is conserved unless eaten"
- Performance regression: "1000 agents complete 100 ticks in <2 seconds"

### 6.8 Concurrency Model (Addresses Gap G1)

- **Simulation runs in a separate thread** (or `asyncio` task with periodic yields)
- **FastAPI serves the frontend** in the main async loop
- **WebSocket pushes state snapshots** at the rendering framerate (e.g., 30fps), while the simulation may tick faster internally
- **Control commands** (play/pause/step/rewind) go from frontend → WebSocket → engine control queue

### 6.9 Academic References for the Thesis (from P03)

| Reference | Relevant For |
|-----------|-------------|
| Parnas, D.L. "On the Criteria To Be Used in Decomposing Systems into Modules" (1972) | Justifying the modular architecture |
| Martin, R.C. "The Clean Architecture" (2012) | The dependency rule ("dependencies point inward") |
| PEP 544 — Protocols: Structural subtyping | Python contract mechanism choice |
| Mesa ABM framework | Reference point for agent-based modelling in Python |
| Wilensky & Rand, "An Introduction to Agent-Based Modeling" (2015) | ABM theory and methodology |

---

## 7. Recommended Development Roadmap

Adapted from P01's practical roadmap, with P03's "smallest vertical slice" principle:

### Phase 1 — Foundation (Week 1-2)
1. Define all Pydantic domain models (Layer 0)
2. Define all Python Protocols (one per module boundary)
3. Write contract conformance test stubs for each Protocol
4. Set up pytest infrastructure

### Phase 2 — Core Engine (Week 3-4)
5. Implement `engine` module — tick loop, scheduling, signal diffusion/decay
6. Implement `physics` module — movement, collision, boundary enforcement
7. Implement `history` module — snapshot storage, rewind, replay
8. Determinism test: fixed seed → fixed state hash at tick N

### Phase 3 — First Scenario (Week 5-6)
9. Implement `agents` module — schema factory, behavior strategies
10. Implement `scenarios` module — ant foraging as first projection
11. Headless integration test: 100 ants, 5 food sources, 500 ticks, verify emergence

### Phase 4 — API + Rendering (Week 7-8)
12. Implement `api` module — FastAPI + WebSocket state streaming
13. Implement `renderer` — PixiJS canvas rendering agents/food/signals
14. Basic UI controls: play, pause, step, reset, speed slider

### Phase 5 — Full UI + Features (Week 9-10)
15. Agent Designer panel (read/write agent schemas)
16. Scenario selector (choose ant/drone scenarios)
17. Rewind controls (timeline scrubber using history module)
18. Screenshot export, simulation save/load

### Phase 6 — Desktop Packaging + Second Scenario (Week 11-12)
19. PyWebView packaging for Linux desktop app
20. Second scenario: drone storm hunting (proves generality)
21. Final testing pass, documentation, thesis writing

### Feature Priority (from P01, refined)

**Must-have (v1):**
1. Domain models and Protocol contracts
2. Tick loop engine with deterministic stepping
3. Physics module (movement, boundaries)
4. Ant foraging scenario
5. FastAPI + WebSocket API
6. PixiJS renderer with basic controls (play/pause/step/reset)
7. State snapshot history with rewind
8. Per-module contract tests

**High value (v1.1):**
9. Agent schema factory with UI designer panel
10. Scenario registry with second scenario (drones)
11. Signal field module (pheromone diffusion/decay)
12. Screenshot and simulation export

**Advanced (v2, if time permits):**
13. PyWebView desktop packaging
14. Live parameter tuning mid-simulation
15. Metrics dashboard (emergence metrics plots)
16. Agent inspector (click agent, see internal state)

---

## 8. Conclusion

### Score Card

| Dimension | P01 (Claude) | P02 (Google Studio) | P03 (ChatGPT) | Unified |
|-----------|:---:|:---:|:---:|:---:|
| Architecture rigor | 6/10 | 7/10 | 9/10 | 8/10 |
| Technology pragmatism | 9/10 | 4/10 | 6/10 | 9/10 |
| Requirement coverage | 9/10 | 7.5/10 | 10/10 | 10/10 |
| Testing strategy | 4/10 | 1/10 | 9/10 | 8/10 |
| TFG feasibility | 7/10 | 4/10 | 5/10 | 8/10 |
| Feature prioritization | 9/10 | 2/10 | 4/10 | 9/10 |
| Academic value (thesis) | 3/10 | 3/10 | 9/10 | 8/10 |
| Innovation | 6/10 | 8/10 | 7/10 | 7/10 |
| **Overall** | **6.6/10** | **4.6/10** | **7.4/10** | **8.4/10** |

### What Each Proposal Contributed to the Unified Version

- **From P01 (Claude):** Practical layered architecture, concrete tech stack (FastAPI+PixiJS+PyWebView), scenario mapping table, agent schema factory, prioritized feature list, development roadmap
- **From P02 (Google Studio):** Snapshot-based state history for rewind (simplified from Event Sourcing), composable behavior idea (simplified from Behavior Trees), frontend-knows-nothing principle
- **From P03 (ChatGPT):** Explicit dependency rule, 3-type testing strategy, academic references, configuration validation (Pydantic+JSON Schema), history module as isolated port, Module Charter concept (lightweight version), logging/observability awareness

### Final Recommendation

The unified proposal takes the **skeleton from Claude** (most buildable), the **rigor from ChatGPT** (most complete), and the **innovations from Google Studio** (most creative) — while deliberately discarding the over-engineering from each (ECS, Tauri, Taichi, full Hexagonal, Module Charters, entry_points).

The result is an 8-module framework with clear contracts, a concrete tech stack, a tested rewind mechanism, and a phased roadmap that can realistically be completed in one academic term.
