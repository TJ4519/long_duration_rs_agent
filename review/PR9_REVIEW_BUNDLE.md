# PR 9 Review Bundle

## 1) Executive Summary (5–10 lines)
This PR adds evidence ledger helpers and schemas for claims and evidence.
Evidence records capture claim IDs, chunk IDs, quotes, and spans.
Claim records bundle evidence lists for downstream outputs.
Helper functions allow attaching evidence immutably to claims.
Unit tests cover evidence attachment and schema defaults.
Contracts add evidence/claim schema exports without API changes.
Ops status and task log are updated for PR9.

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
- Output schema changed: yes (claim/evidence schemas exported).
- Citation format changed: no.

## 3) Verification Transcript (exact commands + PASS snippets)
- `python scripts/generate_contracts.py` → PASS (no output; contracts generated).
- `pytest -q` → PASS (13 passed, 1 skipped in 0.30s).

## 4) Behavioral Guarantees (what’s now enforced)
- Invariants guaranteed by tests: evidence attachment is immutable and defaults are empty.
- New stop rules / budgets: none.
- New fallback behavior: none.

## 5) Risk Notes (Top 3)
- Risk 1: Evidence schemas may diverge from DB schema (medium).
- Risk 2: No validation of span keys beyond ints (low).
- Risk 3: Status field is free-form (low).

## 6) Rollback Plan
Revert the PR commit(s) and delete evidence schema/helper files.

## 7) What I (human) should review (max 3 items)
- contracts/output_schema.json for new evidence/claim schema.
- contracts/openapi.json for unchanged API surface.
- review/PR9_REVIEW_BUNDLE.md verification transcript.
