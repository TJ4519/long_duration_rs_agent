# External Memory Architecture (Prompt Pack #6)

## Purpose
Define the external memory architecture for Project Alexandria with a local-first, audit-grade design that cleanly upgrades to managed storage later.

## Inputs/Outputs
### Inputs
- `run_id`, step context, and runtime events.
- Prebuilt corpus index and chunk provenance (ingestion is out of scope for runtime).
- Evidence ledger and manifests referenced by ID.

### Outputs
- Persistent runtime state in Postgres (metadata, snapshots, evidence ledger, manifests, events).
- Persistent artifacts on filesystem (tool outputs, PDFs, slices) addressed by run-scoped paths with hashes.
- Pointers (not blobs) linking DB records to filesystem artifacts and evidence slices.

## Guarantees
- **Auditability**: Event log is the authoritative history; snapshots are authoritative runtime state; evidence ledger is authoritative for claims/evidence.
- **No blob drift**: DB stores pointers/metadata only (no blobs >64KB); filesystem is authoritative for raw bytes.
- **Rehydration predictability**: Runtime reads snapshots + recent events (not full log replay) under bounded latency; log replay is for verification/recovery.
- **Integrity**: Artifacts carry hashes; evidence IDs are deterministic and namespaced by corpus/index identity.
- **Retention**: MVP retains all artifacts indefinitely (audit-first posture).

## Stop semantics
- If a critical pointer (e.g., evidence slice, manifest, required artifact) cannot be resolved:
  1) Retry once (to cover transient FS/IO).
  2) If still missing, stop the run with `SYSTEM_ERROR` and log the missing pointer type/id/path/hash.
- Non-critical cached tool outputs may be skipped only if they are not used for evidence/manifests/claims.

## Default vs requirement
### Requirements
- Authoritative stores:
  - Event log: authoritative for history/audit (append-only).
  - Snapshots: authoritative for runtime working state (materialized checkpoints).
  - Evidence ledger (claims/evidence): authoritative for all claim/evidence records.
  - Context manifests: authoritative for “what was in the window and why”; stored inline in DB (JSON).
  - Filesystem artifacts: authoritative for raw bytes (tool outputs, PDFs, slices); DB holds pointers only.
- Derived only: narrative markdown and any template renderings.
- Pointer-only rule: DB must not store blobs >64KB; pointers include path + hash (integrity).
- Evidence pointer shape: `evidence_id` (deterministic, namespaced by `corpus_id/index_id`) + `chunk_id` + `span`.

### MVP defaults (changeable later)
- **Storage stack**: Local Postgres + local filesystem. S3 is a later swap for filesystem; managed Postgres is a later swap for DB.
- **Retention**: Keep everything indefinitely (DB + filesystem).
- **Artifact layout**: Run-addressed filesystem paths with hash metadata (no dedup required). Hash is stored in DB for integrity/idempotency.
- **Artifacts table (Postgres)**:
  - Single table with PK `artifact_id`; columns `{run_id, step_id, path, hash, mime_type, size_bytes, created_at, metadata jsonb}`.
  - Indexes: `(run_id, step_id)` and `hash`.
- **Snapshots vs log**:
  - Runtime uses snapshots + events since last snapshot for state; log replay is for recovery/verification.
  - Snapshots are append-only; a “latest pointer” may be kept for convenience.
- **Manifests**: Stored inline in DB as JSON with `manifest_id`; referenced by ID from snapshots/events.

## Pointer semantics
- Artifacts: `artifact_id`, `run_id`, `step_id`, `path`, `hash`, `mime_type`, `size_bytes`.
- Slices/tool outputs: `artifact_id` + `offset/span` (or slice descriptor) + `mime_type`; no blobs in DB.
- Evidence: `evidence_id` (deterministic, namespaced) + `chunk_id` + `span`.
- Manifests: `manifest_id` with inline JSON (DB).

## How to verify
- Store an artifact and read back the metadata: hashes match; DB holds no blob.
- Attempt to resolve a missing pointer: system retries once; if missing, stops with `SYSTEM_ERROR` and logs diagnostics.
- Insert and read a manifest: stored inline JSON; referenced by ID from snapshots/events.
- Check DB schema: artifacts table exists as single table; indexes present on `(run_id, step_id)` and `hash`.
