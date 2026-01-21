# Codex Handoff

## Identity
- `domain`: `builder`
- `identity_id`: `ALEX-SPEC`
- `active_roles`: ["principal-architect", "contract-first-editor", "doc-only"]

## Objective
- Synthesize Nate prompt-pack topics into enterprise-grade runtime contracts/specs for Project Alexandria (starting with #5 Summarization Schema Design), then progress sequentially toward an enterprise agent.

## Rehydration Sources Used (in order)
- `AGENT.MD`
- `handoff_13jan_Codex_mobile.md`
- `long_duration_rs_agent/spec/HUMAN_BLUEPRINT.md`
- `long_duration_rs_agent/spec/AGENT_BLUEPRINT.md`
- `long_duration_rs_agent/spec/REVIEW_MAP.md`
- `long_duration_rs_agent/ops/STATUS.md`
- `long_duration_rs_agent/ops/TASK_LOG.md`
- `long_duration_rs_agent/review/PR13_REVIEW_BUNDLE.md`
- `long_duration_rs_agent/contracts/openapi.json`
- `long_duration_rs_agent/contracts/output_schema.json`
- `long_duration_rs_agent/contracts/prompts_manifest.json`
- `long_duration_rs_agent/contracts/migrations_summary.md`
- `long_duration_rs_agent/review/PR16_REVIEW_BUNDLE.md`
- `long_duration_rs_agent/review/PR17_REVIEW_BUNDLE.md`

## Decisions
- Prompt pack #5: Compaction output uses a binding structured JSON snapshot; narrative is optional and must be strictly template-derived (no LLM call).
- Ingestion/indexing/chunking are out of scope for the runtime agent; runtime assumes prebuilt indexes exist.
- Compaction trigger should be threshold-based with an N-step fallback; MVP trigger proxy should be event-count-based (not token/bytes).
- Snapshot storage should be append-only (immutable history) with a 'latest pointer' for convenience; MVP uses full snapshots (not deltas).
- Evidence in snapshots should be stored as pointers, not inlined: use evidence_id plus chunk_id + span to support evals, auditability, and loop detection.
- Event-count thresholds require an explicit event taxonomy; compaction thresholds should count a stable subset of high-signal events rather than all emissions.
- Event log policy: coarse + verbose events allowed, but compaction thresholds count only terminal PLAN/ACT/OBSERVE counted events (stable unit of 3 counted events per step).
- MVP defaults confirmed: EVENT_THRESHOLD=18 counted events; N_STEP_FALLBACK=8 steps; compaction validation invariants are a hard gate per blueprint.
- Prompt pack #6: MVP runs locally with Postgres + filesystem object store; S3 is a later swap-in for object storage.
- Prompt pack #6: Retention policy (MVP): keep all run artifacts indefinitely (audit/provenance first).
- Prompt pack #6: Event log is authoritative for history/audit; snapshots are authoritative for runtime working state (materialized checkpoints). Rebuild-from-log is a verification/recovery path, not the default read path.
- Prompt pack #6: Filesystem object store is run-addressed with hash metadata; Postgres stores pointers only (no blobs >64KB).
- Prompt pack #6: Postgres artifacts table is single-table with artifact_id PK and columns {run_id, step_id, path, hash, mime_type, size_bytes, created_at, metadata jsonb}; indexed on (run_id, step_id) and hash.
- Runtime guardrails spec added: tool I/O caps + pagination metadata, zero-result guidance, loop detection with typed overrides, schema enforcement with repair loop.
- Prompt pack #7: Multi-agent scope design spec added (planner/executor split, structured handoff, isolation rules).

## Open Questions
- Confirm PR14 (Summarization Schema Design) is accepted/merged into main.
- Confirm PR15 (External Memory Architecture) is accepted/merged into main.
- Confirm PR17 (Runtime Guardrails) is accepted/merged into main.
- Confirm PR16 (Multi-Agent Scope Design) is accepted/merged into main.

## Next Actions (PR-sized where possible)
- Prompt pack #8: Draft cache stability optimization spec (prefix stability, caching breakpoints, deterministic assembly).

## Files Touched This Session (workspace)
- `AGENT.MD`
- `ALEX_SESSION.json`
- `tools/alex_handoff.py`

## Notes
Builder/runtime boundary enforced in workspace governance; handoff process is agent-driven with CLI as fallback.

## Metadata
- `generated_at_utc`: `2026-01-21T11:42:07Z`
- `generator`: `tools/alex_handoff.py`
