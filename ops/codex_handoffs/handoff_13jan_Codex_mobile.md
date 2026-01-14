# HANDOFF_CONTEXT.md

## 1) ROLE & CONSTRAINTS (verbatim from this thread)

### Role
- “You are my **Principal Architect** for Project Alexandria.”
- “You must follow the contract‑first workflow.”
- “Do **not** read implementation code unless explicitly instructed.”
- “Rehydrate context only from canonical artifacts.”
- “Every PR must include `review/PR_<NN>_REVIEW_BUNDLE.md` and updated `contracts/*`.”
- “Update `ops/STATUS.md` and `ops/TASK_LOG.md` every PR.”
- “Use small diffs; no refactors unless necessary.”
- “If uncertain, add TODO + explanation.”

### Canonical rehydration sources (read in order)
1) `spec/HUMAN_BLUEPRINT.md`
2) `spec/AGENT_BLUEPRINT.md`
3) `spec/REVIEW_MAP.md`
4) `ops/STATUS.md`
5) `ops/TASK_LOG.md`
6) `review/PR13_REVIEW_BUNDLE.md`
7) `contracts/openapi.json`
8) `contracts/output_schema.json`
9) `contracts/prompts_manifest.json`
10) `contracts/migrations_summary.md`

### Required output (before coding)
A) Summarize current state in 5–8 bullets (only from artifacts above).
B) Propose the next PR‑sized task toward the enterprise‑grade agent.
C) Confirm the review surface and required outputs for that PR.
D) Ask for confirmation before coding.

### Additional instructions from the thread
- “Create/update ONLY spec documents (no implementation code).”
- “Do NOT rewrite spec/HUMAN_BLUEPRINT.md or spec/AGENT_BLUEPRINT.md.”
- “Every spec must include: Purpose, Inputs/Outputs, Guarantees, Stop semantics, Default vs requirement, How to verify.”
- “If a value is a starter default, label it ‘MVP default’ and include what metric will justify changing it.”
- “Add a short index section to README.md linking to new specs.”
- “Produce review/PR_<NN>_REVIEW_BUNDLE.md summarizing only doc changes.”
- “Commit your changes on the current branch.”
- “Use the make_pr tool after git commit.”

---

## 2) USER INTENT (verbatim excerpts)

### Enterprise‑grade definition (verbatim)
- “What does enterprise‑grade mean? I would say it means token spend and latency and compliance with things like providence over what information is being looked at per department (this implies the user‑research agent contract definition).”

### Offline ingestion expectation (verbatim)
- “FOR OFFLINE INGESTION, yes I would like us to have an indexing and chunking system that is capable of ingesting new incoming reports— I haven't thought of a pipeline yet maybe I decide to download to s3 bucket and then run.”

### Intent decomposition motivation (verbatim)
- “Intent decomposition is a feature of promoting the research agent which is essentially implicating the run time user‑agent contract.”

### Data corpus (verbatim)
- “I was thinking about the following data corpus which is Michael Cembalest's reports which are usually not part of any training LLM corpus and is proprietary, and the composition of the reports covers a wide range of topics, and charts and figures.”

---

## 3) VERBATIM SOURCE MATERIALS FROM THIS THREAD

### 3.1 Cembalest notes (verbatim as provided)
- “Here's me opening Michael Cembalest's reports page and you see many pdfs.”
- (Screenshots were shared in the thread; no additional text was provided.)

### 3.2 DM with Francis (verbatim)
```
<Dm with Francis>
I also just remembered what inspired this idea of intent decomposition of prompts:
Hey TJ, these are great reflections and insights you've put together above! Forgive me for taking so long to answer; it's been a packed week. To tackle some of your questions:
• Yes, applying this type of reasoning across a large corpus is computationally expensive, and carries significant latency if tried to do during runtime.
• So preprocessing the corpus during ingestion (or at some point before runtime) becomes indispensable, in order to have these semantic enrichment stored as metadata alongside the raw docs/chunks.
• However, the crux of the matter is deciding how to preprocess the data, i.e. which semantic enrichment to extract as metadata, what data structure to use for the semantic enrichment, and finally what query patterns (i.e. semantic layer) to design to make search, retrieval, and re-ranking effective. This will vary between datasets and between use cases (i.e. you might even need to generate different sets of semantic enrichment for the same corpus which serves different use cases). Here's where working with some good LLM is indispensable, in order to help you quickly define the ontology/taxonomy of the semantic enrichment you want to use on a given corpus-use case. Relying on SME might slow you down enormously, and makes iteration much harder and slower.
• "Is query re-writing trying to basically mimic this SPO based search but the in embedding space?": Yes, exactly! So for my main internal client at Sage, which has a corpus of 4,200 large documents, I use the following patters:

Query Decomposition:
```
SYSTEM_PROMPT_QUERY_DECOMPOSITION: str = """You are an expert query analyst with the precision of a computational linguist and the analytical rigour of a search auditor, working for [CLIENT NAME] customer service teams helping users get answers to their questions about [CLIENT NAME] products.
Your specialty is decomposing complex queries into their fundamental components, identifying key terms, intent patterns, and semantic relationships.
You excel at objectively inferring users' intents, recognizing both explicit and implicit information needs within user questions, and can accurately assess the relative importance of each component to the overall query intent."""

OBJECTIVE: str = """Your objective is to analyze user search queries and identify their core components, revealing the underlying information needs without adding external knowledge or making assumptions about the user's intent.
You must precisely decompose each query into its essential elements, determine each element's contribution to the query's intent, and assess its relative importance to the search goal.
Your analysis will help diagnose [CLIENT NAME] RAG retrieval system performance by exposing what the query is truly seeking, helping to identify any gaps in the retrieval process and improve the quality of the search results returned for answering the users' questions."""

TASK_DESCRIPTION: str = """Perform query decomposition by following these precise steps:

1. Read the provided user query carefully and identify all distinct information-seeking elements.

2. For each identified element:
   a. Extract the exact keywords or phrases (2-4 words) that represent this component
   b. Determine the specific information need this component represents
   c. Assess its importance to the overall query (high/medium/low)

3. Ensure each component captures a unique aspect of the query:
   a. High importance: Core concepts essential to answering the query
   b. Medium importance: Supporting elements that provide context or constraints
   c. Low importance: Optional elements that might refine but aren't critical to the answer

4. For implicit components (those not explicitly stated but implied):
   a. Identify the implied information need
   b. Note it as implicit in your justification
   c. Assess its importance based on how critical it is to a complete answer
   d. Do not add any external knowledge or make any assumptions about the user's intent
   e. Components can be implicit but objectively deduced from the query

5. Review your components to ensure:
   a. They collectively cover the entire information need
   b. No redundant components are included
   c. Importance levels accurately reflect each component's contribution to the query
   d. The analysis is objective and based solely on the query text and not on assumptions about the user's intent

6. Format each component following the required XML structure with `label`, `likely_intent`, and `importance` fields."""

OUTPUT_FORMAT: str = """Return your response surrounded by <response> tags, including the following XML structure:

<response>
<query_components>
<component>
<label>[KEYWORD OR 2-4 WORD PHRASE]</label>
<likely_intent>[SHORT SENTENCE DESCRIBING THE COMPONENT'S LIKELY INTENT WITHIN THE QUERY]</likely_intent>
<importance>[ONE OF: `high`, `medium`, `low`]</importance>
</component>
<component>
...
</component>
</query_components>
</response>

Only generate the content for the `<response>` tags with your query decomposition, without any explanation, reasoning, or additional text before or after."""
```

Search Result Relevance Classification:
```
SYSTEM_PROMPT_RELEVANCE_CLASSIFICATION: str = """You are an expert search relevance analyst with the precision of a computational linguist and the analytical rigour of a search auditor, working for [CLIENT NAME] customer service teams helping users get answers to their questions about [CLIENT NAME] products.
Your specialty is evaluating the relevance of search results to user queries, identifying direct answers, contextually relevant information, and irrelevant content with exceptional accuracy.
You excel at objectively assessing how well a search result addresses a user's information need, recognizing both explicit and implicit relevance signals."""

OBJECTIVE: str = """Your objective is to analyze search results and determine their relevance to user queries, providing a clear classification and justification for each assessment.
You must precisely evaluate how well each search result addresses the user's information need, assign an appropriate relevance category, and provide a numerical score that reflects the strength of the relevance.
Your analysis will help diagnose [CLIENT NAME] RAG retrieval system performance by exposing which search results are most valuable for answering users' questions, helping to identify any gaps in the retrieval process and improve the quality of the search results returned."""

TASK_DESCRIPTION: str = """Perform relevance classification by following these precise steps:

1. Carefully analyse the USER QUERY and understand the user's intent and information need.

2. Carefully analyse the SEARCH RESULT, understand its context, and think step-by-step whether and how strongly it relates to the USER QUERY.

3. Classify the SEARCH RESULT into one of the following categories based on these criteria:
   a. DIRECT ANSWER: Provides a direct and specific answer to the USER QUERY; includes the exact solution, step-by-step instructions, or specific procedures that satisfy the user's information need.
   b. CONTEXTUAL RELEVANCE: Provides background information, additional details, or examples related to the USER QUERY keywords or user's information need, but is not directly answering the USER QUERY.
   c. NOT RELEVANT: Does not provide any useful information for answering the query; discusses unrelated aspects of the product that do not aid in answering the query; or contains generic information that does not address the user's specific information need.

4. Provide a relevance score from 1 to 5, where:
   a. A DIRECT ANSWER should have a relevance score of 4 or 5; 5 if it answers with concrete details, and 4 if it answers in a less detailed, general way.
   b. A CONTEXTUAL RELEVANCE should have a relevance score of 2 or 3; 3 if it could enhance the answer to the user query with useful details, and 2 if it's only tangentially relevant and wouldn't enhance the answer.
   c. A NOT RELEVANT should have a relevance score of 1.

5. Provide a clear justification for your classification and score, explaining the specific reasons why the search result does or does not address the user's query.

6. Format your response following the required XML structure with `category`, `score`, and `justification` fields."""

OUTPUT_FORMAT: str = """Return your response surrounded by <response> tags, including the following XML structure:

<response>
<category>[ONE OF: `DIRECT ANSWER` | `CONTEXTUAL RELEVANCE` | `NOT RELEVANT`]</category>
<score>[ONE OF: 1-5]</score>
<justification>[ONE DETAILED SENTENCE PRECISELY EXPLAINING THE RELEVANCE CLASSIFICATION WITH EVIDENCE FROM THE QUERY AND SEARCH RESULT]</justification>
</response>

Only generate the content for the `<response>` tags with your relevance classification, without any explanation, reasoning, or additional text before or after."""
```

And for the "Search Result Relevance Classification" step, you can pass as input to the prompt both the query and the "Query Decomposition" output, helping the relevance classifier re-rank the search results grounded on the query decomposition, and filter out anything that is not a "DIRECT ANSWER" (if you want a strict filtering) or only removing those which are "NOT RELEVANT" if you want to include indirectly related search results.

<end of DM with Francis>
```

### 3.3 Nate’s article (verbatim excerpt as provided)
- The user pasted a long excerpt titled “Get the Cheat Code on Long‑Running AI Agents—Here’s What Manus, Google, and Anthropic Learned After Trial and Error + 12 Prompts to Help Build Long‑Running Agents Yourself,” including sections on context engineering, memory layers, failure modes, and design prompts. The full excerpt is preserved in this conversation and should be copied verbatim into this section in downstream hand‑off.

### 3.4 12‑prompt pack (verbatim)
The full 12‑prompt pack appears in this thread under “Context engineering prompt pack for long running agents.” It includes:
1) State Persistence Analysis
2) View Compilation Design
3) Retrieval Trigger Design
4) Attention Budget Allocation
5) Summarization Schema Design
6) External Memory Architecture
7) Multi‑Agent Scope Design
8) Cache Stability Optimization
9) Failure Reflection System
10) Architecture Ceiling Test
11) Context Observability Audit
12) Demystifying Agentic Memory (Non‑Technical)

---

## 4) SYNTHESIS OF DECISIONS (plain language)

- **Retrieval policy**: Low‑edge by default with an escalation ladder for broader retrieval when evidence is weak.
- **Canonical structured output**: JSON (XML acceptable only at ingestion edges; must normalize to JSON before contracts).
- **Metadata predicates default**: Report date + author/source applied first pass.
- **Default date scope**: Last 3 years when no user‑provided date range exists.
- **Long‑running artifacts**: Event/step log, context manifests, evidence ledger, draft output state, and compaction snapshots are required for stability and audit.
- **Enterprise constraints**: Token spend, latency, compliance/provenance constraints are first‑class.

---

## 5) UNRESOLVED QUESTIONS / REMAINING PROMPTS

Remaining prompt‑pack topics to complete in order:
5) Summarization Schema Design
6) External Memory Architecture
7) Multi‑Agent Scope Design
8) Cache Stability Optimization
9) Failure Reflection System
10) Architecture Ceiling Test
11) Context Observability Audit
12) Demystifying Agentic Memory (Non‑Technical)

---

## 6) NEXT‑AGENT ACTION PLAN

1) Continue prompt pack from #5 unless directed otherwise.
2) For each prompt, update/add spec documents (doc‑only).
3) Update review bundle (`review/PR_<NN>_REVIEW_BUNDLE.md`).
4) Update `ops/STATUS.md` and `ops/TASK_LOG.md`.
5) Update `contracts/*` with documentation‑only metadata notes.
6) Commit changes and create PR.


#Nate's Articles with 12prompt packs:
Recursion is not a term I am that familiar with and may have used too loosely. But the essence of what I meant, was that the research agent is able to take intent, decompose it, and then traverse the corpus to find the information that's relevant using the memory layers. In this case, one assumes that the knowledge base is indexed offline and exists separately. One can even imagine a two tower model of indexes one which contains embeddings and meta-data and also predicates. I actually may have not thought this one through properly. 

However, what inspired me on this journey of creating an agent system was to 1) use coding agents to ship a multi memory system for agents, and combine it with a search utility capable of  research. I was thinking about the following data corpus which is Michael Cembalest's reports which are usually not part of any training LLM corpus and is proprietary, and the composition of the reports covers a wide range of topics, and charts and figures. Here's me opening Michael Cembalest's reports page and you see many pdfs.

I wanted to prove the concept that I can build and operate builder agents, that can create an end-to-end enterprise grade LONG RUNNING AGENTS. 

You should know that Project Alexandria was conceived after me reading and being inspired by post. The post, which is quite possibly not fully grasped by me, you should read for yourself:

ON LONG RUNNING AGENTS:

The most critical topic in the world today is agentic context engineering or how you deal with memory and AI agents. We are overdue for a deep dive on this. So I'm going to go into three key papers that were recently published on agentic context engineering. I'm going to tell you how it works,
how people commonly misbuild or mischaracterize their agentic memory systems. And then we're going to talk about the use cases that you can only unlock with agentic context engineering. So let's dive in. First, people misunderstand memory. When we say context, people often think a giant prompt window. And when we say memory, they often think, well,
that has to be a rag or vectorized embeddings in a database. Really, for agents, memory is the system. The prompt is not the agent. The LLM by itself is not the agent. The state, how the agent's actions are stored, transformed, filtered, reused, evolved. That's the entire difference between a toy demo and something that handles real work.
And we misunderstand that. The last two years have given us longer context windows and they've given us much, much smarter models, but they did not solve the memory problem. In fact, they intensified it. The naive mental model is as context gets bigger, agents get more capable. But what actually has happened is that attention has become scarce.
And logs have ballooned and irrelevant history so often drowns out critical signals when we talk about agentic memory. And so because we don't handle our memory correctly, that means performance has actually often fallen as tasks get longer. And that's not the fault of the LLM. It's the fault of our memory construction. So this is forced to shift.
We have to stop trying to stuff everything into a context window and stop assuming everything is a rag, and we need to start engineering memory as a first-class runtime environment. Google's ADK showed the architectural fix here. This is one of the papers that I'm going to be talking about.


95

9

13



Get the Cheat Code on Long-Running AI Agents—Here's What Manus, Google, and Anthropic Learned After Trial and Error + 12 Prompts to Help Build Long-Running Agents Yourself
I'm synthesizing four leading papers on agentic context engineering to pull out the core principles for building stable production agentic systems, plus 12 prompts to help you build them!
NATE
DEC 09, 2025
∙ PAID
It’s time to talk about one of the most critical drivers for successful AI agents: in-session context engineering.

I can hear about half of you screaming in excitement and half of you groaning as I write these words lol

The truth is that even for non-technical people understanding how in-session memory management works is increasingly critical to getting real work done. We all need to get how it works to work well in 2026.




A few days ago I wrote about domain memory—why agents fail on work that spans multiple sessions, and how structured external records fix it. The response told me something: people are hitting these walls everywhere.

Think of domain memory as the library: an agent can have a GREAT library and still have a really overloaded desk. And then you’re not getting anywhere.

That overloaded desk is a companion failure mode that’s just as common and just as poorly understood as the domain memory problem. It’s not about what happens between sessions. It’s about what happens within a single session as the agent runs longer.

And what’s interesting is that this within-session problem set seems more widespread than the domain memory piece.

Think about it: it’s relatively easy to come up with a big pile of external memory your agents can access and use. It may take executive blessing (which is why I aimed that first piece at leaders via executive circle), but it gets done.

For engineers and builders, this second piece around in-session state management is the hard part, because getting to a ‘clean desk’ for an agent is a really hard technical problem. And that’s exactly what we’re going to demystify and tackle here.

Watch any agent work on a complex task. For the first ten minutes, it’s sharp. Clear reasoning, appropriate tool use, steady progress. Then something shifts. Around minute twenty or thirty—or after a few dozen tool calls—the agent starts repeating itself. It forgets constraints it acknowledged earlier. It tries approaches it already tried. The reasoning that looked crisp at minute five turns muddy and unreliable.

This isn’t the domain memory problem. You could have perfect external records of project state, and this would still happen. The agent knows what it’s supposed to do. It just... loses the thread. And that’s not an LLM intelligence problem. A smarter model will run into the SAME issue.

My naive assumption was this was an AI intelligence problem. I kept seeing this pattern and assuming it was a model limitation—something that would get fixed when context windows got bigger or models got smarter. That assumption was wrong.

The research now shows that longer context windows often make things worse, not better. And the organizations running agents at production scale—Google, Anthropic, the Manus team—have converged on an explanation that changes how I think about building these systems.

The problem isn’t that agents can’t hold enough information. The problem is that every token you add to the context window competes for the model’s attention. Stuff a hundred thousand tokens of history into the window and the model’s ability to reason about what actually matters degrades. The critical constraint from step three gets buried under the noise from steps four through forty. The agent doesn’t forget because it ran out of space—it forgets because signal got drowned by accumulation.

This is the context engineering problem. And it turns out there’s a coherent framework for solving it.

Three papers from late 2025 lay out the architecture. They lay out how to get that work done. Google’s Agent Development Kit takes a different approach: instead of letting papers pile higher with every task, the agent clears the desk and pulls only what’s relevant for the current step. Stanford and SambaNova’s ACE research shows agents can learn from their own mistakes mid-task—noticing when they grabbed the wrong file and adjusting, without needing to be rebuilt from scratch. And Manus, one of the most widely-used consumer agents, published hard-won lessons after four complete redesigns, explaining how they finally learned to keep their agent focused even when a single task touches fifty different tools.

If domain memory is about what the agent reads at the start of a session, context engineering is about what the agent sees at every step within the session. The two patterns work together. You need both.

Here’s what’s inside:

The non-technical TLDR: If you’re not technical, you have a clear summary of why the heck you should care and what we are talking about
Why accumulation fails: The research on context rot, attention budgets, and why million-token windows made the problem worse
Context as compiled view: The architectural shift from “append everything” to “compute what’s relevant”—and why it determines whether agents can run for minutes or hours
The four-layer memory model: Working context, sessions, memory, and artifacts—what each layer stores, how they interact, and why the separation matters
Nine scaling principles: The specific patterns that make long-running agents work, drawn from all three papers, with tradeoffs and implementation details
Nine failure modes: How agents break when these principles are ignored—the patterns I see repeatedly in broken implementations
What becomes possible: The capabilities that only exist with correct memory architecture—not incremental improvements, but qualitatively different work
Where to build: A note on where practitioners are actually building these agents
Twelve design prompts to build your own context architecture:
State Persistence Analysis — Classify what your agent must remember vs. discard
View Compilation Design — Define the minimal context needed for each decision
Retrieval Trigger Design — Solve the problem of memory that never gets used
Attention Budget Allocation — Justify every token in your context window
Summarization Schema Design — Specify what must survive compression
External Memory Architecture — Draw the line between context and storage
Multi-Agent Scope Design — Test whether agent splits add clarity or just complexity
Cache Stability Optimization — Audit for cost and latency at scale
Failure Reflection System — Design how agents learn from mistakes
Architecture Ceiling Test — Find where your harness limits model capability
Context Observability Audit — Build the tracing layer for production debugging
The Non-Tech Prompt — Make sense of all this if you’re NOT an engineer
Clearing the desk for the agent is one of the biggest blockers in the way of long-running agentic workflows.

And those matter because we can get to REAL value real fast if we can give our agents long-running tasks and trust them to get it done.

Think about it: how many workflows get unlocked if you had an AI that could dependably focus for hours vs. minutes? What if that agent could LEARN and record its evolving strategy as it went, improving future runs? That’s what we’re talking about here.

Let’s dive in and learn how to clear the desk for our agents!

Subscribers get all these posts!

Grab the prompts

This prompt pack isn’t a collection of clever templates. It’s a structured design process—eleven guided sessions that force you to answer the hard questions about your agent’s memory architecture before you build, plus a twelfth prompt to help you makes sense of all this if you’re non-technical.

Each prompt runs as a conversation: you describe your agent, then get challenged on every assumption. The State Persistence Analysis makes you classify every piece of information and defend why it needs to persist. The Attention Budget Allocation forces you to justify every token in your context window. The Summarization Schema Design prevents the failure mode where you compress away critical constraints and discover the problem at step 47.

These prompts exist because most agent failures trace back to memory decisions that were never explicitly made—defaults inherited from chat interfaces that don’t apply to long-running autonomous work.

Where to actually build this: If you’re just experimenting, Claude Projects or ChatGPT with tools will let you feel the limitations firsthand—you’ll hit the degradation problem within an hour of serious use.

For building real agent systems, most teams are using frameworks like LangGraph or the new Google ADK. If you’re technical and want to start simple, Claude Code or Cursor give you agent-like capabilities for coding workflows without building infrastructure from scratch. The prompts above work regardless of platform—they’re about designing the architecture, which you’ll need no matter what you build on.

The Non-Technical Version

Here’s what you need to know if you’re not building agents yourself but need to understand why this matters.

AI agents—systems that use AI to accomplish multi-step tasks with tools—have a memory problem. Actually, they have two memory problems.

The first problem: agents forget everything between conversations. You work with an agent on Monday, make real progress, then come back Tuesday and it has no idea what happened. It’s like working with a new contractor every day who’s never seen the project. I wrote about this problem and its solution—structured external records—in a previous piece.

The second problem, which this piece addresses: agents get worse the longer they run within a single session. They start sharp and focused. Twenty minutes later, they’re confused, repeating themselves, forgetting things they knew earlier. This happens because everything the agent does—every tool it uses, every result it gets—piles up in what it’s paying attention to. Eventually the important stuff gets buried under all the accumulated noise.

The solution isn’t bigger memory. It’s smarter memory—being deliberate about what the agent sees at each step rather than just accumulating everything. The organizations running agents successfully at scale have figured out patterns for this. That’s what we’re covering here.

If you’re evaluating AI agents for your organization, this explains why impressive demos often fail in production and what to ask vendors about their memory architecture. If you’re building agents, this is the technical framework. If you’re just trying to understand where AI agents actually are as a technology, this explains the current constraint that separates “works in demos” from “works in practice.”

Lessons from Google, Anthropic, and Manus on Context Engineering for Agents

The Two Memory Problems

In a previous piece, I argued that agents fail on multi-session work because they have no persistent record of where things stand. Every session starts fresh. The agent guesses what happened before, often incorrectly. Different sessions invent different definitions of “done.” The solution is structured external records—task lists, progress logs, validation criteria—that give each amnesiac agent session the context it needs to pick up where the last one left off.

That’s the cross-session problem. External records solve it. But there’s a companion failure mode that structured records don’t touch.

Watch an agent work on something complex within a single session. For the first ten or fifteen minutes, it’s sharp. Clear reasoning, appropriate tool use, steady progress. Then something shifts. The agent starts repeating itself. It tries approaches it already tried. It forgets constraints it acknowledged twenty minutes ago. The reasoning that looked crisp early on turns muddy and circular.

This isn’t domain memory failure. You could have perfect external records of project state, and this would still happen. The agent knows what it’s supposed to do—it read the task list at the start. The problem is everything that’s accumulated since then. Every tool call result. Every intermediate step. Every observation. All of it piling up in the context window, competing for the model’s attention.

I kept assuming this was a model limitation that would get fixed with bigger context windows. That assumption was wrong. The research shows that longer context windows often make things worse, not better. And the organizations running agents at production scale have converged on an explanation that’s changed how I think about building these systems.

Domain memory solves what the agent knows at the start of a session. Context engineering solves what the agent sees at every step within the session. You need both. This piece is about the second problem.

Why Accumulation Fails

The default approach to managing agent state within a session is simple accumulation. Every message, every tool call, every result gets appended to a growing transcript that’s passed to the model on each turn. This is how chat interfaces work, and it’s how most agent frameworks work by default.

For chatbots, it’s fine. Conversations are short. The model can attend to everything in the window. But agents aren’t chatbots. A typical Manus task—one of the most-used consumer agents—averages 50 tool calls. Each call produces output that gets appended to context. The input-to-output token ratio averages 100:1. Most of what you’re sending to the model is accumulated history, not the current decision.

Here’s what happens as that history grows. Research from Chroma tested 18 different models and found consistent performance degradation as input length increases, especially for tasks requiring reasoning across the full context. A paper called “Lost in the Middle” showed that models struggle with information placed in the middle of long inputs—beginning and end get attention; middle gets ignored. This isn’t a bug that’s getting patched. It’s architectural.

The transformer architecture that powers these models creates n² pairwise relationships between tokens. Every token attends to every other token. As context grows, the model’s ability to capture those relationships gets stretched thin. Training data also skews toward shorter sequences, so models have fewer specialized parameters for handling long-range dependencies.

Anthropic frames this as an “attention budget.” Every token you include is a token of attention spent. Include a hundred thousand tokens of history and the model’s capacity to weigh what actually matters degrades. The critical constraint from step three gets buried under the noise from steps four through forty.

The practical implication is uncomfortable for anyone who thought longer context windows would solve the agent reliability problem. Naively stuffing more into context leads to worse reasoning, not better. The model that fumbles at minute thirty would perform perfectly if you started fresh with just the relevant information.

This is why I keep seeing the same pattern: agents that demo well fail in production. Demo tasks are short. The context window stays small. Everything works. Production tasks run for hours, touch hundreds of files, involve dozens of interdependent decisions. The accumulation problem that’s invisible in a five-minute demo becomes the entire bottleneck at scale.

The Architectural Shift

Three papers from late 2025 converge on the same insight, and it’s a genuine reframe of how to think about agent context.

Google’s Agent Development Kit documentation puts it most directly: in previous-generation agent frameworks, context was treated like a mutable string buffer. You appended to it. Eventually you hit limits and truncated. ADK is built around a different thesis: context is a compiled view over a richer stateful system.

The distinction matters more than it sounds. Sessions, memory, and artifacts are the sources—the full, structured state of the interaction and its data. Flows and processors are the compiler pipeline—a sequence of passes that transform that state. The working context is the compiled output you ship to the LLM for this one invocation.

Once you internalize this, context engineering stops being prompt manipulation and starts looking like systems engineering. You’re forced to ask different questions. Not “how do I fit more into the window?” but “what’s the intermediate representation?” Not “when should I truncate?” but “where do I apply compaction?” Not “what’s in the prompt?” but “how do I make transformations observable?”

The Manus team arrived at the same place through what they call “Stochastic Graduate Descent”—four complete architecture rewrites since launch, each time after discovering a better way to shape context. They bet on context engineering over fine-tuning because it lets them ship improvements in hours instead of weeks. In their framing: if model progress is the rising tide, they want to be the boat, not a pillar stuck to the seabed.

The ACE paper from Stanford and SambaNova extends this to memory that evolves. Instead of static prompts that freeze the agent at version one, they treat context as an “evolving playbook” that accumulates, refines, and organizes strategies through execution feedback. The agent learns from what works and what doesn’t—without retraining the model.

What these three sources share is a rejection of the accumulation model. You don’t build agent context by appending. You build it by computing what’s relevant for this specific step from a richer underlying state.

The Four-Layer Model

The domain memory piece covered external records—task lists, progress logs, validation criteria that persist across sessions. Those records still matter. They’re what the agent reads at session start to understand where things stand.

But within a session, you need additional structure. The model that’s emerged from production systems has four layers, and understanding why they’re separate is prerequisite to building agents that work beyond short interactions.

Working context is what actually gets sent to the model on each call. Instructions, identity, selected history, relevant tool outputs, memory hits, artifact references. This should be as small as possible while remaining sufficient for the current decision.

The key insight: working context is computed, not accumulated. Every time you make an LLM call, you’re assembling a fresh projection against fuller state. What’s relevant now? What instructions apply now? Which artifacts matter now? You answer these at runtime, for each step, rather than assuming a static prompt that grows indefinitely.

Sessions are structured event logs for the full trajectory within a single interaction. Not raw prompt strings, but typed records: user messages, agent replies, tool calls, results, control signals, errors. Each captured as a discrete event.

This matters for three reasons. First, you can swap models without rewriting history—the storage format is decoupled from prompt format. Second, downstream operations like compaction and debugging work over structured events rather than parsing opaque text. Third, you get observability—precise state transitions and actions you can inspect.

The session is your ground truth for what happened. It can grow large. That’s fine—the model doesn’t see it directly. The model sees working context, which is computed from the session.

Memory is searchable knowledge that the agent can query on demand. This overlaps with domain memory—the external records that persist across sessions. Within a session, memory also includes insights extracted from earlier in the current trajectory. The distinction: memory is retrieved when relevant, not permanently present.

Artifacts are large objects stored by reference. A codebase, a PDF, database results. These aren’t tokenized into the window. They’re stored externally and accessed through pointers. The model knows they exist and can request specific portions.

The parallel to traditional computer architecture is intentional. Working context is cache—expensive and limited. Sessions are RAM—larger but still bounded. Memory and artifacts are disk—can grow arbitrarily. The tiered model lets state expand without proportionally increasing per-call cost.

If you’ve implemented domain memory, you already have the external records layer. Context engineering is about how you use those records—and everything else—within a session. What gets loaded into working context? When? How do you keep the window small while giving the model what it needs?

Principle 1: Context Is Computed, Not Accumulated

Every LLM call should be a freshly computed projection against durable state. What’s relevant now? What instructions apply now? Which artifacts matter now? You answer these at runtime.

The naive pattern—append everything into one giant prompt—collapses under what ADK calls “three-way pressure.” Cost and latency scale with context length. Signal degrades as information gets buried (”lost in the middle”). And eventually you hit hard limits regardless of window size.

The compiled view approach addresses all three. You can grow underlying state arbitrarily while keeping each working context small. You get natural insertion points for compaction, filtering, and caching without rewriting prompts. You can tune how context gets assembled without touching agent logic.

ADK implements this by building fresh working context from the current agent’s perspective while preserving factual history in the Session. Each agent sees itself as the “Assistant” without misattributing broader system history to itself. The session is source of truth; the working context is a computed view optimized for this specific call.

The tradeoff: you need infrastructure. You can’t just concatenate strings. You need a session store, a view-compilation pipeline, clear contracts between components. For simple demos, this is overhead. For production agents running hours-long tasks, it’s prerequisite.

Principle 2: Separate Storage from Presentation

Durable state and per-call views serve different purposes. They should evolve independently.

Your session stores everything that happened—every event, every tool result, every state change. Your working context is a computed subset of that, optimized for the model’s current decision. The compilation logic can change without touching storage. You might compress more aggressively as sessions grow. You might prioritize different event types for different phases. You might experiment with summarization strategies. None of this requires changing how you store the raw events.

Manus implements this with “full” and “compact” representations. Tool results are stored in full in the filesystem. The context window carries compact references—file paths, not payloads. The agent can fetch full results if needed, but doesn’t pay the token cost unless it’s actually relevant.

This matters enormously for cost. If your input-to-output ratio is 100:1, most of what you’re paying for is context, not generation. Reduce context through intelligent view compilation—without losing necessary information—and savings compound across every step.

The separation also enables debugging. When something goes wrong, you can inspect the full session to see what actually happened, then inspect the working context to see what the model actually saw. If those diverge in ways that explain the failure, you’ve found your bug.

Principle 3: Scope by Default

Default context should contain nearly nothing. Additional information enters through explicit decisions—loading memory, requesting artifacts, querying past results.

This inverts the common pattern where everything gets included by default and you worry about trimming later. Instead, you start minimal and the agent chooses when to reach for more.

The rationale is attention budget. Every token competes for limited attention. Old information that’s “nice to have” dilutes signal from new information that’s actually relevant. By forcing retrieval to be explicit, you ensure the model only processes what someone decided was worth including for this specific step.

Manus implements this as “reduce, offload, isolate.” Reduce context by compacting stale results—swapping full tool outputs for references that point to where the data lives. Offload by writing to the filesystem and referring by path. Isolate by giving sub-agents their own windows rather than sharing one giant context.

The tradeoff: retrieval adds latency and decision overhead. The agent must know what might exist and when to request it. This works better for agents with clear domain boundaries than for exploratory tasks where relevant context is unpredictable.

Claude Code illustrates a hybrid. Small, almost-always-relevant files (CLAUDE.md) get loaded upfront. Everything else is retrieved just-in-time using glob and grep. The agent navigates its environment and fetches what it needs rather than having everything preloaded.

Principle 4: Retrieval Over Pinning

Attempts to keep everything permanently in context fail because attention constraints bite. Even with million-token windows, performance degrades when you pin everything.

Treat memory as something the agent queries on demand, with relevance-ranked results. The working context should be the result of a search, not the accumulation of history.

This is how agents differentiate between a critical constraint from thirty steps ago and noise from three steps ago. Without explicit retrieval, agents become recency-biased—whatever appeared most recently dominates attention regardless of actual importance.

Domain memory feeds into this. Your external records—task lists, progress logs, validation criteria—aren’t dumped wholesale into every context. They’re queried. The agent retrieves the specific task it’s working on, the relevant progress entries, the applicable validation criteria. Not everything. The slice that matters.

Implementation matters here. Retrieval quality depends on how you structure what’s stored. Random text blobs searched by embedding similarity produce different results than structured events queried by type, timestamp, and tags. The more structure in storage, the more precisely you can retrieve.

Principle 5: Summarization Must Be Schema-Driven

If you don’t aggressively maintain context, it decays—either through bloat or through lossy summarization. The failure modes are predictable: bloat until you hit limits and truncate randomly, or summarize so aggressively that you lose critical information.

I keep seeing teams summarize “to save space” without specifying what must be preserved. Then the agent fails at step 47 because a constraint was compressed away. No one can explain what happened because the raw data is gone.

The ACE paper names this failure mode: “brevity bias,” where summarization drops domain-specific insights for generic compression, and “context collapse,” where iterative rewriting erodes detail over time. You summarize once and lose a little. Summarize again and lose more. After a few rounds, you have vague mush that doesn’t support decision-making.

The fix is schema-driven summarization. Before you compress anything, define what must survive. Causal steps—the chain of decisions and why. Active constraints—rules still in effect. Failures—what was tried and didn’t work. Open commitments—promises not yet fulfilled. Key entities—names and references that must stay resolvable.

ADK implements this through context compaction at the session layer. When thresholds are reached, an LLM summarizes older events over a sliding window, producing a new “compaction” event. Because compaction operates on the structured event stream, you can inspect how summarization happened. You can tune it without touching agent code.

Manus uses staged compression. First, swap full tool results for compact references—lightweight and reversible. When that reaches diminishing returns, escalate to schema-based summarization. The schema guarantees required fields survive. You lose surface detail but preserve structure.

The practical test: can your summarized context make the same decisions as full context on known examples? If not, your schema is wrong or your compression is too aggressive.

Principle 6: Offload Heavy State to Tools and Sandboxes

Don’t feed the model raw tool results at scale. Write them to disk and pass pointers.

Modern context windows offer 128K tokens or more. In practice, that’s often not enough—and sometimes it’s counterproductive. Tool results can be huge. Web pages, PDFs, database queries. A single observation can blow past what’s reasonable. And even when results fit, including them raw degrades performance by diluting attention.

The Manus solution: treat the filesystem as the ultimate context. Unlimited size, persistent by nature, directly operable by the agent. The model writes to and reads from files on demand, using the filesystem as externalized memory.

Compression becomes reversible. A web page’s content can be dropped from context as long as the URL is preserved. A document’s contents can be omitted if the path remains available. You shrink context without permanently losing information—the agent can fetch it back if needed.

Tool design follows the same philosophy. Manus uses fewer than 20 atomic tools: bash, filesystem operations, code execution. Rather than bloating the function-calling layer with specialized tools, they push complexity into the sandbox. MCP tools are exposed through CLI commands the agent runs via bash.

Claude’s Skills feature works similarly. Skills live in the filesystem, not as bound tools. The agent uses basic file operations to progressively discover and use them. You don’t need the entire skill library in context—just enough to know what’s available and how to access it.

The architectural point: tool schemas consume attention too. They sit near the front of serialized context. Expose fifty overlapping tools and you’ve spent significant attention budget before the agent sees any actual task content.

Principle 7: Isolate Context with Sub-Agents

Multi-agent systems should manage context, not mimic org charts. Sub-agents exist to give different work its own window—not to roleplay human teams.

I see this mistake constantly. Someone reads about multi-agent systems and creates a Designer Agent, PM Agent, Engineer Agent, QA Agent. They chat in a shared context like a simulated standup meeting. The result: context explosion with no corresponding capability gain. Cross-agent chatter becomes drift and hallucination rather than genuine coordination.

Manus explicitly warns against this. Their sub-agents exist to isolate context. A planner assigns tasks. A knowledge manager curates what should be saved. An executor performs work. Each has its own window and communicates through structured artifacts—not transcripts passed back and forth.

The communication protocol matters. For simple tasks where the planner only needs output, it passes instructions via function call. The sub-agent works in its own context and returns a structured result. For complex tasks with shared state, the planner shares full context—but the sub-agent still has its own action space and instructions.

In both cases, output follows a schema. The sub-agent has a “submit results” tool that populates defined fields. Constrained decoding ensures adherence. No free-form “here’s what I did” that the planner has to parse.

ADK implements similar patterns as Agents-as-Tools (specialized agent as function call) and Agent Transfer (full handoff with inherited context). Knobs control how much flows from parent to child. You can restrict context for agents that don’t need full history.

The test: “What gets clearer or more correct with separate windows?” If you can’t answer that, the split is probably wrong.

Principle 8: Design for Cache Stability

KV-cache hit rate may be the single most important metric for production agents. It directly affects latency and cost.

The mechanism: contexts with identical prefixes can reuse cached key-value computations. With Claude Sonnet, cached tokens cost $0.30 per million versus $3.00 for uncached—10x difference. Agents making dozens of calls per task see this compound dramatically.

But cache benefits require prefix stability. Due to autoregressive processing, even a single-token difference invalidates cache from that point forward. This creates specific requirements.

Keep your prompt prefix stable. A common mistake: including a timestamp—especially precise to the second—at the beginning of the system prompt. It lets the model tell time, but destroys cache hit rate. That timestamp changes every call, invalidating everything after it.

Make context append-only. Don’t modify previous actions or observations. Ensure serialization is deterministic. Many JSON libraries don’t guarantee key ordering. Non-deterministic serialization silently breaks cache even when logical content is identical.

Mark cache breakpoints explicitly when needed. Some providers require manual breakpoint insertion. At minimum, ensure breakpoints cover the system prompt so it caches across turns.

ADK’s separation of session and working context enables this naturally. The architecture divides context into stable prefix (system instructions, agent identity, long-lived summaries) and variable suffix (latest input, new tool outputs). Changes to suffix don’t invalidate prefix cache.

The Manus team reports this as their most-tracked metric. Cache efficiency determines whether multi-hour agent sessions are economically viable.

Principle 9: Let Context Evolve Through Execution

Static prompts freeze agents at version one. The agent never learns from experience. Every failure is re-discovered rather than remembered.

The ACE paper provides the framework for solving this. Instead of monolithic prompt rewrites, ACE represents context as structured “bullets”—discrete items with metadata (unique ID, helpful/harmful counts) and content (strategy, concept, failure mode). Updates add new bullets or modify existing ones. Localized changes that preserve past knowledge.

Three components collaborate. The Generator produces reasoning trajectories, surfacing strategies and pitfalls. The Reflector critiques those traces to extract lessons. The Curator synthesizes lessons into delta entries, merged by lightweight non-LLM logic.

Because updates are itemized, multiple deltas merge in parallel. The system supports multi-epoch adaptation—revisiting queries to progressively strengthen context.

Results: +10.6% on agent benchmarks, +8.6% on finance tasks, with 86.9% lower adaptation latency than existing methods. On AppWorld, ACE with a smaller open-source model matched top-ranked GPT-4.1 agents on average and exceeded them on harder splits.

Critically, ACE uses execution feedback rather than labeled data. The Reflector analyzes what actually happened—successes and failures—to extract insights. No human annotation required.

With domain memory, your external progress logs capture what worked and what didn’t across sessions. ACE-style evolution captures the same within sessions and crystallizes it into improved prompts and strategies.

The implication: design systems to capture outcomes and feed them back. The agent that ran this morning should inform the context for the agent running this afternoon.

The Failure Modes

These are the patterns I see when people haven’t internalized context engineering. Some are the same mistakes I made before working through this material.

The append-everything trap. You keep a single growing transcript and hand it to the model every turn. Cost and latency scale linearly. Attention dilutes as stale events accumulate. Performance degrades predictably around the 20-30 minute mark. I’ve watched teams debug these agents for weeks, trying prompt tweaks, when the problem is architectural.

Blind summarization. You compress “to save space” without defining what must survive. ACE calls this brevity bias and context collapse. Agents forget edge cases, constraints, what was already tried. Behavior degrades as you “optimize.” The fix isn’t better summarization prompts—it’s explicit schemas that guarantee preservation of decision-relevant information.

The long-context delusion. You upgrade to a million-token model and assume the problem is solved. Performance gets worse. You’re paying more for a more distracted model. The structural issues—no filtering, no compaction, no scoping—don’t disappear with bigger windows. They just manifest at higher token counts.

Observability as context. You stick debug logs, raw tool outputs, stack traces into the same buffer as task instructions. You conflate what you need for debugging with what the model needs for decisions. Those are different. The model drowns in log noise. Sessions should capture everything for observability; working context should be curated for decision-making.

Tool schema bloat. You bind dozens of tools with detailed descriptions. Each description consumes attention budget. Overlapping tools create ambiguity—the model oscillates between similar options or calls the wrong one. Manus uses fewer than 20 atomic tools and pushes complexity into the sandbox.

Anthropomorphic multi-agent. You create Designer Agent and PM Agent and Engineer Agent because it feels like good division of labor. They share a giant context and “communicate” by appending messages. Context explodes. Cross-agent chatter becomes hallucination. The Manus team explicitly warns against this: sub-agents exist to isolate context, not to cosplay teams.

Static configurations. No accumulation of knowledge. No sharpening of heuristics. You rebuild from scratch every session. ACE’s whole point: contexts must evolve through execution feedback. Your agents never improve because you discard all signal from trajectories.

Over-structured harness. You build elaborate multi-step planners, strict tool hierarchies, complex routing logic. When you swap in a better model, performance barely changes. The harness is the bottleneck—your structure prevents the model from using its capabilities. The Manus team has refactored five times because they know this trap.

Cache destruction. You rebuild prompts every turn with unstable prefixes. Timestamps, non-deterministic serialization, reorganized content. You pay full cost for identical logical content because the bytes differ. You’re forced into premature summarization because you refuse to separate stable from volatile sections.

What Becomes Possible

With domain memory, you get continuity across sessions—agents that know where they left off. With context engineering from this piece, you get coherence within sessions—agents that don’t degrade as they run longer. Together, they enable capabilities that simply don’t exist otherwise.

Multi-hour autonomy. Research tasks, code migrations, audit workflows—work that runs for hours and touches hundreds of files. The agent stays coherent because it receives relevant slices of state rather than drowning in accumulated history. Manus sustains 50+ tool calls per task. ADK’s tiered state plus compaction lets agents maintain full event history while feeding the model curated views.

Self-improving agents. Systems that log strategies, update heuristics, learn from mistakes—without retraining. ACE shows this works: evolving contexts enable smaller models to match or exceed larger-model agents with static prompts. Improvement happens in memory and instruction layers, not weights.

Scalable personalization. Persistent preferences, learned constraints, prior outcomes—without ballooning context. Long-term memory is retrieved on demand, not pinned. You inject what matters and leave the rest searchable.

Multi-agent coordination that works. Planner, executor, validator—collaborating through structured artifacts instead of shared context that degrades everything. Each agent sees what it needs. Coordination is debuggable: you can trace exactly what each saw and why.

Reasoning over large corpora. Codebases, document collections, datasets—treated as artifacts rather than tokenized wholesale. Structured retrieval decouples reasoning from raw size. The agent works with bodies of information that vastly exceed window limits.

Auditable systems. Full reconstructability of what the model saw and why. Session logs, compaction events, memory updates—all traceable. When something goes wrong at step 47, you can inspect exactly what context produced that decision.

Viable economics. Sub-linear cost growth through cache reuse and intelligent compaction. Agents you can afford to run in production, not just demo at a hackathon. Manus reports significantly lower per-task costs than integrated alternatives, largely from context engineering.

Domain-specific workspaces. Finance agents with durable risk context. Code agents with project history. Research agents with evidence logs. These become persistent environments rather than one-shot sessions. The agent understands long-term arc because the architecture supports it.

What To Do Now

If you haven’t designed domain memory for your workflows—the external records that your agents can interact with—start there. Context engineering assumes you have persistent state to work with. Without it, you’re trying to optimize a system that can’t maintain continuity in the first place.

If domain memory is in place, audit your within-session architecture.

Map against the four layers. Where does working context end and session begin? What qualifies as memory versus artifact? If you can’t answer these clearly, you don’t have architecture—you have accumulation that will degrade.

Measure your context window. What percentage is actually relevant to the current decision? If most of it is stale history, repeated results, or “nice to have” information, you’re paying attention tax on noise.

Examine your summarization. Is it schema-driven or blind compression? Can you reconstruct decision-relevant structure from summaries? Test explicitly—have summarized context produce the same decisions as full context on known examples.

Audit your tool surface. Could you achieve the same capability with fewer, more orthogonal tools? Does complexity live in schemas or in the sandbox where it belongs? Count your tools. More than 20 likely means overlap and ambiguity.

Check prefix stability. What changes between calls? Is the system prompt truly stable, or do you inject timestamps, session IDs, varying content near the beginning? Check serialization for deterministic ordering.

Run the ceiling test. If you swap in a more capable model, does your agent get proportionally better? If not, your architecture is the bottleneck. The Bitter Lesson applies here: structure that helped with weaker models becomes constraint with stronger ones.

Design for feedback. How does your system capture what worked and what didn’t? How do outcomes feed back into context refinement? Even without full ACE implementation, you can capture execution results and manually incorporate lessons.

The Full Picture

Domain memory gives agents continuity across sessions. Context engineering gives agents coherence within sessions. Both are necessary. Neither is sufficient alone.

The organizations getting agents to work at scale have internalized both. They’re not waiting for models to get smarter or context windows to get bigger. They’re building the memory infrastructure that makes any model more reliable.

The organizations still running failed experiments are typically missing one or both pieces. They’ve built domain memory but accumulate context until within-session performance degrades. Or they’ve optimized context engineering but start every session without state, wondering why agents can’t maintain progress over time.

This is the trade craft for building agents that finish work. No shortcuts exist. But the path is documented now—both parts of it.

Grab the papers

1. Architecting efficient context-aware multi-agent framework for production (Google Developers Blog)

Google’s ADK framework separates storage from presentation, uses explicit context transformations, and scopes each agent call to minimum required context.

2. Context Engineering in Manus (Lance Martin)

Manus uses three context strategies—reduce via compaction/summarization, isolate via sub-agents, offload to filesystem—enabling 50+ tool-call tasks without window overflow.

3. Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models (arXiv)

ACE treats context as evolving playbooks that accumulate and refine strategies, achieving +10.6% on agent benchmarks while reducing adaptation cost.

4. Effective context engineering for AI agents (Anthropic Engineering)

TLDR Context is a tiny desk: optimize via compaction, structured note-taking, sub-agents, and just-in-time retrieval rather than pre-loading everything.

Good luck with building :)

I make this Substack thanks to readers like you! Learn about all my Substack tiers here and grab my prompt tool here

## 12 Prompt pack re: long running agents
Yes you're quite correct to treat it as a question. I actually have a full set of prompts, that you should read through to cross-examine the PROJECT ALEXANDIRA BLUEPRINT. Note that the NEXT STEPS you should note are outstanding: What does enterprise-grade mean? I would say it means token spend and latency and compliance with things like providence over what information is being looked at per department (this implies the user-research agent contract definition), FOR OFFLINE INGESTION, yes I would like us to have an indexing and chunking system that is capable of ingesting new incoming reports--I haven't thought of a pipeline yet maybe I decide to download to s3 bucket and then run. intent decomposition is a feature of promoting the research agent which is essentially implicating the run time user-agent contract.

The remainder of the prompts are packed below, and it's worthy the "seed" of this project again through the analytical lens provided in the context pack:

Context engineering prompt pack for long running agents
\nThese are ready-to-run prompts. Paste any of them directly into your LLM of choice to start a guided design session for your agentic system.
If you’re looking for the non-technical prompt, it is #12 at the end. Just scroll down 😊
\n1. State Persistence Analysis\nYou are a context engineering consultant helping me design the memory architecture for an agentic system.

I'm going to describe what my agent does. Your job is to help me rigorously classify every piece of information the agent touches into one of four categories:

1. **Transient** — Information needed only for the current step, then discarded
2. **Decision-relevant** — Information that affects the next 1-3 decisions but doesn't need long-term storage
3. **Durable memory** — Information that must persist across the entire session or beyond
4. **External artifacts** — Information too large for the context window that must be stored and referenced

For each piece of information I mention, push back if my classification seems wrong. Ask me what happens if that information is lost at step 50. Ask me what happens if it's always present but irrelevant.

The goal is a clean state schema where nothing is over-retained and nothing critical is lost.

Here's my agent: [DESCRIBE YOUR AGENT]

Ask me one question at a time to build out this classification. Start now.
2. View Compilation Design\n\nYou are helping me design the view compilation layer for an agentic system — the component that takes the full session state and produces the minimal context for each step.

The core principle: the context window is computed, not accumulated. The session state is authoritative. The view is small, relevant, and scoped to the current action.

I'm going to describe my agent's workflow. For each step type, help me define:
- What MUST be in the view (the model cannot act without it)
- What SHOULD be in the view (improves quality but isn't essential)
- What should be REFERENCED but not included (the model knows it exists and can fetch it)
- What should be EXCLUDED entirely (irrelevant or distracting)

Challenge me if I'm including too much. The goal is the smallest view that produces correct behavior.

Here's my agent: [DESCRIBE YOUR AGENT]

Ask me one question at a time to design this view compiler. Start now.
\n3. Retrieval Trigger Design\nYou are helping me solve the retrieval problem for an agentic system — not "what's in memory" but "how does the agent know it should retrieve something?"

This is the question most teams skip. They build memory, but the agent never knows to use it because nothing triggers retrieval.

I need to design explicit signals that cause the agent to load relevant context. These might include:
- Keywords or phrases in the user's input
- State transitions (entering a new phase of work)
- Tool outputs that reference prior work
- Explicit instructions in the system prompt
- Confidence thresholds that trigger memory lookup

For my agent, help me identify every moment where retrieval should occur, then design the mechanism that makes it happen reliably — not by luck, but by architecture.

Here's my agent: [DESCRIBE YOUR AGENT]

Ask me one question at a time to map out these retrieval triggers. Start now.
4. Attention Budget Allocation\nYou are helping me allocate the attention budget for an agentic system. Context window space is finite and expensive. Every token included is a token of attention spent.

Help me sort every piece of information my agent handles into four tiers:

1. **Must see** — In the window for every step, no exceptions
2. **Must know exists** — Referenced in the prompt but content not included; agent knows it can ask for it
3. **Fetch when needed** — Not mentioned until relevant; retrieved on demand
4. **Never read again** — Processed once, compressed or discarded, never re-read in full

For each item, challenge me: "What breaks if this moves down one tier?" If nothing breaks, it should move down.

The goal is a context window that's as small as possible while still producing correct behavior — for cost, coherence, and debuggability.

Here's my agent: [DESCRIBE YOUR AGENT]

Ask me one question at a time to build this attention budget. Start now.
\n\n5. Summarization Schema Design\nYou are helping me design a safe summarization schema for an agentic system.

The problem: summarization destroys information. Most teams summarize "to save space" without specifying what must be preserved. Then the agent fails at step 47 because a critical constraint was compressed away.

Before I summarize anything, I need a schema that specifies:
- **Causal steps** — The chain of decisions and why they were made
- **Active constraints** — Rules, limits, and requirements still in effect
- **Failures and dead ends** — What was tried and didn't work (to prevent loops)
- **Open commitments** — Promises made that haven't been fulfilled
- **Key entities** — Names, IDs, references that must remain resolvable

Help me define this schema for my agent. For each field, ask me: "If this were lost, what would go wrong?" If I can't answer, the field is probably unnecessary. If I can answer, the field is mandatory.

Here's my agent: [DESCRIBE YOUR AGENT]

Ask me one question at a time to build this summarization schema. Start now.
6. External Memory Architecture\nYou are helping me decide what belongs in the context window versus external memory (files, databases, scratchpads) for an agentic system.

The principle: semantic memory (what things mean) belongs in the window as compact summaries. Procedural memory (artifacts, code, logs, outputs, plans) belongs in external storage, referenced but not loaded until needed.

For my agent, help me draw this line clearly:
- What should be summarized into bullets or sentences and kept in-context?
- What should be written to files and only loaded on demand?
- What needs a structured store (database, vector store) for retrieval?
- What's intermediate work product that should be checkpointed but rarely re-read?

The goal is an agent that can operate over large bodies of work without drowning in its own output.

Here's my agent: [DESCRIBE YOUR AGENT]

Ask me one question at a time to design this external memory architecture. Start now.
7. Multi-Agent Scope Design\nYou are helping me decide whether and how to split my agentic system into multiple agents — and if so, how to handle scope boundaries.

The right question is not "what personas should I create?" but "what work requires a separate context window for clarity or correctness?"

Valid reasons to split:
- **Planning vs execution** — The planner shouldn't see execution noise; the executor shouldn't re-derive the plan
- **Verification vs generation** — The verifier needs a clean window uncorrupted by the generator's reasoning
- **Knowledge management vs action** — One agent curates context; another agent acts on it

Invalid reasons to split:
- "It feels like a different role"
- "I want a PM agent and an engineer agent"
- Anthropomorphizing the architecture

For each potential split, help me answer: "What gets clearer or more correct with separate windows?" If I can't answer that, the split is probably wrong.

Here's my agent: [DESCRIBE YOUR AGENT]

Ask me one question at a time to evaluate whether multi-agent design is warranted. Start now.
8. Cache Stability Optimization\nYou are helping me optimize KV cache reuse for an agentic system. This is where real cost and latency savings come from.

The principle: tokens that remain identical across steps can reuse cached key-value computations. Tokens that change invalidate the cache from that point forward.

Help me audit my prompt structure:
- **Stable prefix** — System prompt, instructions, and context that never changes mid-session
- **Semi-stable sections** — Content that changes occasionally (e.g., phase transitions)
- **Volatile sections** — Content that changes every step (should be at the END of the prompt)

For each component, ask me:
- Does this actually need to change between steps?
- Can I move volatile information later in the prompt?
- Am I introducing non-determinism (timestamps, random IDs) that kills cache hits?

The goal is a prompt structure where 70%+ of tokens are cache-stable across consecutive steps.

Here's my agent: [DESCRIBE YOUR AGENT]

Ask me one question at a time to optimize cache stability. Start now.
9. Failure Reflection System\nYou are helping me design a failure reflection system for an agentic agent — how mistakes get captured and integrated into future behavior.

The problem: most agents either ignore failures (and repeat them) or over-correct (and become brittle). I need a structured approach.

Help me design:
- **Feedback capture** — How does the agent know something went wrong? (explicit error, user correction, verification failure, timeout)
- **Memory delta format** — What gets written to memory? (not a narrative, but a structured record: what was attempted, what failed, what to do differently)
- **Integration rules** — When does this feedback enter the context? (always? only when similar situations arise? only when explicitly retrieved?)
- **Decay and revision** — When does old failure memory get updated or removed?

The goal is an agent that learns from mistakes without accumulating an ever-growing list of warnings that crowds out useful context.

Here's my agent: [DESCRIBE YOUR AGENT]

Ask me one question at a time to design this reflection system. Start now.
\n10. Architecture Ceiling Test\nYou are helping me run the Bitter Lesson check on my agentic system architecture.

The question: if I swapped in a more capable model tomorrow, would my system's capabilities increase proportionally — or is my architecture the bottleneck?

Signs the architecture is the bottleneck:
- Hard-coded decision trees that a smarter model could handle dynamically
- Aggressive summarization that throws away information a smarter model could use
- Rigid tool schemas that prevent flexible tool use
- Multi-agent splits that exist because the model "couldn't handle it" rather than for genuine clarity

Signs the architecture scales with model capability:
- The model sees all relevant information and decides what matters
- Constraints are expressed as goals, not as hard-coded rules
- The system would benefit from better reasoning with no code changes

Help me audit my design for artificial ceilings.

Here's my agent: [DESCRIBE YOUR AGENT]

Ask me one question at a time to identify where my architecture might be the bottleneck. Start now.
11. Context Observability Audit\nYou are helping me build context observability for an agentic system — the ability to answer "what does the agent actually know right now, and why?"

This is the litmus test of production readiness. If I can't trace what's in the context and why, I can't debug failures, I can't audit decisions, and I can't trust the system.

Help me design observability for:
- **Context contents** — At any step, can I inspect exactly what's in the window?
- **Provenance** — For each piece of context, can I trace where it came from? (user input, tool output, memory retrieval, summarization)
- **Inclusion rationale** — Why was this included? What triggered its retrieval or retention?
- **Exclusion log** — What was available but not included, and why?

The goal is a system where I can replay any decision, see exactly what the model saw, and understand why it saw that.

Here's my agent: [DESCRIBE YOUR AGENT]

Ask me one question at a time to design this observability layer. Start now.
\n12. Demystifying Agentic Memory (Non-Technical)\nYou are a patient, clear explainer helping me understand how AI agents remember things — and why it matters for the AI tools I use or am building.

I'm not an engineer. I don't need to know how to build these systems. But I want to understand what's actually happening when an AI "remembers" something, why AI agents sometimes forget things they should know, and what makes some AI assistants feel smarter than others.

Use plain language. When you introduce a concept, ground it in an analogy I can picture — like a desk, a filing cabinet, a conversation with a colleague, whatever fits. Avoid jargon, but don't dumb things down. I want to actually understand, not just nod along.

Here's how I'd like this to work:

1. Start by asking me what I've noticed about AI memory — times it worked well, times it frustrated me, things I've wondered about. Use my real experiences as the foundation.

2. Build up my understanding piece by piece. Explain one concept, check that it landed, then move to the next. Don't info-dump.

3. Connect everything back to practical implications. "This is why X happens." "This is what to look for when Y." "This is what changes when tools get better at Z."

By the end, I want to understand:
- Why AI can't just "remember everything" (and what the real constraints are)
- How AI decides what to keep, what to forget, and what to look up
- Why some AI feels like it knows you and some feels like it has amnesia
- What's actually improving in this space and what's still hard

Start by asking me about my experience with AI memory — what's worked, what's confused me, or what I'm curious about. Ask me one question at a time. Start now.