"""Application configuration helpers."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str
    environment: str
    log_level: str


def get_settings() -> Settings:
    """Load settings from environment variables with safe defaults."""
    return Settings(
        app_name=os.getenv("ALEXANDRIA_APP_NAME", "Project Alexandria"),
        environment=os.getenv("ALEXANDRIA_ENVIRONMENT", "development"),
        log_level=os.getenv("ALEXANDRIA_LOG_LEVEL", "INFO"),
    )
