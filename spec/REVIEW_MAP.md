# Review Map — Finger‑Tippy Review (Contract-First)

## 1) The rule
You review contracts and verification artifacts, not implementation code.

If contracts are correct and verification passes, you can merge confidently.

## 2) Canonical review surface (read fully)
- review/PR_<NN>_REVIEW_BUNDLE.md
- contracts/openapi.json
- contracts/output_schema.json
- contracts/prompts_manifest.json
- contracts/migrations_summary.md

## 3) Merge Gates (what must be true before merging)
Gate 1: Review bundle exists and follows the template.
Gate 2: Contract exports are updated and committed.
Gate 3: Verification transcript includes PASS results for required commands.
Gate 4: Ops memory (STATUS + TASK_LOG) updated for the PR.

## 4) The 10-minute PR review checklist
- [ ] Read review/PR_<NN>_REVIEW_BUNDLE.md
- [ ] Inspect contract diffs in contracts/
- [ ] Verify ops updates in ops/STATUS.md and ops/TASK_LOG.md
- [ ] Run verification commands listed in the review bundle

## 5) Stop conditions (do NOT merge if)
- review bundle missing or deviates from template
- contracts/ missing required exports
- verification transcript missing PASS snippets
- ops memory not updated
