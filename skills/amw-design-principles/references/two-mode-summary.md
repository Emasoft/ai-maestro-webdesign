# Two operating modes — orchestrator summary

The orchestrator distinguishes two modes on every incoming request. Full spec at [two-mode-workflow](./two-mode-workflow.md); this file is the on-demand summary the orchestrator's SKILL.md links to.

## Command mode (fast path)

**Trigger:** the user invokes a `/amw-*` slash command explicitly, or supplies a concrete format + parameters with no ambiguity (file path, `--to svg`, named tool, etc.).

**Behavior:** dispatch directly to the matching sub-skill. No Phase A iteration loop. No Phase B spawning. One skill, one artifact, done.

**Key point:** commands are **shortcuts** for users who already know what they want and how. They expose a narrow slice of what each sub-skill can do. An agent operating in Main-agent mode is NOT limited to command vocabulary — it may invoke any technique any skill exposes, including techniques no command surfaces.

## Main-agent mode (requirements path)

> **Executed by `ai-maestro-webdesign-main-agent`** (defined in the plugin's `agents/` folder; or any upstream orchestrator following the same Phase A/B contract). See that agent for the full interactive discovery flow, resource-gathering checklist, sub-agent delegation rules, and Phase B spawning roster.
>
> The `agents/` folder ships 1 main-agent + 19 amw-* sub-agents across 4 tiers (discovery, production, specialists, QA). All sub-agents follow the canonical 14-section template documented at [agent-authoring-philosophy](./agent-authoring-philosophy.md). Cross-agent data hand-offs and the one-way tree topology are in [agent-interaction-patterns](./agent-interaction-patterns.md). Veto power (legal-expert, accessibility-auditor) and conflict-resolution rules are in [authority-hierarchy](./authority-hierarchy.md). The YAML return-contract schema every sub-agent emits is at [sub-agent-return-contract](./sub-agent-return-contract.md). The DO/DON'T rules agents follow when invoking skills are at [skill-invocation-protocol](./skill-invocation-protocol.md).

**Trigger:** the user states goals, requirements, or broad intent without a concrete format — "design a landing page", "build a dashboard UI", "I need a timeline graphic for the team".

**Phase A (conversational — low-fi, low-token):**

The orchestrator examines requirements, proposes low-fidelity design artifacts (ASCII wireframes, ASCII diagrams, ASCII sketches), and iterates with the user in chat until no issues remain. Token cost is intentionally near zero — ASCII costs ~1% of HTML. The user can push 10+ revisions before Phase A approaches the cost of a single HTML generation.

Phase A uses **only direct chat output**. No sub-agents. No file writes. No browser calls. No validators.

Phase A ends **only** on the canonical satisfaction tokens: `yes`, `ship it`, `approved`, `that's the one`, `perfect`, `done`, `go ahead`, `let's do it`. Ambiguous acknowledgement (`looks good`, `sure`, `ok`, `fine`) is NOT approval — ask once: *"Should I go ahead with this direction?"*

**The agent MUST NOT start producing real artifacts until Phase A satisfaction tokens are received.** This gate is non-skippable.

**Phase B (non-conversational — spawning):**

After Phase A approval, the orchestrator stops talking to the user and spawns sub-agents to implement the approved design. The orchestrator speaks to the user exactly TWICE during Phase B: a transition confirmation at the start, and the job-completion report at the end.

Phase B always includes `dev-browser`-driven scenario tests for every browser-runnable artifact (`dev-browser` is the only input-automation primitive in this plugin). See [two-mode-workflow](./two-mode-workflow.md) §4 for the mandatory test checklist.

## Approval gate invariant

The Phase A → Phase B boundary is a hard stop. There is no "Phase B starts optimistically while Phase A is still refining." If Phase B output is later found to be based on an unconfirmed direction, discard it and restart Phase B from the approved direction.
