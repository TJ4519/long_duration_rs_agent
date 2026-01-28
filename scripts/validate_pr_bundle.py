#!/usr/bin/env python3
"""
Validate the PR review bundle for a GitHub Pull Request.

This is a low-ceremony, machine-enforced version of the existing "review bundle" convention:
- Require `review/PR<NUM>_REVIEW_BUNDLE.md` to be present and changed in the PR.
- Require YAML front matter with a small set of typed metadata.
- Compute a minimum risk level from the diff and prevent under-labeling.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from enum import IntEnum
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


class Risk(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


_RISK_BY_NAME: dict[str, Risk] = {"low": Risk.LOW, "medium": Risk.MEDIUM, "high": Risk.HIGH}


@dataclass(frozen=True)
class BundleMeta:
    risk: str
    spec_refs: list[str]
    rollback_strategy: str
    rollback_notes: str
    risk_override_reason: str | None = None


def _run_git(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        stderr = proc.stderr.strip()
        stdout = proc.stdout.strip()
        detail = stderr or stdout or "(no output)"
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return proc.stdout


def _changed_files(base_sha: str, head_sha: str) -> list[str]:
    if head_sha.upper() == "WORKTREE":
        changed: set[str] = set()
        for cmd in (
            ["diff", "--name-only", base_sha],
            ["diff", "--name-only", "--staged", base_sha],
            ["ls-files", "--others", "--exclude-standard"],
        ):
            out = _run_git(cmd)
            changed.update(line.strip() for line in out.splitlines() if line.strip())
        return sorted(changed)

    out = _run_git(["diff", "--name-only", f"{base_sha}..{head_sha}"])
    return [line.strip() for line in out.splitlines() if line.strip()]


def _min_risk_for_paths(paths: list[str]) -> Risk:
    relevant = [p for p in paths if not re.fullmatch(r"review/PR\d+_REVIEW_BUNDLE\.md", p)]
    if not relevant:
        return Risk.LOW

    def starts_with_any(path: str, prefixes: tuple[str, ...]) -> bool:
        return any(path.startswith(prefix) for prefix in prefixes)

    if any(starts_with_any(p, ("app/", "contracts/", "db/", "eval/")) for p in relevant):
        return Risk.HIGH
    if any(starts_with_any(p, (".github/", "spec/", "scripts/", "tests/")) for p in relevant):
        return Risk.MEDIUM
    if any(p.endswith((".py", ".sh")) for p in relevant):
        return Risk.MEDIUM
    return Risk.LOW


def _extract_front_matter(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "\n".join(lines[1:idx])
    return None


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if "#" in value and not (value.startswith('"') or value.startswith("'")):
        value = value.split("#", 1)[0].rstrip()
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def _parse_simple_yaml(front_matter: str) -> dict[str, Any]:
    """
    Parse a strict YAML subset:
    - key: value
    - key:
        nested_key: value
    - key:
        - item
        - item
    """

    lines = front_matter.splitlines()
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(0, root)]

    def next_nonempty_line(start: int) -> tuple[int, str] | None:
        for j in range(start, len(lines)):
            candidate = lines[j]
            stripped = candidate.strip()
            if not stripped or stripped.startswith("#"):
                continue
            return j, candidate
        return None

    for i, line in enumerate(lines):
        if not line.strip() or line.strip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        while stack and indent < stack[-1][0]:
            stack.pop()
        if not stack:
            raise ValueError(f"invalid indentation at line {i + 1}")

        container = stack[-1][1]
        stripped = line.strip()

        if stripped.startswith("- "):
            if not isinstance(container, list):
                raise ValueError(f"list item without list context at line {i + 1}")
            container.append(_parse_scalar(stripped[2:]))
            continue

        if ":" not in stripped:
            raise ValueError(f"expected 'key: value' at line {i + 1}")

        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()

        if not isinstance(container, dict):
            raise ValueError(f"mapping entry inside non-mapping at line {i + 1}")

        if raw_value != "":
            container[key] = _parse_scalar(raw_value)
            continue

        lookahead = next_nonempty_line(i + 1)
        if lookahead is None:
            container[key] = {}
            continue

        _, next_line = lookahead
        next_indent = len(next_line) - len(next_line.lstrip(" "))
        if next_indent <= indent:
            container[key] = {}
            continue

        next_stripped = next_line.strip()
        if next_stripped.startswith("- "):
            child: Any = []
        else:
            child = {}

        container[key] = child
        stack.append((next_indent, child))

    return root


def _require_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"front matter '{field}' must be a non-empty string")
    return value.strip()


def _require_string_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"front matter '{field}' must be a non-empty list of strings")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"front matter '{field}' must contain only non-empty strings")
    return [item.strip() for item in value]


def _parse_bundle_meta(meta: dict[str, Any]) -> BundleMeta:
    risk = _require_string(meta.get("risk"), "risk")
    spec_refs = _require_string_list(meta.get("spec_refs"), "spec_refs")

    rollback = meta.get("rollback")
    if not isinstance(rollback, dict):
        raise ValueError("front matter 'rollback' must be a mapping with {strategy, notes}")

    rollback_strategy = _require_string(rollback.get("strategy"), "rollback.strategy")
    rollback_notes = _require_string(rollback.get("notes"), "rollback.notes")

    risk_override_reason = meta.get("risk_override_reason")
    if risk_override_reason is not None:
        risk_override_reason = _require_string(risk_override_reason, "risk_override_reason")

    return BundleMeta(
        risk=risk,
        spec_refs=spec_refs,
        rollback_strategy=rollback_strategy,
        rollback_notes=rollback_notes,
        risk_override_reason=risk_override_reason,
    )


def _validate_spec_refs_exist(spec_refs: list[str]) -> None:
    missing = [ref for ref in spec_refs if not Path(ref).exists()]
    if missing:
        raise ValueError(f"spec_refs contains missing paths: {missing}")


def _validate_risk(meta: BundleMeta, min_risk: Risk) -> tuple[Risk, Risk]:
    risk_value = meta.risk.lower()
    if risk_value == "auto":
        declared = min_risk
        return declared, min_risk

    if risk_value not in _RISK_BY_NAME:
        raise ValueError("front matter 'risk' must be one of: auto|low|medium|high")

    declared = _RISK_BY_NAME[risk_value]
    if declared < min_risk and not meta.risk_override_reason:
        raise ValueError(
            f"risk under-labeled: declared={risk_value}, computed_min={min_risk.name.lower()}; "
            "set risk>=computed_min or provide risk_override_reason"
        )
    return declared, min_risk


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate PR review bundle and metadata.")
    parser.add_argument(
        "--pr-number",
        type=int,
        default=None,
        help="Optional PR number. If provided and the matching bundle is changed, it is preferred.",
    )
    parser.add_argument("--base-sha", default=None)
    parser.add_argument("--head-sha", default=None)
    args = parser.parse_args(argv)

    base_sha = args.base_sha or os.environ.get("GITHUB_BASE_SHA")
    head_sha = args.head_sha or os.environ.get("GITHUB_SHA") or "HEAD"
    if not base_sha:
        print("ERROR: missing --base-sha (or GITHUB_BASE_SHA env var).", file=sys.stderr)
        return 2

    try:
        _run_git(["rev-parse", "--is-inside-work-tree"])
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: not in a git repo: {exc}", file=sys.stderr)
        return 2

    try:
        changed = _changed_files(base_sha, head_sha)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: failed to compute git diff: {exc}", file=sys.stderr)
        return 2

    bundle_candidates = [
        path for path in changed if re.fullmatch(r"review/PR\d+_REVIEW_BUNDLE\.md", path)
    ]
    if not bundle_candidates:
        print(
            "ERROR: missing PR review bundle change. Add/update exactly one file matching: "
            "`review/PR<NN>_REVIEW_BUNDLE.md`",
            file=sys.stderr,
        )
        return 1
    if len(bundle_candidates) > 1:
        print(
            f"ERROR: multiple PR review bundles changed ({len(bundle_candidates)}). "
            "Change exactly one bundle per PR.\n"
            f"Bundles: {bundle_candidates}",
            file=sys.stderr,
        )
        return 1

    expected_bundle = None
    if args.pr_number:
        candidate = f"review/PR{args.pr_number}_REVIEW_BUNDLE.md"
        if candidate in bundle_candidates:
            expected_bundle = candidate

    bundle_path = expected_bundle or bundle_candidates[0]
    bundle_file = Path(bundle_path)
    if not bundle_file.exists():
        print(f"ERROR: bundle path in diff not found on disk: {bundle_path}", file=sys.stderr)
        return 2

    text = bundle_file.read_text(encoding="utf-8")
    front_matter = _extract_front_matter(text)
    if front_matter is None:
        print(
            "ERROR: missing YAML front matter. Start the bundle with:\n"
            "---\n"
            "risk: auto\n"
            "spec_refs:\n"
            "  - spec/REVIEW_MAP.md\n"
            "rollback:\n"
            "  strategy: revert\n"
            "  notes: \"...\"\n"
            "---\n",
            file=sys.stderr,
        )
        return 1

    try:
        meta_raw = _parse_simple_yaml(front_matter)
        meta = _parse_bundle_meta(meta_raw)
        _validate_spec_refs_exist(meta.spec_refs)
        min_risk = _min_risk_for_paths(changed)
        declared, computed = _validate_risk(meta, min_risk=min_risk)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: invalid PR bundle metadata: {exc}", file=sys.stderr)
        return 1

    print("OK: PR bundle validated.")
    print(f"- bundle: {bundle_path}")
    print(f"- files_changed: {len(changed)}")
    print(f"- risk: declared={declared.name.lower()} computed_min={computed.name.lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
