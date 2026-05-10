---
name: TECH-focal-accent-discipline
category: editorial-layout
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-focal-accent-discipline

## What it does

Enforces the rule that an editorial diagram uses **one accent colour**
applied to **1–2 focal nodes maximum**. Every other element uses `ink`,
`muted`, `paper-2`. The point is: if everything is accent, nothing is
accent.

## When to use

- **Every diagram**, regardless of type — architecture, flowchart,
  sequence, timeline, quadrant, etc.
- **Every variant** — the sketchy filter, annotated versions, onboarded
  brand palettes.
- **Never allow** 3+ accent elements unless they are the entire point of
  a Venn or quadrant chart (and even then, the intersection / focal
  quadrant is still a single accent region).

## How it works

**Accent selection rule:** pick the single node the reader should look at
first. That is the focal node. Examples:

- Architecture diagram → the service the article is about (API Gateway if
  the post is on zero-trust, Auth Service if it's on SSO).
- Flowchart → the decision that forks the critical path.
- State machine → the failure state or the accepting state, depending on
  the post's angle.
- Quadrant → the surprising item ("Why is this in Quick Wins?").
- Funnel → the conversion drop-off the piece is about.

**Visual encoding:**

```
standard node:  fill=paper-2, stroke=ink 1px
accent node:    fill=accent, no stroke, text fill=accent-fg
```

The accent node has no border because `accent` against `paper` provides
enough contrast on its own. Adding a 1px `ink` stroke around an accent
fill doubles the visual weight and kills the "focal pop" effect.

## Minimal example

Correct (1 accent in a 4-node diagram):

```html
<!-- Standard node -->
<rect x="60" y="196" width="160" height="48" rx="6"
      fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
<text x="140" y="216" text-anchor="middle" font-size="12"
      fill="var(--ink)">Frontend</text>

<!-- Focal node (accent) -->
<rect x="240" y="80" width="160" height="48" rx="6"
      fill="var(--accent)"/>
<text x="320" y="100" text-anchor="middle" font-size="12"
      font-weight="600" fill="var(--accent-fg)">API Gateway</text>
```

Incorrect (5 accent nodes in a 7-node diagram):

```html
<!-- Every node accent = no focal at all -->
<rect ... fill="var(--accent)"/>  <!-- A -->
<rect ... fill="var(--accent)"/>  <!-- B -->
<rect ... fill="var(--accent)"/>  <!-- C -->
<rect ... fill="var(--accent)"/>  <!-- D -->
<rect ... fill="var(--accent)"/>  <!-- E -->
```

Reader sees 5 equally-important components; the diagram has no story.

## Gotchas

- **The accent-fg text colour is non-negotiable.** Putting `ink`-coloured
  text on an accent-filled node fails WCAG AA on most brand palettes.
  Use `accent-fg` (usually `paper` or near-white) specifically.
- **Don't stroke the accent node.** `fill=accent` with no stroke is the
  canonical form. A border would blur the "jumps out" effect.
- **2 accent nodes allowed ONLY if they are paired** (sender and
  receiver, before and after, input and output). Three independent
  accent nodes is always wrong.
- **Coloured edges are NOT accent.** Edges stay on `muted`. If the edge
  itself needs emphasis, make it thicker (1.5px) and solid — not
  accent-coloured.

## Cross-references

- [SKILL](../SKILL.md) — non-negotiables list (this is item 4)
- [design-system](design-system.md) — semantic tokens (`accent`, `accent-fg`, `paper-2`)
  > Grid · Typography · Loading the fonts · Type scale · Colour discipline · Rules · Focal node vs standard node · Connection styling · Density calibration · Coordinate-level checklist
- [TECH-density-4-of-10](TECH-density-4-of-10.md) — the companion rule on diagram density
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-four-px-grid-snap](TECH-four-px-grid-snap.md) — the other structural hard rule
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [troubleshooting](troubleshooting.md) — diagnose "looks AI-generated" / too-busy diagrams
  > Symptom-to-fix table · Diagrams look generic / AI-generated · Colours don't match the user's site · Fonts fall back to Times / Arial · WCAG contrast fails on brand colour · Diagram is too dense / cluttered · Wrong type chosen · `bin/amw-svg-render.py` render check fails · Brand onboarding fetched the wrong palette · Diagram output opens blank · When NOT to use this skill
