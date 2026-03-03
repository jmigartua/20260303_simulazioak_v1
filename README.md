# sim-framework

Modular multi-agent simulation framework for deterministic, headless experiments.

## What is included

- Contracts layer (`sim_framework/contracts`) with core domain models, ports, behavior protocol, and schema validators.
- Core runtime layer (`sim_framework/core`) with signal grid, history buffer, deterministic engine, and physics/spatial hash.
- Scenario layer (`sim_framework/scenarios`) with `ants_foraging` state-machine behavior.

## Local setup

```bash
uv venv --python 3.11
source .venv/bin/activate
uv pip install -e .[dev]
```

## Run tests

```bash
.venv/bin/python -m pytest -v
```

## Current status

- Deterministic engine loop and command handling implemented.
- Rewind/history snapshot support implemented.
- Ant foraging scenario runs headless and is covered by integration tests.
