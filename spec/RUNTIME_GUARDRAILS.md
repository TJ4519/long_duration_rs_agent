# Runtime Guardrails (Tool I/O, Loop Control, Schema Enforcement)

## Purpose
Define runtime guardrails that prevent context flooding, blind-alley failures, infinite loops, and invalid structured outputs.

## Inputs/Outputs
### Inputs
- `run_id`, `step_id`, and run invariants.
- Tool invocations (name + args) and tool outputs.
- Plan JSON outputs and tool argument payloads.

### Outputs
- Truncated tool outputs with pagination metadata.
- Typed validation error events and repair attempts.
- Typed override constraints when loop conditions are detected.

## Guarantees
- **Tool I/O bounded**: File-read tools must enforce hard caps and return pagination metadata.
- **Path hygiene**: Paths in context must be normalized to workspace-relative form.
- **Zero-result feedback**: Search tools returning zero results must emit a guidance prompt for the next navigation step.
- **Unknown tool handling**: Tool calls to undefined names must emit a typed error and force correction (no silent failure).
- **Loop guard**: Repeated identical actions trigger a typed override constraint.
- **Schema enforcement**: Structured outputs and tool arguments are validated by a decoding layer; invalid JSON triggers repair before execution.

## Stop semantics
- If schema repair fails after the configured attempts, stop the run with `SYSTEM_ERROR` and log validation diagnostics.
- If loop repetition persists after a loop override, stop the run with `SYSTEM_ERROR` and log the repeated action signature.

## Default vs requirement
### Requirements
- **File-read caps**:
  - File-read tools (e.g., `read_file`) MUST enforce a hard limit (lines or tokens).
  - Responses MUST include pagination metadata: `lines_shown`, `lines_remaining`, and `has_more`.
- **Path normalization**:
  - All paths inserted into L1/L2 context MUST be normalized to workspace-relative paths.
- **Zero-result feedback**:
  - If a search returns zero results, the response MUST include a guidance message (e.g., "no matches found; try `ls`, check alternate naming, or broaden filters").
- **Unknown tool errors**:
  - If a tool name is not registered, the runtime MUST emit a typed error event and force a correction step.
- **Loop detection**:
  - Runtime MUST hash the last N actions (action_type + tool name + args hash + target path) and compare for repetition.
  - On repetition beyond threshold, runtime MUST inject a typed override constraint (no free-text prompt rewriting).
- **Schema enforcement**:
  - Plan JSON, tool arguments, and output schemas MUST be validated by a decoding layer before use.
  - Invalid JSON MUST trigger a repair loop that returns the validation error and requires corrected output.
- **Budget enforcement**:
  - If `max_steps` is configured, it MUST be enforced as a hard limit unless explicitly marked soft.

### MVP defaults (changeable later)
- **read_file limit**: `max_lines=500`.
- **Pagination metadata**: `lines_shown`, `lines_remaining`, `has_more` (boolean).
- **Loop detection**:
  - `REPEAT_WINDOW`: 3 steps.
  - `LOOP_REPEAT_THRESHOLD`: 3 identical action signatures.
  - `LOOP_OVERRIDE_MAX_RETRIES`: 1 (second repeat after override triggers stop).
- **Schema repair**: `REPAIR_MAX_ATTEMPTS`: 2.

**Change when**:
- Lower caps if context bloat or "lost in the middle" incidents rise.
- Raise caps if evidence coverage drops due to over-truncation.
- Adjust loop thresholds when false-positive overrides become common or when loop rate stays high.

## How to verify
- Read a file >500 lines and confirm output is truncated with pagination metadata.
- Run a search that yields zero results and confirm the guidance message is returned.
- Call an unknown tool and confirm a typed error event is emitted and correction is required.
- Repeat the same action signature 3 times and confirm a typed override is injected; repeat again and confirm `SYSTEM_ERROR`.
- Emit invalid JSON in a plan/tool args payload and confirm repair attempts are enforced and stop after the limit.
