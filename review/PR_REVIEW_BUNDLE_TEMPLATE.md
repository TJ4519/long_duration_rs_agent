---
risk: auto  # auto|low|medium|high
spec_refs:
  - spec/REVIEW_MAP.md
rollback:
  strategy: revert
  notes: "Revert the merge commit; no data migrations."
---

# PR <NUM> Review Bundle

## 1) Executive Summary (5–10 lines)
- What this PR does
- What it does *not* do
- Why it exists (tie back to objective/spec)

## 2) Contract Changes (the real review surface)
### API
- Added/changed endpoints:
- Request/response schema changes:
- Breaking changes:

### Data / DB
- Migrations added:
- Tables/columns/indexes changed:
- Provenance fields touched:

### Prompts
- Prompts added/changed:
- Prompt hashes (before/after):
- Assembly order changed:

### Outputs
- Output schema changed:
- Citation format changed:

## 3) Verification Transcript (exact commands + PASS snippets)
- Commands run:
- Key PASS snippets:

## 4) Behavioral Guarantees (what’s now defined)
- What invariants are now guaranteed
- What failure modes are explicitly handled

## 5) Risk Notes (Top 3)
- Risk 1:
- Risk 2:
- Risk 3:

## 6) Rollback Plan
- Keep this actionable; one command if possible.

## 7) What I (human) should review (max 3 items)
- Limit human attention to the true review surface.

