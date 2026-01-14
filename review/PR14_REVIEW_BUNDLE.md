# PR 14 Review Bundle

## 1) Executive Summary (5–10 lines)
This PR adds a summarization schema specification for compaction (snapshotting) behavior.
The new spec defines a binding Compaction Snapshot JSON contract and an optional deterministic narrative template derived from that JSON (no LLM call).
It specifies compaction trigger semantics (threshold-based with an N-step fallback) and formalizes a stable counted-events definition to avoid dependence on verbose event emission rates.
It also documents evidence pointer requirements (evidence_id + chunk_id + span) and deterministic evidence_id semantics namespaced by corpus/index identity.
Contracts are updated with documentation-only metadata notes; no API, DB, prompt, or output schema shape changes are introduced.
Ops status and task log are updated accordingly, and README is updated to include the new spec in the index.

## 2) Contract Changes (the real review surface)
### API
- Added/changed endpoints: none.
- Request/response schema changes: none.
- Breaking changes: no.

### Data / DB
- Migrations added: none.
- Tables/columns/indexes changed: no.
- Provenance fields touched: no (documentation-only).

### Prompts
- Prompts added/changed: none.
- Prompt hashes (before/after): none → none.
- Assembly order changed: no.

### Outputs
- Output schema changed: no (comment note only).
- Citation format changed: no (specifies pointer shape; implementation unchanged).

## 3) Verification Transcript (exact commands + PASS snippets)
- Not run (documentation-only change).

## 4) Behavioral Guarantees (what’s now defined)
- Compaction produces a binding JSON snapshot and an optional template-derived narrative markdown.
- Compaction validation is a hard gate: objective/done invariants stable; verified claims require evidence; conflicts require two-sided citations.
- Compaction triggering is stable under verbose logging by counting only terminal `PLAN_DONE/ACT_DONE/OBSERVE_DONE` events, with MVP defaults documented.
- Evidence references are pointer-only and must include `evidence_id`, `chunk_id`, and `span`, with deterministic `evidence_id` semantics namespaced by corpus/index identity.

## 5) Risk Notes (Top 3)
- Risk 1: The event taxonomy and counted terminal events are defined at the spec level; implementation must align to preserve trigger stability (medium).
- Risk 2: Deterministic `evidence_id` semantics depend on stable `corpus_id/index_id` identifiers; ingestion/indexing pipeline must publish those IDs (medium).
- Risk 3: Contracts carry documentation-only metadata notes; remove when real schema exports are generated (low).

## 6) Rollback Plan
Revert the PR commit(s) and remove:
- `spec/SUMMARIZATION_SCHEMA.md`
- README index update
- Documentation-only metadata note updates under `contracts/`
- Ops status/task log entries
- `review/PR14_REVIEW_BUNDLE.md`

## 7) What I (human) should review (max 3 items)
- `spec/SUMMARIZATION_SCHEMA.md`
- `review/PR14_REVIEW_BUNDLE.md`
- `contracts/openapi.json` metadata note update (documentation-only)

