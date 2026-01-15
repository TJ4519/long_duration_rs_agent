# PR 15 Review Bundle

## 1) Executive Summary (5–10 lines)
This PR adds an external memory architecture specification.
The spec defines authoritative vs derived stores (event log, snapshots, evidence ledger, manifests, artifacts) and pointer semantics.
It locks a local-first storage stack (Postgres + run-addressed filesystem) with hashes for integrity and indefinite retention.
It formalizes recovery/failure behavior for missing pointers (retry once, then SYSTEM_ERROR) and keeps DB pointer-only (no blobs >64KB).
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
- Event log is authoritative history; snapshots are authoritative runtime state; evidence ledger and manifests are authoritative records; filesystem is authoritative for raw bytes.
- DB stores pointers/metadata only (no blobs >64KB); artifacts are run-addressed with hash metadata; evidence pointers include deterministic `evidence_id` + `chunk_id` + `span`.
- Runtime rehydrates from snapshots + recent events; log replay is for recovery/verification.
- Missing critical pointers trigger a retry and then SYSTEM_ERROR with diagnostics.
- Retention is indefinite (MVP) on local Postgres + filesystem; S3 swap-in is deferred.

## 5) Risk Notes (Top 3)
- Risk 1: Implementation must align event/manifest schemas to the documented authoritative/derived split (medium).
- Risk 2: Hash integrity and deterministic `evidence_id` depend on stable corpus/index identifiers (medium).
- Risk 3: Contracts carry documentation-only metadata notes; remove when real schema exports are generated (low).

## 6) Rollback Plan
Revert the PR commit(s) and remove:
- `spec/EXTERNAL_MEMORY_ARCHITECTURE.md`
- README index update
- Documentation-only metadata note updates under `contracts/`
- Ops status/task log entry
- `review/PR15_REVIEW_BUNDLE.md`

## 7) What I (human) should review (max 3 items)
- `spec/EXTERNAL_MEMORY_ARCHITECTURE.md`
- `review/PR15_REVIEW_BUNDLE.md`
- `contracts/openapi.json` metadata note update (documentation-only)

