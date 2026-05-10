---
name: TECH-type-sequence
category: editorial-layout
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in: SKILLS-TO-INTEGRATE/diagrams-skills/ux-flow-designer-main/references/mermaid-patterns.md
---

# TECH-type-sequence

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Emits a **sequence diagram** — horizontally arranged actor boxes at the top
with vertical dashed lifelines dropping down; labelled horizontal arrows
between lifelines show messages in temporal order. Editorial HTML+SVG,
no Mermaid runtime.

## When to use

- Time-ordered messages between 2–5 actors (OAuth handshake, webhook
  delivery, multi-service API call, login-to-token exchange).
- The *order* of operations is load-bearing — reordering changes meaning.
- The reader already knows what each actor is; the diagram teaches *how
  they interact*.

Do not use for: states of a single entity (state machine), static
component topology (architecture), or a decision tree (flowchart).

## How it works

Top row: actor boxes, evenly spaced, 100px wide × 36px tall, rounded 6px.
The first actor (often "Browser" / "User / Client") gets the accent fill.
Vertical lifelines: dashed 1px `muted`, dropping from each actor's bottom
centre down the canvas. Each message: one horizontal arrow between two
lifelines, solid for requests, dashed for responses (4 3 dash pattern),
label above in muted 10px `Geist Sans`. Arrow marker: small triangle,
`refX="5" refY="3"` on a `6×6` viewport.

## Minimal example

OAuth 2.0 authorization code flow, attributed to
`diagram-design-editorial/SKILL.md` lines 326-408:

```html
<svg width="600" height="360" viewBox="0 0 600 360"
     font-family="Geist, system-ui, sans-serif">
  <rect width="600" height="360" fill="var(--paper)"/>

  <!-- Actors -->
  <rect x="40"  y="40" width="100" height="36" rx="6"
        fill="var(--accent)"/>
  <text x="90"  y="63" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--accent-fg)">Browser</text>

  <rect x="248" y="40" width="100" height="36" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="298" y="63" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--ink)">Auth Server</text>

  <rect x="456" y="40" width="100" height="36" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="506" y="63" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--ink)">API</text>

  <!-- Lifelines -->
  <line x1="90"  y1="76" x2="90"  y2="340"
        stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 3"/>
  <line x1="298" y1="76" x2="298" y2="340"
        stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 3"/>
  <line x1="506" y1="76" x2="506" y2="340"
        stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 3"/>

  <defs>
    <marker id="seq-arrow" markerWidth="6" markerHeight="6"
            refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--ink)"/>
    </marker>
  </defs>

  <!-- 1: request -->
  <line x1="90" y1="120" x2="292" y2="120"
        stroke="var(--ink)" stroke-width="1" marker-end="url(#seq-arrow)"/>
  <text x="194" y="114" text-anchor="middle" font-size="10"
        fill="var(--muted)">GET /authorize</text>

  <!-- 2: response (dashed) -->
  <line x1="298" y1="152" x2="96" y2="152"
        stroke="var(--ink)" stroke-width="1" stroke-dasharray="4 3"
        marker-end="url(#seq-arrow)"/>
  <text x="194" y="146" text-anchor="middle" font-size="10"
        fill="var(--muted)">302 → login page</text>
</svg>
```

## Gotchas

- **Actor columns on multiples of 4 AND equidistant.** Uneven spacing is
  the fastest visual tell. At 600px width with 3 actors, 208px centre-to-
  centre spacing is the sweet spot.
- **Request = solid, response = dashed.** Flipping this convention breaks
  the reader's pattern-matching instantly.
- **Y-spacing between message rows.** 32px between rows is the editorial
  default. Tighter than 28px and the labels collide; looser than 36px and
  the diagram feels airless.
- **No nested lifelines.** If one actor's lifeline forks into sub-actors,
  you need a second diagram — sequence isn't the right primitive.

## Cross-references

- [SKILL](../SKILL.md) — type table; sequence is for *time-ordered messages*
- [TECH-mermaid-sequence-authenticated](../../amw-ux-flows/references/TECH-mermaid-sequence-authenticated.md) —
  > What it does · When to use · How it works · Actor reference · Message syntax · Error-handling pattern · Minimal example · Gotchas · Cross-references
  Mermaid equivalent when docs are in Markdown
- [TECH-type-architecture](TECH-type-architecture.md) — if the diagram is about static topology
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  rather than temporal flow
- [design-system](design-system.md) — lifeline dash pattern, arrow marker sizing
  > Grid · Typography · Loading the fonts · Type scale · Colour discipline · Rules · Focal node vs standard node · Connection styling · Density calibration · Coordinate-level checklist
