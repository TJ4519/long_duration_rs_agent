# Multi-Agent Scope Design (Prompt Pack #7)

## Purpose
Define when and how Project Alexandria may split into multiple agents, and the handoff contract between them. The goal is to gain context isolation and auditability without uncontrolled cross-agent chatter.

## Inputs/Outputs
### Inputs
- `run_id`, current `objective`, and run invariants.
- Planner outputs (typed plan object).
- Evidence ledger, manifests, and artifacts referenced by ID.

### Outputs
- Structured handoff artifacts between agents (plan + manifests + evidence pointers).
- Event log entries and snapshots that reflect cross-agent transitions.

## Guarantees
- **Isolation by design**: Each agent operates in its own context window; no shared chat logs.
- **Structured handoff only**: Agents exchange typed artifacts (plan JSON, manifests, evidence pointers), never free-form chat.
- **Auditability**: Every cross-agent handoff is logged as an event and is referenced in snapshots; no orphaned actions.
- **Evidence-first**: Executor cannot assert verified claims without evidence pointers; planner cannot bypass evidence rules.

## Stop semantics
- If a required handoff artifact (plan/manifests/evidence pointers) is missing or invalid:
  1) Reject the handoff, log the error, and retry handoff once.
  2) If still invalid, stop the run with `SYSTEM_ERROR` and record diagnostics.

## Default vs requirement
### Requirements
- Agent roles:
  - **Planner**: Produces a structured plan (action_type, rationale, expected outputs, stop_condition). No tool execution.
  - **Executor**: Executes tool calls, retrieval, evidence attachment, and emits events/snapshots.
- Handoff contract (Planner → Executor):
  - Plan JSON (as in `spec/AGENT_BLUEPRINT.md` plan object).
  - References only by ID/pointer (manifests, evidence pointers, artifact IDs); no inline blobs.
- Context isolation:
  - No shared conversational context; only structured artifacts are exchanged.
  - Executor may read run-level snapshots/manifests/evidence ledger via IDs, not via Planner’s context buffer.
- Event log:
  - Cross-agent handoff must emit an event recording handoff artifact IDs and the target agent role.
- Snapshots:
  - Snapshots capture which agent produced which actions (e.g., `agent_role: PLANNER|EXECUTOR`).
- No free-form cross-agent chat:
  - Agents must not exchange unstructured messages; all communication is via structured artifacts.

### MVP defaults (changeable later)
- Pattern: Optional **two-agent split** (Planner ↔ Executor) for isolation; default remains single agent when split is not needed.
- Trigger to split: Use Planner/Executor split when a plan requires multi-step tool/action execution that risks context bloat or looping; otherwise keep single-agent execution.
- Handoff retry: Retry invalid handoff once; then fail with SYSTEM_ERROR.
- Agent roles are fixed (no additional sub-agents) for MVP.

## How to verify
- Create a run that uses Planner → Executor handoff:
  - Handoff is logged as an event with artifact IDs; snapshot records `agent_role`.
  - Executor executes only from structured plan; no free-form chat content appears in logs between agents.
  - Verified claims produced by Executor have evidence pointers; Planner outputs do not circumvent evidence rules.
- Inject an invalid handoff (missing plan fields) and confirm:
  - Handoff is rejected, logged, retried once; on failure, run stops with SYSTEM_ERROR and diagnostic.
