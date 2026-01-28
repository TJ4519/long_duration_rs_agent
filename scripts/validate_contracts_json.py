#!/usr/bin/env python3
"""
Validate contracts JSON files.

- Ensures JSON is parseable.
- Rejects duplicate keys anywhere in the document (helps avoid "accept both" merge artifacts).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def _no_duplicate_keys_object_pairs_hook(pairs: list[tuple[object, object]]) -> dict[object, object]:
    obj: dict[object, object] = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate JSON key: {key!r}")
        obj[key] = value
    return obj


def _validate_json_file(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    json.loads(raw, object_pairs_hook=_no_duplicate_keys_object_pairs_hook)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate contracts JSON files.")
    parser.add_argument(
        "--contracts-dir",
        default="contracts",
        help="Directory containing contract JSON files (default: contracts).",
    )
    args = parser.parse_args(argv)

    contracts_dir = Path(args.contracts_dir)
    if not contracts_dir.exists():
        print(f"ERROR: contracts dir not found: {contracts_dir}", file=sys.stderr)
        return 2

    json_paths = sorted(contracts_dir.glob("*.json"))
    if not json_paths:
        print(f"ERROR: no .json files found in: {contracts_dir}", file=sys.stderr)
        return 2

    failures: list[str] = []
    for path in json_paths:
        try:
            _validate_json_file(path)
        except Exception as exc:  # noqa: BLE001 - we want actionable CI errors
            failures.append(f"- {path}: {exc}")

    if failures:
        print("Contracts JSON validation failed:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1

    print(f"OK: validated {len(json_paths)} contract JSON file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

