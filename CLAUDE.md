# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`ai-maestro-webdesign` — a **Claude Code plugin** that consolidates the Claude Design system prompt (translated to English and rewritten as the orchestrator skill `amw-design-principles`), three new ASCII-centric skills, and fifteen adapted executor skills across diagrams, image generation, browser automation, style extraction, UX process, and reference documentation. It ships its own `bin/` folder of shared scripts, its own slash commands, and a single hook.

The plugin is built in small, verified phases. The inventory of source skills (kept read-only for reference) lives at `SKILLS-TO-INTEGRATE/`. The build target lives at `.claude-plugin/`, `skills/`, `commands/`, `hooks/`, `bin/`, `external/`.

## Plugin layout

```
ai-maestro-webdesign/
├── .claude-plugin/plugin.json   Manifest (name, version, skills/commands/hooks paths)
├── README.md                    User-facing plugin overview
├── CLAUDE.md                    THIS FILE — guidance for future Claude sessions
├── LICENSE                      MIT (plugin); sub-skill originals preserved per-skill
├── .gitignore
├── agents/                      Agent layer — 1 main-agent + 19 amw-* specialized sub-agents (4 tiers)
│   ├── ai-maestro-webdesign-main-agent.md  Tier 1 — PRIMARY ORCHESTRATOR (main-agent mode, user-facing)
│   │                                         -- Tier 2 — Discovery / Research (Phase A primarily) --
│   ├── amw-legal-expert-agent.md             Legal/compliance specialist (VETO on mandatory elements)
│   ├── amw-multilanguage-copywriter-agent.md Multilingual copy + RTL + microcopy
│   ├── amw-brand-researcher-agent.md         Competitor analysis + token extraction
│   ├── amw-accessibility-auditor-agent.md    WCAG 2.1 AA audit (A spot-check, B full audit; VETO on hard blockers)
│   ├── amw-seo-strategist-agent.md           Keyword research + IA (A), on-page + schema.org (B)
│   ├── amw-user-research-analyst-agent.md    Persona + journey + onboarding flow + empty-state guidance
│   ├── amw-design-md-auditor-agent.md        DESIGN.md 5-pass audit (structural / drift / a11y / completeness / consistency); no veto
│   │                                         -- Tier 3 — Production / Execution (Phase B only) --
│   ├── amw-wireframe-builder-agent.md        ASCII → HTML with shadcn/Tailwind integration; empty/error/loading states
│   ├── amw-diagram-producer-agent.md         All diagram formats (editorial/architecture/Mermaid/SVG/box/text-visual)
│   ├── amw-infographic-builder-agent.md      Dense HTML/PNG/PDF infographics via 24 templates
│   ├── amw-asset-generator-agent.md          SVG icons/logos + pretext typography + gated Excalidraw
│   ├── amw-video-producer-agent.md           HTML → MP4 via amw-hyperframes-bridge
│   ├── amw-browser-tester-agent.md           amw-dev-browser scenario tests + amw-ux-evaluator
│   ├── amw-design-md-author-agent.md         Author DESIGN.md from a brief / codebase / URL / 5-Q interview
│   ├── amw-design-md-extractor-agent.md      Extract DESIGN.md from URL / Tailwind config / codebase scan
│   │                                         -- Tier 4 — Specialists (Phase B, on-demand) --
│   ├── amw-form-designer-agent.md            Booking/contact/checkout/multi-step forms; validation UX; form a11y
│   ├── amw-email-designer-agent.md           Transactional + marketing emails (MJML, table-layout, dark-mode)
│   ├── amw-motion-designer-agent.md          Page transitions + scroll animations + microinteractions; reduced-motion
│   └── amw-component-library-architect-agent.md  Design tokens + variant matrix + Style Dictionary / Figma-tokens export
├── bin/                         Shared scripts invoked by multiple skills
├── commands/                    Slash commands (/amw-*)
├── hooks/hooks.json             One UserPromptSubmit nudge
├── skills/
│   ├── amw-design-principles/         ORCHESTRATOR — owns the broad design vocabulary
│   ├── amw-ascii-sketch/              Plan-phase ASCII 3-variant loop (input workflow)
│   ├── amw-ascii-to-svg/              DEPRECATED — superseded by `amw-diagram-convert` (IR pivot). Kept as low-level primitive + backward-compat for `/amw-ascii-to-svg` command.
│   ├── amw-ascii-to-html/             ASCII wireframe → responsive HTML
│   ├── amw-ascii-creator/             Single-artifact perfect-ASCII author + validator driver
│   ├── amw-ascii-validator/           Render (JSON→ASCII) + validate (Perl alignment); mandatory gate for all ASCII output
│   ├── amw-ascii-diagrams-reference/  Classic `+-|` ASCII idioms reference library for docs/ADRs
│   ├── amw-box-diagram/               Unicode rounded-corner box-diagram author (pipelines, topologies)
│   ├── amw-text-visual-workflows/     ASCII flowcharts / timelines for PR / launch / triage / incident flows
│   ├── amw-text-visual-arch/          Layered ASCII architecture diagrams for terminals / PRs / ADRs
│   ├── amw-text-visual-state/         ASCII state machines + journey storyboards
│   ├── amw-text-visual-cheatsheets/   ASCII CLI cheat-sheet panels (macOS/Linux vs Windows side-by-side)
│   ├── amw-text-visual-retro/         ASCII retro grids / milestone timelines / heatmaps
│   ├── amw-dev-browser/               The ONLY browser-automation primitive (input)
│   ├── amw-design-extract/            URL → design tokens via designlang (multi-format dump: Tailwind, shadcn, React, Figma, CSS-vars, W3C tokens)
│   ├── amw-design-md/                 Author / lint / extract / audit / convert DESIGN.md (Variant 1 official @google/design.md + Variant 2 community 9-section)
│   ├── amw-ui-ux-reasoning/           Fallback reasoning library
│   ├── amw-ux-designer/               UX process methodology
│   ├── amw-ux-flows/                  PRD → wireframes + Mermaid
│   ├── amw-ux-evaluator/              Systematic UX evaluation
│   ├── amw-diagram-svg/               Natural language → SVG
│   ├── amw-diagram-editorial/         Editorial-quality HTML+SVG diagrams (13 types)
│   ├── amw-diagram-architecture/      Free text → JSON/Mermaid/SVG/PNG (+ optional on-disk versioning)
│   ├── amw-mermaid-render/            Mermaid text → themed SVG / terminal ASCII via vendored beautiful-mermaid
│   ├── amw-excalidraw-illustrations/  GATED — hand-drawn concept illustrations via Gemini API (needs GEMINI_API_KEY)
│   ├── amw-svg-creator/               GATED to icons/logos/technical SVG only
│   ├── amw-infographics/              Dense editorial HTML/PNG/PDF
│   ├── amw-pretext/                   Unified pretext skill — 78 TECH-NN-*.md reference files (API, measure, layout, typography, art, motion, tables, 3d, integrate, workflow, consult). Supersedes pretext-art.
│   ├── amw-pretext-art/               DEPRECATED — redirects to ../amw-pretext/ (kept for backward-compatible trigger routing)
│   ├── amw-hyperframes-bridge/        HTML → MP4 via external/hyperframes
│   ├── amw-shadcn-ui/                 50+ component reference docs
│   ├── amw-tailwind-4/                Tailwind v4 reference
│   ├── amw-seo/                       SEO evaluation framework
│   │
│   │   ── Cross-format diagram toolchain (2026-04-22) ──
│   ├── amw-diagram-formats/           META-SKILL: authoritative format/IR/matrix/diff specs — references only, never emits diagrams
│   ├── amw-html-diagram/              Author or edit HTML-rendered editorial/infographic-style diagrams
│   ├── amw-svg-diagram/               Author or edit standalone SVG diagrams (freeform or layered architecture)
│   ├── amw-mermaid-diagram/           Author or edit Mermaid source text (all 9 grammar types); delegates rendering to amw-mermaid-render
│   ├── amw-diagram-convert/           Cross-format conversion across full 5-format matrix (ASCII/HTML/SVG/Mermaid/PNG)
│   ├── amw-diagram-compare/           IR-level structural diff between two diagrams (formats may differ)
│   ├── amw-webpage-to-diagram/        URL or local HTML → diagram. TWO modes: STRUCTURAL (landmark/link IR graph → ASCII/SVG/Mermaid) + SPATIAL (rendered-DOM geometry → box-drawing ASCII wireframe, agent-facing plan-phase tool, via bin/amw-page-to-ascii-layout.py)
│   ├── amw-diagram-webpage-sync/      Edited diagram (ASCII/SVG/Mermaid) → regenerate target webpage (round-trip reverse leg)
│   │
│   │   ── React-component reference skills (from SKILLS-TO-INTEGRATE/react-components/, 2026-05-24) ──
│   ├── amw-react-colorful/            react-colorful (MIT) — tiny dependency-free color-picker component (Hex/Rgba/Hsl pickers + HexColorInput)
│   ├── amw-progressive-blur/          progressive-blur (MIT) — gradient backdrop blur for React (RadialBlur/LinearBlur)
│   ├── amw-hypercomp/                 hypercomp (MIT) — TS image-processing API compiling to SVG filters (references/operators.md + render-and-react.md)
│   ├── amw-vecui/                     vecui (MIT) — immutable vec2/rect math for JS-driven animated layouts
│   └── amw-react-promptify/           react-promptify (MIT) — async createPrompter/prompt() value-returning modals
├── external/
│   ├── hyperframes/               Vendored submodule — not in skills/
│   └── mermaid-render/            Vendored wrapper for beautiful-mermaid npm package
└── SKILLS-TO-INTEGRATE/           READ-ONLY source material; see docs_dev/ for inventories
```

## Agent layer

The plugin ships an `agents/` folder containing the primary orchestrator plus 19 specialized sub-agents across four tiers. These agents implement the **main-agent mode** of the two-mode workflow (see `skills/amw-design-principles/references/two-mode-workflow.md`).

### Agent-authoring philosophy (read before editing any agent file)

Skills are recipes. Agents are professionals. A skill can be deterministic — "if A then B, if X then Y". An agent operates on variable, incomplete, often contradictory input and cannot anticipate every situation. Writing an agent like a skill produces a brittle wrapper that fails the moment reality deviates from the recipe. Every agent spec in this plugin follows a canonical 14-section template with mandatory **recipe layer** (input contract, operations, skill-decision matrix, return contract) AND mandatory **judgment layer** (mental model, knowledge boundaries, universal decision criteria, uncertainty handling, conflict patterns, delegation rules). Main-agent adds a 15th Orchestration Doctrine section.

The philosophy and template are canonical at `skills/amw-design-principles/references/agent-authoring-philosophy.md`. Every new agent added to `agents/` must follow it; every edit to an existing agent must preserve both layers.

### Tier 1 — Primary orchestrator

`agents/ai-maestro-webdesign-main-agent.md` (opus) — The main orchestrator. Activated on broad design intent ("create a landing page for X", "design a dashboard for Y"). Runs Phase A (interactive discovery + low-fi iteration) and delegates Phase B (implementation) to sub-agents. This is the ONLY agent that talks to the user.

### Tier 2 — Discovery / Research sub-agents (Phase A primarily)

| Agent | Role | Veto |
|---|---|---|
| `amw-legal-expert-agent` | GDPR / ADA / CCPA compliance, disclaimers, jurisdictional restrictions | YES |
| `amw-multilanguage-copywriter-agent` | Web copy for any locale, pluralization, RTL, cultural adaptation | no |
| `amw-brand-researcher-agent` | Competitor analysis, design-token extraction from reference URLs | no |
| `amw-accessibility-auditor-agent` | WCAG 2.1 AA audit (A spot-check, B full audit) | YES |
| `amw-seo-strategist-agent` | Keyword research + IA (A); on-page audit + structured data (B) | no |
| `amw-user-research-analyst-agent` | Persona synthesis, user-journey maps from research artifacts | no |
| `amw-design-md-auditor-agent` | DESIGN.md 5-pass audit (structural / drift / a11y / completeness / consistency); diagnoses, never repairs | no |

### Tier 3 — Production / Execution sub-agents (Phase B only)

| Agent | Role |
|---|---|
| `amw-wireframe-builder-agent` | ASCII → HTML via ascii-to-html + shadcn + Tailwind |
| `amw-diagram-producer-agent` | All diagram formats (editorial/architecture/Mermaid/SVG/box/text-visual); owns format-selection decision |
| `amw-infographic-builder-agent` | Dense HTML/PNG/PDF infographics via 24 templates |
| `amw-asset-generator-agent` | SVG icons/logos/patterns + pretext typography + gated Excalidraw |
| `amw-video-producer-agent` | HTML → MP4 via amw-hyperframes-bridge |
| `amw-browser-tester-agent` | amw-dev-browser scenario tests + amw-ux-evaluator for Phase B verification |
| `amw-design-md-author-agent` | Author Variant 1 DESIGN.md from a brief / codebase / URL / 5-Q interview; lint gate + WCAG contrast pre-flight |
| `amw-design-md-extractor-agent` | Extract Variant 1 DESIGN.md from a live URL / Tailwind config / codebase scan; faithful transcription only |

### Tier 4 — Specialists (Phase B, on-demand)

| Agent | Role | Veto |
|---|---|---|
| `amw-form-designer-agent` | Booking / contact / checkout / multi-step forms with validation UX, error states, form a11y | no |
| `amw-email-designer-agent` | Transactional + marketing emails (MJML, table-layout responsive, dark-mode, plain-text fallback) | no |
| `amw-motion-designer-agent` | Page transitions + scroll-driven animations + microinteractions; prefers-reduced-motion compliance | no |
| `amw-component-library-architect-agent` | Design tokens authoring + variant matrix + design-system handoff exports (JSON / Style Dictionary / Figma tokens) | no |

Tier 4 specialists have NO veto power. They produce specs / exports that Tier 3 producers (typically `amw-wireframe-builder-agent`) consume for final rendering. `amw-email-designer-agent` is the exception — it owns its own render path because email is not a webpage. Tier 4 agents are spawned on-demand only when domain-specific intent is detected (no forms ⇒ no form-designer; no motion ⇒ no motion-designer).

### Shared reference docs (mandatory reading before editing any agent)

All under `skills/amw-design-principles/references/`:

- `agent-authoring-philosophy.md` — judgment layer vs recipe layer; the canonical 14-section template
- `sub-agent-return-contract.md` — YAML header schema every amw-* sub-agent returns
- `agent-interaction-patterns.md` — data hand-offs Phase A + B; one-way tree topology
- `skill-invocation-protocol.md` — DO/DON'T block that blocks orchestrator re-routing
- `authority-hierarchy.md` — conflict resolution; veto power for legal-expert + accessibility-auditor

### Naming convention

New sub-agents follow the pattern `amw-<role>-agent.md` and are placed in `agents/`.

### Delegation rule (hard invariants)

1. Sub-agents NEVER interact with the user directly. All user communication flows through `ai-maestro-webdesign-main-agent`.
2. Delegation is one-way: main-agent → sub-agent → main-agent. Sub-agents do NOT call peer sub-agents directly (prevents loops and keeps context isolated).
3. Sub-agents return structured YAML headers per the canonical schema; main-agent parses the header mechanically and only reads the full markdown body when the summary is insufficient.
4. Veto-holding sub-agents (legal-expert, accessibility-auditor) block Phase B forward progress on their veto domain until user override or resolution.

---

## Core architectural rule — orchestrator priority

`amw-design-principles/SKILL.md` owns the broad design vocabulary: *design, UI, mockup, landing page, wireframe, prototype, slide, deck, poster, website*. It is the first skill Claude Code activates when any of those appear in a user prompt.

Every other skill in `skills/` has its `description` deliberately narrowed to **specific technical triggers** — "extract design tokens from URL", "build a tokenomics infographic", "render HTML as video", "architecture diagram", etc. This guarantees:

- Generic intent ("design a landing page") → `amw-design-principles` activates first, applies its three hard rules, and routes to an executor.
- Specific intent ("build a flowchart of this architecture") → the relevant executor activates without `amw-design-principles` hijacking.

**When editing any SKILL.md, keep this invariant.** A description that re-claims general design vocabulary breaks orchestration.

### Two operating modes (see `skills/amw-design-principles/references/two-mode-workflow.md`)

The orchestrator distinguishes two modes on every incoming request:

- **Command mode** — the user invokes a `/amw-*` command with explicit parameters. Dispatch directly to the target skill; no approval loop.
- **Main-agent mode** — the user states requirements without a concrete format. Phase A (conversational, low-fi, low-token ASCII iteration) runs first via `agents/ai-maestro-webdesign-main-agent.md`; Phase B (sub-agent spawning, real artifacts) starts ONLY after explicit satisfaction tokens are received.

The Phase A → Phase B approval gate is a hard invariant: `amw-design-principles` MUST NOT spawn sub-agents or produce real artifacts (HTML, SVG, PNG, MP4) until the user has confirmed the low-fi direction with `yes`, `ship it`, `approved`, `that's the one`, `perfect`, `done`, `go ahead`, or `let's do it`. Commands are a subset of what each sub-skill enables; an agent in Main-agent mode may invoke any technique any skill exposes, not just those surfaced by commands.

## The three hard rules `amw-design-principles` enforces

1. **Gather context before designing.** Require design system, brand tokens, or reference examples. The `last resort` fallback is `amw-ui-ux-reasoning` — do not fall back to "let me guess."
2. **Always produce at least three variants** (baseline → advanced → experimental). Single-answer output is a failure mode. Use `amw-ascii-sketch` when the user hasn't committed to HTML yet — it is cheap to iterate.
3. **Reject AI-slop patterns.** The full list is in `skills/amw-design-principles/ai-slop-avoid.md`. Any HTML output runs a final check against that file before delivery.

These rules apply to every skill in the plugin. Sub-skills inherit them via the orchestrator; they do not override them.

## ASCII-first plan phase (default workflow)

**The plan phase of every webpage design runs in ASCII, not HTML.** When the user asks for a webpage, landing page, dashboard, or any design artifact, the orchestrator enters `/amw-sketch` and stays there. Iteration on position, size, alignment, and component choice happens in ASCII because:

- ASCII costs ~1% of the tokens that HTML iteration does — the user can push 10+ revisions without hitting context decay.
- ASCII is synchronous in chat, no file writes, no `dev-browser` round trips, no `amw-preview` screenshots until the skeleton is right.
- Each ASCII variant is instant to read and easy to describe edits against ("move the CTA to the right of the hero", "make the feature row 2×2 instead of 3×1").

The loop ends **only** on the canonical satisfaction tokens: `yes`, `ship it`, `convert it`, `that's the one`, `perfect`, `done`. Ambiguous acknowledgement (`looks good`, `sure`, `ok`, `fine`) is not approval — `/amw-sketch` and `/amw-ascii-to-html` both have non-skippable satisfaction gates. After approval, `/amw-ascii-to-html` runs once to produce the real HTML using design-principles tokens and the selected starter-component chrome.

Skills that bypass the ASCII loop (e.g. a user who pastes a design brief and says "build the HTML now") are fine — but the default when the intent is a new webpage is ASCII-first. Do not shortcut to HTML unless the user explicitly opts out.

## amw-dev-browser is the only input-automation primitive

Any skill that needs to inspect a live page — screenshot, DOM extraction, style capture, interactive fill — goes through `skills/amw-dev-browser/` (which wraps the `dev-browser` CLI from https://github.com/SawyerHood/dev-browser, installed by `/amw-init`).

Skills that use Playwright, Puppeteer, or Chromium **only for output rendering** (`amw-infographics/scripts/export.py`, `amw-hyperframes-bridge`, any HTML→PNG pipeline in `bin/amw-html-export.py`) keep their internal render backends because those are output emitters, not interactive automation.

If you are adding a capability that reads live-page state, wire it through `skills/amw-dev-browser/` or `bin/amw-dev-browser-wrapper.sh`. Do not add Chrome DevTools MCP, Playwright MCP, or a new puppeteer wrapper.

## Shared `bin/` scripts

Cross-skill utilities live in `bin/`, not duplicated inside each skill:

| Script | Used by |
|---|---|
| `amw-svg-render.py` | amw-svg-creator, amw-ascii-to-svg, amw-diagram-editorial |
| `amw-html-export.py` | amw-infographics, amw-hyperframes-bridge, amw-ascii-to-html (optional PDF export) |
| `amw-preview-server.py` | amw-infographics interactive-builder, amw-ascii-sketch multi-variant preview |
| `amw-ascii-parse.py` | amw-ascii-to-svg, amw-ascii-to-html |
| `amw-ascii-render.py` | amw-ascii-validator, amw-ascii-sketch (perfect-ascii pure-Python renderer, 4 modes: diagram/table/layers/sequence, 78-col max) |
| `amw-validate-ascii.py` | amw-ascii-validator, amw-ascii-sketch, amw-ascii-to-html (alignment + width + wide-char + forbidden-char validator, with FIX hints) |
| `amw-designlang-wrapper.sh` | amw-design-extract |
| `amw-dev-browser-wrapper.sh` | amw-dev-browser, amw-preview, amw-extract-style, any interactive-inspection workflow |
| `amw-diagram-ir.py` | amw-diagram-convert, amw-diagram-compare, amw-html-diagram, amw-svg-diagram, amw-mermaid-diagram, amw-webpage-to-diagram, amw-diagram-webpage-sync (IR parse/validate/emit/diff) |
| `amw-diagram-detect-format.sh` | amw-validate-diagram.sh, amw-diagram-convert, amw-diagram-compare (sniff ASCII/HTML/SVG/Mermaid/PNG) |
| `amw-parse-html-diagram.py` | amw-diagram-ir.py (HTML → IR parser) |
| `amw-parse-svg-diagram.py` | amw-diagram-ir.py (SVG → IR parser) |
| `amw-parse-mermaid-diagram.py` | amw-diagram-ir.py (Mermaid → IR parser) |
| `amw-validate-html-diagram.sh` | amw-validate-diagram.sh (HTML diagram structure validation) |
| `amw-validate-svg-diagram.sh` | amw-validate-diagram.sh (SVG diagram structure validation) |
| `amw-mermaid-lint.sh` | amw-validate-diagram.sh (Mermaid syntax lint via mmdc) |
| `amw-validate-diagram.sh` | amw-validate-any-diagram-format, amw-diagram-convert, amw-diagram-compare (unified format-dispatch validator) |
| `amw-dom-to-ir.py` | amw-webpage-to-diagram (HTML DOM landmarks → IR graph; STRUCTURAL mode) |
| `amw-page-to-ascii-layout.py` | amw-webpage-to-diagram (rendered-DOM `getBoundingClientRect` geometry → box-drawing ASCII spatial wireframe; SPATIAL mode; self-validates via amw-validate-ascii.py; clean-room) |
| `amw-html-diff.py` | amw-diagram-webpage-sync (HTML structural diff for showing what changed after re-emission) |
| `amw-design-md-lint.sh` | amw-design-md, amw-design-md-author-agent, amw-design-md-extractor-agent, amw-wireframe-builder-agent (wraps `npx @google/design.md lint` — official linter) |
| `amw-design-md-validate.py` | amw-design-md (offline pure-Python frontmatter + section + token-reference validator) |
| `amw-design-md-contrast.py` | amw-design-md, amw-accessibility-auditor-agent (WCAG-AA pair-level contrast on every color pair in DESIGN.md) |
| `amw-design-md-from-url.sh` | amw-design-md-extractor-agent (URL → DESIGN.md; delegates to amw-dev-browser for DOM + computed styles) |
| `amw-design-md-from-tailwind.{ts,mjs}` | amw-design-md-extractor-agent (Tailwind v3/v4 config + globals.css → DESIGN.md; pure-local, no remote calls) |
| `amw-design-md-from-codebase.py` | amw-design-md-extractor-agent (codebase scan → DESIGN.md; auto-detects Tailwind / shadcn / Chakra / vanilla-CSS / styled-components) |
| `amw-design-md-emit-companions.py` | amw-design-md, amw-component-library-architect-agent (DESIGN.md → tokens.css / tokens.json / component-inventory.md / usage-prompt.md) |
| `amw-design-md-convert-v2-to-v1.py` | amw-design-md (Variant 2 community 9-section → Variant 1 canonical YAML + 8-section) |
| `amw-design-md-diff.sh` | amw-design-md (wraps `npx @google/design.md diff` with Python YAML-aware fallback) |
| `amw-mermaid-render.sh` | amw-mermaid-render, any skill that emits Mermaid source (wrapper over `external/mermaid-render/`; Mermaid text → SVG or ASCII) |
| `amw-mjml-render.sh` | amw-email-designer-agent (MJML source → HTML email; requires mjml npm package) |
| `amw-html-validate.sh` | amw-validate-diagram.sh and any HTML validation flow (xmllint + tidy wrapper) |
| `amw-validate-ascii.py` | amw-ascii-validator, amw-ascii-sketch, amw-ascii-to-html (Python ASCII validator — sole validator; replaces former Perl version) |
| `amw-ai-slop-check.py` | amw-wireframe-builder-agent, amw-diagram-producer-agent, amw-infographic-builder-agent, amw-asset-generator-agent, amw-email-designer-agent (mechanical enforcement of `amw-design-principles/ai-slop-avoid.md`) |
| `amw-validate-cross-refs.sh` | CI-time gate; called by maintainers / `/amw-doctor` |
| `amw-skill-trigger-collision.py` | CI-time gate; called by maintainers / `/amw-doctor` |
| `amw-html-section-count.py` | amw-wireframe-builder-agent, amw-infographic-builder-agent, amw-design-md-author-agent (replaces LLM-based section/heading audits) |

When extracting a utility from a source skill, prefer upgrading it to `bin/` if at least two skills benefit. Skill-specific one-offs stay in the skill's own folder.

## Runtime dependencies

Three classes, all surfaced by `/amw-doctor`:

- **System-required (user responsibility):** `node ≥22`, `git`, `python ≥3.8`.
- **Installed at runtime via `/amw-init`:** `bun`, `ffmpeg`, `playwright` (+ Chromium), `cairosvg`, `dev-browser` CLI (+ `dev-browser install`).
- **Bundled:** only the Python / shell scripts in `bin/`. No compiled binaries — keeps the plugin repo reviewable.

## Non-obvious conventions

### Tweaks postMessage protocol (hard rules, preserved from original)
See the `<!-- HARD INVARIANTS -->` comment at the top of `skills/amw-design-principles/starter-components/tweaks-block.html` for the three invariants any editor must preserve (listener-before-post ordering, partial-update-only payloads, valid-JSON editmode block).

### React/Babel pinning
`skills/amw-design-principles/starter-components/react-babel-pins.md` pins exact React 18.3.1 + Babel 7.29.0 UMD CDN URLs with integrity hashes. Do not drop the `integrity` attributes, do not use `react@18` without the patch version, do not switch to `type="module"`.

### Dimensional hard limits
- 1920×1080 slides: min font 24px
- Mobile mockups: min font 14px, min hit target 44×44px
- Desktop body copy: min 16px
- Slides carry `data-screen-label="01 Title"` (1-indexed); player/position state persists to localStorage.

### Animation stack order
Use `starter-components/animations.html` (≈50-LOC timeline core) first. Fall back to Popmotion only for physics/spring/drag. **No Framer Motion, no GSAP.**

### Scroll behavior
`scrollIntoView` is banned — it corrupts the parent window's scroll position when output is embedded in an iframe host. Use manual offset + `window.scrollTo({top, behavior: 'smooth'})`.

### File-management rules `amw-design-principles` imposes on users
- Descriptive English filenames for generated artifacts (`Landing Page.html`, not `design.html`).
- No `v2`/`v3` proliferation — variants become Tweaks inside the main file. Duplicate files only when the user explicitly wants to compare old vs new.
- Split when a file exceeds ~1000 lines.

### The original skill was bilingual Chinese-English; this plugin is English-only
The source `claude-design-principles/` on disk is Chinese-first. The plugin target `skills/amw-design-principles/` is a full English rewrite that preserves every rule, threshold, table, and example. When adding content to `amw-design-principles/`, write in English.

## Build state (phase-by-phase)

The plan lives at `~/.claude/plans/jazzy-skipping-engelbart.md`. Completed 2026-04-21 in one session via a parallel opus-agent swarm:

- **Group A (A1/A2/A3)** — Plugin skeleton: manifest, README, root CLAUDE.md, LICENSE, .gitignore, 8 slash commands, 1 hooks.json. DONE.
- **Group B (B1/B2)** — Shared `bin/` scripts: amw-svg-render.py, amw-html-export.py, amw-preview-server.py, amw-ascii-parse.py, amw-dev-browser-wrapper.sh, amw-designlang-wrapper.sh. DONE.
- **Group C (C1/C2/C3/C3b/C3c)** — amw-design-principles English rewrite: SKILL.md, ai-slop-avoid, color-system, typography-system, spacing-rhythm, design-heuristics, question-templates, and all 9 starter-components (translated in-place from bilingual source). DONE.
- **Group D (D1/D2/D3/D4/D5/D6)** — 15 adapted executor skills in plugin house style (narrow triggers, orchestrator header, dependency schema, cross-references): amw-dev-browser, amw-design-extract, amw-ui-ux-reasoning, amw-ux-designer, amw-ux-evaluator, amw-ux-flows, amw-diagram-svg, amw-diagram-editorial, amw-diagram-architecture, amw-svg-creator (gated), amw-infographics, amw-pretext-art, amw-hyperframes-bridge, amw-shadcn-ui, amw-tailwind-4, amw-seo. DONE.
- **Group E (E1)** — 3 NEW ASCII skills: amw-ascii-sketch (plan-phase loop), amw-ascii-to-svg, amw-ascii-to-html. DONE.
- **Group F** — Structural verification (CJK residue, frontmatter validity, banned-ref scan, model-pin scan, file counts). DONE.

**Inventory addendum (react-components integration, 2026-05-24):** +5 React-component reference skills (`amw-react-colorful`, `amw-progressive-blur`, `amw-hypercomp`, `amw-vecui`, `amw-react-promptify`, all MIT, sourced from `SKILLS-TO-INTEGRATE/react-components/`) and +1 bin script (`amw-page-to-ascii-layout.py`). `amw-webpage-to-diagram` gained a second SPATIAL mode (rendered-DOM geometry → ASCII wireframe). `framer-motion-theatre` was evaluated and SKIPPED (proprietary Theatre.js/Framer-Motion deps + no-Framer-Motion rule); `figma-copy-as-markdown` was NOT ported (unlicensed) — its capability was reimplemented clean-room as the SPATIAL mode. Current totals: 46 skill dirs (45 live + `amw-pretext-art` deprecated redirect), 38 bin scripts, 29 slash commands, 20 agents.

**Final inventory (after diagrams-skills synthesis round + cross-format build + pretext unification, 2026-04-24):** 40 SKILL.md files (amw-pretext-art now redirects to the new unified `amw-pretext/` skill; +1 new `amw-pretext/` with 78 `references/TECH-NN-*.md` files across 11 categories: api, measure, layout, typography, art, motion, tables, 3d, integrate, workflow, consult), 201 shadcn MDX docs preserved, 24 infographic templates, 15 infographic examples, 8 infographic resources, 9 translated starter-components, 7 CHI'24 ASCII-archetype reference files, 20 slash commands, 33 bin scripts, 1 hook, 1 plugin.json, 1 external vendored backend (amw-mermaid-render). Zero CJK in text files. No outdated model pins. All sub-skills reference the orchestrator explicitly.

**Pretext unification (2026-04-24):** The 21 zipped pretext variants + 10 loose `SKILL-NN.md` in `SKILLS-TO-INTEGRATE/web-design/pretext-skills/` were consolidated into ONE plugin skill: `skills/amw-pretext/`. Each distinct technique (13 API functions, 5 measurement prerequisites, 6 layout / obstacle patterns, 9 typography techniques, 14 art effects, 9 motion demo families, 3 tables variants, 2 3D techniques, 9 integration patterns, 5 workflow assemblies, 3 consult routings) lives in its own `references/TECH-NN-<slug>.md` file. Orchestrator routes the narrow trigger set ("pretext", "text-on-path", "shrink-wrap text", "virtualized list", "balanced headline", "kinetic typography", etc.) to `skills/amw-pretext/SKILL.md`. The existing `skills/amw-pretext-art/` was redirected (not deleted — repo is not git-tracked). Full backup at `docs_dev/backups/20260424_035817+0200-pretext-unify/`.

**Diagrams + ASCII toolchain** (integrated from `SKILLS-TO-INTEGRATE/diagrams-skills/`):

- `bin/amw-ascii-render.py` — perfect-ascii's pure-Python renderer (JSON → ASCII). 4 modes (diagram / table / layers / sequence), 78-col max. Alignment guaranteed by construction.
- `bin/amw-validate-ascii.py` — Python ASCII validator (ASCII → PASS/FAIL with `FIX:` hints). Catches width mismatches, nested-box corner drift, vertical `│` misalignment, wide-char leak (emoji/CJK), forbidden chars (`▼▲⟶⇒`).
- `bin/amw-mermaid-render.sh` + `external/mermaid-render/` — Mermaid text → SVG or themed ASCII, vendored beautiful-mermaid backend.
- `skills/amw-ascii-creator/` — SINGLE-artifact authoring (ASCII twin of svg-creator) with 2 modes: Mode A structured via ascii-render.py, Mode B freeform via validator loop.
- `skills/amw-ascii-validator/` — documents the toolchain + the MANDATORY validation gate every ASCII emitter must pass before delivery.
- `skills/amw-ascii-diagrams-reference/` — CHI'24-based archetype library (flowcharts, state-machines, trees, data-structures, network-topology, sequences-tables, graphs-annotations).
- `skills/amw-box-diagram/` — Clean Unicode rounded-corner box diagrams (`╭╮╰╯│─`) for pipeline/workflow charts.
- `skills/amw-mermaid-render/` — Mermaid SVG+ASCII renderer with 15+ themes.
- `skills/amw-excalidraw-illustrations/` — Gemini-API hand-drawn concept illustrations (GATED — explicit cost, `$GEMINI_API_KEY` required).
- `skills/amw-text-visual-{workflows,arch,state,cheatsheets,retro}/` — 5 paste-into-PR ASCII visualization skills.

All skills reference `amw-design-principles/SKILL.md` as orchestrator and require `bin/amw-validate-ascii.py` pass before ASCII emission.

**Cross-format diagram toolchain (2026-04-22, Phases 0–4 of the 12-commands build):**

The plugin now ships a full cross-format diagram authoring, conversion, comparison, and webpage round-trip capability. Key architectural elements:

- `skills/amw-diagram-formats/` — shared reference library: format specs (ASCII, HTML, SVG, Mermaid), the IR schema, the N×N conversion matrix, format-detection contract, validate-dispatcher, modify-flow, diff-algorithm. Referenced by all 7 new executor skills. Never emits diagrams itself.
- **IR (`diagram-ir/1.0`)** — the pivot format for every cross-format conversion. Every parser emits IR; every emitter consumes IR. This decouples N parsers from N emitters without N² special cases.
- New bin scripts (11 total): `amw-diagram-ir.py` (IR parse/validate/emit/diff), `amw-diagram-detect-format.sh` (sniff ASCII/HTML/SVG/Mermaid/PNG), `amw-parse-html-diagram.py`, `amw-parse-svg-diagram.py`, `amw-parse-mermaid-diagram.py` (format parsers → IR), `amw-validate-html-diagram.sh`, `amw-validate-svg-diagram.sh`, `amw-mermaid-lint.sh`, `amw-validate-diagram.sh` (unified dispatcher), `amw-dom-to-ir.py` (webpage DOM → IR), `amw-html-diff.py` (HTML structural diff).
- PNG is **output-only** across the entire plugin — no parser exists for PNG input. Any skill that would need to read a PNG refuses the request and explains why.
- New 12 slash commands (Phases 2–4): `amw-create-or-modify-ascii-diagram`, `amw-create-or-modify-html-diagram`, `amw-create-or-modify-svg-diagram`, `amw-create-or-modify-mermaid-diagram`, `amw-create-excalidraw-like-diagram-png`, `amw-convert-any-diagram-format`, `amw-validate-any-diagram-format`, `amw-compare-diagrams`, `amw-create-diagram-from-webpage`, `amw-create-webpage-from-diagram`, `amw-modify-webpage-from-diagram`, `amw-modify-diagram-of-webpage`.

**Not yet done:**
1. **Runtime acceptance tests** — behavioral scenarios `/amw-extract-style https://stripe.com`, `/amw-sketch "dashboard"`, `/amw-ascii-to-html`. Requires the plugin to be installed and dependencies via `/amw-init`. Out of build scope — user runs these.
2. **`external/hyperframes/` submodule** — cloned 2026-04-26 from `https://github.com/heygen-com/hyperframes` (canonical fork) at v0.4.30 (244MB). Bridge skill + agent realigned to v0.4.30 in same session. The bridge previously documented an invalid `bun run render --input <html>` invocation — that was a pre-existing bug (the script never existed; `--input` was never a real flag). Fixed: render path is now `cd <project_dir> && npx hyperframes render --output <mp4>` with two contracts (default `html_scene_path` → bridge scaffolds a temp project; advanced `project_dir` → bridge uses directly). Pre-render gate sequence is now `lint → validate → inspect → render` (added `inspect` — new in v0.4.30 — for visual layout audit). New attribute `data-variable-values` documented for per-instance variable injection into sub-compositions.
3. **Publishing** — eventual push to `Emasoft/ai-maestro-plugins` after runtime acceptance.

## Session gotchas for future Claude instances

- `SKILLS-TO-INTEGRATE/` is **read-only** by user directive — extract and adapt, do not modify sources.
- Deletion of anything in this repo requires the file to be git-tracked and committed **in the current session**. This repo is not yet a git repo. Before any delete or significant rewrite of an existing file, back it up into `docs_dev/` first.
- Inventory reports are authoritative for what each source skill does and depends on:
  - `docs_dev/2026-04-20-inventory-diagrams-skills.md`
  - `docs_dev/2026-04-20-inventory-image-generation.md`
  - `docs_dev/2026-04-20-inventory-web-design.md`
- When in doubt about a source skill's capability, read its inventory entry first — do not re-explore the source.
