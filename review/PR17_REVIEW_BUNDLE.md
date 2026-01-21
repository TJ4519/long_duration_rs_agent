# PR 17 Review Bundle

## 1) Executive Summary (5–10 lines)
This PR adds a runtime guardrails specification.
The spec defines tool I/O caps, pagination metadata, and path hygiene to prevent context flooding.
It formalizes zero-result guidance and unknown-tool handling to avoid blind alleys.
It adds loop detection with typed overrides and schema enforcement with repair loops.
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
- File-read tools must enforce hard caps and return pagination metadata; paths are normalized to workspace-relative form.
- Zero-result searches return guidance; unknown tool calls emit typed errors and force correction.
- Loop detection hashes repeated actions and injects typed overrides; repeated loops after override stop with SYSTEM_ERROR.
- Plan/tool/output JSON is validated by a decoding layer; invalid JSON triggers a repair loop with bounded attempts.

## 5) Risk Notes (Top 3)
- Risk 1: Implementation must align tool wrappers with new cap/pagination/path hygiene requirements (medium).
- Risk 2: Loop detection + override needs a consistent action signature across tools (medium).
- Risk 3: Schema repair loop requires a decoding/validation layer to be wired into runtime execution (medium).

## 6) Rollback Plan
Revert the PR commit(s) and remove:
- `spec/RUNTIME_GUARDRAILS.md`
- README index update
- Documentation-only metadata note updates under `contracts/`
- Ops status/task log entry
- `review/PR17_REVIEW_BUNDLE.md`

## 7) What I (human) should review (max 3 items)
- `spec/RUNTIME_GUARDRAILS.md`
- `review/PR17_REVIEW_BUNDLE.md`
- `contracts/openapi.json` metadata note update (documentation-only)
