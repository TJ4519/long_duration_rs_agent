# User Contract

## Purpose
Define the user-facing contract for a run: what inputs are accepted, what outputs are produced, and how the system decides to stop. This contract is the canonical interface between a human or external system and Project Alexandria, and it cross-references the execution lifecycle defined in `spec/AGENT_BLUEPRINT.md`.

## Inputs/Outputs
### Inputs
- **objective** (required): The research goal for the run.
- **budgets** (optional):
  - **max_steps** (optional): Maximum number of step cycles.
  - **max_wall_time** (optional): Time cap for the run.
  - **max_cost** (optional): Budget cap for provider usage.

### Outputs
- **ResearchOutput JSON** (required): Schema-aligned output object (see `contracts/output_schema.json`).
- **Final Report Markdown** (required): Human-readable report artifact referencing the JSON output.

## Guarantees
- **Evidence-first claims**: Every **verified** claim MUST link to at least one evidence record with a quote/span and provenance fields. (See evidence ledger rules in `spec/AGENT_BLUEPRINT.md`.)
- **Abstain on insufficiency**: If retrieved evidence fails the evidence rule (e.g., no candidate chunk meets the retrieval/rerank acceptance criteria), the system MUST abstain from asserting a verified claim and MUST emit an explicit uncertainty or limitation note instead of guessing.

## Stop semantics
Runs end only with a structured **stop_reason** code. The run MUST record the stop reason in output metadata.

### Stop reason codes
- **OBJECTIVE_ACHIEVED**: All required outputs are produced with evidence-backed claims.
- **BUDGET_EXCEEDED**: A hard limit (steps/time/cost) is reached.
- **NO_EVIDENCE**: Retrieval/rerank yields no acceptable evidence for the objective after fallback (see `spec/AGENT_BLUEPRINT.md`).
- **HUMAN_REQUESTED**: Human or supervising system requests stop.
- **SYSTEM_ERROR**: A non-recoverable error occurs.

### Hard vs soft limits
- **Hard limit**: Exceeding a hard budget immediately triggers **BUDGET_EXCEEDED**.
- **Soft limit**: Exceeding a soft threshold should trigger a warning and request for human guidance, but does not stop the run on its own.

## Default vs requirement
- **Requirements**:
  - Inputs must include `objective`.
  - Outputs must include ResearchOutput JSON + Final Report Markdown.
  - Verified claims must have evidence with provenance.
  - Stop reasons must be explicit and recorded.
- **MVP defaults** (changeable with evidence-based metrics):
  - **max_steps**: MVP default = 12 steps. Change when median run success requires fewer/more steps to reach OBJECTIVE_ACHIEVED without increasing NO_EVIDENCE rate.
  - **max_wall_time**: MVP default = 15 minutes. Change when median run time consistently exceeds 80% of budget while still producing valid outputs.
  - **max_cost**: MVP default = $10/run. Change when cost per verified claim consistently exceeds acceptable threshold for the target use case.

## How to verify
- Create a run with a trivial objective and inspect output artifacts:
  - ResearchOutput JSON exists and validates against `contracts/output_schema.json`.
  - Final Report Markdown exists and references the JSON output.
  - Any verified claims contain at least one evidence record with quote/span and provenance fields.
- Force a budget exceed condition and verify **BUDGET_EXCEEDED** is recorded.
- Force a retrieval miss and verify **NO_EVIDENCE** is recorded with abstention.
