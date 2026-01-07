#!/usr/bin/env python3
"""Simple evaluation harness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Project Alexandria eval")
    parser.add_argument("--golden", required=True, help="Path to golden JSON")
    parser.add_argument("--candidate", required=True, help="Path to candidate JSON")
    args = parser.parse_args()

    golden = json.loads(Path(args.golden).read_text())
    candidate = json.loads(Path(args.candidate).read_text())

    passed = golden == candidate
    if passed:
        print("PASS: candidate matches golden")
    else:
        print("FAIL: candidate does not match golden")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
