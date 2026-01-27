# PR 21 Review Bundle

## 1) Executive Summary (5–10 lines)
This PR adds a context observability audit specification (Prompt Pack #11).
The spec defines manifest-by-default observability with inclusion/exclusion logs and fault-triggered prompt snapshots.
It formalizes pointer-only storage with full prompt and tool output capture only on fault triggers.
It requires traceability for every context item and an exclusion rationale for items not included.
Contracts are updated with documentation-only metadata notes; no API/DB/prompt/output schema shape changes are introduced.
Ops status and task log are updated accordingly, and README includes the new spec.

## 2) Contract Changes (the real review surface)
### API
- Added/changed endpoints: none.
- Request/response schema changes: none.
- Breaking changes: no.

### Data / DB
- Migrations added: none.
- Tables/columns/indexes changed: no (documentation-only).
- Provenance fields touched: no.

### Prompts
- Prompts added/changed: none.
- Prompt hashes (before/after): none → none.
- Assembly order changed: no.

### Outputs
- Output schema changed: no (comment note only).
- Citation format changed: no.

## 3) Verification Transcript (exact commands + PASS snippets)
- Not run (documentation-only change).

## 4) Behavioral Guarantees (what’s now defined)
- Context manifests are written every step with inclusion and exclusion logs.
- Manifests store pointers/hashes only (no raw blobs); artifacts store raw bytes.
- Full prompt and tool output snapshots are captured only on fault triggers.
- Traceability is enforced for all context items and exclusions.

## 5) Risk Notes (Top 3)
- Risk 1: Failure to capture prompt snapshots on fault triggers reduces forensic value (medium).
- Risk 2: Exclusion logs may be omitted by implementers unless explicitly enforced in validation (medium).
- Risk 3: Documentation-only metadata notes should be removed when real schema exports are generated (low).

## 6) Rollback Plan
Revert the PR commit(s) and remove:
- `spec/CONTEXT_OBSERVABILITY_AUDIT.md`
- README index update
- Documentation-only metadata note updates under `contracts/`
- Ops status/task log entry
- `review/PR21_REVIEW_BUNDLE.md`

## 7) What I (human) should review (max 3 items)
- `spec/CONTEXT_OBSERVABILITY_AUDIT.md`
- `review/PR21_REVIEW_BUNDLE.md`
- `contracts/openapi.json` metadata note update (documentation-only)
