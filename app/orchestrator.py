"""Step orchestration state machine scaffold."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .memory import Event, EventType


class StepPhase(str, Enum):
    COMPILE = "COMPILE"
    PLAN = "PLAN"
    ACT = "ACT"
    OBSERVE = "OBSERVE"
    CHECKPOINT = "CHECKPOINT"
    EGRESS = "EGRESS"


@dataclass(frozen=True)
class StepState:
    run_id: str
    step_id: int
    phase: StepPhase


class Orchestrator:
    """Placeholder orchestrator for future step execution."""

    def __init__(self, state: StepState) -> None:
        self._state = state

    @property
    def state(self) -> StepState:
        return self._state

    def advance(self, next_phase: StepPhase) -> "Orchestrator":
        """Return a new orchestrator with the updated phase."""
        return Orchestrator(
            StepState(
                run_id=self._state.run_id,
                step_id=self._state.step_id,
                phase=next_phase,
            )
        )

    def emit_event(self, payload: dict[str, object]) -> Event:
        """Create a typed event for the current phase."""
        event_type = EventType(self._state.phase.value)
        return Event(
            run_id=self._state.run_id,
            step_id=self._state.step_id,
            event_type=event_type,
            payload=payload,
        )
