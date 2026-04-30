---
name: TECH-type-swimlane
category: editorial-layout
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in:
---

# TECH-type-swimlane

## What it does

Emits a **swimlane diagram** — horizontal rows (lanes), each representing
an actor or team; within each lane, step rectangles arranged left-to-right
in temporal order. Editorial HTML+SVG. The focus is "who does what,
when" for cross-functional flows.

## When to use

- A process spans 2–5 roles (Design, Eng, PM, Legal, Support) and the
  reader needs to see handoffs.
- Sequence within each lane matters; absolute time doesn't.
- 3–6 steps per lane. If one lane has 8 steps and another has 1, you have
  a flowchart, not a swimlane — rebalance or switch.

Do not use for: cross-actor API-level interaction (sequence), pure
decision logic (flowchart), or roles that don't interact (parallel
workflows — those are separate flowcharts).

## How it works

Lane band: a large rect (`fill="var(--paper-2)"`, very light opacity, full
diagram width). Lane label on the far left in `Geist Sans` 11px **uppercase
with `letter-spacing: 0.05em`**, vertically centred. Horizontal divider
lines between lanes: 1px `muted`.

Step rectangles inside lanes: same 160×48 rounded rect with 1px hairline
as other diagram types. Handoff arrows: dashed 1px `muted` crossing
lane boundaries; within-lane progression is solid.

Typical width: 820–960px; lane height 88–96px (enough for the step +
`16px` padding top/bottom).

## Minimal example

3-lane swimlane, PR review process:

```html
<svg width="720" height="320" viewBox="0 0 720 320"
     font-family="Geist, system-ui, sans-serif">
  <rect width="720" height="320" fill="var(--paper)"/>

  <!-- Lane 1: Author -->
  <rect x="0" y="40" width="720" height="88" fill="var(--paper-2)" opacity="0.5"/>
  <text x="16" y="88" font-size="12" font-weight="600"
        fill="var(--ink)">Author</text>
  <rect x="120" y="64" width="140" height="40" rx="6"
        fill="var(--accent)"/>
  <text x="190" y="88" text-anchor="middle" font-size="11"
        font-weight="600" fill="var(--accent-fg)">Open PR</text>
  <rect x="440" y="64" width="140" height="40" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="510" y="88" text-anchor="middle" font-size="11"
        fill="var(--ink)">Address feedback</text>

  <line x1="0" y1="128" x2="720" y2="128"
        stroke="var(--muted)" stroke-width="1"/>

  <!-- Lane 2: Reviewer -->
  <rect x="0" y="128" width="720" height="88" fill="var(--paper)"/>
  <text x="16" y="176" font-size="12" font-weight="600"
        fill="var(--ink)">Reviewer</text>
  <rect x="280" y="152" width="140" height="40" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="350" y="176" text-anchor="middle" font-size="11"
        fill="var(--ink)">Request changes</text>

  <line x1="0" y1="216" x2="720" y2="216"
        stroke="var(--muted)" stroke-width="1"/>

  <!-- Lane 3: CI -->
  <rect x="0" y="216" width="720" height="88" fill="var(--paper-2)" opacity="0.5"/>
  <text x="16" y="264" font-size="12" font-weight="600"
        fill="var(--ink)">CI</text>
  <rect x="600" y="240" width="100" height="40" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="650" y="264" text-anchor="middle" font-size="11"
        fill="var(--ink)">Build</text>

  <!-- Handoff arrows (dashed across lanes) -->
  <defs>
    <marker id="sl-arrow" markerWidth="6" markerHeight="6"
            refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--muted)"/>
    </marker>
  </defs>
  <path d="M 260 84 Q 270 148, 280 168"
        fill="none" stroke="var(--muted)" stroke-width="1"
        stroke-dasharray="4 3" marker-end="url(#sl-arrow)"/>
  <path d="M 420 172 Q 430 148, 440 84"
        fill="none" stroke="var(--muted)" stroke-width="1"
        stroke-dasharray="4 3" marker-end="url(#sl-arrow)"/>
</svg>
```

## Gotchas

- **Lane label on the left, bold, 12px.** Rotating 90° is tempting but
  hurts readability — keep it horizontal.
- **Alternate lane shading for visibility.** Paper-2 at 50% opacity on
  odd rows, `paper` on even rows. Hard 100% paper-2 is too heavy.
- **Handoff arrows must actually cross the lane divider.** Arrows that
  terminate inside the same lane belong to within-lane progression — use
  solid lines for those.
- **Accent the step that reveals the bottleneck**, not always the first
  step. A swimlane's value is surfacing where work stalls.

## Cross-references

- `../SKILL.md` — 13-type table
- `TECH-type-flowchart.md` — if the process is single-actor
- `../../amw-ux-flows/references/mermaid-patterns.md` — Mermaid has no
  first-class swimlane; use subgraphs per actor if Mermaid is required
- `design-system.md` — lane-band opacity and divider-line conventions
