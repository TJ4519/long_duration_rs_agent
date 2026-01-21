# Cache Stability Optimization (Prompt Pack #8)

## Purpose
Define prompt cache stability rules that minimize latency and cost for long-running runs by maximizing prefix cache hits.

## Inputs/Outputs
### Inputs
- System prompt, tool schemas, static policies.
- Per-step dynamic inputs (objective, plan, retrieval outputs).

### Outputs
- Deterministic prompt assembly strategy that preserves cacheable prefixes.
- Recorded prefix hashes for cache monitoring in manifests.

## Guarantees
- **Immutable cached prefix**: Within a run, cached prefix tokens are identical across steps.
- **Dynamic data moved to suffix**: Per-step variables never appear in the cached prefix.
- **Deterministic serialization**: All structured content in the prefix uses stable key ordering and formatting.
- **Stable tool ordering**: Tool schema order is fixed within a run.

## Stop semantics
If the system detects prefix instability that drops cache hit rate below the target threshold:
1) Emit a warning in the run log.
2) Request human guidance if the instability is persistent.

## Default vs requirement
### Requirements
- No timestamps, counters, or random IDs in cached prefix tokens.
- Provider cache boundary support (if available) must be used to isolate dynamic sections.
- Prefix hash recorded per step in the context manifest.

### MVP defaults (changeable with evidence-based metrics)
- Target cache hit rate: ≥ 0.8 (adjust when median latency/cost per step exceeds budget).
- Prefix hash storage: stored in manifest with `prefix_hash` and `prefix_length`.
- Breakpoint placement:
  - OpenAI/Anthropic: keep static content first; dynamic content only after cached prefix.
  - Anthropic: use `cache_control` breakpoints at end of stable sections.
  - Gemini: prefer explicit caching for large stable context; rely on implicit caching only with stable prefixes.

## How to verify
- Validate that `prefix_hash` is identical across steps in a run.
- Inject a timestamp into the prefix and confirm cache hit rate drops (non-production test).
- Confirm that reordering tool schemas changes the prefix hash and is flagged.
