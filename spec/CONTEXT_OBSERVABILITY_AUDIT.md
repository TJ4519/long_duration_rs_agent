# Context Observability Audit (Prompt Pack #11)

## Purpose
Define the observability contract that answers: **what did the RUNTIME_AGENT see, why did it see it, and what was available but excluded**.

This spec makes context construction auditable without defaulting to full prompt retention, using **context manifests by default** and **full prompt/intermediate logging only on faults**.

## Inputs/Outputs
### Inputs
- `run_id`, `step_id`, objective, and invariants.
- Context compiler outputs (retrieval query, candidates, reranker scores, selected chunks).
- Tool outputs and artifact pointers.
- Failure signals and override events.

### Outputs
- **Context Manifest** (required, per step): structured record of what is in L1 and why.
- **Inclusion Log** (required, per step): per-item inclusion rationale and provenance.
- **Exclusion Log** (required, per step): items considered but excluded and why.
- **Prompt Snapshot Artifact** (faults only): exact L1 prompt bytes and assembly metadata.
- **Tool Output Snapshots** (faults only): raw tool outputs captured as artifacts.

## Guarantees
- **Manifest-by-default**: every step writes a context manifest with inclusion + exclusion rationale.
- **Pointer-only**: manifests/logs store pointers and hashes, not raw blobs; artifacts carry raw bytes.
- **Fault snapshots**: when a fault occurs, the exact L1 prompt and intermediate tool outputs are captured as artifacts for forensic replay.
- **Reconstructability**: for non-fault steps, the manifest + pointers are sufficient to reconstruct the context at a best-effort level.
- **Auditability**: every context item is traceable to a source (user input, tool output, memory retrieval, summarization).

## Stop semantics
- If a manifest cannot be written for a step, the run must stop with `SYSTEM_ERROR` and log the failure.
- If a fault trigger occurs and a prompt snapshot cannot be stored, the run must stop with `SYSTEM_ERROR` and record the missing artifact pointer.

## Fault triggers (capture full prompt + intermediates)
A **fault** is any of the following events:
- `SYSTEM_ERROR`
- Schema repair failure (after max attempts)
- Loop guard override (repeat threshold exceeded)
- Tool execution error or timeout
- Missing critical pointer resolution (manifest/evidence/artifact)
- Explicit `RUNTIME_USER` or `BUILDER_USER` debug snapshot request

On any fault, the system MUST:
- Store the exact L1 prompt bytes as a **Prompt Snapshot Artifact**.
- Store raw tool outputs for the step as **Tool Output Snapshots** (artifact pointers), in addition to any truncated outputs used in context.

## Default vs requirement
### Requirements
- **Context Manifest** must include at minimum:
  - `run_id`, `step_id`, `snapshot_id`
  - `intent` object
  - `retrieval_query`
  - `candidate_chunk_ids`
  - `selected_chunk_ids`
  - `reranker_model` + `version`
  - `token_budget`
  - `compiler_version`
  - `prefix_hash` + `prefix_length` (per `spec/CACHE_STABILITY_OPTIMIZATION.md`)
- **Inclusion Log** must include per item:
  - `item_id` (chunk_id/artifact_id/evidence_id)
  - `item_type` (user_input|tool_output|memory|evidence|policy|summary)
  - `source_ref` (pointer to origin)
  - `included_reason` (retrieval trigger, plan dependency, policy requirement)
- **Exclusion Log** must include per item:
  - `item_id`
  - `item_type`
  - `excluded_reason` (score below threshold, budget limit, policy filter)
- **Prompt Snapshot Artifact** (faults only):
  - stored as an artifact with `{artifact_id, path, hash, size_bytes, created_at}`
  - referenced by event log + manifest
- **Tool Output Snapshots** (faults only):
  - stored as artifacts (raw bytes)
  - referenced by event log + manifest
- **Path normalization**: all artifact paths are workspace-relative and hashed (per `spec/RUNTIME_GUARDRAILS.md`).

### MVP defaults (changeable with evidence-based metrics)
- **Capture mode**: manifest-only by default; full prompt + intermediates only on fault triggers.
- **Retention**: prompt snapshots are retained for a shorter window than manifests (policy-defined) to minimize sensitive data exposure.
- **Sampling (optional)**: if silent regressions are common, capture 1 in N successful prompts as debug snapshots.

## How to verify
- Run a normal step and confirm a manifest with inclusion/exclusion logs is stored.
- Trigger a schema repair failure and confirm:
  - a prompt snapshot artifact is stored,
  - tool output snapshots are stored,
  - manifest/event log references the artifacts.
- Confirm no raw blobs >64KB are stored in DB; only pointers are stored.
