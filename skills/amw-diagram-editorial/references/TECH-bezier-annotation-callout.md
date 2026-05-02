---
name: TECH-bezier-annotation-callout
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


# TECH-bezier-annotation-callout

## What it does

Adds an **editorial annotation callout** to any diagram — italic
`Instrument Serif` text in the margin connected to a target element
inside the diagram via a dashed Bézier curve leader. This is the
editorial signature primitive: it reads as "author's commentary" next to
the technical content, not as part of the diagram itself.

## When to use

- **In-margin aside** that explains a non-obvious placement, a surprising
  behaviour, a footnote-level remark.
- When a label inside the diagram would clutter but the point still
  needs to be made.
- Essays, blog posts, books — anywhere the author's voice is welcome.

Do NOT use in technical ADRs, runbooks, or API docs — the italic serif
reads too informal for customer-facing documentation.

## How it works

Two primitives, always together:

1. **Dashed Bézier leader.** A 1px `muted` path with
   `stroke-dasharray="3 3"` and `fill="none"`, curving gently from the
   margin callout text to the target element. Cubic curve
   (`C cx1 cy1, cx2 cy2, tx ty`) with control points biased toward a
   gentle S-shape rather than a straight diagonal.
2. **Italic serif callout text.** `Instrument Serif` 400 italic at 12px,
   `fill="var(--muted)"`. Sits in the margin (left or right of the
   diagram), not inside it.

The combination is visually distinct from the inner diagram's `Geist Sans`
labels and from state-machine arrow markers — readers recognize it as
"author's voice" immediately.

## Minimal example

Attributed to `diagram-design-editorial/SKILL.md` lines 416-436:

```html
<svg width="520" height="320" viewBox="0 0 520 320">
  <defs>
    <style>
      .callout-text {
        font-family: 'Instrument Serif', Georgia, serif;
        font-style: italic;
        font-size: 12px;
        fill: var(--muted);
      }
    </style>
  </defs>

  <!-- Imagine a node at (260, 148) — the API Gateway -->
  <rect x="240" y="124" width="120" height="48" rx="6"
        fill="var(--accent)"/>
  <text x="300" y="152" text-anchor="middle" font-size="12"
        fill="var(--accent-fg)">API Gateway</text>

  <!-- Bézier leader line (dashed, 1px, gently curved) -->
  <path d="M 180,200 C 200,180 220,160 260,148"
        stroke="var(--muted)" stroke-width="1"
        stroke-dasharray="3 3" fill="none"/>

  <!-- Callout text — sits in left margin -->
  <text x="80" y="204" class="callout-text">only runs on cold start</text>
</svg>
```

## Gotchas

- **Dashed pattern must be `3 3`, not `4 3`.** The leader line is a
  different visual register from the in-diagram dashed edges (which are
  `4 3`). Keeping them distinct preserves the "author's voice vs.
  content" distinction.
- **Bézier must actually curve.** A straight dashed line reads as a
  callback leader in a technical spec; the curve is what makes it
  editorial. Aim for ~20-40px of curvature between control points.
- **Callout text stays in the margin.** If it's inside the diagram
  bounding box, it competes with the content — defeating the purpose.
  Left/right margin is the editorial convention.
- **Never use this primitive for routine labels.** Inside-diagram labels
  belong to `Geist Sans`. The italic serif callout is reserved for
  actual editorial commentary — running it on every label cheapens it.

## Cross-references

- `../SKILL.md` — Primitives section
- [primitive-annotation](primitive-annotation.md) — the full primitive spec this technique
  generalises
- [TECH-three-family-typography](TECH-three-family-typography.md) — the rule that keeps italic serif
  reserved for this role
- [design-system](design-system.md) — `muted` token, dash pattern convention
