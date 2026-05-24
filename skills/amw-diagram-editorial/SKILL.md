---
name: amw-diagram-editorial
description: Editorial-quality HTML+SVG diagrams with brand-matched styling — 13 types (architecture, flowchart, sequence, state, ER, timeline, swimlane, quadrant, nested, tree, layer, Venn, pyramid/funnel). Triggers on "sequence diagram", "ER diagram", "blog-ready architecture diagram". NOT for generic design, freeform SVG, or graph JSON — routes to design-principles / svg-creator / diagram-architecture. Use when creating an editorial diagram. Trigger with /amw-create-or-modify-html-diagram.
version: 0.1.0
author: ai-maestro-webdesign
---

# Diagram Editorial

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> This skill is an executor. Triggers are editorial-diagram-specific only — `design-principles` routes here when the user wants a blog-ready or documentation-ready diagram and has committed to one of the 13 canonical types.

## Overview

Editorial-quality HTML+SVG diagrams with brand-matched styling. Supports 13 fixed diagram types (architecture, flowchart, sequence, state machine, ER, timeline, swimlane, quadrant, nested, tree, layer stack, Venn, pyramid/funnel). Emits self-contained HTML with inline CSS and inline SVG, respecting the 4px grid, oklch palette, WCAG AA, and the three-family typography system.

## Activation

Callable directly via the `/amw-create-or-modify-html-diagram` command with `--style editorial` (user shortcut). Also invoked by the `design-principles` orchestrator as a Phase B renderer after Phase A approval in Main-agent mode. In Main-agent mode the orchestrator may apply any of the 13 diagram types and brand-onboarding techniques beyond what the command's `--style` flag exposes.

This skill is **autonomous and self-contained** — any agent can use it by reading this SKILL.md and its references.

## Position in flow

**OUTPUT (Phase B).** Emits self-contained HTML files — inline CSS + inline SVG, no external assets other than optional Google Fonts / Bunny Fonts. Each file respects design-principles color and typography tokens (4px grid, oklch palette, WCAG AA) and is ready to paste into a blog post, docs site, or MDX article.

This skill does NOT substitute for:
- `../amw-diagram-svg/` — freeform SVG primitives from natural-language intent.
- `../amw-diagram-architecture/` — graph JSON / Mermaid / SVG / PNG for architecture-only diagrams.
- `../amw-svg-creator/` — icons, logos, animated SVG (gated scope).

When in doubt about which diagram skill to use, route back to `design-principles`.

## Trigger conditions

Activate only on editorial-diagram intents that name one of the 13 canonical types or ask for "blog-ready" / "editorial" diagrams (e.g. "sequence diagram of <flow>", "ER diagram for <schema>", "Venn diagram", "pyramid / funnel", "onboard editorial diagrams to <url>"). Do NOT activate on generic intent ("draw a picture", "design a page", "make an illustration") — those belong to `design-principles`.

## Prerequisites

- **runtime_binaries (system):** none at run-time — HTML output opens in any browser. `node ≥ 22` only if pairing with `../amw-dev-browser/` for preview screenshots.
- **runtime_binaries (installed via `/amw-init`):** none required. Optional: `dev-browser` CLI for `/amw-preview`, `python ≥ 3.8` + `cairosvg` for `bin/amw-svg-render.py` render-verify loop.
- **Optional upstream:** `../amw-dev-browser/` — used only during the brand-onboarding flow. Never use raw WebFetch for onboarding.

## The 13 diagram types (selection table)

| Type | Use when… |
|---|---|
| **architecture** | Components + connections (services, APIs, infra). |
| **flowchart** | Decision logic, yes/no branches. |
| **sequence** | Messages over time (OAuth, API calls, user flows). |
| **state machine** | States + transitions (order lifecycle, auth state). |
| **ER / data model** | Entities + fields + relationships. |
| **timeline** | Events on a horizontal or vertical axis. |
| **swimlane** | Cross-functional flows (who does what, when). |
| **quadrant** | Two-axis positioning (impact vs effort, risk vs value). |
| **nested** | Hierarchy by containment (layers inside layers). |
| **tree** | Parent → children (org chart, file tree, decision tree). |
| **layer stack** | Stacked abstractions (OSI model, tech stack). |
| **Venn** | Set overlap (2–3 circles). |
| **pyramid / funnel** | Ranked hierarchy or conversion drop-off. |

**Selection rule:** ask *"would a reader learn more from this than from a well-written paragraph?"* If no, do not draw. Default to deletion over addition. Full per-type rules (canonical layout, anchor coordinates, concrete HTML+SVG scaffolds) live in [type-rules](references/type-rules.md).

## Design system (compact)

Full spec in [design-system](references/design-system.md). Non-negotiables:

- **Grid.** Every coordinate/width/gap divisible by **4px**. No shadows. Max `border-radius: 10px`. Borders 1px hairline only.
- **Typography.** Three families, three roles: `Instrument Serif` (titles, italic callouts), `Geist Sans` (node names, labels), `Geist Mono` (technical sublabels).
- **Color discipline.** One accent color. Accent for **1–2 focal nodes**; everything else uses `ink`, `muted`, `paper-2`. Density target **4/10**.
- **Tokens.** `paper`, `ink`, `muted`, `paper-2`, `accent`, `accent-fg`. Defaults stone + rust: `paper: oklch(96% 0.01 80)`, `ink: oklch(25% 0.02 80)`, `accent: oklch(62% 0.19 45)`.

## Brand onboarding (60 seconds)

To match the user's existing site:

1. User invokes `"onboard editorial diagrams to https://<site>"`.
2. Route through `../amw-dev-browser/` (**never** raw WebFetch) to fetch homepage + DOM.
3. Extract palette + font stack. Map to `paper`, `ink`, `muted`, `paper-2`, `accent`, `accent-fg`.
4. Run WCAG AA contrast checks against [color-system](../amw-design-principles/color-system.md). Auto-propose adjustments for failures; never silently ship a failing pair.
5. Show diff; on confirmation, write tokens to [style-guide](references/style-guide.md).

**First-run gate.** If defaults still in place on first use, pause and ask: *"Run onboarding, paste tokens manually, or proceed with default (stone + rust)?"* Do not guess.

## Instructions

1. Identify the diagram type from the user's intent using the 13-type selection table.
2. Run the 60-second brand onboarding: extract or confirm primary/secondary/accent/neutral colors plus typeface.
3. Select the relevant TECH reference(s) from the technique catalog below.
4. Author the HTML+SVG diagram following the editorial design system: 4px grid snap, three-family typography, WCAG-AA contrast on every color pair.
5. Render and visually inspect with `bin/amw-svg-render.py` or `dev-browser`; apply AI-slop gate.
6. Export the final artifact and write the job-completion report with all artifact paths.

## Examples

See worked examples in `./references/TECH-type-*.md` (e.g. OAuth sequence in `TECH-type-sequence.md`, data model in `TECH-type-er.md`). All conform to the 4px grid + three-family typography + oklch WCAG-AA palette.

## Technique catalog

Every technique is in `./references/TECH-*.md`. Each contains: What it does · When to use · How it works · Minimal example · Gotchas · Cross-references.

**Type techniques (13 + selection rule):** `TECH-type-selection-rule`, `TECH-type-architecture`, `TECH-type-flowchart`, `TECH-type-sequence`, `TECH-type-state-machine`, `TECH-type-er`, `TECH-type-timeline`, `TECH-type-swimlane`, `TECH-type-quadrant`, `TECH-type-nested`, `TECH-type-tree`, `TECH-type-layers`, `TECH-type-venn`, `TECH-type-pyramid`.

**Cross-cutting techniques:** `TECH-brand-url-onboarding`, `TECH-four-px-grid-snap`, `TECH-three-family-typography`, `TECH-focal-accent-discipline`, `TECH-density-4-of-10`, `TECH-wcag-contrast-validation`, `TECH-bezier-annotation-callout`, `TECH-sketchy-fractal-filter`.

## Resources

- Upstream: [amw-design-principles](../amw-design-principles/SKILL.md) (orchestrator), [color-system](../amw-design-principles/color-system.md), [typography-system](../amw-design-principles/typography-system.md), [spacing-rhythm](../amw-design-principles/spacing-rhythm.md), [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md), [amw-dev-browser](../amw-dev-browser/SKILL.md).
- References: [type-rules](references/type-rules.md), [design-system](references/design-system.md), [troubleshooting](references/troubleshooting.md), [primitive-sketchy](references/primitive-sketchy.md), [primitive-annotation](references/primitive-annotation.md).
- Tools: `../../bin/amw-svg-render.py` (render-verify), `../../bin/amw-html-export.py` (HTML→PNG).

## Completion checklist

Verify every item before reporting complete. FAIL on any item triggers a remediation loop.

- Inputs captured verbatim (no silent paraphrasing).
- At least one `TECH-*.md` from `references/` was consulted and cited.
- Output passes the Non-negotiables section.
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
- Emitted HTML/SVG validated by `bin/amw-html-export.py` or `bin/amw-svg-render.py`.
- Cross-skill hand-offs documented.
- User-facing filename is descriptive English (e.g. `OAuth Sequence.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — editorial HTML + SVG diagram files. Output path determined by **project inference** per [project-output-routing](../amw-design-principles/references/project-output-routing.md) (priority: user-supplied → framework convention → `./design/<subtype>/` → generic fallback → `/tmp/amw-diagram-editorial-<slug>/` scratch).
2. **Job-completion report** at `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md` with sections: Inputs, Method, Artifacts (each `- <path> — <desc> — **How to use:** <tip> — **Next steps:** <followup>`), Checklist (PASS/FAIL/N/A), Deviations.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`. Every artifact MUST be linked from the report.

## Non-negotiables

- **Output is self-contained HTML.** Inline `<style>` + inline `<svg>` in a single `.html`. No external CDN assets except optional Google Fonts / Bunny Fonts `<link>`. Canonical inline form: `<link rel="stylesheet" href="https://fonts.bunny.net/css?family=geist:400,600|instrument-serif:400i">`.
- **No AI-drawn illustrations.** Structural diagram primitives only — rectangles, lines, circles, arrows, text. Never generate portraits, scenes, mascots, decorative SVG art.
- **Every coordinate divisible by 4.**
- **One accent color, 1–2 focal nodes.**
- **Delete nodes until it hurts, then delete one more.** Target density 4/10.
- **Brand onboarding flows through `dev-browser`, not raw WebFetch.**
- **oklch colors, WCAG AA.** All palette changes go through [color-system](../amw-design-principles/color-system.md) validation.
- **Do not substitute for `../amw-diagram-svg/`, `../amw-diagram-architecture/`, `../amw-svg-creator/`.**

## Error Handling

Full symptom-to-fix table in [troubleshooting](references/troubleshooting.md). Common cases:

- **Looks AI-generated:** coordinates off the 4px grid OR too many accent nodes → re-snap; reduce accent to 1–2 focal nodes.
- **Colors don't match site:** brand onboarding never ran → re-run via `dev-browser`, or paste hex into [style-guide](references/style-guide.md).
- **Fonts fall back to Times/Arial:** missing Bunny Fonts `<link>` in `<head>` → add it.
- **WCAG contrast fail:** no 4.5:1 pair at 12px → darken `ink` or lighten `paper`.
- **Too dense:** > 8 nodes / density > 6/10 → delete non-essential, split, or switch to `nested` / `layer stack`.
- **Wrong type:** ask the user to override explicitly; do not silently switch.
- **ASCII/terminal request:** route to `../amw-ascii-sketch/`.
- **Comparison/tabular intent:** route to `design-principles`; tables beat diagrams.
