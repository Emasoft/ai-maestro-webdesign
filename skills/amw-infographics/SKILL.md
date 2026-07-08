---
name: amw-infographics
description: Dense editorial infographics as HTML + PNG + PDF from a structured data brief — tokenomics, whitepaper summaries, ecosystem maps, roadmaps, airdrop guides, staking breakdowns, stat posters. Triggers on "infographic", "tokenomics graphic", "ecosystem map", "turn stats into a graphic". NOT for generic design (design-principles) or editorial diagrams (diagram-editorial). Use when producing a dense infographic from a data brief. Trigger with /amw-create-or-modify-html-diagram.
author: ai-maestro-webdesign
---

# Infographics

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Triggers are data-infographic-specific only — `design-principles` routes here when the user has real data or a structured brief and wants a shareable, dense editorial graphic.

## Overview

Produces dense editorial infographics as self-contained HTML + retina PNG + print-ready PDF from a 24-template library and 175-design DNA set. Three execution modes: Interactive Builder (component-by-component with live preview), One-Shot (full infographic in one pass), and Guided Creative (two composition options before building). Near-black backgrounds, warm+cool accent palettes, all-caps condensed display fonts, high content density (8–15 blocks on portrait-medium). Not a generic webpage renderer — closer to a crypto research poster or game cheat sheet.

## Instructions

1. Classify the invocation mode: Interactive Builder, One-Shot, or Guided Creative. Full step-by-step workflows in [_execution-modes](references/_execution-modes.md).
> [_execution-modes.md] A. Interactive Builder · B. One-Shot · C. Guided Creative · Quality gate (before delivery) · Cross-references
2. For One-Shot and Guided Creative: ask the three Design Brief questions (brand, platform, key insight); classify the content type, archetype, and dominant component.
3. Build the infographic as a single self-contained HTML with required head includes (Google Fonts, Phosphor Icons, optional Chart.js); apply playbook colors/fonts; all CSS inline with `:root` custom properties.
4. Run the Anti-Frontend Checklist and Reduction Pass per the Quality Gate (see [_execution-modes](references/_execution-modes.md)).
> [_execution-modes.md] A. Interactive Builder · B. One-Shot · C. Guided Creative · Quality gate (before delivery) · Cross-references
5. Export via `bin/amw-html-export.py -i {file}.html -o {name} -f all --width {W} --scale 2`.

## Activation

Callable directly via the `/amw-create-or-modify-html-diagram` command with `--style infographic`. Also invoked by the `design-principles` orchestrator as a Phase B renderer after Phase A approval in Main-agent mode. In Main-agent mode the orchestrator may apply the full 24-template library, 175-design DNA, and multi-format export techniques beyond what the command's parameters expose.

This skill is **autonomous and self-contained** — any agent can use it by reading this SKILL.md and its references.

## Position in flow

**OUTPUT (Phase B).** Emits self-contained HTML + retina PNG + print-ready PDF. Each file is dense editorial reference material — closer to a crypto research poster or game cheat sheet than a website. Not a substitute for `../amw-diagram-editorial/`, `../amw-svg-creator/`, or `../amw-ascii-to-html/`.

## What this skill produces

- **HTML** — self-contained, CDN fonts (Bebas Neue, Montserrat, Teko, Orbitron via Google Fonts) + Phosphor Icons + optional Chart.js.
- **PNG** — retina (2x) via `../../bin/amw-html-export.py` (Playwright + Chromium).
- **PDF** — print-ready via the same script.
- **Canvas sizes** (7): portrait-medium 1080×1440 (default), Twitter/X 1200×675, Instagram 1080×1080, Instagram portrait 1080×1350, LinkedIn 1200×627, Pinterest 1000×1500, website 1100×auto. Full table in [platform-sizes](resources/platform-sizes.md).
> [platform-sizes.md] Quick Reference · Layout & Font Adjustments Per Platform · Font Size Scaling by Platform · Watermark / Attribution Rule by Platform · export.py Commands by Platform

## Design DNA + non-negotiable rules

Derived from 175 real designs. Density is the defining trait (8–15 content blocks), backgrounds are near-black, palette is warm+cool, display fonts are all-caps condensed (Bebas Neue default), Stacked Reference archetype is the default. Full rules in [_design-dna](references/_design-dna.md). Seven non-negotiable rules (no fabricated data, no generic display fonts, no emojis as icons, brand color first, dark default, real assets only, footer by default) in [_non-negotiables](references/_non-negotiables.md).
> [_non-negotiables.md] Rules 1–7 · Cross-references
> [_design-dna.md] Density is the defining trait · Backgrounds are near-black · Palette is warm + cool together · Display fonts are all-caps condensed · Stacked Reference is the default composition · Section variety is mandatory · Arrows are load-bearing · Visible borders, not ghost borders · Tight spacing inside sections · Content format hierarchy · Cross-references

## 24-template index

24 fully-built reference templates ship in `templates/` (13 crypto/web3 + 11 generic). Each uses V4 CSS standards (12px dense tables, `▸` bullet panels, arrow connectors, stat strips). Full inventory + user-says-to-template selection table in [_template-registry](references/_template-registry.md).
> [_template-registry.md] Crypto / Web3 (13 templates) · Generic (11 templates) · Template selection table · Cross-references

## Execution modes

Three modes — Interactive Builder, One-Shot, Guided Creative. Full workflows + Quality Gate in [_execution-modes](references/_execution-modes.md).
> [_execution-modes.md] A. Interactive Builder · B. One-Shot · C. Guided Creative · Quality gate (before delivery) · Cross-references

## Technique selection

Pick a technique category, then look up the specific TECH file in [_index](references/_index.md). Every TECH file shares a TOC structure (What it does · When to use · How it works · CSS · HTML · Gotchas · Cross-references) plus 1–4 technique-specific subsections.
> [_index.md] Modes (3) · Archetypes (5) · Playbooks (5 content-type playbooks) · Components (15) · Charts (10) · Color & typography (8) · Copy (3) · Aesthetic systems (3) · Pre-delivery / quality (2) · Pipeline / preview / export (3) · Cross-references

Categories: Mode (3), Archetype (5), Playbook (5 content-type playbooks), Component (15), Chart (12), Color & typography (8), Copy (3), Aesthetic systems (3), Pre-delivery / quality (2), Pipeline / preview / export (4).

## Prerequisites + pipeline + examples

System `python3 ≥ 3.8`; Playwright + Chromium and `playwright ≥ 1.40.0` installed via `/amw-init`; CDN fonts/icons at run-time. Full dependency list, the token-economics One-Shot worked example, and the output/report schema are in [_pipeline-and-examples](references/_pipeline-and-examples.md).
> [_pipeline-and-examples.md] Prerequisites · Examples · Output

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — upstream orchestrator.
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — final AI-slop scan every HTML output must pass.
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- [color-system](../amw-design-principles/color-system.md) — brand-color / WCAG AA validation when a custom color is supplied.
> [color-system.md] I. Always prefer oklch over rgb / hex / hsl · II. WCAG contrast — hard requirement · III. Palette structure (cap at 5–7 colors) · IV. Dark mode is not a simple inversion · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [typography-system](../amw-design-principles/typography-system.md) — type-scale rules that compose with this skill's display-font hierarchy.
> [typography-system.md] I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax · VIII. Forbidden AI-giveaway fonts (T-043)
- `../../bin/amw-html-export.py` — PNG / PDF / SVG export pipeline.
- `../../bin/amw-preview-server.py` — Mode A live preview server, port 7883.
- [design-brief](resources/design-brief.md) — 5-question intake framework + aesthetic decision table.
> [design-brief.md] The 5 Brief Questions · Question 2 → Aesthetic Decision Mapping · Question 3 → Platform Decision Mapping · Question 1 → Light/Dark Suitability · Thesis Extraction · From raw numbers: · From a topic brief: · Thesis formula: · Tone → Palette Mapping · Audience Sophistication → Density & Vocabulary · Skip-Brief Defaults · Brief → Design Decision Checklist
- [style-details](resources/style-details.md) — full design system with component CSS patterns, type playbooks, reduction-pass rules.
> [style-details.md] The Big Picture · Visual Treatments (radius, borders, shadows, spacing, decorations) · Composition Components (logos, progress bars, dense tables) · Composition Rules and Atmospheric Depth · Annotation, Typography, Reduction Pass · Reference Image Patterns (Vision Analysis — 12 real pieces)
- [layout-patterns](resources/layout-patterns.md) — full layout and archetype scaffold library.
> [layout-patterns.md] Layout Statistics · Your Dominant Infographic Types · Layout Recipes by Type · Composition Archetype CSS Implementations · Stats Bar / KPI Strip (74/175 = 42%)
- [charts](resources/charts.md) — chart rules (bar / line / pie / radar / stat callouts) with annotation-first placement.
> [charts.md] When to Use What · 1. SVG Pie Chart (Token Allocation — Your Most-Used) · 2. CSS Horizontal Bar Chart (Vesting / Allocation Strips) · 3. Chart.js — Complex Charts via CDN · 4. Pure CSS Progress Bar (Vesting Timeline) · 5. Waffle Chart (% of Total — Pure HTML/CSS) · 6. Slope Chart (Before/After — Inline SVG) · 7. Annotated Bar Chart (SVG — Hero Bar + Benchmark) · 8. Proportional Circles (SVG — Area = Value) · 9. Dot Plot (SVG — Distribution / Individual Points)
- [color-palettes](resources/color-palettes.md) — full palette library by content type.
> [color-palettes.md] Key Statistics · Per-Type Signature Palettes · Brand Distinction Strategy · Your Signature Background Colors · Your Most-Used Accent Colors (Primary) · Palette Recipes (Named Collections) · Standout / High-Contrast Palettes · Glow Color Reference (Top confirmed glow colors) · Light Mode Palettes (When background: "light")
- [font-pairings](resources/font-pairings.md) — display-font prevalence table and body-font pairings per type.
> [font-pairings.md] Key Statistics · Your Font Rules (Non-Negotiable) · Your Core Display Fonts (Ranked by usage) · Your Body Font (Almost Always the Same) · Tested Font Pairings (Your Actual Combinations) · Typography Constants (Always Apply)
- [platform-sizes](resources/platform-sizes.md) — 7 canvas sizes with per-platform adjustments and safe zones.
> [platform-sizes.md] Quick Reference · Layout & Font Adjustments Per Platform · Font Size Scaling by Platform · Watermark / Attribution Rule by Platform · export.py Commands by Platform
- [copy-guide](resources/copy-guide.md) — headline, callout, and label writing rules.
> [copy-guide.md] The Core Rule · Stat Formatting Rules · Headline Formulas · Per-Component Word Budgets · Color-Coded Keyword Highlighting · Disclaimers & Source Citations · Badge & Tag Copy · Body Copy Rules — Bullets Over Paragraphs · Common Mistakes to Avoid
- `templates/` — 24 reference templates (inventory in [_template-registry](references/_template-registry.md)).
> [_template-registry.md] Crypto / Web3 (13 templates) · Generic (11 templates) · Template selection table · Cross-references
- `examples/` — 15 rendered PNG reference outputs.
- `evals/evals.json` — 5 scenario test prompts + expected outcomes.
- [_index](references/_index.md) — flat catalog of every TECH file with one-line descriptions.
> [_index.md] Modes (3) · Archetypes (5) · Playbooks (5 content-type playbooks) · Components (15) · Charts (10) · Color & typography (8) · Copy (3) · Aesthetic systems (3) · Pre-delivery / quality (2) · Pipeline / preview / export (3) · Cross-references
- [_template-registry](references/_template-registry.md) — 24 template inventory + selection table.
> [_template-registry.md] Crypto / Web3 (13 templates) · Generic (11 templates) · Template selection table · Cross-references
- [_execution-modes](references/_execution-modes.md) — three execution modes with quality gate.
> [_execution-modes.md] A. Interactive Builder · B. One-Shot · C. Guided Creative · Quality gate (before delivery) · Cross-references
- [_design-dna](references/_design-dna.md) — non-negotiables derived from 175 real pieces.
> [_design-dna.md] Density is the defining trait · Backgrounds are near-black · Palette is warm + cool together · Display fonts are all-caps condensed · Stacked Reference is the default composition · Section variety is mandatory · Arrows are load-bearing · Visible borders, not ghost borders · Tight spacing inside sections · Content format hierarchy · Cross-references
- [_non-negotiables](references/_non-negotiables.md) — seven enforcement rules.
> [_non-negotiables.md] Rules 1–7 · Cross-references
- [_error-handling](references/_error-handling.md) — symptom-to-fix table for delivery failures.
> [_error-handling.md] Symptom-to-fix table · Cross-references

## Error Handling

Common build symptoms (output looks like a SaaS landing page / dashboard / slide deck, component demo repetition, floating-islands sections, Playwright missing, CDN font fallback, fabricated stats, wrong template, wrong light/dark mode, build interrupted, export font issues) and their fixes are catalogued in [_error-handling](references/_error-handling.md). The skill must consult that table when delivery fails the Quality Gate.
> [_error-handling.md] Symptom-to-fix table · Cross-references

## Completion checklist

Before reporting a job complete, verify each item. FAIL on any item triggers a remediation loop.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing.
- At least one `TECH-*.md` file from `references/` was consulted and is cited in the final report.
- Output passes [_non-negotiables](references/_non-negotiables.md).
> [_non-negotiables.md] Rules 1–7 · Cross-references
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- Output rendered/validated by the matching tool (`bin/amw-html-export.py`).
- Cross-skill hand-offs documented — every routed-through skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

Two kinds of output: (1) **Artifact(s)** — HTML + retina PNG + print-ready PDF infographic posters, path chosen by project inference; (2) **Job-completion report** — markdown at `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`. Every artifact MUST be linked from the report. Full output-routing rule + report schema (Inputs / Method / Artifacts / Checklist / Deviations + `$MAIN_ROOT` resolution) in [_pipeline-and-examples](references/_pipeline-and-examples.md).
> [_pipeline-and-examples.md] Prerequisites · Examples · Output
