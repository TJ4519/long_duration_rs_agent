---
risk: auto  # auto|low|medium|high
spec_refs:
  - spec/REVIEW_MAP.md
rollback:
  strategy: revert
  notes: "Revert the PR commit(s); removes CI gates and bundle validator scripts."
---

# PR 24 Review Bundle

## 1) Executive Summary (5–10 lines)
This PR adds a minimal GitHub Actions “PR gates” workflow to enforce the review-bundle convention in CI.
It introduces a small validator that requires exactly one `review/PR<NN>_REVIEW_BUNDLE.md` change per PR and a typed YAML front matter header.
It also adds a contracts JSON validator that rejects duplicate keys (common merge-conflict artifact).
Finally, CI runs a syntax compile pass over `app/` and `scripts/` to catch obvious breakage early.
No runtime/API/DB behavior changes are introduced.

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
- `python scripts/validate_contracts_json.py` (PASS locally)
- `python -m compileall app scripts` (PASS locally)

## 4) Behavioral Guarantees (what’s now defined)
- PRs must include a review bundle with typed YAML metadata (risk, spec refs, rollback).
- Contracts JSON files are rejected if they contain duplicate keys.
- Python source under `app/` and `scripts/` must compile (syntax check) before merge.

## 5) Risk Notes (Top 3)
- Risk 1: CI will block PRs that don’t include a bundle + YAML front matter (intentional; medium).
- Risk 2: The YAML subset parser is intentionally strict; unusual YAML features may be rejected (low).
- Risk 3: Contracts validation may surface pre-existing duplicate keys if reintroduced by merge conflicts (low).

## 6) Rollback Plan
Revert the PR commit(s) and remove:
- `.github/workflows/pr-gates.yml`
- `scripts/validate_pr_bundle.py`
- `scripts/validate_contracts_json.py`
- `review/PR_REVIEW_BUNDLE_TEMPLATE.md`
- PR24 entries in ops + migrations summary

## 7) What I (human) should review (max 3 items)
- `.github/workflows/pr-gates.yml`
- `scripts/validate_pr_bundle.py`
- `spec/REVIEW_MAP.md`

