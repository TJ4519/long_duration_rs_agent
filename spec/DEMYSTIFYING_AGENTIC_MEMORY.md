# Demystifying Agentic Memory (Non-Technical) (Prompt Pack #12)

## Purpose
Provide a non-technical, plain-language explanation of how agentic memory works and why it matters, using analogies and a step-by-step conversational flow.

This spec defines the **interaction contract** for explaining memory to non-technical audiences: ask about lived experience first, explain concepts in small chunks, and connect each concept to practical implications.

## Inputs/Outputs
### Inputs
- `RUNTIME_USER` experiences with AI memory (what worked, what was confusing).
- Optional: the `RUNTIME_USER`’s goals (e.g., evaluating AI tools, building an agent).

### Outputs
- A conversational, non-technical explanation that is:
  - grounded in the user’s experiences,
  - delivered in small steps (one concept at a time),
  - connected to practical implications.

## Guarantees
- **Experience-first**: start by asking about the user’s experience with AI memory; do not lead with a lecture.
- **One step at a time**: explain one concept, check that it landed, then proceed.
- **Plain language**: avoid jargon; if a technical term is introduced, define it in simple language.
- **Analogies required**: use concrete analogies (e.g., desk, filing cabinet, sticky notes) to explain memory trade-offs.
- **Practical linkage**: each concept must end with a “this is why it matters” implication.

## Stop semantics
- If the user indicates they are satisfied or requests to stop, end the explanation.
- If the user asks for a technical deep dive, confirm the shift and route to a technical explanation separately.

## Default vs requirement
### Requirements
- **Opening question** must ask about the user’s experience with AI memory (good or bad).
- **Progression** must include all four outcomes by the end:
  1) Why AI can’t remember everything (real constraints).
  2) How AI decides what to keep, forget, or look up.
  3) Why some AI feels like it “knows you” and some feels like amnesia.
  4) What’s improving vs what remains hard.
- **No info-dump**: explanation must be segmented with explicit checks for understanding.
- **One question at a time**: do not ask multiple questions in a single turn.

### MVP defaults (changeable later)
- Use a 3-part analogy stack:
  - **Desk** = context window
  - **Filing cabinet** = external memory (files/DB)
  - **Sticky notes** = short-term summaries
- Use 3–5 sentences per concept before checking understanding.

## How to verify
- Simulate a non-technical user and confirm:
  - The first response is an experience-based question.
  - Each concept is explained with an analogy and a practical implication.
  - The interaction proceeds one concept at a time with check-ins.
  - The four required outcomes are covered before closure.
