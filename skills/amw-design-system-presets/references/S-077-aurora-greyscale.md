---
id: S-077
name: Aurora (Greyscale Wireframe)
aesthetic_position: classical-modernist monochrome
source_attribution: "styles-A §Aurora (Greyscale Wireframe); upstream: `claude-design-mode-main/README.md` 'Aurora' design example. LICENSE: MIT."
license: MIT
---

# S-077 — Aurora (Greyscale Wireframe)

## Identity

Aurora is the "designer's intent, stripped of color" idiom — a monochrome structural wireframe where the grid IS the design. The fingerprint is Manrope display (geometric, even rhythm) sitting above JetBrains Mono for labels and secondary metadata, a five-step greyscale palette (grey-50 / grey-100 / grey-300 / grey-400 / grey-900), 1px grey-300 hairline borders, zero shadows, zero radius elevation, and a visible 12-column CSS grid that the layout obeys rather than hides. There is no accent. Reach for it when the deliverable is an early-stage design system review, an internal design-tooling page that should not look "finished", a documentation site that wants to telegraph "structural clarity over decoration", or the planning surface before color is added in a later pass. Avoid for consumer marketing — there is no warmth, no accent, no payoff.

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  --primary:      #18181B;   /* near-black ink */
  --accent:       transparent; /* Aurora has NO accent — structural greyscale only */
  --bg:           #FAFAFA;   /* page background — grey-50 */
  --surface:      #F4F4F5;   /* card / elevated surface — grey-100 */
  --text:         #18181B;   /* primary text — grey-900 near-black */
  --text-muted:   #71717A;   /* secondary text — grey-500 */
  --text-faint:   #A1A1AA;   /* faint label — grey-400 */
  --border:       #D4D4D8;   /* hairline border — grey-300 */
  --border-strong:#71717A;   /* emphatic structural border — grey-500 */
  --font-display: 'Manrope', 'Inter', system-ui, sans-serif;
  --font-body:    'Manrope', 'Inter', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Menlo', monospace;
  --radius:       0px;       /* structural wireframe — sharp edges */
  --shadow:       none;      /* no elevation; structure is the only signal */
  --spacing:      8px;       /* base spacing unit */

  /* Grid primitives — the 12-column grid is visible by intent */
  --grid-cols:    12;
  --grid-gap:     24px;
  --grid-margin:  32px;
}
```

Tailwind theme extension (equivalent):
```js
{
  theme: {
    extend: {
      colors: {
        primary: '#18181B',
        bg: '#FAFAFA',
        surface: '#F4F4F5',
        text: '#18181B',
        'text-muted': '#71717A',
        'text-faint': '#A1A1AA',
        border: '#D4D4D8',
        'border-strong': '#71717A',
      },
      fontFamily: {
        display: ['Manrope', 'Inter', 'system-ui', 'sans-serif'],
        body:    ['Manrope', 'Inter', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', 'Menlo', 'monospace'],
      },
      borderRadius: { DEFAULT: '0px' },
      boxShadow: { DEFAULT: 'none' },
    }
  }
}
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --primary:     #FAFAFA;
  --bg:          #18181B;
  --surface:     #27272A;
  --text:        #FAFAFA;
  --text-muted:  #A1A1AA;
  --text-faint:  #71717A;
  --border:      #3F3F46;
  --border-strong:#71717A;
}
```

## "Breaks if" invariants

- Breaks if any saturated chromatic color appears anywhere — Aurora is structural greyscale only, accent is forbidden by definition.
- Breaks if `box-shadow` introduces elevation — the only depth signal is the contrast step between grey-50 / grey-100 / grey-300.
- Breaks if `border-radius` exceeds 0px on any structural surface (card, panel, button) — the wireframe stays sharp.
- Breaks if Manrope is replaced by a serif or a humanist sans (the geometric Manrope rhythm is the typographic fingerprint).
- Breaks if JetBrains Mono is replaced by a proportional font for labels / metadata — the display/mono pairing IS the wireframe signature.
- Breaks if the 12-column grid is hidden or not respected — Aurora's grid is meant to be visible enough to read alignment by eye.
- Breaks if photography or illustration is added before color is layered in a later pass — Aurora is the pre-color phase.
- Breaks if greyscale steps are not drawn from a discoverable ramp (the grey-50 / 100 / 300 / 500 / 900 spacing is the canonical Tailwind/zinc scale; arbitrary greys destroy the rhythm).

## Canonical render-test pointer

Skeleton: `references/_test-skeleton.html`
Source render: no standalone upstream demo — tokens direct-ported from `styles-A.md §Aurora (Greyscale Wireframe)` description; upstream `claude-design-mode-main/README.md` carries the prose-level description but no published HTML/CSS file.
Parity threshold: A-class justified (no renderable upstream demo)

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 106834 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-001 Swiss (also monochromatic-disciplined, but uses a single chromatic accent — Aurora is greyscale-only), S-022 Minimal Pure (low density), S-076 Cosmic Scale Animation (also monochrome, but geometry-loop rather than structural grid), S-009 Aurora original (different style — dark cinematic, do not confuse: this S-077 is greyscale-wireframe Aurora).
- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- [_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- [_harness-wiring.md](./_harness-wiring.md) — parity verification pipeline
- Source attribution: reports/batch9-harvest/styles-A.md §Aurora (Greyscale Wireframe) — upstream claude-design-mode-main/README.md, MIT.

## Attribution

Visual description and font pairing (Manrope + JetBrains Mono) ported from styles-A.md §Aurora (Greyscale Wireframe). Token hex values are the canonical Tailwind/zinc grey scale, chosen to match the upstream prose ("grey-50/100, grey-300, grey-400, grey-500, grey-900"). Upstream source repo `claude-design-mode-main` is MIT-licensed; this reference inherits MIT. Naming intentionally disambiguated from S-009 Aurora (dark cinematic) via the `-greyscale` suffix.
