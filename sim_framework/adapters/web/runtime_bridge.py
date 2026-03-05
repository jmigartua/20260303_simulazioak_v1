from __future__ import annotations

import inspect
import threading
import time
from dataclasses import dataclass, replace
from typing import Any

from pydantic import TypeAdapter

from sim_framework.contracts.models import ControlCommand, PauseCommand, ResetCommand, SimulationState
from sim_framework.core.environment import SignalGrid
from sim_framework.core.history import SnapshotHistory
from sim_framework.core.physics import WorldBounds
from sim_framework.core.runtime import RuntimeConfig, RuntimeMode, create_engine
from sim_framework.scenarios.registry import get_scenario, list_scenarios


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
        self._max_tick_reached = 0

        self._rebuild()

    def _require_engine(self):
        if self._engine is None:
            raise RuntimeError("WebRuntimeBridge engine is not initialized")
        return self._engine

    def _require_state(self) -> SimulationState:
        if self._state is None:
            raise RuntimeError("WebRuntimeBridge state is not initialized")
        return self._state

    def _require_history(self) -> SnapshotHistory:
        if self._history is None:
            raise RuntimeError("WebRuntimeBridge history is not initialized")
        return self._history

    def _require_runner(self):
        if self._runner is None:
            raise RuntimeError("WebRuntimeBridge runner is not initialized")
        return self._runner

    def _require_signal_grid(self) -> SignalGrid:
        if self._signal_grid is None:
            raise RuntimeError("WebRuntimeBridge signal grid is not initialized")
        return self._signal_grid

    @property
    def available_scenarios(self) -> list[str]:
        return list_scenarios()

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
        state = engine.tick(
            state,
            runner,
            history=history,
            post_step_hook=self._evolve_signal_field,
        )
        engine.drain_published_events()

        self._scenario = scenario
        self._initial_state = state.model_copy(deep=True)
        self._state = state
        self._signal_grid = signal_grid
        self._runner = runner
        self._engine = engine
        self._history = history
        self._max_tick_reached = 0

    def switch_scenario(self, scenario_name: str) -> None:
        with self._lock:
            if scenario_name not in self.available_scenarios:
                raise ValueError(f"Unknown scenario: {scenario_name}")
            if scenario_name == self._config.scenario_name:
                return
            self._config = replace(self._config, scenario_name=scenario_name)
            self._rebuild()

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
            state = self._require_state()
            engine = self._require_engine()
            history = self._require_history()
            runner = self._require_runner()
            self._state = engine.tick(
                state,
                runner,
                history=history,
                post_step_hook=self._evolve_signal_field,
            )
            self._max_tick_reached = max(self._max_tick_reached, self._state.tick)
            engine.drain_published_events()

    def _evolve_signal_field(self) -> None:
        signal_grid = self._require_signal_grid()
        signal_grid.diffuse_step()
        signal_grid.decay_step()

    def apply_command(self, payload: dict[str, Any]) -> None:
        with self._lock:
            try:
                command = _COMMAND_ADAPTER.validate_python(payload)
            except Exception as exc:
                raise ValueError(f"Invalid command payload: {exc}") from exc
            if isinstance(command, ResetCommand):
                self._rebuild()
                return
            engine = self._require_engine()
            engine.enqueue_command(command)

    def state_payload(self) -> dict[str, Any]:
        with self._lock:
            state = self._require_state()
            engine = self._require_engine()
            signal_grid = self._require_signal_grid()

            signal_data = [row[:] for row in signal_grid.data]
            return {
                "scenario": self._config.scenario_name,
                "tick": state.tick,
                "paused": engine.is_paused,
                "speed_multiplier": engine.speed_multiplier,
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
                    "signal_total": signal_grid.total_signal(),
                },
                "timeline": {
                    "current_tick": state.tick,
                    "max_tick_reached": self._max_tick_reached,
                },
                "signal": {
                    "kind": signal_grid.kind,
                    "width": signal_grid.width,
                    "height": signal_grid.height,
                    "data": signal_data,
                },
            }

    def meta_payload(self) -> dict[str, Any]:
        with self._lock:
            target_tick_hz = 1.0 / self._config.step_interval_s
            return {
                "available_scenarios": self.available_scenarios,
                "current_scenario": self._config.scenario_name,
                "boundary_mode": self._config.boundary_mode,
                "runtime_mode": self._config.runtime_mode.value,
                "agents": self._config.agents,
                "step_interval_ms": int(self._config.step_interval_s * 1000),
                "target_tick_hz": round(target_tick_hz, 2),
            }
