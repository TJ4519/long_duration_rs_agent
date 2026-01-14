# Summarization Schema Design (Compaction Snapshot Contract)

## Purpose
Define how Project Alexandria compacts long-running state without drift.

This spec defines:
- A binding **Compaction Snapshot JSON** (authoritative state).
- An optional **deterministic narrative Markdown** derived from the snapshot via template rendering (no LLM call).

This spec is part of the execution lifecycle described in `spec/AGENT_BLUEPRINT.md` and enforces the evidence-first guarantees in `spec/USER_CONTRACT.md`.

## Inputs/Outputs
### Inputs
- `run_id`, `objective`, and the “done definition” / invariants for the run.
- Append-only event log since the previous snapshot.
- Evidence ledger records referenced by ID.
- Context manifests for steps since the previous snapshot.

### Outputs
1) **Compaction Snapshot JSON** (required, canonical)
2) **Narrative Markdown** (optional, deterministic template-derived)

## Guarantees
- **Single source of truth**: The snapshot is canonical. Narrative is not authoritative.
- **No new verified claims**: Compaction must not create new verified claims unless they already exist in the evidence ledger with citations.
- **Evidence pointers only**: The snapshot must reference evidence via pointers and must not inline large/raw blobs.
- **Auditability**: The snapshot must preserve enough provenance to answer: what sources were cited, what filters were applied, and what was selected/excluded.

## Stop semantics
Compaction is a **hard validation gate**:
- If snapshot validation fails, the run must not proceed as if state is valid.
- **Failure behavior (MVP)**:
  1) Retry compaction once with the same inputs and deterministic rendering.
  2) If validation still fails, stop with **SYSTEM_ERROR** and record a clear diagnostic message.

## Default vs requirement
### Requirements
**A) Snapshot persistence**
- Snapshots are **append-only** (immutable).
- Each snapshot has a stable `snapshot_id`, a `sequence` number, and a `created_at` timestamp.
- A separate “latest snapshot pointer” may be maintained for convenience (not required by this spec).

**B) Snapshot validation invariants (binding)**
- `objective` and the “done definition” / invariants must not change across snapshots.
- Every **verified** claim must have ≥1 evidence pointer.
- Every recorded conflict must have ≥2 evidence pointers (two-sided citation requirement).

**C) Evidence pointer shape (binding)**
Evidence references must include:
- `evidence_id` (stable identifier)
- `chunk_id`
- `span` (start/end offsets or equivalent)

**D) Deterministic evidence IDs**
- `evidence_id` must be deterministic and namespaced by corpus/index identity to avoid collisions across corpora.
- **MVP approach**: derive `evidence_id` from (`index_id` or `corpus_id`) + `chunk_id` + `span` (+ optional `quote_hash`).

**E) Narrative (optional)**
- If produced, narrative Markdown must be rendered from snapshot JSON via a deterministic template (no LLM call).

### MVP defaults (changeable with evidence-based metrics)
**Compaction trigger**
- Primary: `counted_events_since_last_compaction >= EVENT_THRESHOLD`
- Fallback: `steps_since_last_compaction >= N_STEP_FALLBACK`

**Counted events definition (stable unit)**
- The event log may contain coarse and verbose events.
- Compaction counting includes only terminal events:
  - `PLAN_DONE`
  - `ACT_DONE`
  - `OBSERVE_DONE`
- This yields a stable default of **3 counted events per step**.

**Default thresholds**
- `EVENT_THRESHOLD` (MVP default): 18 counted events (~6 steps)
- `N_STEP_FALLBACK` (MVP default): 8 steps

**Tuning metric (what justifies changing defaults)**
Adjust thresholds based on:
- loop rate + constraint-forget incidents + **NO_EVIDENCE** stalls,
while keeping latency/cost per verified claim acceptable.

## Snapshot JSON shape (v1, canonical)
The snapshot is a single JSON object with stable keys.

### Top-level fields
- `snapshot_id` (string)
- `run_id` (string)
- `sequence` (int)
- `created_at` (ISO8601 string)
- `objective` (string)
- `done_definition` (object or string; must remain stable)
- `provenance_mode` (string; MVP default: `audit_only`)
- `policy_snapshot_ref` (string|null)
- `counts` (object):
  - `steps_since_last_compaction` (int)
  - `counted_events_since_last_compaction` (int)
- `latest_context_manifest_ids` (array of strings)
- `state` (object):
  - `claims` (array)
  - `conflicts` (array)
  - `open_questions` (array of strings)
  - `failures` (array)
  - `source_coverage` (object)
- `retrieval_diagnostics` (object; summary + pointers only)
- `validation` (object; see below)

### Claim object (minimum)
- `claim_id` (string)
- `status` (string; e.g., `verified`, `candidate`, `retracted`)
- `statement` (string)
- `evidence_refs` (array of evidence pointers)

### Conflict object (minimum)
- `conflict_id` (string)
- `description` (string)
- `side_a_refs` (array of evidence pointers)
- `side_b_refs` (array of evidence pointers)

### Failure object (minimum)
- `failure_id` (string)
- `category` (string)
- `where` (string)
- `why` (string)

### Source coverage (minimum)
- `source_ids_seen` (array of strings)
- `chunk_ids_seen` (array of strings)
- `chunk_ids_cited` (array of strings)

### Validation object (binding semantics)
- `status`: `PASS` | `FAIL`
- `checks`: array of `{name, status, message}`
- `failure_action_taken`: `NONE` | `RETRY` | `SYSTEM_ERROR`

## Narrative template (optional, deterministic)
If emitted, narrative Markdown must use a stable section order and must reference only snapshot content.

Suggested required sections:
1) Objective + budgets + provenance mode
2) What changed since last snapshot (counts + deltas)
3) Verified claims (each with evidence pointers)
4) Conflicts (two-sided pointers)
5) Failures encountered
6) Open questions / unknowns
7) Next actions (1–3)
8) Manifest references

## How to verify
- Create a synthetic run state and generate a snapshot:
  - JSON keys exist and types match this spec.
  - A `verified` claim without evidence pointers fails validation.
  - A conflict with fewer than two-sided evidence pointers fails validation.
- Determinism check: identical snapshot JSON yields identical narrative markdown output.
- Trigger check:
  - Add verbose/non-terminal events and confirm compaction cadence depends only on terminal `PLAN_DONE/ACT_DONE/OBSERVE_DONE` plus fallback steps.

