# Run Report Template

## Purpose
Provide a standardized report template for each run that captures objective, budgets, stop reasons, evidence coverage, and traceability to manifests/events. This template is used for human review and auditability.

## Inputs/Outputs
### Inputs
- Run metadata (objective, budgets, stop reason)
- Outputs (ResearchOutput JSON + Final Report Markdown)
- Manifest/event identifiers

### Outputs
- A single Markdown report per run, following the template below.

## Guarantees
- Every report includes objective, stop reason, budgets used, docs accessed, retrieval stats, outputs paths, supervisor interventions, and links/IDs to manifests/events.

## Stop semantics
- The report must include the run stop reason and whether it was a hard or soft limit.

## Default vs requirement
- **Requirements**:
  - All required sections appear in the report.
  - IDs/links to manifests/events are present for traceability.
- **MVP defaults** (changeable with evidence-based metrics):
  - Report filename: `outputs/run_<run_id>/report.md`. Change when multi-run orchestration requires alternative paths.

## How to verify
- Produce a run report and verify all sections are present with non-empty values.
- Verify manifest/event IDs match stored artifacts.

---

## Template

# Project Alexandria — Run Report

## Objective
- `<objective>`

## Stop Reason
- `stop_reason`: `<STOP_REASON_CODE>`
- `limit_type`: `<HARD|SOFT|N/A>`

## Budgets Used
- `max_steps`: `<value or none>`
- `max_wall_time`: `<value or none>`
- `max_cost`: `<value or none>`
- `steps_used`: `<value>`
- `wall_time_used`: `<value>`
- `cost_used`: `<value>`

## Docs Accessed
- `source_ids`: `[ ... ]`
- `artifact_ids`: `[ ... ]`

## Retrieval Stats
- `candidates_retrieved`: `<count>`
- `candidates_selected`: `<count>`
- `reranker_model`: `<name/version>`
- `acceptance_threshold`: `<value>`

## Outputs
- `research_output_json_path`: `<path>`
- `final_report_markdown_path`: `<path>`

## Supervisor Interventions
- `overrides_applied`: `[ ... ]`
- `override_reasons`: `[ ... ]`

## Manifests & Events
- `context_manifest_ids`: `[ ... ]`
- `event_log_ids`: `[ ... ]`
- `snapshot_ids`: `[ ... ]`
