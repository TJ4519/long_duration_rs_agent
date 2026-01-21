# Project Alexandria — Agent Blueprint (Codex Implementation Brief)

## 0) Rules for agents
- Prefer small diffs. No refactors unless necessary.
- Everything must be reproducible: every step creates a Context Manifest.
- Output must be schema-validated (JSON), or fail fast.
- Evidence must be stored separately from narrative.
- If unsure: add TODO + explanation, do not guess silently.

## 1) Stack assumptions (edit as needed)
- Python 3.11+
- FastAPI
- Postgres + pgvector
- Object storage: local filesystem first (S3-compatible later)
- Embeddings via provider API (configurable)
- LLM calls via provider API (configurable)

## 2) Core modules + responsibilities
### app/orchestrator.py
Implements step state machine:
COMPILE → PLAN → ACT → OBSERVE → (CHECKPOINT) → EGRESS
Persists all step events.

### app/compiler/
- intent.py: stand-alone query + intent extraction (schema output)
- retrieval.py: hybrid retrieval (vector + FTS + metadata filters)
- rerank.py: batched reranking + caching
- assemble.py: build L1 prompt in stable order
- manifest.py: writes Context Manifest

### app/artifacts/
- manager.py: streaming ingestion + idempotency
- slicing.py: fetch excerpt by chunk_id/span

### app/memory/
- events.py: event log (typed events)
- snapshots.py: snapshot schema + read/write
- evidence.py: claims + claim_evidence
- compaction.py: dual-track compaction + validation
- overrides.py: strategic override constraints (typed, TTL)

### app/schemas/
- events.py
- outputs.py
- manifest.py
- plan.py
- overrides.py

## 3) Database schema (minimum required tables)
A) runs
B) agent_events (append-only)
C) agent_memory_snapshots (JSONB for narrative + summary view)
D) processed_sources (normalized coverage map)
E) failed_queries
F) artifacts (pointers + hashes)
G) chunks (chunk_id, source_id, artifact_id, offsets/spans, text_preview)
H) embeddings (chunk_id, vector)
I) claims
J) claim_evidence
K) context_manifests
L) outputs
M) active_strategic_overrides

## 4) Required object contracts (schemas)

### 4.1 Context Manifest (stored every step)
Fields:
- run_id, step_id
- snapshot_id used
- intent object
- retrieval query
- candidate_chunk_ids
- selected_chunk_ids
- reranker_model + version
- token budget info
- compiler version

### 4.2 Plan Object (the PLAN phase output)
Must be JSON with:
- action_type: SEARCH | FETCH_SLICE | SYNTHESIZE | ASK_HUMAN | STOP
- rationale (short)
- tool_calls (if any): name + arguments
- expected_output_artifacts: list of outputs that will be produced
- stop_condition (when to checkpoint/egress)

### 4.3 Evidence Objects
- Claim must link to evidence records
- Evidence records must include chunk_id + quote + span/page metadata

### 4.4 Strategic Override (Supervisor)
Typed constraints only, with TTL:
- tool_budget constraints
- force_action constraints
- widen_retrieval flag
No free-text system prompt rewriting.

## 5) Retrieval + reranking behavior
- Hybrid retrieval returns top-N candidates.
- Rerank in batches (1–3 calls) with DIRECT/CONTEXT/NOT labels + numeric score.
- If max_score < threshold:
  1) run deterministic retrieval fallback (widen filters, bigger N)
  2) if still low, inject constraint: "No direct evidence found; admit uncertainty."

## 6) Compaction rules
Trigger:
- every N steps OR when event log grows beyond threshold

Dual-track:
A) structured delta (new sources, new claims, failures, conflicts)
B) narrative update (what changed / uncertain / next)

Validation:
- invariants unchanged (objective/done definition)
- verified claims have evidence
- conflicts have ≥2 citations

If validation fails: retry compaction or raise error.

## 7) Implementation plan (PR-sized tickets)

PR1 — Scaffold + configs
- create modules and basic FastAPI app
- config system (env vars)
Done: app boots, tests run.

PR2 — DB schema + migrations
Done: tables exist and basic CRUD works.

PR3 — Artifact Manager (local storage) + idempotency hash
Done: ingest file/url stream → artifact pointer row.

PR4 — Chunking pipeline + chunk provenance mapping
Done: chunks table populated with offsets/spans.

PR5 — Embeddings + pgvector index + hybrid retrieval
Done: can retrieve top-N candidates.

PR6 — Reranker (batched) + cache
Done: returns labels + scores.

PR7 — Context compiler + manifest writer
Done: compile produces prompt + context manifest row.

PR8 — Step machine (orchestrator) + typed events
Done: can run 5–10 steps end-to-end in a demo run.

PR9 — Evidence ledger + output schemas
Done: produces ResearchOutput JSON with citations.

PR10 — Dual-track compaction + validation
Done: snapshot updates without drift.

PR11 — Supervisor (proactive) with typed overrides
Done: detects loop/stall and injects constraints.

PR12 — Demo CLI + golden eval harness
Done: run a sample objective and produce outputs folder + metrics.

## 8) Test/verification commands (placeholders)
- pytest
- python scripts/demo_run.py --objective "..."
- python scripts/eval.py --golden ./eval/golden.json

## 9) "Do Not Touch" constraints
- Never store raw >64KB text in DB events; store pointers.
- Never allow narrative summaries to introduce new verified claims without evidence.
