## Table of Contents

- [1. Grid](#1-grid)
- [2. Typography](#2-typography)
  - [Loading the fonts](#loading-the-fonts)
  - [Type scale](#type-scale)
- [3. Colour discipline](#3-colour-discipline)
  - [Rules](#rules)
  - [Focal node vs standard node](#focal-node-vs-standard-node)
  - [Connection styling](#connection-styling)
- [4. Density calibration](#4-density-calibration)
- [5. Coordinate-level checklist](#5-coordinate-level-checklist)


# Design System — full spec for editorial diagrams

Load this file when a diagram needs the complete grid / typography / colour contract and the primitive scaffolds. The compact SKILL.md carries the summary; this file carries the full rules and worked examples.

---

## 1. Grid

Every coordinate, width, height, and gap is divisible by **4px**. This single rule prevents the "AI-generated jitter" tell more than any other.

- Node width: `160` (default), `200` (ER entities), `100` (sequence actors). All multiples of 4.
- Node height: `48` (default), `36` (sequence actors), `56` (layer stack).
- Lane height (swimlane): `96` minimum.
- Vertical spacing between rows: `80` or `116`.
- Arrow-label offset: `6` above, `12` from the arrowhead tail.

**No shadows anywhere.** No `filter: drop-shadow`, no `<feDropShadow>`, no CSS `box-shadow`. Editorial diagrams read as flat ink-on-paper.

**Max `border-radius`: `10px`.** Default `rx="6"` for rectangles; `rx="0"` for diamonds (rotated 45° squares). Circles use `<circle>`, never a `rect` with `rx="50%"`.

**Borders.** All borders `stroke-width="1"`. The only exceptions:
- Terminal state in a state machine: stack two `<rect>` with 2px offset, not `stroke-width="3"`.
- Sketchy-filter variant: `stroke-width="1.5"` to survive displacement noise.

---

## 2. Typography

Three families, three semantic roles. These three are load-bearing for the editorial feel — do not swap them for alternates without the user's explicit instruction.

| Family | Role | Use |
|---|---|---|
| `Instrument Serif` | Title + italic callouts | Diagram titles, margin annotations, editorial asides. Always italic for callouts. |
| `Geist Sans` | Primary UI text | Node names, labels, axis labels, role labels. Font weight 600 for bold. |
| `Geist Mono` | Technical sublabels | Ports (`:443`, `:5432`), URLs (`/authorize`), HTTP verbs (`GET`, `POST`), field types (`uuid`, `text`), IDs. Never the primary label. |

Mono is specifically for technical content. Do not reach for Mono to get a "dev aesthetic" — use `Geist Sans` for names, `Geist Mono` only for things a reader would copy-paste.

### Loading the fonts

Diagrams use system fallbacks by default — Geist and Instrument Serif load only if available. For exact rendering, add to the output HTML's `<head>`:

```html
<link rel="preconnect" href="https://fonts.bunny.net">
<link href="https://fonts.bunny.net/css?family=instrument-serif:400,400i|geist:400,600|geist-mono:400&display=swap"
      rel="stylesheet">
```

Bunny Fonts is preferred over Google Fonts because it's privacy-friendly (no tracking, GDPR-compliant) and identical on the wire. If the user explicitly wants Google Fonts:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;600&family=Geist+Mono&family=Instrument+Serif:ital@0;1&display=swap"
      rel="stylesheet">
```

### Type scale

| Element | Size | Weight | Family |
|---|---|---|---|
| Title | `15` | `600` | Geist Sans |
| Node label (primary) | `12`–`13` | `600` | Geist Sans |
| Node sublabel (technical) | `10` | `400` | Geist Mono |
| Axis / quadrant label | `11` | `600` with letter-spacing `0.05em` (uppercase) | Geist Sans |
| Edge label | `10` | `400` | Geist Sans |
| Callout | `12` | `400` italic | Instrument Serif |
| Small standalone text | `9` | `400` | Geist Sans |

Never use font-size below 9px. Never use font-size above 15px in the diagram body (a title is fine; anything else that size is a slide, not an editorial diagram).

---

## 3. Colour discipline

Six semantic tokens — do not introduce new roles without explicit user instruction. Defaults are stone + rust (warm off-white paper, charcoal ink, rust-orange accent):

```css
:root {
  --paper:    #F8F5F0;  /* diagram background */
  --ink:      #1A1A1A;  /* primary text, borders */
  --muted:    #6B6560;  /* secondary labels, grid lines */
  --paper-2:  #EEEAE4;  /* card fills, lane backgrounds */
  --accent:   #B5523A;  /* focal nodes, 1–2 per diagram */
  --accent-fg:#FFFFFF;  /* text on accent nodes */
}
```

### Rules

- **One accent colour per diagram.** Introducing a second accent creates visual ties and forces the reader to choose what matters. Don't let the reader choose — the diagram must.
- **Accent reserved for 1–2 focal nodes.** The thing the reader looks at first. If everything is accent, nothing is accent.
- **Everything else uses `ink`, `muted`, `paper-2`.** In that order of prominence.
- **Target visual density: 4/10.** Ruthlessly sparse. Seven nodes is usually enough; twelve is always too many.
- **oklch equivalents validate against `../../amw-design-principles/color-system.md`.** Brand-onboarded palettes must pass WCAG AA (4.5:1 at 12px) before shipping.

### Focal node vs standard node

```html
<!-- Accent node — 1–2 per diagram only -->
<rect width="160" height="48" rx="6" fill="var(--accent)"/>
<text fill="var(--accent-fg)" font-family="Geist, sans-serif" font-size="13">
  Primary Component
</text>

<!-- Standard node — the other 5–6 -->
<rect width="160" height="48" rx="6"
      fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
<text fill="var(--ink)" font-family="Geist, sans-serif" font-size="13">
  Secondary Component
</text>
```

### Connection styling

Line style carries meaning. Keep it consistent within a diagram:

- **Solid 1px `var(--muted)`** — synchronous / primary flow / default edge.
- **Dashed `4 3` 1px `var(--muted)`** — async / event / eventual consistency.
- **Solid 1px `var(--ink)`** — sequence-diagram request (stronger than muted).
- **Dashed `4 3` 1px `var(--ink)`** — sequence-diagram response.

Arrowheads use a shared `<marker>`:

```html
<defs>
  <marker id="arrow" markerWidth="6" markerHeight="6"
          refX="5" refY="3" orient="auto">
    <path d="M0,0 L6,3 L0,6 Z" fill="var(--muted)"/>
  </marker>
</defs>
```

Keep arrowhead fill matching the line colour. A muted arrow on an ink line looks wrong.

---

## 4. Density calibration

The design system's strongest rule: **delete nodes until it hurts, then delete one more.**

| Node count | Diagnosis |
|---|---|
| ≤ 5 | Usually right. The diagram earns its place. |
| 6–8 | Borderline. Each node must earn a word in the caption. |
| 9–11 | Too many. Delete or split. |
| ≥ 12 | Always wrong. Split into overview + detail, or switch to a nested / layer stack / tree type. |

Eliminate any node the reader doesn't need to understand the point. The reader has a paragraph nearby for detail — the diagram is the gist.

---

## 5. Coordinate-level checklist

Run this checklist before handing off any diagram:

- [ ] Every `x`, `y`, `width`, `height`, `cx`, `cy`, `r` divisible by 4.
- [ ] Every `stroke-width` is `1` (or `1.5` for sketchy-filter nodes).
- [ ] Every `rx` is `0`, `6`, `8`, or `10` — nothing else.
- [ ] No `filter: drop-shadow`, no `<feDropShadow>`, no `box-shadow`.
- [ ] Accent colour used on ≤ 2 nodes.
- [ ] Title uses Geist Sans 15 / 600, not Instrument Serif.
- [ ] Technical sublabels use Geist Mono, primary labels use Geist Sans.
- [ ] Any callout uses Instrument Serif italic 12.
- [ ] Font size never below 9 or above 15.
- [ ] Total node count ≤ 8 unless the type is nested / layer stack / tree.
- [ ] Output file is self-contained HTML — no external `<script>`, no external `<img>`, no external `<link>` except optional fonts.

If any box fails, fix before handoff.
