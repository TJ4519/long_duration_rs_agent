"""Output schema stubs."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ResearchOutput(BaseModel):
    """Minimal output schema placeholder."""

    summary: str = Field(..., description="Human-readable summary output.")
