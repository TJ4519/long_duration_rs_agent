# Project Alexandria — Human Blueprint (v1)

## 1. What this system is
Project Alexandria is a long-running research agent that can operate over a 4,000+ document corpus and produce research outputs with evidence.

Key idea: the LLM is a stateless CPU. We do not append chatlogs. We compile a fresh, relevant context for every step.

## 2. The core problem we are solving
Long-duration research fails for three predictable reasons:
1) Context rot: the prompt becomes stale, contradictory, and overfilled.
2) Heavy I/O: PDFs/HTML/large texts crash services or pollute context.
3) Precision: scientific research requires high signal retrieval and evidence grounding.

## 3. Design principles (what we will not violate)
1) Stateless inference: state lives in storage, not in the model.
2) Compiled context: each step builds L1 context from scratch.
3) Data gravity: large artifacts live in object storage (S3/local). DB stores pointers + slices.
4) Dual-track memory:
   - Structured (for programmatic control, loop prevention, metrics)
   - Narrative (for nuance: uncertainty, strategy, conflicts)
5) Evidence-first outputs: claims must be tied to citations; summaries cannot invent facts.

## 4. System components (plain English)
A) Orchestrator (FastAPI/worker):
- runs the step loop: COMPILE → PLAN → ACT → OBSERVE → (CHECKPOINT) → EGRESS
- stores an event log so we can replay/debug

B) Context Compiler:
- turns the current goal + recent events + memory into a curated prompt
- does retrieval + reranking + assembly
- produces a Context Manifest per step (auditability)

C) Artifact Manager:
- streams ingestion of heavy objects (PDFs, large HTML)
- stores objects in object storage
- writes pointer metadata into DB
- supports "slice inflation" (fetch only relevant excerpt)

D) Memory System:
- L2 Event Log: immutable record of what happened
- L3 Snapshots: compressed state (structured + narrative)
- Evidence Ledger: claims and citations that can be audited

E) Retrieval Engine:
- hybrid retrieval (vector + full-text + metadata filters)
- reranker (judge) for high precision context selection

## 5. Memory layers
L1 Hot: compiled prompt context (ephemeral)
L2 Warm: event log for the run (append-only)
L3 Warm: snapshots + structured state + evidence pointers
L4 Cold: heavy artifacts in object storage

## 6. The step lifecycle (what happens repeatedly)
1) COMPILE
- build a standalone query + intent
- retrieve candidates
- rerank candidates
- assemble L1 prompt
- write a Context Manifest

2) PLAN
- decide the next action type (search, fetch slice, synthesize, ask human)
- output must be structured JSON (schema validated)

3) ACT
- run tools (search, fetch, artifact slicing)
- store results as events and/or artifacts

4) OBSERVE
- update structured state: processed sources, new claims, conflicts
- update narrative: what changed, uncertainty, next step

5) CHECKPOINT (periodic)
- run compaction (dual-track)
- validate invariants and evidence consistency

6) EGRESS
- produce final or interim outputs (report JSON + readable markdown)
- store outputs + references to evidence + manifests

## 7. Summarization / compaction (anti-drift)
We compact periodically using dual-track:
- Track A (structured delta): new source_ids, new claims, query failures, conflicts
- Track B (narrative update): what changed, what’s uncertain, what to do next
Rule: narrative cannot create new claims unless evidence ledger is updated with citations.

We run "summary unit tests":
- objective unchanged
- invariants unchanged
- verified claims must have ≥1 citation
- conflicts must have ≥2 citations (two sides)

## 8. What success looks like (demo definition)
Given an objective like: "Find evidence linking compound X to liver failure in 2023 studies"
The system produces:
- key findings with citations (doc_id + chunk + quote/span)
- conflicts/contradictions with citations on both sides
- limitations ("what we could not verify")
- run manifest references for reproducibility

## 9. Known limits / non-goals (v1)
- Not a fully autonomous production on-call agent
- Not perfect recall; we optimize precision
- Supervisor loop is typed constraints only (no free-text prompt rewriting)
- If retrieval fails, system must admit ignorance or request clarification

## 10. Risk hotspots (where we must be careful)
- chunking + provenance mapping (citations must be reproducible)
- reranker thresholds and fallback behavior
- summary drift (narrative smoothing contradictions)
- idempotency of artifact ingestion
- cost/latency blowups from reranking
