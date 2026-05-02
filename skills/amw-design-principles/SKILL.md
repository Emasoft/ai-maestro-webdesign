---
name: amw-design-principles
description: Orchestrator for any web, UI, slide, prototype, poster, or design task. Enforces three hard rules — (1) gather design context before designing, (2) always produce at least three variants, (3) reject catalogued AI-slop patterns — and routes to the appropriate executor skill in ai-maestro-webdesign. Triggers on any design intent ("design a page", "build a landing page", "mockup", "UI for", "prototype", "wireframe", "slide deck", "poster", "dashboard", "website", "brand", "style"). The plan phase runs in ASCII via /amw-sketch until the user is explicitly satisfied; HTML is generated only after approval.
version: 2.0.0
author: ai-maestro-webdesign
source: Distilled and rewritten in English from the Claude Design system prompt as publicly archived in elder-plinius/CL4R1T4S. All rights to the original prompt belong to Anthropic. This skill is a learning/interpretation layer, not a redistribution.
---

# Design Principles — the orchestrator

> **Core insight:** good design is not guessed from scratch; it grows out of existing context. This skill compresses the Claude Design judgment set into an executable checklist and routes technical execution to the sub-skills in this plugin.

---

## 🚦 When to trigger (read first)

Any of the following task types activates this skill:

- Websites, landing pages, component libraries
- Slide decks, pitch decks, presentation documents
- App and web prototypes, interactive demos
- Posters, visual assets, infographics
- Brand collateral, cards, badges
- Any HTML or SVG output that "must not look AI-generated"

Trigger vocabulary: *design, UI, mockup, prototype, slide, deck, poster, landing, wireframe, mock, interface, page, website, dashboard, brand, style, visual.*

When this skill activates, it **owns the task** until it explicitly routes to an executor. Other skills in this plugin — `ascii-sketch`, `diagram-*`, `infographics`, `svg-creator`, `design-extract`, etc. — are executors that run under this skill's rules.

---

## Two operating modes

Full spec: `./references/two-mode-workflow.md`. Summary here — read the full spec before modifying either mode.

### Command mode (fast path)

**Trigger:** the user invokes a `/amw-*` slash command explicitly, or supplies a concrete format + parameters with no ambiguity (file path, `--to svg`, named tool, etc.).

**Behavior:** dispatch directly to the matching sub-skill. No Phase A iteration loop. No Phase B spawning. One skill, one artifact, done.

**Key point:** commands are **shortcuts** for users who already know what they want and how. They expose a narrow slice of what each sub-skill can do. An agent operating in Main-agent mode is NOT limited to command vocabulary — it may invoke any technique any skill exposes, including techniques no command surfaces.

### Main-agent mode (requirements path)

> **Executed by `../../agents/ai-maestro-webdesign-main-agent.md`** (or any upstream orchestrator following the same Phase A/B contract). See that agent for the full interactive discovery flow, resource-gathering checklist, sub-agent delegation rules, and Phase B spawning roster.
>
> The `agents/` folder ships 1 main-agent + 19 amw-* sub-agents across 4 tiers (discovery, production, specialists, QA). All sub-agents follow the canonical 14-section template documented at `./references/agent-authoring-philosophy.md`. Cross-agent data hand-offs and the one-way tree topology are in `./references/agent-interaction-patterns.md`. Veto power (legal-expert, accessibility-auditor) and conflict-resolution rules are in `./references/authority-hierarchy.md`. The YAML return-contract schema every sub-agent emits is at `./references/sub-agent-return-contract.md`. The DO/DON'T rules agents follow when invoking skills are at `./references/skill-invocation-protocol.md`.

**Trigger:** the user states goals, requirements, or broad intent without a concrete format — "design a landing page", "build a dashboard UI", "I need a timeline graphic for the team".

**Phase A (conversational — low-fi, low-token):**

The orchestrator examines requirements, proposes low-fidelity design artifacts (ASCII wireframes, ASCII diagrams, ASCII sketches), and iterates with the user in chat until no issues remain. Token cost is intentionally near zero — ASCII costs ~1% of HTML. The user can push 10+ revisions before Phase A approaches the cost of a single HTML generation.

Phase A uses **only direct chat output**. No sub-agents. No file writes. No browser calls. No validators.

Phase A ends **only** on the canonical satisfaction tokens: `yes`, `ship it`, `approved`, `that's the one`, `perfect`, `done`, `go ahead`, `let's do it`. Ambiguous acknowledgement (`looks good`, `sure`, `ok`, `fine`) is NOT approval — ask once: *"Should I go ahead with this direction?"*

**The agent MUST NOT start producing real artifacts until Phase A satisfaction tokens are received.** This gate is non-skippable.

**Phase B (non-conversational — spawning):**

After Phase A approval, the orchestrator stops talking to the user and spawns sub-agents to implement the approved design. The orchestrator speaks to the user exactly TWICE during Phase B: a transition confirmation at the start, and the job-completion report at the end.

Phase B always includes `dev-browser`-driven scenario tests for every browser-runnable artifact (`dev-browser` is the only input-automation primitive in this plugin). See `./references/two-mode-workflow.md` §4 for the mandatory test checklist.

### Approval gate invariant

The Phase A → Phase B boundary is a hard stop. There is no "Phase B starts optimistically while Phase A is still refining." If Phase B output is later found to be based on an unconfirmed direction, discard it and restart Phase B from the approved direction.

---

## ⛔ The three hard rules (violating any one of these is a failure)

### Rule 1: Gather design context before designing

There is no "I have a good idea in my head, let me start coding." Before any design work, obtain at least **one** of:

- An existing UI kit or design system file
- Brand tokens (color palette, font stack, spacing rules, radius scale)
- Screenshots of reference sites or products
- Components already in the project's codebase
- An explicit brand manual (e.g. Equation brand guide)

**If none of these are available → ask the user first,** or together pin down a "visual DNA anchor" (e.g. "like Aesop — cream-white + serif + whitespace").

The recommended structured form for a brand-token spec — both as Phase A *output* (when the user asks "give me a design system") and as Phase A *input* (when the user shows up with one already) — is a Variant 1 DESIGN.md (the official `@google/design.md` format). The plugin's `amw-design-md` skill owns authoring, extraction, lint, audit, conversion, and companion emission. When this rule fires and the user has neither a UI kit nor a brand manual, offer `/amw-design-md-create` (5-Q interview), `/amw-design-md-from-url <url>` (extract from a reference site), or `/amw-design-md-from-codebase` (scan an existing project). The produced DESIGN.md becomes the canonical token source for Phase B sub-agents (wireframe-builder, component-library-architect, accessibility-auditor).

> Mocking from scratch is a **last resort**. It produces generic AI slop.

### 🆘 Last-resort path (when context is genuinely unavailable)

When the user has supplied no design system and cannot name a reference:

1. **Invoke the `ui-ux-reasoning` sub-skill** for a library of 50+ visual styles / 21+ palettes / 50+ font combinations as ammunition.
2. **Vocalize assumptions:** state out loud *"I am going with X typeface + Y color temperature + Z layout rhythm"* and wait for the user's nod before going further.
3. If you have to proceed without confirmation, annotate the file header: *"These are temporary visual assumptions. Replace with real brand assets when available."*

**Stance:** mocking from scratch only produces "barely passable" generic output. It never produces premium work.

### Rule 2: Deliver at least three variants, baseline → advanced → experimental

A single answer is never the full answer. Every design task must include:

- **Variant A (Baseline):** strictly follows the existing design system; zero risk.
- **Variant B (Advanced):** builds on the system but shifts one dimension (color, layout, typographic rhythm).
- **Variant C (Experimental):** allowed to break the system — new metaphors, novel layouts, bold typography.

Present them side-by-side (tabs, stacked cards, multi-slide deck) so the user can mix and match.

**The plan-phase medium for variant exploration is ASCII via `/amw-sketch`, not HTML.** See the "ASCII-first plan phase" section below — Rule 2 is almost always easier to satisfy in ASCII than in HTML.

### Rule 3: Reject every AI-slop pattern

Specific patterns are an instant tell for AI generation. The complete list is in `ai-slop-avoid.md` (26 patterns + positive-stance section). Highlights:

- ❌ Large purple-blue or pink-orange linear gradients
- ❌ Rounded-card + 4px left accent bar
- ❌ AI-drawn SVG illustrations of people / mascots / scenes
- ❌ Inter / Roboto / Arial / Fraunces / system default fonts
- ❌ Emoji carpet-bombing (unless the brand explicitly uses emoji)
- ❌ Filler data, icons, statistics added just to fill space
- ❌ Invented testimonials, placeholder portraits
- ❌ "Trust markers" / customer logo walls on every section

Every HTML output runs a final scan against `ai-slop-avoid.md` before delivery.

---

## 🧭 ASCII-first plan phase (the default workflow)

**When the user asks for a webpage design, the plan phase runs in ASCII, not HTML.** Iterate on position, size, alignment, and component choice in ASCII until the user explicitly says they are satisfied. Only then convert to HTML.

```
  User asks for a design
         │
         ▼
  ┌────────────────────────────────────┐
  │ 1. design-principles orchestrator  │
  │    Rules 1, 2, 3 apply             │
  └────────────────┬───────────────────┘
                   ▼
  ┌────────────────────────────────────┐
  │ 2. /amw-sketch                      │
  │    3 ASCII variants → feedback →   │
  │    revision → feedback → ...       │
  │    (loop until "ship it")          │
  └────────────────┬───────────────────┘
                   ▼
  ┌────────────────────────────────────┐
  │ 3. /amw-ascii-to-html (terminal)    │
  │    tokens applied, chrome wrapped, │
  │    preview via /amw-preview         │
  └────────────────────────────────────┘
```

The loop is cheap because ASCII costs ~1% of the tokens of HTML iteration. Users can push 10+ revisions without context decay. Iteration ends only on the canonical satisfaction tokens: `yes`, `ship it`, `convert it`, `that's the one`, `perfect`, `done`. Ambiguous acknowledgement (`looks good`, `sure`, `ok`, `fine`) is NOT approval — ask a clarifying question before proceeding.

Skip the loop only when the user has already committed to a layout (e.g. they pasted a wireframe and said "build this"). Otherwise, ASCII-first is default.

---

## 📐 7-step execution flow

```
1. Read the brief       → decide whether this skill fires
2. Gather context       → request UI kit / brand assets / references; ask if absent
3. Question checklist   → use question-templates.md; ask ≥ 10 questions
4. Declare visual system → state "I will use X font + Y palette + Z spacing rhythm"
5. Build variants       → ≥ 3 in ASCII via /amw-sketch; loop to satisfaction
6. Self-check           → run ai-slop-avoid.md over the chosen direction
7. Deliver              → /amw-ascii-to-html → /amw-preview → show the user
```

---

## 🕐 Workflow rhythm

- **Show your reasoning and assumptions early — in chat, not on disk.** State the assumptions you're working from in your dialog with the user during Phase A. Write them out in plain text inside the chat so the user can correct them before any artifact is committed. Once approved in Phase B, write the HTML to disk with assumption notes alongside (in code comments or a sibling .notes.md file).
- **Accumulate, don't restart.** After writing React components into the HTML, show once more, followed by a "next steps" list.
- **One main file + Tweaks > multiple files.** When the user wants a new version, append as a Tweak to the existing main file. Do not stack v2 / v3 / v4 files.
- **Only duplicate when the user asks for side-by-side comparison** (`My Design.html` → `My Design v2.html`).

---

## 🎛️ Tweaks live-tuning mode (recommended)

Embed a JSON config block in HTML output with the marker below. This lets you precisely replace the config on a subsequent edit, and lets the user hand-edit and refresh:

```html
<script>
const TWEAKS = /*EDITMODE-BEGIN*/{
  "primaryColor": "#D97757",
  "fontSize": 16,
  "radius": 8,
  "dark": false
}/*EDITMODE-END*/;
</script>
```

Full template: `starter-components/tweaks-block.html`.

### Tweaks protocol — three non-negotiable rules

1. **Register the `message` listener BEFORE posting `__edit_mode_available`.** Otherwise the host's activate message races ahead of the listener and toggle silently fails.
2. **`__edit_mode_set_keys` must carry partial updates** — only the changed keys, never the full config object on each change.
3. **The `EDITMODE-BEGIN/END` block must be valid JSON** — double-quoted keys, double-quoted string values. The host parses this and writes it back to disk; any syntax slip bricks persistence.

---

## 📊 Dimensional hard limits (no discussion)

| Medium | Min font | Min hit target |
|---|---|---|
| 1920×1080 slides | 24 px | — |
| Print documents | 12 pt | — |
| Mobile mockups | 14 px | 44 × 44 px |
| Desktop body copy | 16 px | — |

- Slides must carry `data-screen-label` (1-indexed, format `"01 Title"`). When the user says "page 5" they mean label `"05"`, not `array[4]`.
- Any content with a **playback position** (slides, video timeline) must persist the current position to `localStorage`. Users reload constantly during dev — not persisting position breaks their flow.

---

## 🎬 Animation stack order

When animation is needed:

1. **First choice:** `starter-components/animations.html` (Stage + Sprite + timeline + Easing — ~50 LOC core, covers 90% of use cases).
2. **Fallback:** Popmotion (`https://unpkg.com/popmotion@11.0.5/dist/popmotion.min.js`) for physics, spring, drag.
3. **Banned:** Framer Motion, GSAP. Too heavy; the scaffolds above are sufficient.

---

## 🧭 Decision tree — which file to load when

```
Task received
    │
    ▼
ALWAYS start here — this SKILL.md and its three hard rules
    │
    ▼
 ┌────────────────────────────────────────────────────────┐
 │ Task type → load this companion or route to sub-skill │
 ├────────────────────────────────────────────────────────┤
 │ About to emit any HTML  → ai-slop-avoid.md             │
 │ Need to ask the user    → question-templates.md        │
 │ Picking fonts/sizes     → typography-system.md         │
 │ Picking colors          → color-system.md              │
 │ Picking spacing/radius  → spacing-rhythm.md            │
 │ PC webpage chrome       → starter-components/browser-window.html │
 │ Mobile app chrome       → starter-components/ios-frame.html      │
 │                            /android-frame.html         │
 │ Slide deck              → starter-components/deck-stage.html     │
 │ Multi-variant canvas    → starter-components/design-canvas.html  │
 │ Animation               → starter-components/animations.html     │
 │ Live-editable params    → starter-components/tweaks-block.html   │
 │ Something feels off,    → design-heuristics.md         │
 │   can't name what         (Gestalt / Fitts / Hick / etc.)        │
 └────────────────────────────────────────────────────────┘
```

---

## 🔧 Downstream executor sub-skills (the plugin's routing table)

These are the sub-skills that live under `../` and execute specific capabilities under this orchestrator's rules. Invoke them only when their specific technical trigger applies.

### Input — gather context for Rule 1

| Sub-skill | Use when |
|---|---|
| `../amw-dev-browser/` | Need to screenshot, inspect DOM, or interact with a live page. Plugin's ONLY browser-automation primitive for input. |
| `../amw-design-extract/` | User points at a reference URL and wants its colors, fonts, spacing, and tokens extracted. Wraps `designlang`. |
| `../amw-ui-ux-reasoning/` | Last-resort fallback when the user has no design system and no reference — 161 reasoning rules + 67 styles + 161 palettes + 57 font pairings. |

Slash commands: `/amw-extract-style <url>` combines dev-browser + design-extract.

### Plan phase — satisfy Rule 2 in ASCII

| Sub-skill | Use when |
|---|---|
| `../amw-ascii-sketch/` | **Default for any webpage design.** Runs the ASCII iteration loop (3 variants → feedback → revision → ... → explicit satisfaction). |
| `../amw-ux-flows/` | Product already has a PRD and the user wants user-case extraction → Mermaid diagrams → clickable HTML wireframes. |
| `../amw-ux-designer/` | Need the full UX methodology — research, personas, IA, prototyping, handoff. |

Slash command: `/amw-sketch <intent>`.

### Output — render the approved direction

| Sub-skill | Use when |
|---|---|
| `../amw-ascii-creator/` | User already knows what they want — produce ONE validated perfect-ASCII artifact (flowchart, table, sequence, layered arch, or framed wireframe) in a single invocation. Mode A uses bin/amw-ascii-render.py; Mode B hand-authors and runs bin/amw-validate-ascii.py. |
| `../amw-ascii-validator/` | Validate hand-authored ASCII OR render perfect ASCII from structured JSON — the toolchain that enforces alignment across every ASCII emitter in this plugin. |
| `../amw-ascii-to-html/` | User approved an ASCII wireframe → generate responsive HTML using design-principles tokens + starter-components chrome. Consumes output from ascii-sketch (plan-phase) OR ascii-creator (single-artifact). |
| `../amw-ascii-to-svg/` | User has an ASCII box-and-arrow diagram → render clean SVG. Consumes output from ascii-creator Mode A. |
| `../amw-diagram-svg/` | Natural-language request → SVG diagram primitives. |
| `../amw-diagram-editorial/` | Editorial-quality HTML+SVG diagrams (13 types: architecture, flowchart, sequence, ER, timeline, etc.). |
| `../amw-diagram-architecture/` | Free-text system description → graph JSON / Mermaid / SVG / PNG. |
| `../amw-svg-creator/` | **Gated.** Icons, logos, technical SVG, patterns, animations. NOT characters or scenes. |
| `../amw-infographics/` | Data + brief → dense editorial HTML + PNG + PDF (175-design library). |
| `../amw-pretext/` | Pretext-driven typography, measurement, layout, obstacle routing, shrink-wrap, virtualized tables, kinetic text, calligrams, ASCII-on-canvas, and 3D text — ~78 techniques catalogued in `references/TECH-NN-*.md`. NOT a general typography system — orchestrator keeps "make the type nice" here. |
| `../amw-hyperframes-bridge/` | HTML composition → MP4 video. |
| `../amw-mermaid-render/` | Mermaid text → SVG or Unicode ASCII. Themed output, 15+ themes. Consumes structured Mermaid syntax; emits a self-contained SVG or a validator-passing ASCII block. |
| `../amw-box-diagram/` | Clean Unicode rounded-corner box diagrams (`╭╮╰╯│─`) for pipelines, fan-out/fan-in, workflow charts, layered stacks. Richer typography than plain ASCII; always validator-passing. |
| `../amw-excalidraw-illustrations/` | **Gated.** Hand-drawn Excalidraw-style conceptual illustrations via Gemini API. Educational/slides use only; requires `$GEMINI_API_KEY` and user-confirmed cost per call. Exception to the ai-slop ban on AI-drawn illustrations because scope is constrained (sketchy, white-bg, concept-diagram shape). |
| `../amw-html-diagram/` | Author or edit an HTML-rendered editorial/infographic-style diagram. Narrow trigger: "create HTML diagram", "modify HTML diagram at …", "/amw-create-or-modify-html-diagram". Thin dispatcher over `diagram-editorial` and `infographics`. |
| `../amw-svg-diagram/` | Author or edit a standalone SVG diagram. Narrow trigger: "create SVG diagram", "modify SVG diagram at …", "/amw-create-or-modify-svg-diagram". Thin dispatcher over `diagram-svg` and `diagram-architecture`. |
| `../amw-mermaid-diagram/` | Author or edit Mermaid source text (9 grammar types). Narrow trigger: "create Mermaid diagram", "modify Mermaid at …", "/amw-create-or-modify-mermaid-diagram". Rendering is delegated to `mermaid-render`. |
| `../amw-diagram-convert/` | Cross-format diagram conversion across the 5-format matrix (ASCII/HTML/SVG/Mermaid → any; PNG is output-only). Narrow trigger: "convert this diagram to X", "/amw-convert-any-diagram-format". |
| `../amw-diagram-compare/` | IR-level structural diff between two diagrams (formats may differ). Narrow trigger: "compare these diagrams", "diff two flowcharts", "/amw-compare-diagrams". |
| `../amw-webpage-to-diagram/` | Extract the structural diagram of a webpage (URL or local `.html`) and emit ASCII/SVG/Mermaid. Narrow trigger: "extract diagram from webpage", "diagram this URL", "/amw-create-diagram-from-webpage". |
| `../amw-diagram-webpage-sync/` | Re-emit an existing webpage from an edited diagram source. Narrow trigger: "sync this diagram back into my HTML", "/amw-modify-webpage-from-diagram". |

Slash commands: `/amw-ascii-to-html`, `/amw-ascii-to-svg`, `/amw-create-or-modify-ascii-diagram`, `/amw-create-or-modify-html-diagram`, `/amw-create-or-modify-svg-diagram`, `/amw-create-or-modify-mermaid-diagram`, `/amw-create-excalidraw-like-diagram-png`, `/amw-convert-any-diagram-format`, `/amw-validate-any-diagram-format`, `/amw-compare-diagrams`, `/amw-create-diagram-from-webpage`, `/amw-create-webpage-from-diagram`, `/amw-modify-webpage-from-diagram`, `/amw-modify-diagram-of-webpage`.

### Text visualization — ASCII artifacts for PRs, ADRs, terminals, and chat

These executors are distinct from the `diagram-*` skills above: they produce **monospaced ASCII only**, designed to paste unmodified into GitHub PRs, issue comments, Slack, Notion, READMEs, ADRs, and terminal output. They are not renderers to SVG or HTML — if the user wants pixels, run one of these first to approve the ASCII, then hand off to `../amw-ascii-to-svg/` or `../amw-ascii-to-html/`. Every artifact these skills emit passes `../../bin/amw-validate-ascii.py` before delivery (LLMs cannot count monospace columns reliably — the validator is how the plugin compensates).

| Sub-skill | Use when |
|---|---|
| `../amw-text-visual-workflows/` | Multi-step workflow as ASCII flowchart, timeline, or swimlane (PR lifecycle, launch plan, triage ops). |
| `../amw-text-visual-arch/` | Layered ASCII architecture diagram (context / container / component) for terminals, PRs, ADRs. |
| `../amw-text-visual-state/` | ASCII state machine for user journey, retention loop, issue lifecycle, experiment status. |
| `../amw-text-visual-cheatsheets/` | ASCII CLI command panel with macOS/Linux and Windows columns side by side. |
| `../amw-text-visual-retro/` | ASCII retrospective grid, milestone timeline, or heatmap for retros, post-mortems, experiment readouts. |

These skills do NOT ship dedicated slash commands (text-visual output overlaps heavily with `/amw-sketch` and `/amw-ascii-to-svg`; a separate command would confuse routing). Invoke via direct skill activation (narrow trigger phrases listed in each skill's description) or via `/amw-sketch` when in the plan phase.

### Validation + reference

| Sub-skill | Use when |
|---|---|
| `../amw-ux-evaluator/` | Systematic UX scoring (Position / Visual Weight / Spacing) on a finished page. |
| `../amw-seo/` | Performance / Core Web Vitals evaluation framework. |
| `../amw-shadcn-ui/` | Need to emit copy-paste shadcn/ui components. |
| `../amw-tailwind-4/` | Tailwind v4 config / migration questions. |
| `../amw-ascii-diagrams-reference/` | Reference library of validated ASCII archetypes (flowcharts, state-machines, trees, data-structures, network-topology, sequences-tables, graphs-annotations) distilled from the CHI'24 paper on 2,156 real diagrams in Linux/Chromium/LLVM/TensorFlow. Consulted by ascii-sketch / ascii-creator / text-visual-* when selecting a canonical pattern. |
| `../amw-diagram-formats/` | **Meta-skill (cross-reference, not executor).** Authoritative specs for every diagram-format concern: format specs (ASCII/HTML/SVG/Mermaid), the IR schema (`diagram-ir/1.0`), the N×N conversion matrix, the format-detection contract, the validate-dispatcher, the modify-flow pipeline, and the IR-level diff algorithm. All diagram-authoring and diagram-conversion skills import their rules from here — do NOT re-author these specs in the consumer skills. Never triggers independently; consulted implicitly whenever a diagram skill needs a spec. |
| `./references/project-output-routing.md` | Detection rules for project-inferred artifact output paths. Every sub-skill references this before writing artifacts instead of hardcoding `/tmp/amw-<skill>/`. Consult when the user has not specified an output path — the doc determines the right folder based on `package.json`, existing design folders, Claude design markers, and framework conventions. |

Slash commands: `/amw-eval`, `/amw-preview`, `/amw-doctor`, `/amw-init`.

### Tier-4 specialists (on-demand, Phase B only)

`amw-form-designer-agent`, `amw-email-designer-agent`, `amw-motion-designer-agent`, and `amw-component-library-architect-agent` are spawned by `ai-maestro-webdesign-main-agent` when the brief surfaces form / email / motion / token-system intent. They have no veto power and produce specs or exports consumed by Tier-3 producers. They are agents, not skills — invoke them via Task delegation, not skill activation. Full roster and delegation rules: `../../agents/ai-maestro-webdesign-main-agent.md` and `./references/two-mode-workflow.md`.

---

## 📁 File-management rules

- **Descriptive English filenames** for generated artifacts: `Landing Page.html`, `Dashboard Variants.html`, `iPhone App Prototype.html`. Never `design.html` / `test.html` / `output.html`.
- **Do NOT stack `v2` / `v3` files by default.** New variants become Tweaks in the existing main file. Only duplicate when the user explicitly requests a side-by-side comparison.
- **Split any file > ~1000 lines.** For React, split JSX components into sub-files and have the main file compose.

---

## 💬 Closing note

Ninety percent of design failures come from not asking enough questions, not enough context, and delivering only one option. Treat this SKILL.md as a checklist; walk every step.

"Fast output" and "good design" are not the same thing. Use ASCII-first iteration to get both — fast iteration *and* good judgment.
