# PR 12 Review Bundle

## 1) Executive Summary (5–10 lines)
This PR adds a demo CLI runner and an evaluation harness.
The demo script writes a small JSON output for a given objective.
The eval script compares a candidate output to a golden file.
Unit tests validate demo output creation and eval passing.
Contracts are unchanged; this is CLI tooling only.
Ops status and task log are updated for PR12.

## 2) Contract Changes (the real review surface)
### API
- Added/changed endpoints: none.
- Request/response schema changes: none.
- Breaking changes: no.

### Data / DB
- Migrations added: none.
- Tables/columns/indexes changed: no.
- Provenance fields touched: no.

### Prompts
- Prompts added/changed: none.
- Prompt hashes (before/after): none → none.
- Assembly order changed: no.

### Outputs
- Output schema changed: no.
- Citation format changed: no.

## 3) Verification Transcript (exact commands + PASS snippets)
- `python scripts/generate_contracts.py` → PASS (no output; contracts generated).
- `pytest -q` → PASS (19 passed, 2 skipped in 0.35s).

## 4) Behavioral Guarantees (what’s now enforced)
- Invariants guaranteed by tests: demo output is generated; eval passes when outputs match.
- New stop rules / budgets: none.
- New fallback behavior: none.

## 5) Risk Notes (Top 3)
- Risk 1: Demo output is stubbed and not tied to real pipeline (medium).
- Risk 2: Eval compares strict JSON equality only (low).
- Risk 3: Demo output path can overwrite files if misused (low).

## 6) Rollback Plan
Revert the PR commit(s) and delete scripts/demo_run.py, scripts/eval.py, and tests/test_demo_scripts.py.

## 7) What I (human) should review (max 3 items)
- contracts/openapi.json for unchanged API surface.
- contracts/output_schema.json for unchanged output contract.
- review/PR12_REVIEW_BUNDLE.md verification transcript.
