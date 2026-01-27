# Architecture Ceiling Test (Prompt Pack #10)

## Purpose
Define a repeatable audit that checks whether the Project Alexandria architecture scales with better models or whether the architecture itself becomes the bottleneck.

This spec is a Bitter Lesson check: if a more capable model is swapped in tomorrow, the system should improve proportionally without code changes, unless constrained by explicit safety, compliance, or budget requirements.

## Inputs/Outputs
### Inputs
- Current runtime contracts in `spec/` and `contracts/`.
- Model capability assumptions (context length, reasoning quality, tool fluency).
- Current defaults for retrieval, summarization/compaction, and tool schemas.
- Multi-agent split decisions and their rationale.
- Budget constraints (steps, time, cost) and compliance constraints.

### Outputs
- **Architecture Ceiling Test Report** (Markdown): a structured audit of ceilings, their rationale, and mitigation.
- **Ceiling Inventory** (table or list): each potential ceiling with classification, impact, and removal path.

## Guarantees
- **No silent ceilings**: every hard constraint that could limit model capability is explicitly listed with a rationale.
- **Goal-first constraints**: where feasible, constraints are expressed as goals and typed guardrails rather than hard-coded decision trees.
- **Scalability posture**: stronger models should improve outcomes by configuration changes (budgets, thresholds) rather than code changes.
- **Enterprise alignment**: constraints justified by compliance, provenance, latency, or cost are treated as intentional guardrails, not accidental ceilings.

## Stop semantics
- If the audit identifies any **unjustified artificial ceiling** with no mitigation or removal path, the system is not cleared for release until the ceiling is addressed or explicitly accepted by `BUILDER_USER` as a trade-off.

## Ceiling categories (what to look for)
These categories are tested each time the audit is run:

1) **Hard-coded decision trees**
   - Risk: a smarter model could handle decisions dynamically, but the architecture forces fixed branches.
   - Requirement: replace with typed constraints or policy goals where possible.

2) **Aggressive summarization and irreversible compression**
   - Risk: model capability is wasted because critical information is discarded too early.
   - Requirement: compaction must preserve evidence pointers and constraints per `spec/SUMMARIZATION_SCHEMA.md`.

3) **Rigid tool schemas**
   - Risk: tool interfaces constrain how a better model could compose actions.
   - Requirement: schemas must be typed but extensible (allow metadata fields or versioned extensions).

4) **Multi-agent splits without clarity gain**
   - Risk: multi-agent structure exists only to work around weak model reasoning.
   - Requirement: per `spec/MULTI_AGENT_SCOPE.md`, each split must have a clear isolation or correctness rationale and a single-agent fallback path.

5) **Overly fixed thresholds**
   - Risk: fixed top-N retrieval, rerank thresholds, or hard caps become ceilings instead of tunable controls.
   - Requirement: thresholds must be configuration-driven, with documented change conditions.

## Default vs requirement
### Requirements
- **Ceiling inventory** must include:
  - `ceiling_id`
  - `category`
  - `description`
  - `justification` (safety/compliance/budget vs accidental)
  - `impact` (what capability is blocked)
  - `mitigation` (what to change to remove the ceiling)
  - `owner` (role responsible)
- **Model-upgrade simulation**: audit must explicitly answer whether a stronger model would improve results without code changes.
- **Constraint taxonomy**: every constraint must be tagged as one of:
  - `SAFETY/COMPLIANCE`
  - `BUDGET/LATENCY`
  - `DATA/PROVENANCE`
  - `ARTIFICIAL/ACCIDENTAL`
- **Traceability**: each ceiling must reference the contract or module that introduces it.

### MVP defaults (changeable with evidence-based metrics)
- **Audit trigger**: run the ceiling test before any model upgrade and before any PR that adds a new hard constraint.
- **Ceiling severity**:
  - `critical`: blocks evidence quality or causes model regression.
  - `medium`: reduces efficiency or recall but has a mitigation path.
  - `low`: cosmetic or easily parameterized.
- **Acceptance bar**: zero critical artificial ceilings at release; medium ceilings require explicit acceptance with a dated mitigation plan.

## Test procedure (minimum)
1) Inventory all hard constraints and thresholds across specs (retrieval, compaction, tool schemas, multi-agent splits, budgets).
2) Classify each constraint using the taxonomy above.
3) For each `ARTIFICIAL/ACCIDENTAL` ceiling, provide a removal or parameterization path.
4) Simulate a stronger model by increasing context/budgets and relaxing non-safety caps; confirm that the architecture benefits without code changes.
5) Record outcomes in the Architecture Ceiling Test Report.

## How to verify
- Run the audit and confirm:
  - A complete ceiling inventory exists and references the introducing contract.
  - No critical artificial ceilings remain.
  - Each ceiling has a mitigation or acceptance decision.
- Perform a model-upgrade dry run (larger context/budgets) and confirm improved outcomes without code changes.

