#!/usr/bin/env python3
"""Generate contract artifacts for review."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

CONTRACTS_DIR = ROOT / "contracts"
PROMPTS_DIR = ROOT / "prompts"
MIGRATIONS_DIR = ROOT / "db" / "migrations"


def _hash_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _iter_prompt_files() -> Iterable[Path]:
    if not PROMPTS_DIR.exists():
        return []
    return [path for path in PROMPTS_DIR.rglob("*") if path.is_file()]


def write_openapi() -> None:
    if importlib.util.find_spec("fastapi") is None:
        openapi = {
            "openapi": "3.0.0",
            "info": {"title": "Project Alexandria", "version": "0.0.0"},
            "paths": {},
            "warning": "fastapi is not installed; openapi export is stubbed",
        }
        (CONTRACTS_DIR / "openapi.json").write_text(
            json.dumps(openapi, indent=2, sort_keys=True)
        )
        return

    from app.main import create_app

    app = create_app()
    openapi = app.openapi()
    (CONTRACTS_DIR / "openapi.json").write_text(
        json.dumps(openapi, indent=2, sort_keys=True)
    )


def write_prompts_manifest() -> None:
    prompts = []
    for path in sorted(_iter_prompt_files()):
        prompts.append(
            {
                "path": str(path.relative_to(ROOT)),
                "sha256": _hash_file(path),
            }
        )
    (CONTRACTS_DIR / "prompts_manifest.json").write_text(
        json.dumps({"prompts": prompts}, indent=2, sort_keys=True)
    )


def write_output_schema() -> None:
    if importlib.util.find_spec("pydantic") is None:
        schema = {
            "title": "ResearchOutput",
            "type": "object",
            "properties": {},
            "warning": "pydantic is not installed; schema export is stubbed",
        }
        (CONTRACTS_DIR / "output_schema.json").write_text(
            json.dumps(schema, indent=2, sort_keys=True)
        )
        return

    from app.schemas.outputs import ResearchOutput

    schema = ResearchOutput.model_json_schema()
    (CONTRACTS_DIR / "output_schema.json").write_text(
        json.dumps(schema, indent=2, sort_keys=True)
    )


def write_migrations_summary() -> None:
    lines = ["# Migrations Summary", ""]
    if MIGRATIONS_DIR.exists():
        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            content = path.read_text().splitlines()
            preview = content[0] if content else "(empty)"
            lines.append(f"- {path.name}: {preview}")
    else:
        lines.append("- No migrations directory found.")
    (CONTRACTS_DIR / "migrations_summary.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    CONTRACTS_DIR.mkdir(parents=True, exist_ok=True)
    write_openapi()
    write_prompts_manifest()
    write_output_schema()
    write_migrations_summary()


if __name__ == "__main__":
    main()
