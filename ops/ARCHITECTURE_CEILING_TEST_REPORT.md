# Architecture Ceiling Test Report

- date: 2026-01-21
- scope: Prompt Pack #10 audit of Project Alexandria runtime contracts
- auditor: BUILDER_AGENT (ALEX-SPEC)
- sources: `spec/*.md`, `contracts/*.json`, `review/PR20_REVIEW_BUNDLE.md`

## 1) Model-upgrade simulation (explicit)
**Question:** If a more capable model is swapped in tomorrow, do outcomes improve without code changes?

**Answer:** Yes, in principle. The architecture compiles per-step context, uses retrieval + rerank, and stores evidence pointers. A stronger model should improve plan quality and evidence synthesis by configuration-only changes (e.g., larger budgets, larger context window, relaxed caps), provided that hard caps remain configurable and not hard-coded.

**Constraints that could blunt the gain:** fixed tool I/O caps, fixed retrieval scope defaults, and the MVP offline ingestion boundary if the objective requires new data during runtime. These are listed in the ceiling inventory below with mitigation paths.

## 2) Ceiling Inventory (current state)
Each ceiling entry includes category, taxonomy, and references to the contract/spec that introduces the constraint.

### C-001: Offline ingestion boundary
- category: hard-coded decision tree (runtime gating)
- taxonomy: DATA/PROVENANCE
- description: Runtime assumes prebuilt indexes and cannot ingest/index new sources (offline ingestion required for MVP).
- justification: data boundary and provenance control for MVP.
- impact: A stronger model cannot compensate for missing data created after indexing; runtime objectives that require fresh sources are blocked.
- mitigation: Add an online ingestion pipeline with controlled provenance and chunking; allow runtime to request ingestion when policy allows.
- owner: principal-architect
- severity: medium
- references: `spec/DATA_CONTRACT.md`

### C-002: Retrieval scope defaults (metadata predicates + 3-year date scope)
- category: overly fixed thresholds
- taxonomy: DATA/PROVENANCE
- description: Default metadata predicates and a 3-year date scope are applied when no user-provided range exists.
- justification: improves precision and latency for MVP.
- impact: A stronger model could still miss relevant older evidence if defaults are not relaxed.
- mitigation: Keep defaults configurable per objective; allow RUNTIME_USER-provided overrides; document when to widen scope.
- owner: principal-architect
- severity: low
- references: `spec/DATA_CONTRACT.md`

### C-003: Tool I/O caps (read_file max_lines=500)
- category: overly fixed thresholds
- taxonomy: BUDGET/LATENCY
- description: File-read tools are capped at 500 lines by default with pagination metadata.
- justification: prevent context flooding and cost blowups.
- impact: A stronger model with larger context cannot fully utilize its capacity if caps are not adjustable.
- mitigation: Keep caps configurable per run; allow RUNTIME_USER to raise caps when budgets allow.
- owner: principal-architect
- severity: low
- references: `spec/RUNTIME_GUARDRAILS.md`

### C-004: Compaction trigger thresholds (EVENT_THRESHOLD=18, N_STEP_FALLBACK=8)
- category: aggressive summarization and irreversible compression
- taxonomy: BUDGET/LATENCY
- description: Compaction cadence is tied to fixed event/step thresholds.
- justification: control context growth and cost while preserving evidence pointers.
- impact: If thresholds are too low, stronger models may still see over-compacted state, reducing reasoning depth.
- mitigation: Keep thresholds configurable; tune based on evidence coverage metrics; allow larger thresholds when budget allows.
- owner: principal-architect
- severity: low
- references: `spec/SUMMARIZATION_SCHEMA.md`

### C-005: Rerank acceptance threshold (implicit)
- category: overly fixed thresholds
- taxonomy: BUDGET/LATENCY
- description: Rerank acceptance relies on a threshold that, if hard-coded, could gate retrieval unnecessarily.
- justification: ensure evidence quality.
- impact: Stronger models may still be blocked from using near-threshold evidence if the threshold is rigid.
- mitigation: Require threshold to be configuration-driven and recorded in manifests; allow objective-specific tuning.
- owner: principal-architect
- severity: low
- references: `spec/AGENT_BLUEPRINT.md`

### C-006: Multi-agent split justification (watchlist)
- category: multi-agent split without clarity gain
- taxonomy: ARTIFICIAL/ACCIDENTAL
- description: Multi-agent split is allowed but should only be used when it increases isolation or correctness.
- justification: optional split for clarity and context isolation.
- impact: If enforced by default, could become an artificial ceiling that blocks a stronger single model from performing end-to-end reasoning.
- mitigation: Keep split optional with a single-agent fallback; require explicit rationale per run.
- owner: principal-architect
- severity: low
- references: `spec/MULTI_AGENT_SCOPE.md`

## 3) Summary of artificial ceilings
- **Critical artificial ceilings:** none detected in current contracts.
- **Medium artificial ceilings:** none.
- **Low artificial ceilings/watchlist:** C-002, C-003, C-004, C-005, C-006 (configurability and optionality required).

## 4) Required follow-ups
- Confirm all thresholds and caps above are configuration-driven and recorded in manifests (no hard-coded constants in runtime).
- If runtime objectives require fresh sources, define a controlled online ingestion path (policy-gated) to remove C-001 for production.

## 5) Acceptance
- This audit passes the MVP bar: no critical artificial ceilings remain.
- Any future hard constraint must be added to the ceiling inventory with justification and mitigation.
