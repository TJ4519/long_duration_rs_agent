# Codex Agent Handoffs

This folder stores **Codex builder-agent handoff notes** (planning + implementation continuity).

## Boundary (do not mix domains)
- These handoffs are **builder-domain artifacts** (how we build Alexandria).
- Project Alexandria **runtime** contracts live in `spec/` and `contracts/`.
- Do not treat handoff notes as runtime guarantees; they are operational continuity notes for Codex sessions.

## Usage
- Start a new session by reading the newest handoff first, then rehydrate from canonical runtime artifacts as directed by the handoff.
- The most recent handoff is recorded in `ops/codex_handoffs/LATEST.md`.
