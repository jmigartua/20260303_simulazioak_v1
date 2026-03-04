from __future__ import annotations

import inspect
import threading
import time
from dataclasses import dataclass
from typing import Any

from pydantic import TypeAdapter

from sim_framework.app.runtime import RuntimeConfig, RuntimeMode, create_engine
from sim_framework.contracts.models import ControlCommand, PauseCommand, SimulationState
from sim_framework.core.environment import SignalGrid
from sim_framework.core.history import SnapshotHistory
from sim_framework.core.physics import WorldBounds
from sim_framework.scenarios.registry import get_scenario


_COMMAND_ADAPTER = TypeAdapter(ControlCommand)


@dataclass(frozen=True)
class BridgeConfig:
    scenario_name: str = "ants_foraging"
    agents: int = 40
    width: int = 30
    height: int = 30
    seed: int = 42
    boundary_mode: str = "clamp"
    runtime_mode: RuntimeMode = RuntimeMode.INTERACTIVE
    step_interval_s: float = 0.05


def _build_state_for_scenario(
    build_fn,
    *,
    scenario_name: str,
    agents: int,
    width: int,
    height: int,
    seed: int,
) -> SimulationState:
    signature = inspect.signature(build_fn)
    kwargs: dict[str, Any] = {"width": width, "height": height, "seed": seed}

    if "num_ants" in signature.parameters:
        kwargs["num_ants"] = agents
    elif "num_drones" in signature.parameters:
        kwargs["num_drones"] = agents
    elif "num_agents" in signature.parameters:
        kwargs["num_agents"] = agents
    else:
        raise ValueError(
            f"Scenario '{scenario_name}' does not expose a supported agent-count parameter "
            "(expected one of: num_ants, num_drones, num_agents)."
        )
    return build_fn(**kwargs)


def _create_runner_for_scenario(
    runner_factory,
    *,
    bounds: WorldBounds,
    signal_grid: SignalGrid,
    boundary_mode: str,
):
    signature = inspect.signature(runner_factory)
    kwargs = {"bounds": bounds, "signal_grid": signal_grid}
    if "boundary_mode" in signature.parameters:
        kwargs["boundary_mode"] = boundary_mode
    return runner_factory(**kwargs)


class WebRuntimeBridge:
    """Thread-safe runtime bridge used by the M1 web shell."""

    def __init__(self, config: BridgeConfig) -> None:
        self._config = config
        self._lock = threading.RLock()
        self._running = False
        self._thread: threading.Thread | None = None

        self._scenario: dict[str, Any] | None = None
        self._state: SimulationState | None = None
        self._initial_state: SimulationState | None = None
        self._engine = None
        self._history: SnapshotHistory | None = None
        self._runner = None
        self._signal_grid: SignalGrid | None = None
        self._bounds = WorldBounds(width=float(config.width), height=float(config.height))

        self._rebuild()

    def _rebuild(self) -> None:
        scenario = get_scenario(self._config.scenario_name)
        state = _build_state_for_scenario(
            scenario["build_initial_state"],
            scenario_name=self._config.scenario_name,
            agents=self._config.agents,
            width=self._config.width,
            height=self._config.height,
            seed=self._config.seed,
        )
        signal_grid = SignalGrid.from_config(state.signal_fields[0])
        runner = _create_runner_for_scenario(
            scenario["create_behavior_runner"],
            bounds=self._bounds,
            signal_grid=signal_grid,
            boundary_mode=self._config.boundary_mode,
        )
        engine = create_engine(
            seed=state.seed,
            runtime=RuntimeConfig(mode=self._config.runtime_mode),
        )
        history = SnapshotHistory(snapshot_every=1)
        history.snapshot(state, state.tick)

        # Start paused so browser controls drive execution.
        engine.enqueue_command(PauseCommand())
        state = engine.tick(state, runner, history=history)
        engine.drain_published_events()

        self._scenario = scenario
        self._initial_state = state.model_copy(deep=True)
        self._state = state
        self._signal_grid = signal_grid
        self._runner = runner
        self._engine = engine
        self._history = history

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=2.0)
            self._thread = None

    def _run_loop(self) -> None:
        while self._running:
            self.tick_once()
            time.sleep(self._config.step_interval_s)

    def tick_once(self) -> None:
        with self._lock:
            assert self._state is not None
            assert self._engine is not None
            assert self._history is not None
            assert self._runner is not None
            self._state = self._engine.tick(self._state, self._runner, history=self._history)
            self._engine.drain_published_events()

    def apply_command(self, payload: dict[str, Any]) -> None:
        kind = payload.get("kind")
        with self._lock:
            if kind == "reset":
                self._rebuild()
                return
            try:
                command = _COMMAND_ADAPTER.validate_python(payload)
            except Exception as exc:
                raise ValueError(f"Invalid command payload: {exc}") from exc
            assert self._engine is not None
            self._engine.enqueue_command(command)

    def state_payload(self) -> dict[str, Any]:
        with self._lock:
            assert self._state is not None
            assert self._engine is not None
            assert self._signal_grid is not None

            state = self._state
            return {
                "scenario": self._config.scenario_name,
                "tick": state.tick,
                "paused": self._engine.is_paused,
                "speed_multiplier": self._engine.speed_multiplier,
                "world": {"width": self._config.width, "height": self._config.height},
                "colony": {
                    "x": state.colony.position.x,
                    "y": state.colony.position.y,
                },
                "food_sources": [
                    {
                        "id": source.id,
                        "x": source.position.x,
                        "y": source.position.y,
                        "amount": source.amount,
                    }
                    for source in state.food_sources
                ],
                "agents": [
                    {
                        "id": agent.id,
                        "x": agent.position.x,
                        "y": agent.position.y,
                        "carrying": agent.carrying,
                        "state_label": agent.state_label,
                    }
                    for agent in state.agents
                ],
                "metrics": {
                    "agent_count": len(state.agents),
                    "carrying_agents": sum(1 for agent in state.agents if agent.carrying > 0),
                    "signal_total": self._signal_grid.total_signal(),
                },
            }
