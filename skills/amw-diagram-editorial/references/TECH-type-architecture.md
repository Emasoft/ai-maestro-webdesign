---
name: TECH-type-architecture
category: editorial-layout
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/SKILL.md, SKILLS-TO-INTEGRATE/diagrams-skills/baybee-diagram/SKILL.md
---

# TECH-type-architecture

## What it does

Emits an **architecture diagram** — a set of component rectangles joined by
hairline edges — in editorial HTML+SVG. One component per rect; one accent
node maximum; connections shown as 1px lines (dashed for async / optional,
solid for primary flow).

## When to use

- User committed explicitly to an *architecture* diagram (services, APIs,
  queues, databases, infra components).
- The reader needs to see **what talks to what**, not **who does what**
  (swimlane territory) or **state transitions** (state-machine territory).
- ≤10 components total. If the input has more, merge the minor ones or
  split into overview + detail.

If the user hasn't committed — route back to `../SKILL.md` type-selection
question. If the intent is a free-text architecture that needs auto-layout,
route to `../../amw-diagram-architecture/SKILL.md` instead; that skill emits
JSON / Mermaid / SVG / PNG from free text.

## How it works

Coordinates divisible by 4 (hard rule). Rows for logical tiers — usually
client at top, gateway / load-balancer underneath, services in the middle,
storage at bottom. One accent node (focal component) in warm rust; every
other component in `paper-2` with a 1px `ink` stroke. Technical sublabels
(ports, URLs, stack names) live in `Geist Mono`, muted.

## Minimal example

Attributed to `diagram-design-editorial/SKILL.md` lines 180-259:

```html
<svg width="640" height="400" viewBox="0 0 640 400"
     xmlns="http://www.w3.org/2000/svg"
     font-family="Geist, system-ui, sans-serif">
  <rect width="640" height="400" fill="var(--paper)"/>
  <text x="32" y="40" font-size="15" font-weight="600"
        fill="var(--ink)">Application Architecture</text>

  <!-- Focal node: API Gateway (accent) -->
  <rect x="240" y="80" width="160" height="48" rx="6"
        fill="var(--accent)"/>
  <text x="320" y="100" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--accent-fg)">API Gateway</text>
  <text x="320" y="116" text-anchor="middle" font-size="10"
        fill="var(--accent-fg)" opacity="0.8">:443</text>

  <!-- Standard node -->
  <rect x="60" y="196" width="160" height="48" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="140" y="216" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--ink)">Frontend</text>
  <text x="140" y="232" text-anchor="middle" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">Next.js</text>

  <line x1="320" y1="128" x2="140" y2="196"
        stroke="var(--muted)" stroke-width="1"/>
</svg>
```

## Gotchas

- **Accent discipline.** One accent node. If everything is the focal, nothing
  is the focal — the accent loses meaning and the diagram reads busy.
- **Dashed = optional.** Use `stroke-dasharray="4 3"` for async queue hops,
  cache-warming, or optional-on-first-load paths. Primary request paths
  stay solid.
- **Ports and stack labels below the component name**, in `Geist Mono`
  muted. Not above, never beside — that crowds the label.
- **4px grid is the AI-slop tell.** `x="61"` or `width="163"` is the fastest
  way to make a diagram look generated.

## Cross-references

- `../SKILL.md` — type selection table + full 13-type chooser rule
- `design-system.md` — 4px grid, typography, color tokens
- `primitive-annotation.md` — add italic side callouts for editorial asides
- `../../amw-diagram-architecture/SKILL.md` — auto-layout from free text
- `TECH-focal-accent-discipline.md` — the 1–2-accent rule in detail
