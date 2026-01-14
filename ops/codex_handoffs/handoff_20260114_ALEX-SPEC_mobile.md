# Codex Handoff (Mobile Continuation)

## Identity + Scope (must adopt verbatim)
- `identity_id`: `ALEX-SPEC`
- `active_roles`: `["principal-architect", "contract-first-editor", "doc-only"]`
- `builder/runtime boundary`: enforce `BUILDER_*` vs `RUNTIME_*` terminology and artifact boundaries per `/Users/singh/Desktop/rs_agent/AGENT.MD`.
- `scope`: Prompt pack synthesis/spec thinking only (no runtime implementation code changes unless `BUILDER_USER` explicitly changes scope).

## Canonical Rehydration Sources (read in order)
1) `/Users/singh/Desktop/rs_agent/AGENT.MD`
2) `/Users/singh/Desktop/rs_agent/handoff_13jan_Codex_mobile.md`
3) `/Users/singh/Desktop/rs_agent/long_duration_rs_agent/spec/HUMAN_BLUEPRINT.md`
4) `/Users/singh/Desktop/rs_agent/long_duration_rs_agent/spec/AGENT_BLUEPRINT.md`
5) `/Users/singh/Desktop/rs_agent/long_duration_rs_agent/spec/REVIEW_MAP.md`
6) `/Users/singh/Desktop/rs_agent/long_duration_rs_agent/ops/STATUS.md`
7) `/Users/singh/Desktop/rs_agent/long_duration_rs_agent/ops/TASK_LOG.md`
8) `/Users/singh/Desktop/rs_agent/long_duration_rs_agent/review/PR13_REVIEW_BUNDLE.md`
9) `/Users/singh/Desktop/rs_agent/long_duration_rs_agent/contracts/openapi.json`
10) `/Users/singh/Desktop/rs_agent/long_duration_rs_agent/contracts/output_schema.json`
11) `/Users/singh/Desktop/rs_agent/long_duration_rs_agent/contracts/prompts_manifest.json`
12) `/Users/singh/Desktop/rs_agent/long_duration_rs_agent/contracts/migrations_summary.md`

## Verbatim: last three messages in this thread (no edits)

### (1) BUILDER_USER
“The truth is that I simply don't know even order of mangnitude since what could the event even represent,you bring up a point about taxonomies that is underexplored and needs to be spelt out to me fully from an analytical, RAG expertise angle”

### (2) BUILDER_AGENT (ALEX-SPEC)
“You’re right: before you can pick thresholds, you need a crisp mental model of what an “event” is. In RAG/long-running agents, “event taxonomy” isn’t bookkeeping—it’s how you make the system *observable*, *controllable*, and *evaluable*.

### What an “event” represents (RAG expertise framing)
An event is an **append-only, typed record of something that happened** that you might later need to:
- debug (“why did retrieval fail?”),
- audit (“what evidence supported this claim?”),
- prevent loops (“we already tried that query/tool call”),
- evaluate (“did we write a manifest each step?”).

If it can’t serve at least one of those, it shouldn’t be an event.

### The key mistake to avoid
Counting “events” only makes sense if events are **stable units**. If you log every micro-thing (token counts, intermediate lists), you’ll get 30–200 events/step. If you only log phase transitions, you’ll get 3–6 events/step. Both are “right,” but thresholds mean different things.

So we need two layers:

1) **Event log** (rich, append-only, everything you might need)
2) **Compaction counter** (a stable, coarse measure used for triggering)

This is the simplest enterprise pattern: keep rich observability, but trigger on a stable proxy.

### A practical event taxonomy (coarse, stable, enterprise-friendly)
Per step lifecycle (COMPILE → PLAN → ACT → OBSERVE → CHECKPOINT → EGRESS), you can define a *small* set of canonical event types:

- `STEP_STARTED` / `PHASE_CHANGED` (phase transitions)
- `INTENT_COMPILED` (query decomposition / intent object produced)
- `RETRIEVAL_EXECUTED` (query + filters + topN + corpus/index IDs)
- `RERANK_EXECUTED` (model + threshold + scores summary)
- `CONTEXT_MANIFEST_WRITTEN` (manifest id)
- `PLAN_EMITTED` (action_type + rationale)
- `TOOL_CALLED` / `TOOL_RESULT_STORED` (pointer to artifact, not blob)
- `EVIDENCE_ATTACHED` (claim_id + evidence_id + chunk_id + span)
- `CONFLICT_RECORDED`
- `FAILURE_RECORDED` (type + where + why)
- `SNAPSHOT_WRITTEN` (compaction output id)
- `RUN_STOPPED` (stop_reason)

That’s “enterprise-grade”: each type is audit/debug useful.

### How to make “event_count” usable (the missing piece)
Don’t trigger compaction on “all events”. Trigger on a **counted subset** that approximates “how much the agent did / how much state changed”:

**Counted events (for threshold)**
- `RETRIEVAL_EXECUTED`
- `RERANK_EXECUTED`
- `TOOL_RESULT_STORED`
- `EVIDENCE_ATTACHED`
- `FAILURE_RECORDED`
- `CONFLICT_RECORDED`

**Not counted**
- `PHASE_CHANGED`, `STEP_STARTED` (too frequent, low signal)
- `CONTEXT_MANIFEST_WRITTEN` (required every step; counting it forces compaction cadence)
- `PLAN_EMITTED` (one per step, better handled by step fallback)
- purely diagnostic micro-events

Now “20 counted events” becomes meaningful: it roughly means “20 state-changing actions worth compacting,” regardless of how chatty the log is.

### Why this matters specifically for RAG
- RAG failures are usually about **retrieval loops**, **filter mistakes**, **evidence insufficiency**, or **summary drift**. Those correlate with the counted events above.
- Evaluation gates (e.g., manifest integrity, evidence coverage) map directly to specific event types—so your event taxonomy becomes your eval substrate.

### One question (to pin down the taxonomy in enterprise terms)
Do you want the event log to be **coarse-only** (just the canonical types above) or **coarse + verbose** (canonical types plus optional debug events), with compaction thresholds counting only the canonical “counted events”?”

### (3) BUILDER_USER
“I am now want of commiting this conversation as a context for picking it up tomorrow when I'm operating on mobile. I want you to ensure that lossy compression is avoided, and you're not to be lazy when creating a hand-off. This hand-off, should place the last three exchanges between me and you verbatim, and then synthesise the trajectory, analysis and decision points (compared to the intention, which was to look at the previous hand-off, examine the prompts and work off the shared knowledge of the MVP). Plan this out before you commit.”

## Trajectory (why we’re here)
- `BUILDER_USER`’s umbrella intent: use LLM expertise as a thinking partner to synthesize Nate’s long-running-agent lessons, progress through the prompt pack (#5–#12), then execute progressively to build an enterprise-grade agent.
- Current locus: Prompt pack **#5 Summarization Schema Design** (compaction / snapshotting), with enterprise audit/provenance framing, and explicit separation between builder-domain workflow and runtime-domain contracts.
- Constraint from prior handoff (`handoff_13jan_Codex_mobile.md`): contract-first workflow; ask clarifying questions; avoid inventing; prioritize auditability and evidence-first guarantees.

## Key analysis (what was clarified)
- **Enterprise binding artifact** for compaction is structured **JSON snapshot**; narrative is optional.
- Narrative should be **template-derived** from the JSON (no LLM call yet) to reduce drift, cost, and failure surface.
- Ingestion/indexing/chunking is a **separate module**; runtime agent assumes prebuilt index + chunk provenance exist.
- “Event-count threshold” is only meaningful if “event” is defined; we identified the need for a stable **event taxonomy** and a **counted events subset** (high-signal events).

## Decisions made (current working defaults)
- Compaction outputs:
  - Binding: **JSON snapshot**.
  - Optional: deterministic markdown narrative **template-derived from JSON** (no LLM call yet).
- Snapshot persistence:
  - Append-only snapshots + “latest pointer”.
  - MVP uses **full snapshots** (not delta chains).
- Evidence representation inside snapshots:
  - Store **pointers only** (no inlined raw evidence).
  - Pointer shape should include: `evidence_id` + `chunk_id` + `span`.
- Triggering:
  - Prefer threshold-based compaction with an N-step fallback.
  - Trigger proxy should start with deterministic counts (avoid token estimation “magic” early).
  - Event-count thresholds require defining which event types count.

## Open questions (to resolve next)
- Event taxonomy choice: coarse-only vs coarse + verbose logging (with thresholds counting only a stable subset).
- Define compaction snapshot JSON schema fields + required invariants:
  - invariants unchanged (objective/done definition)
  - verified claims have evidence
  - conflicts have ≥2 citations
  - explicit compaction failure semantics (retry vs error)
- Calibrate MVP defaults:
  - `EVENT_THRESHOLD` and `N_STEP_FALLBACK` should be sanity-checked against default `max_steps=12` runs.
- Evidence ID semantics:
  - deterministic vs random (lean deterministic), and whether to namespace by corpus/index version to avoid collisions across corpora.

## Next actions (pick up tomorrow)
1) Answer the pending question: coarse-only vs coarse + verbose event logging (threshold counts remain stable subset either way).
2) Specify the compaction JSON snapshot schema (fields + required invariants + failure semantics).
3) Specify the deterministic markdown narrative template sections derived from JSON.

## Session state file (for continuity)
- `/Users/singh/Desktop/rs_agent/ALEX_SESSION.json` contains the structured state used to generate future handoffs.

