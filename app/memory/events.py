"""Typed event definitions."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum


class EventType(str, Enum):
    COMPILE = "COMPILE"
    PLAN = "PLAN"
    ACT = "ACT"
    OBSERVE = "OBSERVE"
    CHECKPOINT = "CHECKPOINT"
    EGRESS = "EGRESS"


@dataclass(frozen=True)
class Event:
    run_id: str
    step_id: int
    event_type: EventType
    payload: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
