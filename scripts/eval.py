#!/usr/bin/env python3
"""Evaluate demo outputs against a golden file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate demo output")
    parser.add_argument("--golden", required=True, help="Golden JSON path")
    parser.add_argument("--output", required=True, help="Output JSON path")
    parser.add_argument(
        "--metrics",
        default="outputs/eval_metrics.json",
        help="Metrics output path",
    )
    args = parser.parse_args()

    golden = json.loads(Path(args.golden).read_text())
    output = json.loads(Path(args.output).read_text())

    objective_match = golden.get("objective") == output.get("objective")
    metrics = {
        "objective_match": objective_match,
        "golden_status": golden.get("status"),
        "output_status": output.get("status"),
    }

    metrics_path = Path(args.metrics)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")

    if not objective_match:
        raise SystemExit("objective mismatch")


if __name__ == "__main__":
    main()
