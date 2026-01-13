# Data Contract

## Purpose
Define the data boundary between ingestion/indexing and runtime execution. This contract eliminates ambiguity about where data is stored, how it is chunked, and what the runtime can assume about availability of indexed content.

## Inputs/Outputs
### Inputs
- **Offline ingestion artifacts** (required for MVP runtime):
  - Raw source files or URLs to be ingested.
  - Prebuilt index artifacts (vector + full-text) that reference chunk IDs.

### Outputs
- **Object storage artifacts**: Raw or heavy source data stored outside the database.
- **Database pointers**: Metadata and pointers to object storage, chunk tables, and embeddings.

## Guarantees
- **Offline ingestion for MVP**: Ingestion/indexing is **OFFLINE** for MVP. Runtime **assumes** an index exists and does not create it on the fly.
- **Storage boundary**: Any artifact larger than **64KB** MUST be stored in object storage. The database MUST store only pointers and metadata (no raw blobs beyond the limit).
- **Chunk provenance**: Every chunk must include offsets/spans and a link to the originating source artifact.

## Stop semantics
- If runtime detects missing index artifacts or missing chunk provenance, it must stop with **SYSTEM_ERROR** and record a clear diagnostic message.

## Default vs requirement
- **Requirements**:
  - Runtime must not ingest or re-index sources.
  - Artifacts >64KB must be stored in object storage with DB pointers only.
  - Chunk provenance (offsets/spans + source linkage) is mandatory.
- **MVP defaults** (changeable with evidence-based metrics):
  - **Default metadata predicates**: report date range + author/source applied on first pass. Change when recall is consistently low for queries that require broader provenance.
  - **Default date scope**: last 3 years when no user-provided date range exists. Change when trend queries regularly require older baselines or when recall drops below target thresholds.
  - **Chunk size**: MVP default = 800 tokens with 100 token overlap. Change when retrieval precision/recall metrics show a consistent drop in evidence coverage or excessive context bloat.
  - **Chunker strategy**: MVP default = sliding window over normalized text. Change when quote-level alignment or span extraction accuracy falls below target thresholds.
  - **Hybrid retrieval top-N**: MVP default = 40 candidates before rerank. Change when reranker acceptance rate or latency misses targets.
  - **Alternatives** (evaluate when MVP defaults degrade metrics):
    - Section-aware chunking using document headers/structure.
    - Semantic segmentation based on topic shifts.
    - Hybrid fixed/semantic chunking to improve citation spans.

## How to verify
- Ensure ingestion artifacts exist **before** runtime and runtime does not write ingestion outputs.
- Attempt a run without an index and verify **SYSTEM_ERROR** is produced.
- Inspect stored artifacts to confirm >64KB objects are only in object storage with DB pointers.
- Validate chunks contain offsets/spans and source references.
