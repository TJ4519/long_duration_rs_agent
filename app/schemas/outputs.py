"""Output schema definitions."""

from pydantic import BaseModel


class ResearchOutput(BaseModel):
    run_id: str
    summary: str
    citations: list[str]
