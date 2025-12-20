# Review Map — Finger‑Tippy Review (You Can't Read Everything)

## 1) The rule
You review *contracts and safety*, not every line of implementation.

If contracts are correct and tests cover behavior, you can merge confidently.

## 2) Must-Review Artifacts (High leverage, low volume)
### A) Database migrations (always read)
- db/migrations/*.sql
Review for:
- correct keys/indexes
- provenance fields exist (chunk spans, artifact pointers)
- evidence ledger tables exist

### B) Schemas (read fully)
- app/schemas/*.py
Review for:
- Plan schema prevents unsafe actions
- Evidence requires citations
- Context Manifest includes selected chunk IDs

### C) Compiler assembly order + constraints injection (read fully)
- app/compiler/assemble.py
- app/compiler/manifest.py
Review for:
- stable prompt order
- override constraints rendered safely
- low-score fallback logic correct

### D) Artifact Manager boundaries (read fully)
- app/artifacts/manager.py
Review for:
- streaming behavior (no full reads into RAM)
- idempotency via content hash
- no raw blobs in DB

### E) Compaction validation rules (read fully)
- app/memory/compaction.py
Review for:
- invariants copied verbatim
- summary unit tests implemented
- claims cannot be "verified" without evidence

## 3) Skim-Review Artifacts (Medium leverage)
- app/compiler/retrieval.py (skim: query building)
- app/compiler/rerank.py (skim: batching + caching)
- scripts/* (skim)

## 4) Trust-to-Tests Artifacts (Low leverage)
- formatting, logging glue, minor utilities
- endpoint wiring in api.py (unless auth/security)

## 5) Merge Gates (what must be true before merging)
Gate 1: Schema validation passes for Plan and Outputs.
Gate 2: Every verified claim has evidence with provenance fields.
Gate 3: Context Manifest is written every step.
Gate 4: Artifact ingestion is idempotent and pointer-only.
Gate 5: Compaction does not mutate invariants.

## 6) The 10-minute PR review checklist
- [ ] Read PR summary
- [ ] Read migrations
- [ ] Read schema diffs
- [ ] Read compiler assemble/manifest diff
- [ ] Read artifact manager diff
- [ ] Read compaction validation diff
- [ ] Run tests + demo command
- [ ] Confirm output JSON includes citations and manifest refs

## 7) Stop conditions (do NOT merge if)
- any raw blob is stored in DB
- narrative summary adds “verified” claims without evidence
- compiler can proceed when retrieval returns nothing without an explicit constraint
- overrides are free-text prompt rewrites instead of typed constraints
