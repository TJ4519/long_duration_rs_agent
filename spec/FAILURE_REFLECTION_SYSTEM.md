# Failure Reflection System (Prompt Pack #9)

## Purpose
Define how Project Alexandria detects failures, records them as structured memory deltas, and integrates them into future behavior without “warning-bloat” or brittle overcorrection.

This spec is complementary to `spec/RUNTIME_GUARDRAILS.md` (loop guard, schema repair, tool I/O caps) and to the memory/snapshot contracts (`spec/SUMMARIZATION_SCHEMA.md`, `spec/EXTERNAL_MEMORY_ARCHITECTURE.md`).

## Inputs/Outputs
### Inputs
- Runtime events and observations (errors, timeouts, validation failures, retrieval misses).
- Current plan (`spec/AGENT_BLUEPRINT.md` plan object) and step context.
- Context manifests, artifacts, and evidence pointers referenced by ID.
- Optional human feedback/corrections.

### Outputs
1) **Failure Record** (structured, append-only)
2) **Optional Resolution/Revision Record** (structured updates to failure status and usefulness)
3) **Optional Typed Override** (when a failure implies a concrete constraint; stored per `spec/AGENT_BLUEPRINT.md`)

## Guarantees
- **Elicit, don’t invent**: failure records store what happened and what to do differently; they must not create new verified claims.
- **Pointer-first**: all failure records reference supporting context via IDs/pointers (manifest_id, artifact_id, query_id, chunk_id/span), not inline blobs.
- **Actionable integration**: failure records integrate via retrieval into compiled context only when relevant; they do not accumulate as an ever-growing “do not do this” list.
- **Auditability**: each failure record is traceable to the step, plan, and tool invocations that produced it.

## Stop semantics
- If failures indicate an unrecoverable situation (missing critical pointers, repeated schema repair failures, repeated loop detection beyond threshold), the system must stop with `SYSTEM_ERROR` or escalate to `ASK_HUMAN` per the plan/action contract.
- Failure reflection must not “paper over” unrecoverable errors: recording a failure is not a substitute for correct stop behavior.

## Default vs requirement
### Requirements
**A) Failure signals (must be detectable)**
The system must be able to capture at least these signal types:
1) **Tool/runtime errors**: exceptions, timeouts, missing pointer resolution.
2) **Retrieval/rerank failures**: low-confidence evidence, empty results, `NO_EVIDENCE` conditions.
3) **Schema/contract violations**: plan/output validation failures, schema repair loops.
4) **Loop/stall detection**: repeated queries/chunks/steps without progress.
5) **Human correction/feedback**: explicit user correction or override.
6) **Budget pressure**: soft-limit warnings and near-budget conditions.

**B) Failure record schema (binding)**
Each failure record must include:
- `failure_id` (string)
- `run_id` (string), `step_id` (int), `phase` (string)
- `signal_type` (enum)
- `severity` (enum: `low|medium|high|critical`)
- `fingerprint` (stable signature used for dedup/repeat detection)
- `attempted_action` (structured; references plan/action/tool call IDs)
- `observed_outcome` (structured; error/timeout/validation outcome)
- `recommended_adjustment` (structured; typed suggestion, not free-text prompt rewriting)
- `context_refs` (pointers only): `manifest_id`, `artifact_ids`, `query_id`, `chunk_id/span` or `evidence_id` where relevant
- `created_at` (timestamp)

**C) Integration rules (binding)**
- Failure records are stored indefinitely for audit (per `spec/EXTERNAL_MEMORY_ARCHITECTURE.md` retention posture), but **prompt inclusion is selective**.
- The compiler must retrieve only the **top-k relevant** failure records for the current step (by fingerprint match and/or similarity over structured fields).
- Inclusion must be deterministic: stable ranking and ordering.
- Failure records must not be injected as free-form “warnings”; they must be rendered as compact, structured guidance (e.g., “If tool X timed out, cap output to Y; paginate.”).

**D) Decay and revision (binding)**
- Failure records must support resolution/revision:
  - `status`: `active|resolved|superseded`
  - `occurrence_count` (per run)
  - `last_seen_step_id`
  - `helpful_count` / `harmful_count` (when the system can infer outcomes)
- Integration must favor:
  - higher severity,
  - more recent occurrences,
  - higher helpfulness,
and must suppress records marked `resolved|superseded` unless needed for audit.

### MVP defaults (changeable with evidence-based metrics)
**Scope**
- Failure reflection is **run-scoped** by default (no cross-run global failure memory in MVP).

**Repeat thresholds (MVP)**
- If the same `fingerprint` occurs ≥3 times within a run without progress, escalate:
  - `ASK_HUMAN` if clarification can unblock,
  - `SYSTEM_ERROR` if it indicates an unrecoverable invariant breach (e.g., missing critical pointers).

**Top-k inclusion**
- Include at most `k=5` failure records in compiled context per step, ordered deterministically.

**What justifies changing defaults**
Adjust thresholds and top-k based on:
- loop rate reduction,
- decreased repeated failures per run,
- stable evidence coverage rate,
while keeping latency/cost per step acceptable.

## Fingerprint design (how to make failures reusable without bloat)
The fingerprint should be deterministic and derived from structured fields, e.g.:
- `signal_type`
- `tool_name` + `error_code` (if applicable)
- normalized `query_id` or retrieval configuration signature
- repeated `chunk_id` set signature (for loop detection)

This enables:
- deduplication (“same failure keeps happening”),
- targeted retrieval (“only show failures relevant to this tool/query mode”),
- measurable loop prevention.

## How to verify
- Inject each failure signal type and confirm a failure record is written with pointer refs.
- Confirm repeated identical failures produce the same fingerprint and increment occurrence counters.
- Confirm compiler inclusion:
  - includes only top-k relevant records,
  - excludes resolved/superseded records,
  - ordering is deterministic.
- Confirm escalation behavior at repeat threshold (ASK_HUMAN vs SYSTEM_ERROR).

