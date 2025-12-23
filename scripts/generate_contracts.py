"""Generate reviewable contract artifacts."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

CONTRACTS_DIR = BASE_DIR / "contracts"
PROMPTS_DIR = BASE_DIR / "prompts"
MIGRATIONS_DIR = BASE_DIR / "db" / "migrations"


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def export_openapi() -> None:
    if importlib.util.find_spec("fastapi") is None:
        _write_json(
            CONTRACTS_DIR / "openapi.json",
            {
                "openapi": "3.0.0",
                "info": {
                    "title": "Project Alexandria",
                    "version": "0.0.0",
                    "description": "FastAPI not installed; stub OpenAPI exported.",
                },
                "paths": {},
            },
        )
        return

    from app.main import create_app

    app = create_app()
    _write_json(CONTRACTS_DIR / "openapi.json", app.openapi())


def export_output_schema() -> None:
    if importlib.util.find_spec("pydantic") is None:
        _write_json(
            CONTRACTS_DIR / "output_schema.json",
            {
                "title": "ResearchOutput",
                "description": "Pydantic not installed; stub output schema exported.",
                "type": "object",
                "properties": {"summary": {"type": "string"}},
                "required": ["summary"],
            },
        )
        return

    from app.schemas import ResearchOutput

    schema = ResearchOutput.model_json_schema()
    _write_json(CONTRACTS_DIR / "output_schema.json", schema)


def export_prompts_manifest() -> None:
    prompts = []
    if PROMPTS_DIR.exists():
        for path in sorted(PROMPTS_DIR.rglob("*.md")):
            content = path.read_text()
            prompts.append(
                {
                    "path": str(path.relative_to(BASE_DIR)),
                    "sha256": _hash_text(content),
                }
            )
    _write_json(CONTRACTS_DIR / "prompts_manifest.json", prompts)


def export_migrations_summary() -> None:
    lines = ["# Migrations Summary", ""]
    if MIGRATIONS_DIR.exists():
        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            content = path.read_text()
            checksum = _hash_text(content)
            lines.append(f"- {path.name}: {checksum}")
    else:
        lines.append("- No migrations directory found.")
    (CONTRACTS_DIR / "migrations_summary.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    CONTRACTS_DIR.mkdir(parents=True, exist_ok=True)
    export_openapi()
    export_output_schema()
    export_prompts_manifest()
    export_migrations_summary()


if __name__ == "__main__":
    main()
