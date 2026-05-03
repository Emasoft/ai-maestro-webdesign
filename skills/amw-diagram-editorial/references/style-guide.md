## Table of Contents

- [Semantic color tokens (oklch)](#semantic-color-tokens-oklch)
- [Font stack](#font-stack)
- [Grid + line rules](#grid-line-rules)
- [Brand onboarding flow](#brand-onboarding-flow)


# Editorial Diagrams — Brand Style Guide

> **User-editable.** This file holds the semantic color tokens and font stack
> for editorial diagrams, seeded by default to `stone + rust` (warm off-white
> paper, charcoal ink, rust-orange accent). Brand onboarding rewrites this
> file when the user runs `"onboard editorial diagrams to <url>"`.
>
> **Do NOT delete this file** — the skill expects to find it at this path
> and falls back to the defaults below if it is missing.

---

## Semantic color tokens (oklch)

Every editorial diagram must validate against `../amw-design-principles/color-system.md`
(WCAG AA ≥ 4.5:1 for 12px body copy) after any token change.

| Role | Default (stone + rust) | Purpose |
|---|---|---|
| `paper` | `oklch(96% 0.01 80)` | Page / card backgrounds. Warm off-white. |
| `ink` | `oklch(25% 0.02 80)` | Primary text, borders, node strokes. Charcoal. |
| `muted` | `oklch(60% 0.01 80)` | Secondary labels, grid lines, dashed connectors. |
| `paper-2` | `oklch(92% 0.015 80)` | Card fills, lane backgrounds, layer stacks. |
| `accent` | `oklch(62% 0.19 45)` | The 1–2 focal nodes per diagram. Rust-orange. |
| `accent-fg` | `oklch(98% 0 0)` | Text on accent-coloured nodes. Warm white. |

---

## Font stack

| Role | Family | Used for |
|---|---|---|
| Display / titles | `Instrument Serif` | Editorial headings, italic callouts |
| UI / node labels | `Geist Sans` | Node names, lane labels, axis labels |
| Technical | `Geist Mono` | Ports, URLs, field types, IDs, code |

CDN links (Bunny Fonts — GDPR-friendly Google Fonts mirror):

```html
<link rel="preconnect" href="https://fonts.bunny.net">
<link href="https://fonts.bunny.net/css?family=instrument-serif:400,400i&family=geist:400,500,600,700&family=geist-mono:400,500" rel="stylesheet">
```

Offline fallback chain:

```css
font-family: 'Instrument Serif', ui-serif, Georgia, serif;
font-family: 'Geist Sans', ui-sans-serif, system-ui, sans-serif;
font-family: 'Geist Mono', ui-monospace, 'SF Mono', Menlo, monospace;
```

---

## Grid + line rules

- 4px grid. Every `x`, `y`, `width`, `height`, `gap` divisible by 4.
- 1px hairline borders. No shadows anywhere.
- Max `border-radius: 10px`.
- Target density: **4/10**. If there are 12+ nodes, split into two diagrams.

---

## Brand onboarding flow

To rewrite this file from an existing brand URL:

1. User invokes: `"onboard editorial diagrams to https://<site>"`.
2. Skill routes through `../amw-dev-browser/` (never raw WebFetch).
3. Dominant palette + font stack extracted, mapped to the 6 semantic roles above.
4. WCAG AA contrast checks run against [color-system](../../amw-design-principles/color-system.md).
  > I. Always prefer oklch over rgb / hex / hsl · Why · Syntax · Comfort ranges · II. WCAG contrast — hard requirement · Checking tools · III. Palette structure (cap at 5–7 colors) · Standard 6-color framework · Rules · IV. Dark mode is not a simple inversion · Wrong approach · Right approach · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
5. Proposed diff shown to the user; on confirmation, this file is overwritten.

Never hand-edit the semantic-role names. The skill looks them up by name.
