---
name: TECH-stroke-width-4-palette
category: svg-shape
source: SKILLS-TO-INTEGRATE/diagrams-skills/baybee-diagram/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Usage pattern](#usage-pattern)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-stroke-width-4-palette

## What it does

Fixes every shape stroke at **`stroke-width="4"`** and every stroke
colour at **`#0f172a`** (slate-900). Fill colours are chosen from a
flat, limited palette: light (`#f1f5f9`), mid (`#334155`), accent
(`#38bdf8`). The combination produces the "baybee" diagram's signature
bold-and-clean look.

## When to use

- **Every mechanical `diagram-svg` output.** Consistent stroke weight is
  the single biggest legibility lever.
- **Whenever the caller does NOT have brand tokens** — defaults
  consistently.
- **When brand tokens ARE supplied**, substitute the caller's colours
  but keep the stroke-width and the flat-colour principle.

Do not soften the strokes to 2px "for a subtle look" — this skill's
signature is the confident 4px weight; thinner strokes push it toward
editorial territory which is `diagram-editorial`'s domain.

## How it works

Fixed values:

| Attribute | Default | Rationale |
|---|---|---|
| `stroke-width` | `4` | Bold, readable at render sizes from 200px to 1200px |
| `stroke` | `#0f172a` (slate-900) | Near-black; never pure `#000` |
| `fill` (light) | `#f1f5f9` (slate-100) | Default node fill |
| `fill` (mid) | `#334155` (slate-700) | Contrasting node (database, secondary) |
| `fill` (accent) | `#38bdf8` (sky-400) | Focal node — use sparingly |

### Usage pattern

```xml
<!-- Light fill (default) -->
<rect x="100" y="100" width="200" height="80" rx="20"
      fill="#f1f5f9" stroke="#0f172a" stroke-width="4"/>

<!-- Mid fill (database, emphasis) -->
<rect x="100" y="100" width="200" height="80" rx="20"
      fill="#334155" stroke="#0f172a" stroke-width="4"/>
<!-- Text inside mid-fill nodes uses white for contrast -->
<text x="200" y="150" fill="#f8fafc" font-size="24">DB</text>

<!-- Accent fill (focal) -->
<rect x="100" y="100" width="200" height="80" rx="20"
      fill="#38bdf8" stroke="#0f172a" stroke-width="4"/>
<text x="200" y="150" fill="#0f172a" font-size="24">Focus</text>
```

## Minimal example

One-diagram-three-fills:

```xml
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
  <g id="nodes">
    <!-- Client: accent -->
    <rect x="100" y="460" width="200" height="80" rx="20"
          fill="#38bdf8" stroke="#0f172a" stroke-width="4"/>
    <!-- Service: light -->
    <rect x="400" y="460" width="200" height="80" rx="20"
          fill="#f1f5f9" stroke="#0f172a" stroke-width="4"/>
    <!-- Database: mid -->
    <rect x="700" y="460" width="200" height="80" rx="20"
          fill="#334155" stroke="#0f172a" stroke-width="4"/>
  </g>
  <g id="labels">
    <text x="200" y="510" text-anchor="middle" font-size="22" fill="#0f172a">Client</text>
    <text x="500" y="510" text-anchor="middle" font-size="22" fill="#0f172a">Service</text>
    <text x="800" y="510" text-anchor="middle" font-size="22" fill="#f8fafc">DB</text>
  </g>
</svg>
```

## Gotchas

- **Text colour flips based on fill.** On `#334155` mid-fill, text must
  be light (`#f8fafc`) to pass WCAG AA. On `#f1f5f9` or `#38bdf8`, text
  is the slate stroke colour (`#0f172a`).
- **Never pure `#000` stroke.** Slate-900 (`#0f172a`) has a subtle cool
  tint that reads cleaner; pure black looks harsh at 4px thickness.
- **One accent fill per diagram.** The accent (`#38bdf8`) is the focal
  signal — 3+ accent fills dilute it the same way multiple
  accent-coloured nodes dilute an editorial diagram.
- **No gradients.** Flat fills only. Gradients on this stroke weight
  look dated and degrade when rasterised.
- **Stroke-width uniform across the diagram.** Exception: arrowhead
  markers use their own internal sizing; see
  [TECH-arrow-marker-def](TECH-arrow-marker-def.md).

## Cross-references

- `../SKILL.md` — palette in the Style section
- [TECH-node-shape-vocabulary](TECH-node-shape-vocabulary.md) — shapes all share this stroke
- [TECH-arrow-marker-def](TECH-arrow-marker-def.md) — arrow sizing relative to 4px strokes
- `../../amw-diagram-editorial/references/TECH-three-family-typography.md` —
  editorial cousin uses 1px hairlines instead of 4px bolds
- `../../amw-design-principles/color-system.md` — brand override path
