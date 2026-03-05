from __future__ import annotations

import random
from collections import deque
from collections.abc import Callable

from sim_framework.contracts.models import (
    AgentState,
    ControlCommand,
    ErrorEvent,
    LifecycleEvent,
    PauseCommand,
    PlayCommand,
    ResetCommand,
    SeekCommand,
    SetSpeedCommand,
    SimulationEvent,
    SimulationState,
    SnapshotEvent,
    StepCommand,
)
from sim_framework.contracts.ports import HistoryPort

BehaviorRunner = Callable[[AgentState, SimulationState, random.Random], AgentState]
PostStepHook = Callable[[], None]


class SimulationEngine:
    def __init__(self, seed: int = 42, *, emit_snapshot_events: bool = True) -> None:
        self._rng = random.Random(seed)
        self._command_queue: deque[ControlCommand] = deque()
        self._published_events: list[SimulationEvent] = []

        self._paused = False
        self._pending_steps = 0
        self._speed_multiplier = 1.0
        self._seek_target: int | None = None
        self._emit_snapshot_events = emit_snapshot_events

    @property
    def is_paused(self) -> bool:
        return self._paused

    @property
    def speed_multiplier(self) -> float:
        return self._speed_multiplier

    @property
    def emit_snapshot_events(self) -> bool:
        return self._emit_snapshot_events

    def enqueue_command(self, command: ControlCommand) -> None:
        self._command_queue.append(command)

    def drain_published_events(self) -> list[SimulationEvent]:
        out = self._published_events[:]
        self._published_events.clear()
        return out

    def _emit(self, event: SimulationEvent) -> None:
        self._published_events.append(event)

    def _drain_commands(self, tick: int) -> None:
        while self._command_queue:
            command = self._command_queue.popleft()

            if isinstance(command, PlayCommand):
                self._paused = False
                self._emit(LifecycleEvent(status="started", tick=tick))
            elif isinstance(command, PauseCommand):
                self._paused = True
                self._emit(LifecycleEvent(status="paused", tick=tick))
            elif isinstance(command, StepCommand):
                self._paused = True
                self._pending_steps += command.steps
            elif isinstance(command, SeekCommand):
                self._seek_target = command.tick
                self._paused = True
            elif isinstance(command, ResetCommand):
                self._paused = True
                self._pending_steps = 0
                self._seek_target = 0
                self._emit(LifecycleEvent(status="reset", tick=tick))
            elif isinstance(command, SetSpeedCommand):
                self._speed_multiplier = command.speed_multiplier

    def _advance_agents(
        self,
        state: SimulationState,
        behavior_runner: BehaviorRunner,
    ) -> list[AgentState]:
        updated_agents: list[AgentState] = []

        for agent in state.agents:
            try:
                updated = behavior_runner(agent, state, self._rng)
                updated_agents.append(updated)
            except Exception as exc:  # per-agent isolation by design
                self._emit(
                    ErrorEvent(
                        tick=state.tick,
                        message=str(exc) or exc.__class__.__name__,
                        agent_id=agent.id,
                    )
                )
                # Skip failed agent to keep the simulation running.
                continue

        return updated_agents

    def _run_single_step(
        self,
        state: SimulationState,
        behavior_runner: BehaviorRunner,
        history: HistoryPort | None,
        post_step_hook: PostStepHook | None,
    ) -> SimulationState:
        updated_agents = self._advance_agents(state, behavior_runner)
        if post_step_hook is not None:
            post_step_hook()
        # Avoid deep-copying all agents on every tick; only clone static topology
        # structures shallowly to keep state snapshots isolated between ticks.
        next_state = state.model_copy(
            update={
                "tick": state.tick + 1,
                "agents": updated_agents,
                "food_sources": [food.model_copy(deep=False) for food in state.food_sources],
                "colony": state.colony.model_copy(deep=False),
                "signal_fields": [
                    field.model_copy(deep=False) for field in state.signal_fields
                ],
            },
        )

        if history is not None:
            history.snapshot(next_state, next_state.tick)

        if self._emit_snapshot_events:
            self._emit(
                SnapshotEvent(
                    tick=next_state.tick,
                    state=next_state.model_copy(deep=True),
                )
            )
        return next_state

    def tick(
        self,
        state: SimulationState,
        behavior_runner: BehaviorRunner,
        history: HistoryPort | None = None,
        post_step_hook: PostStepHook | None = None,
    ) -> SimulationState:
        self._drain_commands(state.tick)

        if self._seek_target is not None:
            if history is not None:
                state = history.rewind(self._seek_target, state)
            else:
                self._emit(
                    ErrorEvent(
                        tick=state.tick,
                        message="SeekCommand requires history support",
                        agent_id=None,
                    )
                )
            self._seek_target = None

        can_advance = (not self._paused) or (self._pending_steps > 0)
        if not can_advance:
            return state

        if self._paused:
            steps_to_run = 1
        else:
            # Engine speed affects how many deterministic simulation steps are executed
            # per tick() call. Values in (0, 1) clamp to one step.
            steps_to_run = max(1, int(self._speed_multiplier))

        next_state = state
        for _ in range(steps_to_run):
            if self._pending_steps > 0:
                self._pending_steps -= 1
            next_state = self._run_single_step(
                next_state,
                behavior_runner,
                history,
                post_step_hook,
            )

        return next_state
