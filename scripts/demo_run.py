#!/usr/bin/env python3
"""Run a demo objective and emit a stub output payload."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a demo Alexandria objective")
    parser.add_argument("--objective", required=True, help="Objective to execute")
    parser.add_argument(
        "--output",
        default="outputs/demo_run.json",
        help="Output JSON path",
    )
    args = parser.parse_args()

    output = {
        "objective": args.objective,
        "status": "stub",
        "findings": [],
        "citations": [],
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
