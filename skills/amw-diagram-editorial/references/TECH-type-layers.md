---
name: TECH-type-layers
category: editorial-layout
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/references/formats.md
---

# TECH-type-layers

## What it does

Emits a **layer-stack diagram** — horizontal full-width bands stacked
vertically, each band representing a layer of abstraction. Editorial
HTML+SVG. Canonical use: OSI networking stack, tech-stack diagrams,
application/domain/infrastructure layers.

## When to use

- Abstraction stacks: higher layers depend on lower ones; lower layers
  know nothing about higher ones.
- ≤7 layers. OSI itself is 7; anything denser isn't a stack, it's a
  matrix.
- Each layer has a distinct name and role.

Do not use for: containment (nested), explicit topology (architecture), or
categorical data (table).

## How it works

Each layer: full-width rounded rect, 56px tall, **4px vertical gap**
between layers. Layer label: bold `Geist Sans` 13px, left-aligned with
16px x-padding. Optional sublabel in `Geist Mono` muted 10px **right-
aligned on the same baseline** (e.g. "HTTP, HTTPS" for an application
layer). Bottom layer = foundational; top layer = user-facing.

Accent one layer maximum — usually the layer the article focuses on.
Everything else uses `paper-2`. Optional left-edge accent bar (`rect width="3"`)
colour-coded per layer if the diagram doubles as a legend.

## Minimal example

4-layer application stack, focal on "Application":

```html
<svg width="640" height="320" viewBox="0 0 640 320"
     font-family="Geist, system-ui, sans-serif">
  <rect width="640" height="320" fill="var(--paper)"/>

  <!-- Application (accent) -->
  <rect x="40" y="40" width="560" height="56" rx="10"
        fill="var(--accent)"/>
  <text x="56" y="72" font-size="13" font-weight="600"
        fill="var(--accent-fg)">Application</text>
  <text x="584" y="72" text-anchor="end" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--accent-fg)"
        opacity="0.85">HTTP, WebSocket</text>

  <!-- Framework -->
  <rect x="40" y="104" width="560" height="56" rx="10"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="56" y="136" font-size="13" font-weight="600"
        fill="var(--ink)">Framework</text>
  <text x="584" y="136" text-anchor="end" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">Express, FastAPI</text>

  <!-- Runtime -->
  <rect x="40" y="168" width="560" height="56" rx="10"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="56" y="200" font-size="13" font-weight="600"
        fill="var(--ink)">Runtime</text>
  <text x="584" y="200" text-anchor="end" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">Node.js, Python</text>

  <!-- OS -->
  <rect x="40" y="232" width="560" height="56" rx="10"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="56" y="264" font-size="13" font-weight="600"
        fill="var(--ink)">OS</text>
  <text x="584" y="264" text-anchor="end" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">Linux, macOS</text>
</svg>
```

## Gotchas

- **Layers are horizontal bands — never tilted, never split into columns
  within a layer.** A layer with columns is a swimlane.
- **No edges drawn between layers.** The visual containment is the
  dependency signal; drawn edges clutter.
- **Sublabel on the right in mono muted.** Not centred, not on a new line —
  right-aligned keeps the band readable and the sublabel unobtrusive.
- **Top = highest abstraction, bottom = lowest.** Reversing this is
  confusing because OSI established the convention decades ago.

## Cross-references

- `../SKILL.md` — 13-type table
- `TECH-type-nested.md` — for containment-style hierarchy
- `../../amw-diagram-architecture/SKILL.md` — for multi-layer architecture with
  inter-layer edges and auto-layout
- `design-system.md` — sublabel typography (mono, muted, right-aligned)
