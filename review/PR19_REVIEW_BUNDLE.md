# PR 19 Review Bundle

## 1) Executive Summary (5–10 lines)
This PR adds a failure reflection system specification.
The spec defines failure signals, a structured failure record schema, and retrieval-based integration rules to prevent repeat mistakes without accumulating warning-bloat.
It defines decay/revision fields (status, occurrence counters, helpful/harmful counts) and escalation behavior for repeated failures.
It keeps pointer-first semantics (manifest_id, artifact_id, query_id, chunk/span) and disallows introducing new verified claims via reflection.
Contracts are updated with documentation-only metadata notes; no API/DB/prompt/output schema shape changes are introduced.
Ops status and task log are updated accordingly, and README is updated to include the new spec.

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
- Failure signals are captured and written as structured failure records with pointer refs (no blobs).
- Failure records integrate into context selectively (top-k, deterministic ordering) and support decay/revision to avoid bloat.
- Repeated failures can escalate to ASK_HUMAN or SYSTEM_ERROR depending on recoverability.
- Reflection cannot introduce new verified claims without evidence pointers.

## 5) Risk Notes (Top 3)
- Risk 1: Fingerprint design must be stable and useful; poor fingerprints will either miss repeats or over-collide (medium).
- Risk 2: Integration ranking must be deterministic to preserve cache stability and reproducibility (medium).
- Risk 3: Contracts carry documentation-only metadata notes; remove when real schema exports are generated (low).

## 6) Rollback Plan
Revert the PR commit(s) and remove:
- `spec/FAILURE_REFLECTION_SYSTEM.md`
- README index update
- Documentation-only metadata note updates under `contracts/`
- Ops status/task log entry
- `review/PR19_REVIEW_BUNDLE.md`

## 7) What I (human) should review (max 3 items)
- `spec/FAILURE_REFLECTION_SYSTEM.md`
- `review/PR19_REVIEW_BUNDLE.md`
- `contracts/openapi.json` metadata note update (documentation-only)

