---
name: TECH-type-quadrant
category: editorial-layout
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in:
---

# TECH-type-quadrant

## What it does

Emits a **quadrant chart** — a 2-axis plane (x and y) divided into 4
quadrants with labels at each corner; items plotted as labelled circles.
Editorial HTML+SVG. The standard pattern is "impact vs effort", "risk vs
value", "urgency vs importance".

## When to use

- Items are being compared on exactly two independent axes.
- The four quadrants each have a distinct meaning (Quick Wins / Major
  Projects / Fill-ins / Thankless Tasks, or equivalents).
- 5–10 items. Fewer feels empty; more blurs the message.

Do not use for: ranked priorities (pyramid), categorical counts (bar
chart), or single-axis positioning (just a number line).

## How it works

Canvas: square, typically 520×520. Axes: 1px `ink` lines from
`(pad, height-pad)` anchored bottom-left, extending right (x) and up (y).
Quadrant dividers: 1px `muted` dashed lines crossing through the centre.

Axis labels: at each axis endpoint in muted 11px `Geist Sans`
(`← Low ... · High ... →`), the `y` axis rotated 90°. Quadrant labels:
uppercase, letter-spaced (`0.05em`), muted 10px, positioned near each
corner.

Items: `<circle>` markers, size encoded by importance (r between 22–32),
fill `paper-2` with 1px `ink` stroke. One accent item per diagram, filled
`accent`. Label wraps inside the circle across two lines in 9px `Geist
Sans`, text-anchor middle.

## Minimal example

Impact vs effort, one accent item. Attributed to
`diagram-design-editorial/SKILL.md` lines 263-322:

```html
<svg width="520" height="520" viewBox="0 0 520 520"
     font-family="Geist, system-ui, sans-serif">
  <rect width="520" height="520" fill="var(--paper)"/>

  <!-- Axes -->
  <line x1="64" y1="456" x2="456" y2="456"
        stroke="var(--ink)" stroke-width="1"/>
  <line x1="64" y1="64"  x2="64"  y2="456"
        stroke="var(--ink)" stroke-width="1"/>

  <!-- Quadrant dividers -->
  <line x1="260" y1="64" x2="260" y2="456"
        stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 3"/>
  <line x1="64" y1="260" x2="456" y2="260"
        stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 3"/>

  <!-- Axis labels -->
  <text x="260" y="488" text-anchor="middle" font-size="11"
        fill="var(--muted)">← Low Effort · High Effort →</text>
  <text x="20" y="260" text-anchor="middle" font-size="11"
        fill="var(--muted)" transform="rotate(-90, 20, 260)">
    ← Low Impact · High Impact →
  </text>

  <!-- Quadrant labels -->
  <text x="162" y="88" text-anchor="middle" font-size="10"
        font-weight="600" fill="var(--muted)"
        letter-spacing="0.05em">QUICK WINS</text>
  <text x="358" y="88" text-anchor="middle" font-size="10"
        font-weight="600" fill="var(--muted)"
        letter-spacing="0.05em">MAJOR PROJECTS</text>
  <text x="162" y="448" text-anchor="middle" font-size="10"
        font-weight="600" fill="var(--muted)"
        letter-spacing="0.05em">FILL-INS</text>
  <text x="358" y="448" text-anchor="middle" font-size="10"
        font-weight="600" fill="var(--muted)"
        letter-spacing="0.05em">THANKLESS TASKS</text>

  <!-- Focal item (accent) — Quick Wins quadrant -->
  <circle cx="148" cy="148" r="28" fill="var(--accent)" opacity="0.9"/>
  <text x="148" y="144" text-anchor="middle" font-size="10"
        font-weight="600" fill="var(--accent-fg)">Auth</text>
  <text x="148" y="158" text-anchor="middle" font-size="9"
        fill="var(--accent-fg)" opacity="0.85">redesign</text>

  <!-- Standard items -->
  <circle cx="200" cy="200" r="22" fill="var(--paper-2)"
          stroke="var(--ink)" stroke-width="1"/>
  <text x="200" y="196" text-anchor="middle" font-size="9"
        fill="var(--ink)">Dark</text>
  <text x="200" y="208" text-anchor="middle" font-size="9"
        fill="var(--ink)">mode</text>

  <circle cx="340" cy="160" r="26" fill="var(--paper-2)"
          stroke="var(--ink)" stroke-width="1"/>
  <text x="340" y="156" text-anchor="middle" font-size="9"
        fill="var(--ink)">API v2</text>
  <text x="340" y="168" text-anchor="middle" font-size="9"
        fill="var(--ink)">migration</text>
</svg>
```

## Gotchas

- **Axis labels point in the direction of growth.** `← Low Effort · High Effort →`
  — arrows on both ends, term words on both ends. Readers bounce off the
  diagram if only one end is labelled.
- **Quadrant corner labels, not centre labels.** Corner placement makes the
  quadrant boundaries obvious; centre labels fight the items.
- **Circle radius as importance encoding.** Don't let the radius leak into
  meaning if it isn't meant to — if all items are equal, keep radii equal.
- **One accent item.** The quadrant chart's job is to make one item
  obvious; everything else should recede.

## Cross-references

- `../SKILL.md` — 13-type table
- `TECH-type-pyramid.md` — if one-axis ranking is what you really want
- `design-system.md` — axis-label format, dashed divider pattern,
  letter-spacing for quadrant labels
- `primitive-annotation.md` — optional italic callout explaining a
  surprising placement ("why is Auth redesign in Quick Wins?")
