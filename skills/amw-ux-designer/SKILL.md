---
name: amw-ux-designer
description: UX-process methodology — user research plans, persona creation, journey/empathy maps, usability-test protocols, WCAG AA audits, IA (card sort / tree test). Triggers on "user research plan", "persona template", "heuristic review", "WCAG audit", "IA review", "journey map". Does NOT trigger on "design a page" (design-principles), "PRD to flows" (ux-flows), "evaluate this page" (ux-evaluator). Use when producing a UX plan, persona, or journey map. Trigger with "user research plan".
version: 0.1.0
---

# UX Designer

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

UX-process methodology reference covering the full 5-phase research-to-handoff lifecycle: Discover (user research, interviews, 5 Whys), Define (personas, journey maps, empathy maps), Ideate (task flows, IA card sort), Prototype & Test (usability-test protocols, moderated/unmoderated), and Handoff (WCAG AA checklists, microcopy review). Produces written deliverables only — personas, journey maps, IA sitemaps, usability plans, WCAG checklists. Visual output routes downstream to `amw-ascii-sketch` or `amw-ux-flows`.

## Instructions

1. Identify the UX-methodology deliverable requested: persona, user journey map, empathy map, research plan, usability-test protocol, IA sitemap, WCAG AA checklist, or microcopy review.
2. Walk the `## Technique selection` tree and open the relevant TECH reference file from `references/` (e.g. `TECH-ux-persona-template.md`, `TECH-ux-process-discover.md`).
3. Read the appropriate rule file from `rules/` for the deliverable type (e.g. [research](rules/research.md) for interviews/personas, [accessibility](rules/accessibility.md) for WCAG).
4. Produce the structured deliverable using the template in the TECH file (persona: goals/pain points/behaviors/quote; research plan: interview script + participant criteria + synthesis method; WCAG checklist: criteria + pass/fail per component).
5. Route downstream when done: PRD + wireframes → `../amw-ux-flows/`; visual iterations → `../amw-ascii-sketch/`; evaluation of an existing design → `../amw-ux-evaluator/`.

See `## Usage` below.

## Examples

See [TECH-ux-persona-template](references/TECH-ux-persona-template.md) for a complete persona example ("Sarah, The Busy Parent") and [TECH-ux-process-discover](references/TECH-ux-process-discover.md) for a user-research plan example.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during Phase A (when requirements analysis calls for UX methodology deliverables) or Phase B (when a WCAG audit or IA review is part of the implementation). The orchestrator may apply any research, persona, or accessibility technique from this skill without command-layer restriction.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

PLAN (Phase A support). Provides UX-process methodology (research → define → ideate → prototype → handoff) that complements design-principles' visual focus. Produces written deliverables (personas, journey maps, flow analyses, usability-test plans, WCAG checklists) that feed downstream visual skills.

## Trigger conditions
Activate only on UX-process-specific phrases:
- "user research", "research plan", "user interviews", "5 Whys"
- "create personas", "persona template", "build a persona"
- "user journey map", "empathy map", "pain points"
- "user flow diagram", "task flow", "happy path and error states"
- "usability test plan", "moderated/unmoderated test", "task success rate"
- "accessibility review", "WCAG audit", "WCAG AA checklist"
- "information architecture", "card sort", "tree test", "navigation audit"
- "microcopy review", "button copy", "error message review"

Do **not** activate on generic "design a page", "make a UI", "landing page", "wireframe a dashboard" — those belong to the orchestrator (`design-principles`).

## Prerequisites
- runtime_binaries: none (methodology reference)
- python_packages: none
- npm_packages: none

## Usage
Invoked by the orchestrator or directly when a UX-process trigger fires. Reads the appropriate rule file from `rules/` and returns a structured deliverable using the templates below.

**Deliverables produced:**
- Persona (goals, pain points, behaviors, quote)
- User flow (entry point, steps, error states, decision points)
- Design review (usability issues by severity, accessibility concerns with WCAG references, strengths)
- Research plan (interview script, participant criteria, synthesis method)
- WCAG AA audit checklist

**Rule files (read on demand):**
- [research](rules/research.md) — user interviews, personas, synthesis
- [accessibility](rules/accessibility.md) — WCAG AA, inclusive design
- [information-architecture](rules/information-architecture.md) — navigation, content organization
- [interaction-design](rules/interaction-design.md) — user flows, microcopy
- [visual-design](rules/visual-design.md) — hierarchy, design system essentials

**Handoff:**
- When the user has a PRD and wants wireframes → route to [SKILL](../amw-ux-flows/SKILL.md)
- When the user wants visual design iterations → return methodology output, then route to [SKILL](../amw-ascii-sketch/SKILL.md) for 3-variant proposals
- When the user wants validation on an existing design → route to [SKILL](../amw-ux-evaluator/SKILL.md)

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `ux-designer` is the user asking about?
  - **ux** (11 techniques)
    - [TECH-ux-persona-template](./references/TECH-ux-persona-template.md) — Persona template + good vs bad examples
      > What it does · When to use · How it works · Minimal example · Good persona · Bad persona · Gotchas · Cross-references
    - [TECH-ux-process-define](./references/TECH-ux-process-define.md) — UX process — Define (Phase 2)
    - [TECH-ux-process-discover](./references/TECH-ux-process-discover.md) — UX process — Discover & Research (Phase 1)
    - [TECH-ux-process-handoff](./references/TECH-ux-process-handoff.md) — UX process — Handoff & Iterate (Phase 5)
    - [TECH-ux-process-ideate](./references/TECH-ux-process-ideate.md) — UX process — Ideate & Design (Phase 3)
    - [TECH-ux-process-prototype](./references/TECH-ux-process-prototype.md) — UX process — Prototype & Test (Phase 4)
    - (see `## References` for the remaining 5 in this group)

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-ux-persona-template.md](./references/TECH-ux-persona-template.md)**
  > What it does · When to use · How it works · Minimal example · Good persona · Bad persona · Gotchas · Cross-references
  - Description: Persona template + good vs bad examples
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Sarah, The Busy Parent
    - User Type A
    - Gotchas
    - Cross-references
- **[./references/TECH-ux-process-define.md](./references/TECH-ux-process-define.md)**
  - Description: UX process — Define (Phase 2)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Sarah, The Busy Parent
    - Gotchas
    - Cross-references
- **[./references/TECH-ux-process-discover.md](./references/TECH-ux-process-discover.md)**
  - Description: UX process — Discover & Research (Phase 1)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-ux-process-handoff.md](./references/TECH-ux-process-handoff.md)**
  - Description: UX process — Handoff & Iterate (Phase 5)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-ux-process-ideate.md](./references/TECH-ux-process-ideate.md)**
  - Description: UX process — Ideate & Design (Phase 3)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-ux-process-prototype.md](./references/TECH-ux-process-prototype.md)**
  - Description: UX process — Prototype & Test (Phase 4)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-ux-rule-accessibility.md](./references/TECH-ux-rule-accessibility.md)**
  > What it does · When to use · How it works · WCAG AA (minimum floor) — four POUR pillars · Inclusive design patterns (beyond compliance) · Testing checklist · Minimal example · Gotchas · Cross-references
  - Description: Rule — Accessibility & Inclusive Design (WCAG AA)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-ux-rule-ia.md](./references/TECH-ux-rule-ia.md)**
  > What it does · When to use · How it works · Navigation structure · Navigation patterns · Mobile specifics · Content organization · Information scent · Search as navigation · Minimal example · Gotchas · Cross-references
  - Description: Rule — Information Architecture
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-ux-rule-interaction.md](./references/TECH-ux-rule-interaction.md)**
  > What it does · When to use · How it works · Flow best practices · Multi-step flows · Error recovery · Microcopy · Specific rules · Minimal example · Gotchas · Cross-references
  - Description: Rule — Interaction Design (flows + microcopy)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-ux-rule-research.md](./references/TECH-ux-rule-research.md)**
  > What it does · When to use · How it works · Interview planning · During interviews · Synthesis · Good vs bad questions · Minimal example · Gotchas · Cross-references
  - Description: Rule — User Research (interviews + personas + synthesis)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-ux-rule-visual.md](./references/TECH-ux-rule-visual.md)**
  > What it does · When to use · How it works · Establishing hierarchy · Typography scale · Color usage · Layout · Design-system essentials · Component documentation · Minimal example · Gotchas · Cross-references
  - Description: Rule — Visual Design (hierarchy + design system)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-ux-designer/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. UX methodology deliverables — personas, journey maps, IA sitemaps, wireframe instructions). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/references/` or `./design/wireframes/` created fresh)
   - Last-resort scratch: `/tmp/amw-ux-designer-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- <artifact-path> — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.

## Resources
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator; applies the three hard rules
- [SKILL](../amw-ux-flows/SKILL.md) — PRD → wireframes pipeline (when the user has a PRD)
- [SKILL](../amw-ux-evaluator/SKILL.md) — validation at the end of the UX process
- [question-templates](../amw-design-principles/question-templates.md) — question patterns for user research
  > Universal must-ask (every design task) · Context & starting point · Task & goal · Variant dimensions · Tweaks · Hard constraints · Task-specific additions · Landing page / Website · Slides / Deck · App / Prototype · Poster / Single image · Infographic / Data viz · Brand collateral (business cards / invitations / emblems) · Questions NOT to ask · Suggested format · Tip
- [design-heuristics](../amw-design-principles/design-heuristics.md) — Gestalt/Fitts/Hick laws for IA and prototyping
  > I. Gestalt's five principles (organizing the visual field) · Proximity · Similarity · Closure · Continuity · Figure-Ground · II. Fitts's Law · Application · III. Hick's Law · Application · Counter-example · IV. Miller's Law (7 ± 2) · Application · V. Jakob's Law · Application · VI. The four dimensions of visual hierarchy · Counter-example (no hierarchy) · Correct example (clear hierarchy) · VII. F-Pattern vs Z-Pattern reading · F-Pattern (long content / text-dense) · Z-Pattern (short content / visually driven) · VIII. Peak-End Rule · Application · IX. Aesthetic-Usability Effect · Self-check list
- `../amw-design-principles/starter-components/design-canvas.html` — the 8pt-grid canvas where personas land in plan-to-visual handoff.

## Non-negotiables
- Activates only on UX-process-specific triggers. Do not take over generic design intent.
- Output is methodology deliverables (personas, journey maps, wireframe instructions, WCAG checklists), not final visual design — the latter routes through `ascii-sketch` → `ascii-to-html`.
- Personas must be based on real research data. Flag "aspirational" or demographic-only personas as anti-patterns.
- Accessibility is not negotiable: every design-review deliverable includes a WCAG AA section.
- Priority order when issues conflict: User Needs → Accessibility → Usability → Visual Hierarchy → Consistency.

## Error Handling
- Generating personas without requiring real research input (anti-pattern).
- Recommending visual design changes instead of returning methodology output.
- Skipping accessibility review on design-review deliverables.
- Producing wireframes directly instead of handing off to `ux-flows` or `ascii-sketch`.
- Using vague microcopy recommendations ("Submit", "OK") instead of specific verbs ("Create Account", "Delete Project").
