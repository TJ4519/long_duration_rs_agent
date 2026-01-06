#!/usr/bin/env python3
"""Demo CLI runner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Project Alexandria demo run")
    parser.add_argument("--objective", required=True, help="Objective to run")
    parser.add_argument("--output", default="outputs/demo_output.json")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "objective": args.objective,
        "status": "ok",
        "notes": "demo output placeholder",
    }
    output_path.write_text(json.dumps(payload, indent=2) + "\n")

    print(f"Wrote demo output to {output_path}")


if __name__ == "__main__":
    main()
