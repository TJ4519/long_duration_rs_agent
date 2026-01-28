# Review Map — Finger‑Tippy Review (You Can't Read Everything)

## 1) The rule
You review *contracts and safety*, not every line of implementation.

If contracts are correct and tests cover behavior, you can merge confidently.

## 1.1) Machine-enforced review bundle metadata (CI gate)
Every PR must add/update a review bundle at:
- `review/PR_<NN>_REVIEW_BUNDLE.md`

The review bundle must start with YAML front matter so CI can enforce minimal governance:
- `risk`: `auto|low|medium|high`
- `spec_refs`: list of file paths that define the contract/policy this PR follows
- `rollback.strategy` + `rollback.notes`

MVP intent: keep this small and typed so `BUILDER_USER` is not the merge bottleneck.

## 2) Canonical review surface (read fully every PR)
- review/PR_<NN>_REVIEW_BUNDLE.md
- contracts/openapi.json
- contracts/output_schema.json
- contracts/prompts_manifest.json
- contracts/migrations_summary.md

## 3) Merge Gates (what must be true before merging)
Gate 1: Schema validation passes for Plan and Outputs.
Gate 2: Every verified claim has evidence with provenance fields.
Gate 3: Context Manifest is written every step.
Gate 4: Artifact ingestion is idempotent and pointer-only.
Gate 5: Compaction does not mutate invariants.

## 4) The 10-minute PR review checklist
- [ ] Read PR review bundle
- [ ] Read contracts outputs (openapi, output schema, prompts, migrations summary)
- [ ] Run verification commands listed in the review bundle
- [ ] Confirm output JSON includes citations and manifest refs

## 5) Stop conditions (do NOT merge if)
- any raw blob is stored in DB
- narrative summary adds “verified” claims without evidence
- compiler can proceed when retrieval returns nothing without an explicit constraint
- overrides are free-text prompt rewrites instead of typed constraints
