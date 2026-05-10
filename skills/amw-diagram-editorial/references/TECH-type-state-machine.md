---
name: TECH-type-state-machine
category: editorial-layout
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in: SKILLS-TO-INTEGRATE/diagrams-skills/ux-flow-designer-main/references/mermaid-patterns.md
---

# TECH-type-state-machine

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Emits a **state machine** — each state is a rounded rect, each transition
is a labelled arrow between two states. Editorial HTML+SVG. Usually
depicts the lifecycle of a single entity (order, session, document,
connection) as it changes state over time.

## When to use

- A single entity has discrete named states and transitions between them
  (order: `pending` → `paid` → `shipped` → `delivered`).
- Transitions fire on events (`submit`, `payment_received`, `cancel`,
  `refund`) that the reader needs to remember.
- Typical 4–8 states. More than 8 usually means two overlapping machines
  — split them.

Do not use for: decision forks (flowchart), static topology
(architecture), or time-ordered multi-actor interaction (sequence).

## How it works

Initial state marker: small filled circle (`<circle r="6" fill="var(--ink)"/>`)
that arrows into the first state. Terminal state marker: **two stacked
`<rect>` elements with a 2px offset** — do not use `stroke-width="3"`.
States laid out left-to-right for linear lifecycles, or grid-style for
branchy ones. Self-loops (for "retry" etc.) curve above the state using
a cubic `<path>`. Transition labels sit above each arrow in `Geist Sans`
10px muted. No transition arrow is emitted without a label.

## Minimal example

Order lifecycle:

```html
<svg width="640" height="200" viewBox="0 0 640 200"
     font-family="Geist, system-ui, sans-serif">
  <rect width="640" height="200" fill="var(--paper)"/>
  <defs>
    <marker id="state-arrow" markerWidth="6" markerHeight="6"
            refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--ink)"/>
    </marker>
  </defs>

  <!-- Initial marker -->
  <circle cx="40" cy="100" r="6" fill="var(--ink)"/>
  <line x1="46" y1="100" x2="80" y2="100" stroke="var(--ink)"
        stroke-width="1" marker-end="url(#state-arrow)"/>

  <!-- State: Pending (accent) -->
  <rect x="80" y="76" width="100" height="48" rx="6" fill="var(--accent)"/>
  <text x="130" y="104" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--accent-fg)">Pending</text>

  <!-- Transition: Pay -->
  <line x1="180" y1="100" x2="236" y2="100" stroke="var(--ink)"
        stroke-width="1" marker-end="url(#state-arrow)"/>
  <text x="208" y="92" text-anchor="middle" font-size="10"
        fill="var(--muted)">pay</text>

  <!-- State: Paid -->
  <rect x="240" y="76" width="100" height="48" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="290" y="104" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--ink)">Paid</text>

  <!-- Transition: Ship -->
  <line x1="340" y1="100" x2="396" y2="100" stroke="var(--ink)"
        stroke-width="1" marker-end="url(#state-arrow)"/>
  <text x="368" y="92" text-anchor="middle" font-size="10"
        fill="var(--muted)">ship</text>

  <!-- State: Shipped -->
  <rect x="400" y="76" width="100" height="48" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="450" y="104" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--ink)">Shipped</text>

  <!-- Terminal marker -->
  <line x1="500" y1="100" x2="556" y2="100" stroke="var(--ink)"
        stroke-width="1" marker-end="url(#state-arrow)"/>
  <text x="528" y="92" text-anchor="middle" font-size="10"
        fill="var(--muted)">deliver</text>
  <circle cx="572" cy="100" r="8" fill="none" stroke="var(--ink)" stroke-width="1"/>
  <circle cx="572" cy="100" r="4" fill="var(--ink)"/>
</svg>
```

## Gotchas

- **Initial/terminal markers are load-bearing.** Don't omit them. A reader
  needs to know where the lifecycle starts and where it ends.
- **Self-loops curve above the state**, not beside it. Place the label at
  the loop apex, muted 10px.
- **Transition labels name the event, not the result.** `pay` (the event),
  not `Paid` (the state you arrive in).
- **4+ concurrent-state territory means nested states or parallel
  regions** — that's a Mermaid `stateDiagram-v2` with `state Xxx { }`
  blocks territory, often better expressed in `../../amw-ux-flows/`.

## Cross-references

- [SKILL](../SKILL.md) — 13-type selection table
- [TECH-mermaid-state-diagram-screen](../../amw-ux-flows/references/TECH-mermaid-state-diagram-screen.md) —
  > What it does · When to use · How it works · Basic transitions · Nested states · Parallel states · Minimal example · Gotchas · Cross-references
  Mermaid equivalent for per-screen UI state
- [TECH-type-flowchart](TECH-type-flowchart.md) — if the intent is decision logic, not lifecycle
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [design-system](design-system.md) — dot/double-circle terminal marker sizing
  > Grid · Typography · Loading the fonts · Type scale · Colour discipline · Rules · Focal node vs standard node · Connection styling · Density calibration · Coordinate-level checklist
