---
name: amw-infographics
description: Dense editorial infographics as HTML + PNG + PDF from a structured data brief — tokenomics, whitepaper summaries, ecosystem maps, roadmaps, airdrop guides, staking breakdowns, stat posters. Triggers on "infographic", "tokenomics graphic", "ecosystem map", "turn stats into a graphic". NOT for generic design (design-principles) or editorial diagrams (diagram-editorial). Use when producing a dense infographic from a data brief. Trigger with /amw-create-or-modify-html-diagram.
version: 0.1.0
author: ai-maestro-webdesign
---

# Infographics

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Triggers are data-infographic-specific only — `design-principles` routes here when the user has real data or a structured brief and wants a shareable, dense editorial graphic.

## Overview

Produces dense editorial infographics as self-contained HTML + retina PNG + print-ready PDF from a 24-template library and 175-design DNA set. Three execution modes: Interactive Builder (component-by-component with live preview), One-Shot (full infographic in one pass), and Guided Creative (two composition options before building). Near-black backgrounds, warm+cool accent palettes, all-caps condensed display fonts, high content density (8–15 blocks on portrait-medium). Not a generic webpage renderer — closer to a crypto research poster or game cheat sheet.

## Instructions

1. Classify the invocation mode: Interactive Builder, One-Shot, or Guided Creative. Full step-by-step workflows in [_execution-modes](references/_execution-modes.md).
2. For One-Shot and Guided Creative: ask the three Design Brief questions (brand, platform, key insight); classify the content type, archetype, and dominant component.
3. Build the infographic as a single self-contained HTML with required head includes (Google Fonts, Phosphor Icons, optional Chart.js); apply playbook colors/fonts; all CSS inline with `:root` custom properties.
4. Run the Anti-Frontend Checklist and Reduction Pass per the Quality Gate (see [_execution-modes](references/_execution-modes.md)).
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

## Design DNA + non-negotiable rules

Derived from 175 real designs. Density is the defining trait (8–15 content blocks), backgrounds are near-black, palette is warm+cool, display fonts are all-caps condensed (Bebas Neue default), Stacked Reference archetype is the default. Full rules in [_design-dna](references/_design-dna.md). Seven non-negotiable rules (no fabricated data, no generic display fonts, no emojis as icons, brand color first, dark default, real assets only, footer by default) in [_non-negotiables](references/_non-negotiables.md).

## 24-template index

24 fully-built reference templates ship in `templates/` (13 crypto/web3 + 11 generic). Each uses V4 CSS standards (12px dense tables, `▸` bullet panels, arrow connectors, stat strips). Full inventory + user-says-to-template selection table in [_template-registry](references/_template-registry.md).

## Execution modes

Three modes — Interactive Builder, One-Shot, Guided Creative. Full workflows + Quality Gate in [_execution-modes](references/_execution-modes.md).

## Technique selection

Pick a technique category, then look up the specific TECH file in [_index](references/_index.md). Every TECH file shares a TOC structure (What it does · When to use · How it works · CSS · HTML · Gotchas · Cross-references) plus 1–4 technique-specific subsections.

Categories: Mode (3), Archetype (5), Playbook (5 content-type playbooks), Component (15), Chart (12), Color & typography (8), Copy (3), Aesthetic systems (3), Pre-delivery / quality (2), Pipeline / preview / export (4).

## Prerequisites

- **runtime_binaries (system):** `python3 ≥ 3.8`.
- **runtime_binaries (installed via `/amw-init`):** Playwright + Chromium (`python3 -m playwright install chromium --with-deps`), optional Inkscape or pdf2svg for SVG export.
- **python_packages:** `playwright ≥ 1.40.0`.
- **npm_packages:** none required.
- **mcp_servers:** none.
- **CDN assets (run-time):** Google Fonts (Bebas Neue, Teko, Orbitron, Montserrat), Phosphor Icons, optional Chart.js. Offline environments need the CDN resolvable — `html-export.py` spins up a local HTTP server so Playwright resolves them cleanly.
- **Shared scripts:** `../../bin/amw-html-export.py` (PNG / PDF / SVG export), `../../bin/amw-preview-server.py` (Mode A live preview).

## Examples

`examples/` ships 15 rendered PNG reference outputs and `templates/` ships 24 fully-built reference HTML pieces with `{{PLACEHOLDER}}` variables.

**Token-economics example (One-Shot mode):** Input: a tokenomics brief with allocation %, vesting schedule, and brand color. Routing: `token-economics.html` template, [TECH-token-economics-playbook](references/TECH-token-economics-playbook.md), [TECH-stacked-reference-archetype](references/TECH-stacked-reference-archetype.md), [TECH-svg-pie-chart](references/TECH-svg-pie-chart.md), [TECH-progress-bar-vesting](references/TECH-progress-bar-vesting.md). Output: HTML + retina PNG + PDF at 1080×1440 with 11 content blocks.

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — upstream orchestrator.
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — final AI-slop scan every HTML output must pass.
- [color-system](../amw-design-principles/color-system.md) — brand-color / WCAG AA validation when a custom color is supplied.
- [typography-system](../amw-design-principles/typography-system.md) — type-scale rules that compose with this skill's display-font hierarchy.
- `../../bin/amw-html-export.py` — PNG / PDF / SVG export pipeline.
- `../../bin/amw-preview-server.py` — Mode A live preview server, port 7883.
- [design-brief](resources/design-brief.md) — 5-question intake framework + aesthetic decision table.
- [style-details](resources/style-details.md) — full design system with component CSS patterns, type playbooks, reduction-pass rules.
- [layout-patterns](resources/layout-patterns.md) — full layout and archetype scaffold library.
- [charts](resources/charts.md) — chart rules (bar / line / pie / radar / stat callouts) with annotation-first placement.
- [color-palettes](resources/color-palettes.md) — full palette library by content type.
- [font-pairings](resources/font-pairings.md) — display-font prevalence table and body-font pairings per type.
- [platform-sizes](resources/platform-sizes.md) — 7 canvas sizes with per-platform adjustments and safe zones.
- [copy-guide](resources/copy-guide.md) — headline, callout, and label writing rules.
- `templates/` — 24 reference templates (inventory in [_template-registry](references/_template-registry.md)).
- `examples/` — 15 rendered PNG reference outputs.
- `evals/evals.json` — 5 scenario test prompts + expected outcomes.
- [_index](references/_index.md) — flat catalog of every TECH file with one-line descriptions.
- [_template-registry](references/_template-registry.md) — 24 template inventory + selection table.
- [_execution-modes](references/_execution-modes.md) — three execution modes with quality gate.
- [_design-dna](references/_design-dna.md) — non-negotiables derived from 175 real pieces.
- [_non-negotiables](references/_non-negotiables.md) — seven enforcement rules.
- [_error-handling](references/_error-handling.md) — symptom-to-fix table for delivery failures.

## Error Handling

Common build symptoms (output looks like a SaaS landing page / dashboard / slide deck, component demo repetition, floating-islands sections, Playwright missing, CDN font fallback, fabricated stats, wrong template, wrong light/dark mode, build interrupted, export font issues) and their fixes are catalogued in [_error-handling](references/_error-handling.md). The skill must consult that table when delivery fails the Quality Gate.

## Completion checklist

Before reporting a job complete, verify each item. FAIL on any item triggers a remediation loop.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing.
- At least one `TECH-*.md` file from `references/` was consulted and is cited in the final report.
- Output passes [_non-negotiables](references/_non-negotiables.md).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
- Output rendered/validated by the matching tool (`bin/amw-html-export.py`).
- Cross-skill hand-offs documented — every routed-through skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — HTML + retina PNG + print-ready PDF infographic posters. Output path determined by project inference per [project-output-routing](../amw-design-principles/references/project-output-routing.md): user-supplied path → framework convention → existing `./design/<subtype>/` → generic fallback `./design/infographics/` → last-resort scratch `/tmp/amw-infographics-<slug>/`. Every artifact is listed with its path in the report.

2. **Job-completion report** — markdown at `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`. Contains: **Inputs** (user-provided + auto-detected), **Method** (TECH references consulted, pipeline steps), **Artifacts** (per-file bullet — `- <path> — <description> — How to use: <tip> — Next steps: <follow-up>`), **Checklist** (each item PASS/FAIL/N/A), **Deviations** (skipped or changed steps + rationale). The `<8-char-hash>` is the first 8 chars of SHA-256 of the inputs+artifacts list.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`.

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the run is incomplete. `reports/webdesigner/` is for user-facing job outputs (distinct from `reports/audit/` which is for build-time audit artifacts).
