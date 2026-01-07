"""Strategic override constraints."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OverrideType(str, Enum):
    TOOL_BUDGET = "TOOL_BUDGET"
    FORCE_ACTION = "FORCE_ACTION"
    WIDEN_RETRIEVAL = "WIDEN_RETRIEVAL"


@dataclass(frozen=True)
class StrategicOverride:
    override_id: str
    run_id: str
    override_type: OverrideType
    constraints: dict[str, object]
    expires_at: datetime | None = None

    def is_expired(self, now: datetime) -> bool:
        if self.expires_at is None:
            return False
        return now >= self.expires_at
