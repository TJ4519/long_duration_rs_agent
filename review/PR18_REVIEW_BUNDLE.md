# PR 18 Review Bundle

## 1) Executive Summary (5–10 lines)
This PR adds a cache stability optimization specification.
The spec defines immutable cached prefixes, deterministic serialization, stable tool ordering, and placement of dynamic data in suffixes.
It documents provider-specific guidance (OpenAI/Anthropic/Gemini) on breakpoints and explicit caching, while keeping requirements provider-agnostic.
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
- Cached prefix is immutable within a run; dynamic data is moved to suffix.
- Structured content in prefix is deterministically serialized; tool ordering is stable.
- Prefix hash is recorded in manifests for cache monitoring.
- Provider-specific cache breakpoints are supported where available (Anthropic cache_control, Gemini explicit caching).

## 5) Risk Notes (Top 3)
- Risk 1: Cache stability enforcement depends on deterministic serialization in implementation (medium).
- Risk 2: Provider cache semantics may differ; spec assumes identical-prefix requirement, which should be validated per provider (low).
- Risk 3: Contracts carry documentation-only metadata notes; remove when real schema exports are generated (low).

## 6) Rollback Plan
Revert the PR commit(s) and remove:
- `spec/CACHE_STABILITY_OPTIMIZATION.md`
- README index update
- Documentation-only metadata note updates under `contracts/`
- Ops status/task log entry
- `review/PR18_REVIEW_BUNDLE.md`

## 7) What I (human) should review (max 3 items)
- `spec/CACHE_STABILITY_OPTIMIZATION.md`
- `review/PR18_REVIEW_BUNDLE.md`
- `contracts/openapi.json` metadata note update (documentation-only)

