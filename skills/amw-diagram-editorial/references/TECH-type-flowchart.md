---
name: TECH-type-flowchart
category: editorial-layout
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in: SKILLS-TO-INTEGRATE/diagrams-skills/ux-flow-designer-main/references/mermaid-patterns.md, SKILLS-TO-INTEGRATE/diagrams-skills/baybee-diagram/SKILL.md
---

# TECH-type-flowchart

## What it does

Emits a **decision flowchart** — rectangles for process steps, diamonds for
decisions, clear yes/no branches — in editorial HTML+SVG. Top-down flow
by default; left-to-right allowed for short decision chains.

## When to use

- Decision logic with yes/no branches. "Should the user do X?" "If Y, then
  A else B." Conditional forks.
- Retry / error-recovery paths where a step can loop back.
- ≤12 shapes including decisions. Beyond that, split by phase or collapse
  terminal branches into a single "error → contact support" terminal node.

Do **not** use flowchart for: actors interacting over time (sequence),
state machines (state), or simple linear workflows (those are just a list
or a timeline).

## How it works

Process step = rounded rect (`rx="6"`). Decision = diamond (SVG `<polygon>`
with four points forming a rhombus on the 4px grid; use `rx="0"` for
diamonds — do not draw pointy rectangles). Terminal node = a final
rounded rect at the bottom. Edges: 1px solid `muted`, labelled "Yes" /
"No" / "Error" in `Geist Sans` 10px muted; every branch must carry a
label. Happy path goes down; "no" / error branch exits sideways
(consistent direction throughout). One accent on the start node **or**
the terminal success node — not both.

## Minimal example

Decision fork pattern, editorial styling:

```html
<svg width="560" height="360" viewBox="0 0 560 360"
     font-family="Geist, system-ui, sans-serif">
  <rect width="560" height="360" fill="var(--paper)"/>

  <!-- Step: Receive request (top) -->
  <rect x="200" y="40" width="160" height="48" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="280" y="68" text-anchor="middle" font-size="12"
        fill="var(--ink)">Receive Request</text>

  <!-- Decision: Authenticated? (accent diamond) -->
  <polygon points="280,116 360,168 280,220 200,168"
           fill="var(--accent)"/>
  <text x="280" y="172" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--accent-fg)">Auth?</text>

  <!-- Yes branch -->
  <line x1="360" y1="168" x2="460" y2="168"
        stroke="var(--muted)" stroke-width="1"/>
  <text x="410" y="160" text-anchor="middle" font-size="10"
        fill="var(--muted)">Yes</text>
  <rect x="460" y="144" width="80" height="48" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="500" y="172" text-anchor="middle" font-size="12"
        fill="var(--ink)">Serve</text>

  <!-- No branch (dashed — error path) -->
  <line x1="200" y1="168" x2="100" y2="168"
        stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 3"/>
  <text x="150" y="160" text-anchor="middle" font-size="10"
        fill="var(--muted)">No</text>
  <rect x="20" y="144" width="80" height="48" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="60" y="172" text-anchor="middle" font-size="12"
        fill="var(--ink)">401</text>
</svg>
```

## Gotchas

- **Diamond snapping.** A 4px-grid diamond has vertices on `(cx, cy-h)`,
  `(cx+w, cy)`, `(cx, cy+h)`, `(cx-w, cy)` where `w` and `h` are both
  multiples of 4. Easiest mistake: off-center points produce a lopsided
  shape that looks wrong even at a glance.
- **Edge labels above or beside, never on the line.** Reading across a line
  fragments the glyph; text belongs ~6-8px clear of the stroke.
- **No cycles without a loop.** If the flow genuinely re-enters an earlier
  step on retry, draw the loop with a clear labelled back-edge (often
  dashed). Implicit re-entry is confusing.
- **Yes/No labels every decision.** Unlabelled branches are the #1 source
  of reader confusion in generated flowcharts.

## Cross-references

- `../SKILL.md` — type table; flowchart is for *decision logic* specifically
- [TECH-type-state-machine](TECH-type-state-machine.md) — if you find yourself modelling lifecycle,
  that's a state machine, not a flowchart
- `../../amw-ux-flows/references/TECH-mermaid-flowchart-screen-map.md` —
  Mermaid-syntax cousin for screen-navigation flowcharts
- [design-system](design-system.md) — 4px grid for diamond corners
