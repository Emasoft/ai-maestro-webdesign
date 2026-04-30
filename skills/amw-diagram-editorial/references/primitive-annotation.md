# Primitive — Editorial annotation callout

> **Cross-type primitive.** Applies to any of the 13 editorial diagram types
> for in-margin asides — a one-line note about runtime behaviour, cold-start
> caveats, historical nuance, or the single observation that justifies
> writing the whole post.

## When to use

- **Use:** when there's one point about the diagram that doesn't fit inside
  a node or on an edge label, but the reader needs it to understand the
  diagram correctly. Examples: "only runs on cold start", "deprecated in
  v4", "measured at p99", "rust compiler does this automatically".
- **Limit to 1-2 per diagram.** More than 2 annotations crowds the margins
  and starts competing with the diagram body for attention — which is
  exactly the opposite of what a margin note is for.
- **Keep to ≤ 7 words.** Annotations are whispers, not paragraphs. If the
  nuance needs more than 7 words, it belongs in the prose around the
  diagram, not in the margin.

## Required SVG primitives

- `<style>` inside `<defs>` declaring `.callout-text` class with italic
  Instrument Serif at 12px.
- One `<path>` with `stroke-dasharray="3 3"` for the dashed Bézier leader
  line.
- One `<text>` element using the `callout-text` class for the margin text.

## Canonical snippet

```html
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

<!-- Bézier leader line (dashed, 1px) -->
<path d="M 180,200 C 200,180 220,160 260,148"
      stroke="var(--muted)" stroke-width="1"
      stroke-dasharray="3 3" fill="none"/>

<!-- Callout text — sits in the diagram margin -->
<text x="80" y="204" class="callout-text">only runs on cold start</text>
```

## Parameter reference

| Attribute | Value | Rationale |
|---|---|---|
| `font-family` | `'Instrument Serif', Georgia, serif` | Instrument Serif is the editorial typeface for titles and asides. Italic reads as "aside", not body copy. Fallback stack guarantees Georgia when Bunny Fonts is blocked. |
| `font-style` | `italic` | Non-negotiable. The italic cue is how the reader knows "this is not part of the diagram body". |
| `font-size` | `12px` | Smaller than any diagram-body text. Reinforces "margin-note" status. Do NOT scale up — an annotation that rivals the node labels is not an annotation anymore. |
| `fill` | `var(--muted)` | Never `var(--ink)`. Muted tone pulls the annotation OUT of the visual hierarchy. Ink-colored annotations compete with the diagram body for attention. |
| `stroke-dasharray` | `3 3` | Short dash + short gap. Dashed leader distinguishes "soft pointer" (this is commentary) from a solid arrow (this is flow). |
| `stroke-width` on leader | `1` | Thinner than any structural edge in the diagram. A leader line must never look like a diagram connection. |

## Leader-line geometry

The dashed Bézier is a cubic `C` curve, not a straight line — the gentle
curve reads as "commentary pointing at the diagram" rather than "a missed
connection". Four control points:

- `M x1,y1` — where the line starts (usually in the margin, near the text).
- `C cx1,cy1 cx2,cy2 x2,y2` — the curve terminates at the node/edge the
  annotation refers to. The two control points steer the curve shape.

Rule of thumb: keep the leader length between 40 and 120 user units. Longer
leaders cross too much of the diagram and confuse the reader about what is
being annotated.

## 4px grid still applies

Callout text position (`x`, `y`) snaps to multiples of 4 — same as every
other coordinate in the editorial diagram family. The leader line's
endpoints also snap to 4; the control points in the middle of the `C` curve
do not need to.

## Source citation

Ported from `diagram-design-editorial/SKILL.md` lines 417-436 (source SKILL.md
on disk at `SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/`).
