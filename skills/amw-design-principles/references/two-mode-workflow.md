## Table of Contents

- [0. Sub-agent delegation (Main-agent mode only)](#0-sub-agent-delegation-main-agent-mode-only)
- [1. Mode Detection](#1-mode-detection)
- [2. Phase A — Iterative Low-Fi Loop](#2-phase-a-iterative-low-fi-loop)
- [3. Phase B — Implementation and Spawning](#3-phase-b-implementation-and-spawning)
- [4. Scenario Testing via dev-browser (mandatory in Phase B)](#4-scenario-testing-via-dev-browser-mandatory-in-phase-b)
- [5. Anti-Patterns](#5-anti-patterns)


# Two Operating Modes — Formal Spec

This document is the authoritative spec for how `design-principles` and every
sub-skill in this plugin pick between **Command mode** and **Main-agent mode** and
execute accordingly. All orchestrator and sub-skill behavior described here
overrides informal descriptions elsewhere.

> **Main-agent mode is EXECUTED BY `agents/ai-maestro-webdesign-main-agent.md`** (or by any upstream orchestrator that follows the same Phase A/B contract defined in this document). The main-agent is the primary agent that runs the interactive discovery loop (Phase A) and delegates implementation (Phase B) to specialized `amw-*` sub-agents. See `../../agents/ai-maestro-webdesign-main-agent.md` for the full agent definition.

---

## 0. Sub-agent delegation (Main-agent mode only)

When operating in Main-agent mode, the `ai-maestro-webdesign-main-agent` may spawn specialized sub-agents prefixed with `amw-` (ai-maestro-webdesigner). These agents are exclusively subordinate to the main-agent — they never interact with the user directly.

### Naming convention

```
amw-<role>-agent.md
```

Examples: `amw-legal-expert-agent`, `amw-multilanguage-copywriter-agent`, `amw-brand-researcher-agent`.

All sub-agents are located in `../../agents/` (the plugin's `agents/` folder).

### One-way delegation rule

```
main-agent → sub-agent → main-agent
```

Sub-agents return structured findings to the main-agent. The main-agent integrates those findings into its conversation with the user or into Phase B artifacts. Sub-agents are NEVER allowed to respond directly to the user.

### Delegation timing

- **Phase A sub-agents:** Spawn only when specialized information is actually needed (legal flags, competitor research, persona synthesis). Do NOT spawn speculatively.
- **Phase B sub-agents:** Spawn in parallel after the satisfaction gate is passed. Each handles a bounded, non-overlapping task (accessibility audit, SEO audit, copy localization, etc.).

### Full sub-agent roster (19 amw-* agents across four tiers)

**Tier 2 — Discovery / Research** (Phase A primarily; accessibility and SEO dual-mode A and B):

| Agent | Role | Veto power |
|---|---|---|
| `amw-legal-expert-agent` | GDPR / ADA / CCPA compliance, disclaimers, jurisdictional restrictions | YES — regulatory mandatory elements |
| `amw-multilanguage-copywriter-agent` | Multilingual copy, pluralization, RTL, cultural adaptation | no |
| `amw-brand-researcher-agent` | Competitor analysis, design-token extraction from reference URLs | no |
| `amw-accessibility-auditor-agent` | WCAG 2.1 AA / ARIA / keyboard / contrast / reduced-motion audit (A: spot-check, B: full audit) | YES — WCAG AA hard blockers |
| `amw-seo-strategist-agent` | Keyword research + IA planning (A), on-page audit + structured data (B) | no |
| `amw-user-research-analyst-agent` | Persona synthesis, user-journey maps from research artifacts | no |
| `amw-design-md-auditor-agent` | DESIGN.md 5-pass audit (structural / drift / a11y / completeness / consistency); diagnoses only, no repairs | no |

**Tier 3 — Production / Execution** (Phase B only):

| Agent | Role |
|---|---|
| `amw-wireframe-builder-agent` | ASCII → HTML conversion with shadcn/Tailwind integration |
| `amw-diagram-producer-agent` | All diagram formats (editorial, architecture, Mermaid, SVG, box, text-visual); owns format-selection decision |
| `amw-infographic-builder-agent` | Dense HTML/PNG/PDF infographics via the 24 templates |
| `amw-asset-generator-agent` | SVG icons/logos/patterns via svg-creator; typography via pretext; optional gated Excalidraw via GEMINI_API_KEY |
| `amw-video-producer-agent` | HTML → MP4 via hyperframes-bridge |
| `amw-browser-tester-agent` | dev-browser scenario tests + ux-evaluator for Phase B verification |
| `amw-design-md-author-agent` | Author Variant 1 DESIGN.md from a brief / codebase / URL / 5-Q interview; lint gate + WCAG contrast pre-flight |
| `amw-design-md-extractor-agent` | Extract Variant 1 DESIGN.md from a live URL / Tailwind config / codebase scan; faithful transcription only |

**Tier 4 — Specialists** (Phase B; spawned on-demand when domain-specific intent detected):

| Agent | Role |
|---|---|
| `amw-form-designer-agent` | Booking, contact, checkout, multi-step forms with validation UX, error states, form a11y |
| `amw-email-designer-agent` | Transactional + marketing emails (MJML, table-layout responsive, dark-mode, plain-text fallback) |
| `amw-motion-designer-agent` | Page transitions, scroll-driven animations, microinteractions, prefers-reduced-motion compliance |
| `amw-component-library-architect-agent` | Design tokens authoring + variant matrix + design-system handoff exports (JSON / Style Dictionary / Figma Tokens / Tailwind config) |

Tier 4 specialists have **no veto power**. They produce specs/exports that Tier 3 producers (typically `amw-wireframe-builder-agent`) consume for final HTML rendering. `amw-email-designer-agent` is the exception — it is its own render path because email is not a webpage.

The plugin ships 20 agents total (1 main-agent + 7 Tier-2 + 8 Tier-3 + 4 Tier-4 amw-* specialists). Full specifications live at `../../agents/<name>.md`; the canonical agent-authoring philosophy is at [agent-authoring-philosophy](./agent-authoring-philosophy.md).

### Cross-references

- [agent-authoring-philosophy](./agent-authoring-philosophy.md) — why agents differ from skills (recipe layer vs judgment layer); mandatory 14-section template
  > Skills and agents are not the same kind of thing · What an agent actually needs · Recipe layer (deterministic floor) · Judgment layer (non-deterministic surface) · Why the judgment layer matters in this plugin specifically · The 14-section canonical template · What this document is NOT · Cross-references
- [sub-agent-return-contract](./sub-agent-return-contract.md) — YAML header schema every amw-* sub-agent returns to main-agent
  > Schema · Field semantics · `agent` — required, string · `phase` — required, enum `A | B` · `status` — required, enum `ok | partial | failed` · `confidence` — required, enum `high | medium | low` · `execution_time_ms` — optional, int · `max_iterations` — required, int · `attempts_count` — required, int · `attempts_log` — required, list of objects · `blocking_issues` — required (empty list ok), list of strings · `warnings` — required (empty list ok), list of strings · `artifact_paths` — required (empty list ok), list of objects · `recommendations` — required (empty list ok), list of strings · `next_action` — required, string (free-form but see conventions) · `report_path` — required, string · Markdown body structure · How main-agent consumes the contract · Contract invariants (enforced by smoke tests)
- [agent-interaction-patterns](./agent-interaction-patterns.md) — explicit data hand-offs between agents in Phase A and Phase B; the one-way tree topology
  > Topology invariants · Phase A data flow · Phase A data hand-offs (carried by main-agent between sub-agent invocations) · Phase B data flow · Phase B data hand-offs · Phase B sequencing rules · What main-agent does between sub-agent calls · Error propagation · Why this topology (instead of peer-to-peer) · Enforcement
- [skill-invocation-protocol](./skill-invocation-protocol.md) — DO/DON'T block for how agents invoke skills without re-triggering the orchestrator
  > The problem · The protocol · DO · DON'T · Examples · Correct: agent produces an HTML mockup from approved ASCII · Incorrect: agent tries to delegate back through commands · Correct: agent needs to produce a diagram in Mermaid format · Incorrect: agent uses Skill tool with a vague English prompt · Enforcement
- [authority-hierarchy](./authority-hierarchy.md) — conflict-resolution rules; veto power for legal-expert and accessibility-auditor
  > Domains and authority · Veto power — what it means · Resolution rules by conflict pattern · Pattern 1: Visual vs. functional tension · Pattern 2: SEO vs. UX content hierarchy · Pattern 3: Copywriter locale vs. legal disclaimer · Pattern 4: Production agent vs. discovery agent · Pattern 5: Two discovery agents with opposite readings of the same data · Pattern 6: Missing data from a domain · Pattern 7: Upstream contradiction between user and an agent · How main-agent applies the hierarchy · What the hierarchy does NOT do · Enforcement

---

## 1. Mode Detection

The orchestrator reads the incoming user message and classifies it as one of
two modes before any skill or command is dispatched.

### Command mode signals (fast path — dispatch immediately)

Activate Command mode when the message contains **any** of:

| Signal type | Examples |
|---|---|
| Explicit slash-command prefix | `/amw-sketch`, `/amw-ascii-to-html`, `/amw-extract-style`, `/amw-preview`, etc. |
| File path + format hint | `"convert design.txt to SVG"`, `"validate diagram.mmd"` |
| Specific format or tool name | `"ascii-to-html"`, `"validate this mermaid"`, `"render SVG"` |
| Single concrete artifact request with no ambiguity | `"render this Mermaid flowchart as themed SVG with dracula theme"` |
| Parameters spelled out by the user | flags like `--to svg`, `--theme`, `--out`, explicit width/height, named colors |

Command mode means: **the user already knows the exact sub-skill, format, and
parameters.** The agent dispatches directly to the matching skill with no
approval loop, no Phase A iteration, no Phase B spawning. One skill runs; one
artifact is produced.

### Main-agent mode signals (requirements path — enter Phase A first)

Activate Main-agent mode when the message:

- Uses broad design vocabulary with no concrete format: *"design a landing
  page"*, *"build me a dashboard"*, *"I want a website for X"*, *"create a
  UI for this product"*, *"prototype this app screen"*.
- States a goal or outcome, not a tool: *"we need something that converts
  visitors"*, *"the team wants a timeline of our Q3 milestones"*.
- Is a requirements dump: a PRD, a bullet list of features, a paste of brand
  guidelines without a stated format.
- Contains explicit iteration signals: *"let me see some options"*, *"show
  me a few variants"*, *"not sure what layout would work"*.
- Is ambiguous about format, tool, or fidelity.

Main-agent mode means: **the user has requirements but has not committed to any
specific format or sub-skill.** Enter Phase A via `agents/ai-maestro-webdesign-main-agent.md`.

### Tie-breaking rule

When the signal is ambiguous, prefer **Main-agent mode**. Entering Phase A when the
user actually knew what they wanted costs one extra round of confirmation.
Entering Command mode when the user did not know what they wanted skips the
approval gate and wastes Phase B compute on the wrong direction.

---

## 2. Phase A — Iterative Low-Fi Loop

Phase A is a **conversational, low-token, low-fidelity** process. Its entire
purpose is to reach an approved design direction before any real artifact is
built. Phase A is CPU-cheap by design: the wrong direction identified in Phase
A costs one revision; the wrong direction identified in Phase B costs a full
re-run of every sub-agent.

### Inputs

- The user's requirements message (free text, PRD, sketches, reference URLs).
- Any brand context already gathered (Rule 1 of `design-principles`).
- The question checklist from `question-templates.md` (run ≥ 10 questions if
  context is thin).

### Low-fi artifact types (pick the cheapest that fits)

| Situation | Phase A artifact |
|---|---|
| Webpage, dashboard, landing page, app screen | ASCII wireframe via `../amw-ascii-sketch/` — 3 variants, baseline / advanced / experimental |
| Architecture or data-flow diagram | ASCII box diagram via `../amw-box-diagram/` or `../amw-text-visual-arch/` |
| Infographic or data poster | ASCII table layout or ASCII sketch of section structure |
| Workflow, timeline, process map | ASCII flowchart via `../amw-text-visual-workflows/` |
| State machine or user journey | ASCII state diagram via `../amw-text-visual-state/` |
| SVG illustration | Structural sketch in ASCII before any SVG markup is emitted |
| Mermaid diagram | Plain-text Mermaid source draft, NOT rendered |

**The canonical example of Phase A is the `ascii-sketch` loop** (defined in
`skills/amw-ascii-sketch/SKILL.md`). All other Phase A artifacts follow the same
principles: propose multiple options, iterate in chat, emit no files, keep
token cost near zero.

### Iteration rules

1. The orchestrator proposes the low-fi artifact in chat output. No files are
   written to the user's working directory during Phase A.
2. The user gives feedback. Revise and re-propose.
3. Ambiguous acknowledgement (`looks good`, `sure`, `ok`, `fine`) is NOT
   approval. Ask once: *"Should I go ahead with this direction?"* Wait for
   a satisfaction token.
4. Soft iteration budget of 10 rounds. There is no hard limit, but on round 10
   the main-agent surfaces a nudge: *"We've iterated 10 times — want to narrow
   scope, or is there a specific concern I haven't addressed?"* The nudge does
   not block further iteration; it prevents unbounded loops where the user and
   agent are talking past each other.
5. Each revision is cheap (ASCII = ~1% of HTML token cost). Five or ten rounds
   of revision during Phase A is preferable to one round of re-running Phase B.

### RDD (Requirements Design Document) — auto-pass Phase A

When an upstream orchestrator supplies a structured Requirements Design
Document instead of free-text dialog, Phase A can be skipped iff the RDD
contains ALL SIX fields below. Missing any field → RDD is treated as Phase A
input (seed for discovery), not as approval.

| Field | Meaning |
|---|---|
| `brand_context` | Color palette OR brand-token reference URL OR explicit style brief |
| `target_locales` | List of ISO 639-1 codes for all user-facing text |
| `approved_variant` | Labeled ASCII sketch OR explicit reference to a prior Variant (e.g., "Variant B" with matching structure) |
| `success_metrics` | Conversion, engagement, or other measurable goal |
| `legal_notes` | Regulatory constraints OR explicit "no special regulatory requirements" |
| `accessibility_target` | WCAG level (default: AA) |

RDD completeness is checked before any sub-agent is spawned. An incomplete RDD
triggers Phase A with the provided fields pre-filled as context.

### Satisfaction gate (hard stop — non-skippable)

Phase A ends **only** when the user emits one of the canonical satisfaction
tokens:

```
yes | ship it | convert it | that's the one | perfect | done | approved | go ahead | let's do it
```

Silence, partial agreement, or hedged approval is not a satisfaction token.
If the user says *"I think that's close enough"*, interpret as NOT approved —
ask for explicit confirmation. If the user says *"that's the one, but move
the CTA up"*, apply the change, re-show, and wait for a clean satisfaction
token.

**The agent MUST NOT start producing real artifacts — HTML, SVG, PNG, MP4 —
until this gate is passed.**

### What Phase A does NOT include

- Spawning sub-agents. Phase A is a direct conversation between the orchestrator
  and the user. Sub-agents introduce latency and token overhead into what is
  supposed to be a cheap iterative loop.
- Calling `dev-browser`. Browser round trips belong to Phase B.
- Writing files to the user's working directory.
- Producing rendered HTML, SVG, PNG, or MP4.
- Running validators (ascii-validator, ux-evaluator, seo) — validate the real
  artifact in Phase B, not the low-fi sketch.

---

## 3. Phase B — Implementation and Spawning

Phase B begins exactly when the satisfaction gate in Phase A is passed. The
orchestrator stops conversing with the user and spawns sub-agents to build
the real artifact in parallel.

### Transition protocol

At the Phase A → Phase B boundary, the orchestrator:

1. Confirms the approval: *"Understood — going with Variant B. Building now."*
2. Emits a brief implementation plan (one paragraph or bullet list, max 10
   lines) so the user knows what Phase B will produce.
3. Stops interactive conversation. The user is not consulted again until Phase
   B is complete.

### Sub-agent spawning rules

Each sub-agent receives a **bounded, non-overlapping task**. No sub-agent
overlaps with another's output path. Spawn order follows dependency order —
design-token extraction before HTML render, HTML render before validation.

After the satisfaction gate, main-agent does NOT invoke executor skills directly.
It delegates to Tier 3 production sub-agents (which internally invoke the
executor skills). This keeps main-agent's context focused on orchestration,
arbitration, and the final job-completion report.

**Typical Phase B sub-agent roster for a webpage:**

| Sub-agent task | Sub-agent | Internal skill(s) |
|---|---|---|
| Render approved ASCII → HTML with brand tokens + copy + legal fragments | `amw-wireframe-builder-agent` | `../amw-ascii-to-html/`, `../amw-shadcn-ui/`, `../amw-tailwind-4/` |
| Produce embedded diagrams (architecture, flowcharts, sequences) | `amw-diagram-producer-agent` | `../amw-diagram-editorial/`, `../amw-diagram-architecture/`, `../amw-mermaid-diagram/`, `../amw-mermaid-render/`, `../amw-svg-diagram/`, `../amw-box-diagram/`, `../text-visual-*/`, `../amw-diagram-convert/` |
| Produce standalone infographic pages | `amw-infographic-builder-agent` | `../amw-infographics/`, `bin/amw-html-export.py` |
| Produce icons, logos, patterns, typography experiments | `amw-asset-generator-agent` | `../amw-svg-creator/`, `../amw-pretext/`, gated `../amw-excalidraw-illustrations/` |
| Produce video from HTML scenes | `amw-video-producer-agent` | `../amw-hyperframes-bridge/` |
| WCAG 2.1 AA accessibility audit | `amw-accessibility-auditor-agent` (B mode) | `../amw-dev-browser/`, `../amw-ux-evaluator/` |
| On-page SEO audit + structured-data injection | `amw-seo-strategist-agent` (B mode) | `../amw-seo/`, `../amw-dev-browser/` |
| dev-browser scenario tests | `amw-browser-tester-agent` | `../amw-dev-browser/`, `../amw-ux-evaluator/` — see Section 4 |
| Locale copy deltas if multi-locale build | `amw-multilanguage-copywriter-agent` (B mode) | `../amw-pretext/` |

**Parallelism:** production agents (wireframe-builder, diagram-producer,
infographic-builder, asset-generator, video-producer) may run in parallel when
their outputs are independent. Auditors (accessibility, SEO-B,
browser-tester) run AFTER the production output exists — they cannot audit
absent artifacts.

**Dependency chains main-agent must respect:**

1. `diagram-producer` and `asset-generator` run before `wireframe-builder` if
   their outputs are embedded in the HTML; otherwise parallel.
2. `wireframe-builder` runs before `accessibility-auditor (B)`, `seo-strategist
   (B)`, and `browser-tester` — auditors need the artifact.
3. `video-producer` is independent; parallelizes with all others.
4. `multilanguage-copywriter (B)` runs before `wireframe-builder` if copy is
   embedded in the HTML.

**Return contracts:** every sub-agent returns a YAML header per
[sub-agent-return-contract](./sub-agent-return-contract.md). Main-agent parses the header (not the body)
> [sub-agent-return-contract.md] Schema · Field semantics · Markdown body structure · How main-agent consumes the contract · Contract invariants (enforced by smoke tests)
to decide proceed / retry / escalate / stop.

**Authority and vetoes:** sub-agent conflicts are resolved per
[authority-hierarchy](./authority-hierarchy.md). Legal-expert and accessibility-auditor have veto
> [authority-hierarchy.md] Domains and authority · Veto power — what it means · Resolution rules by conflict pattern · How main-agent applies the hierarchy · What the hierarchy does NOT do · Enforcement
power over mandatory regulatory / WCAG AA blockers; other agents hold
non-veto authority in their respective domains.

### Non-conversation rule

During Phase B the orchestrator does NOT:

- Ask the user clarifying questions.
- Send progress updates per sub-agent.
- Show partial results.

The orchestrator speaks to the user exactly TWICE during Phase B: at the
start ("going with Variant B, building now") and at the end (the job-completion
report). All intermediate output is written to files.

### Job-completion report

When all sub-agents have completed, the orchestrator emits one structured
report to the user:

```
## Done

Artifacts produced:
- <filename> — <one-line description>
- <filename> — <one-line description>

Scenario test results:
- <test name>: PASS / FAIL
```

If any sub-agent failed, the report includes the failure summary and asks the
user whether to retry or skip.

---

## 4. Scenario Testing via dev-browser (mandatory in Phase B)

Every artifact that runs in a browser — HTML pages, dashboards, infographics,
interactive diagrams — MUST have a `dev-browser`-driven scenario test produced
as part of Phase B. This is not optional.

### What a scenario test covers

At minimum, every test must verify:

1. **Loads without console errors** — navigate to the file URL, capture
   `dev-browser console` output, assert zero errors.
2. **Renders above the fold** — screenshot at 1440px wide, assert the hero /
   main content area is visible (non-white, non-blank).
3. **Mobile layout** — screenshot at 375px wide (iPhone SE viewport), assert
   no horizontal scroll and font size ≥ 14px in body copy.
4. **Interaction spot check** — if the artifact has tabs, accordions, or
   toggles: click each one via `dev-browser click`, assert the expected
   content becomes visible.

### dev-browser is the ONLY input-automation primitive

Do not use Playwright MCP, Chrome DevTools MCP, Puppeteer, or Selenium for
scenario testing. Every browser interaction in Phase B runs through
`skills/amw-dev-browser/SKILL.md` (which wraps the `dev-browser` CLI).

The distinction between dev-browser and the rendering pipelines in
`bin/amw-html-export.py` / `hyperframes-bridge` / `infographics` is:
- **dev-browser** = input capture (read the live browser state, screenshot,
  DOM dump, interaction).
- **Rendering pipelines** = output emission (HTML → PNG / PDF / MP4).
They serve different axes and are not substitutes.

### Scenario test output format

Each scenario test emits a short markdown block:

```markdown
### Scenario: <name>
- Step 1: <action> → <expected outcome>: PASS / FAIL
- Step 2: <action> → <expected outcome>: PASS / FAIL
...
Overall: PASS / FAIL
```

Include this block in the Phase B job-completion report.

---

## 5. Anti-Patterns

These are the most common failure modes for the two-mode workflow. Every agent
running under this orchestrator MUST avoid them.

### Skipping Phase A when requirements are vague

Symptom: the user says "design a landing page for my SaaS" and the agent
immediately starts generating HTML.

Why it fails: without Phase A, the agent guesses at layout, component choices,
and visual direction. The first HTML output is wrong. The user requests changes.
The agent re-generates HTML — at 100x the token cost of ASCII iteration. Three
rounds of HTML re-generation = the same cost as 300 rounds of ASCII iteration.

Correct behavior: detect Main-agent mode, enter Phase A via `agents/ai-maestro-webdesign-main-agent.md`, propose 3 ASCII variants,
iterate until the satisfaction gate is passed.

### Starting Phase B before explicit approval

Symptom: the user says "sure, that looks fine" and the agent begins spawning
sub-agents.

Why it fails: "sure" is not a satisfaction token. The user may not actually be
satisfied; they may be hedging or waiting for more options. Phase B is expensive
(real artifacts, real tokens, real compute). Wasting Phase B on an unconfirmed
direction is the most expensive mistake in the workflow.

Correct behavior: respond to ambiguous approval with one clarifying question —
*"Should I go ahead with Variant B?"* — and wait for an explicit token.

### Spawning sub-agents during Phase A

Symptom: the user is still choosing between layout options and the agent spawns
a sub-agent to start building HTML "in parallel to save time."

Why it fails: Phase A is cheap because it is conversational and single-threaded.
Sub-agents introduce coordination overhead and spawn new context windows that
will be discarded when the user chooses a different direction. The cost of a
wasted sub-agent exceeds the cost of 50 ASCII iterations.

Correct behavior: Phase A uses only direct chat output. No sub-agents, no file
writes, no browser calls.

### Talking to the user during Phase B

Symptom: an agent in Phase B sends the user progress updates like "sub-agent 2
is now running the UX evaluation..." or asks "should I use Tailwind or vanilla
CSS for this component?"

Why it fails: interrupting Phase B forces the user into a synchronous
decision loop and defeats the purpose of the spawning architecture. Questions
that should have been answered in Phase A delay Phase B completion.

Correct behavior: all Phase B decisions are resolved by the sub-agent using
context already gathered in Phase A. The orchestrator communicates with the
user only at Phase B start (transition confirmation) and at Phase B end
(job-completion report).

### Treating commands as the only path to a skill

Symptom: documentation or agent behavior implies that `svg-creator` can ONLY
be invoked via `/amw-create-or-modify-svg-diagram`, or that infographics can
ONLY be triggered via a specific command.

Why it fails: commands are shortcuts for users who know exactly what they want.
An agent in Main-agent mode can invoke any technique exposed by any skill in the
plugin — including techniques that no command exposes. Restricting to command
vocabulary in Main-agent mode artificially limits the agent's capability.

Correct behavior: commands are a user-facing fast path. In Main-agent mode, the
orchestrator may invoke any skill directly with any technique appropriate to the
approved design direction.

### Omitting scenario tests from Phase B

Symptom: Phase B produces HTML but no `dev-browser` test, so the agent reports
"Done" without verifying the artifact renders correctly in a browser.

Why it fails: LLM-generated HTML frequently has layout bugs, missing font loads,
or JavaScript errors that are invisible in the source but obvious in a browser.
The scenario test is the only way to catch these before the user opens the file.

Correct behavior: every Phase B that produces a browser-runnable artifact MUST
include at minimum the three mandatory checks in Section 4 (console errors,
above-fold render, mobile layout).
