# Agent-authoring philosophy — judgment layer vs recipe layer

This document is the governing principle for every agent under `agents/` in this plugin. It exists because the common mistake when authoring an agent is to write it like a skill — a recipe of "if A then B, if X then Y" — and then discover at runtime that reality doesn't match the recipe.

## Skills and agents are not the same kind of thing

A **skill** is a recipe. Inputs are bounded, outputs are predictable, decisions inside the recipe are deterministic. A skill can be large — hundreds of reference pages, dozens of decision nodes — but its complexity is combinatorial, not semantic. You can test a skill exhaustively by enumerating the input space.

An **agent** is a professional. It operates on variable, incomplete, often contradictory input. It cannot anticipate every situation it will encounter. Testing it exhaustively is impossible because the input space is unbounded — user requests, external state, upstream-agent outputs, broken files, unreachable URLs, half-written briefs. Writing an agent like a skill produces a brittle thing that fails the moment reality deviates from the recipe.

People underestimate this. They treat the hard part as "gathering all the knowledge", which is the skill-building problem, and then they wrap that knowledge in a thin dispatch layer and call it an agent. The result is a fragile automation that looks impressive until someone asks it a question it wasn't scripted for.

## What an agent actually needs

An agent spec has two layers, and both must be present:

### Recipe layer (deterministic floor)
- **Input contract** — the expected shape of input
- **Operations** — the nominal sequence for the happy path
- **Skill-decision matrix** — which skill fires on which signal
- **Return contract** — the structured output the agent owes its caller

This layer is necessary but not sufficient. It covers the expected cases. If reality matches the expected case, the agent follows the recipe and returns a predictable result.

### Judgment layer (non-deterministic surface)
- **Mental model** — the abstract conceptual framework the agent uses to reason about its domain. A legal-expert's mental model is "regulatory frameworks as overlapping constraint sets". A brand-researcher's is "positioning whitespace as the gap between commoditized and differentiated tokens". A wireframe-builder's is "ASCII as a lossless structural spec the HTML layer must honor". The mental model is not a list of facts — it is the lens through which the agent interprets whatever it sees.
- **Knowledge base and responsibility boundaries** — what the agent is responsible for, what it knows, and critically what it does NOT know or is NOT responsible for. Boundaries matter more than knowledge; they prevent the agent from wandering into domains where it will guess badly.
- **Universal decision criteria** — values the agent weights when facing trade-offs. "Regulatory compliance > aesthetic preference". "User confidence beats keyword perfection". "Explicit assumption beats silent guess". Three to seven criteria, ordered by priority. When the recipe doesn't cover a case, the agent falls back to these.
- **Uncertainty handling** — how the agent handles missing, incomplete, or contradictory input. A decision tree: when to ask for more, when to proceed with an explicit assumption, when to return partial, when to stop.
- **Conflict and escalation patterns** — anticipated conflict scenarios and the resolution rule for each. "If input from source X contradicts source Y → action Z". Each pattern terminates with an action: proceed-with-assumption, ask-main-agent, escalate-to-user-via-main-agent, refuse-and-return-partial, or stop.
- **Delegation rules** — what can be delegated, to whom, under what conditions. Also what must NEVER be delegated (things the agent is uniquely qualified to do).

Together these six sections constitute the agent's professional judgment. Without them, the agent is a skill wrapper. With them, the agent can handle novelty.

## Why the judgment layer matters in this plugin specifically

This plugin's main-agent interacts with the user on vague briefs like "create a landing page for a luxury Bora Bora resort, French and English". The main-agent does not know in advance:

- Whether the user has photography, or whether they want AI-generated imagery (which the plugin gates)
- Whether the user has copy, a brochure, a pricing sheet, or nothing at all
- Whether the user cares about GDPR (they might be US-only) or about ADA (they might be EU-only) or about hospitality-specific rules (minimum-stay disclosures, alcohol laws, room-tax surcharges)
- Whether the three ASCII variants will converge after two rounds, or after ten
- Whether the final handoff is to a React codebase, a static site generator, a Figma file, or a PDF print poster
- Whether the user speaks English well enough that the satisfaction gate will trip on the first "perfect" or whether the user says "perfetto" and the main-agent has to recognize it

Every one of these is a judgment call. No skill-decision matrix can pre-enumerate them. The judgment layer is where the main-agent earns its keep.

Sub-agents face the same problem in their narrower domains. The legal-expert doesn't know in advance which jurisdictions apply, whether the user will provide existing legal text, whether the project triggers healthcare or financial disclaimer rules, or whether GDPR is the primary constraint or a secondary one. The multilanguage-copywriter doesn't know in advance whether the user wants native-level copy in all locales or machine-translation drafts flagged for human review. Every sub-agent must have the judgment layer, not just the recipe.

## The 14-section canonical template

Every agent under `agents/` follows this structure. Sections 1, 4, 5, 7, 9, 12, 13, 14 are the recipe layer. Sections 2, 3, 6, 8, 10, 11 are the judgment layer. Main-agent adds §15 for orchestration doctrine.

1. Role and Identity
2. Mental Model *(judgment)*
3. Knowledge Base and Responsibility Boundaries *(judgment)*
4. Trigger Phrases and Activation
5. Input Contract
6. Universal Decision Criteria *(judgment)*
7. Operations (nominal workflow)
8. Uncertainty and Edge-Case Handling *(judgment)*
9. Skill-Decision Matrix
10. Delegation Rules *(judgment)*
11. Conflict and Escalation Patterns *(judgment)*
12. Skill Invocation Protocol
13. Return Contract
14. Hard Rules / Veto Power

Plus for main-agent only:

15. Orchestration Doctrine

The order matters. Identity comes first because everything downstream depends on "who am I as a professional". Mental model and knowledge base come before trigger phrases because an agent must know its own mind before recognizing when it's being called. Operations come after universal decision criteria because criteria govern operations (deviation is legitimate when criteria demand it). Conflict patterns come near the end because they depend on all prior sections. Hard rules / veto power come last because they are absolute constraints that override everything above.

## What this document is NOT

This is not a recipe for writing agents. It is the philosophy that makes the recipe worth writing. The actual step-by-step for authoring a new agent is:

1. Read this document
2. Read `sub-agent-return-contract.md`, `agent-interaction-patterns.md`, `skill-invocation-protocol.md`, `authority-hierarchy.md`
3. Write the 14 sections against the canonical template, filling every section in order
4. Have someone else (human or another Claude session) read the spec and try to predict what the agent would do on three novel inputs you didn't design for — if they can't predict, the judgment layer has holes
5. Only then commit the agent to `agents/`

A spec that can only describe expected-case behavior is incomplete. A spec where the judgment layer is present but vague ("use good judgment") is worse than absent — it lies about having thought through the hard cases.

## Cross-references

- `sub-agent-return-contract.md` — canonical YAML schema that every agent uses to report back to main-agent
- `agent-interaction-patterns.md` — cross-agent data hand-offs, data-flow graphs for Phase A and Phase B
- `skill-invocation-protocol.md` — how agents invoke skills without re-triggering the orchestrator
- `authority-hierarchy.md` — conflict-resolution rules and veto power
- `two-mode-workflow.md` — the command-mode vs main-agent-mode contract
