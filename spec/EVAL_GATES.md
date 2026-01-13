# Eval Gates

## Purpose
Define evaluation metrics, golden-query artifacts, and pass/fail gates for the MVP. This establishes objective, reproducible acceptance criteria for the system’s behavior.

## Inputs/Outputs
### Inputs
- **Golden queries artifact** (required): JSON file defining objectives and expected evidence coverage.
- **Run outputs**: ResearchOutput JSON and associated manifests/events.

### Outputs
- **Eval report**: JSON or text summary containing metric scores and pass/fail status.

## Guarantees
- Eval must be deterministic for a fixed set of outputs and golden queries.
- Eval must operate on stored artifacts; it must not depend on model self-reporting.

## Stop semantics
- If the golden queries artifact is missing or malformed, evaluation stops with **SYSTEM_ERROR** and reports the missing requirement.

## Default vs requirement
- **Requirements**:
  - Eval must compute and report all metrics listed below.
  - Pass/fail status must be explicit for each gate.
- **MVP defaults** (changeable with evidence-based metrics):
  - Gate thresholds below are MVP defaults and should change only after collecting baseline runs across representative objectives.

## Metrics (2–4) and computation
1) **Evidence Coverage Rate**
   - **Definition**: % of verified claims that have ≥1 evidence record with quote/span and provenance.
   - **Computation**: count(verified claims with evidence) / count(verified claims).
2) **Golden Recall**
   - **Definition**: % of required golden evidence IDs present in the output evidence ledger.
   - **Computation**: count(matched golden evidence IDs) / count(total golden evidence IDs).
3) **Abstention Accuracy**
   - **Definition**: % of runs that correctly abstain when no acceptable evidence is available.
   - **Computation**: count(runs with stop_reason=NO_EVIDENCE AND no verified claims) / count(runs labeled as evidence-insufficient in golden queries).
4) **Manifest Integrity**
   - **Definition**: % of steps with a recorded context manifest.
   - **Computation**: count(steps with manifest) / count(total steps).

## Golden queries artifact format
- File: `eval/golden_queries.json`
- Schema (MVP default):
  - `objective` (string)
  - `required_evidence_ids` (array of strings)
  - `evidence_sufficient` (boolean)

## Eval command
- `python scripts/eval.py --golden eval/golden_queries.json --outputs ./outputs`

## Pass/fail gates (MVP defaults)
- **Evidence Coverage Rate**: ≥ 0.95
- **Golden Recall**: ≥ 0.80
- **Abstention Accuracy**: ≥ 0.90
- **Manifest Integrity**: = 1.00
