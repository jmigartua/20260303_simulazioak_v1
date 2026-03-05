from __future__ import annotations

import random
from collections.abc import Callable, Mapping
from typing import Protocol, TypeAlias, runtime_checkable

from sim_framework.contracts.models import AgentState, SimulationState

Perception: TypeAlias = Mapping[str, object]
Decision: TypeAlias = Mapping[str, object]
BehaviorFactory: TypeAlias = Callable[[], "BehaviorProtocol"]


@runtime_checkable
class BehaviorProtocol(Protocol):
    def sense(self, agent: AgentState, state: SimulationState) -> Perception:
        ...

    def decide(self, perception: Perception, rng: random.Random) -> Decision:
        ...

    def act(
        self,
        agent: AgentState,
        decision: Decision,
        state: SimulationState,
    ) -> AgentState:
        ...


class BehaviorRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, BehaviorFactory] = {}

    def register(self, name: str, factory: BehaviorFactory) -> None:
        normalized = name.strip().lower()
        if not normalized:
            raise ValueError("Behavior name must be non-empty")
        if normalized in self._registry:
            raise ValueError(f"Behavior '{normalized}' is already registered")

        behavior = factory()
        if not isinstance(behavior, BehaviorProtocol):
            raise TypeError(
                f"Factory for '{normalized}' does not return a BehaviorProtocol"
            )

        self._registry[normalized] = factory

    def create(self, name: str) -> BehaviorProtocol:
        normalized = name.strip().lower()
        if normalized not in self._registry:
            raise KeyError(f"Unknown behavior '{normalized}'")
        return self._registry[normalized]()

    def exists(self, name: str) -> bool:
        return name.strip().lower() in self._registry

    def names(self) -> list[str]:
        return sorted(self._registry.keys())
