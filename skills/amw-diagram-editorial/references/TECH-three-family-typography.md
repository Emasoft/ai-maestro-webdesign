---
name: TECH-three-family-typography
category: editorial-brand
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in:
---

# TECH-three-family-typography

## What it does

Constrains every editorial diagram to exactly **three font families** each
with a fixed role. The constraint is load-bearing for the editorial
aesthetic — collapsing to one family makes diagrams look like a dev
screenshot; expanding to four+ families makes them look like a stock
image.

## When to use

- **Every editorial diagram.** No per-diagram exceptions.
- **Brand onboarding** replaces which families are chosen, but never
  collapses the three-role distinction.
- **Default (no brand)** families are fixed: `Instrument Serif` +
  `Geist Sans` + `Geist Mono`.

## How it works

Three roles, one family each:

| Role | Family | Used for |
|---|---|---|
| Display / titles | `Instrument Serif` (italic 400 for callouts, 400 for titles) | Diagram title, in-margin italic asides, Venn-overlap editorial labels |
| UI / node labels | `Geist Sans` (400, 500, 600, 700) | Node names, lane labels, axis labels, legend entries |
| Technical | `Geist Mono` (400, 500) | Ports (`:5432`), URLs, field types (`varchar`, `uuid`), IDs, mono date markers |

**"Mono is for technical content specifically — not a blanket 'dev
aesthetic.'"** That distinction is important: using mono for node names
turns every diagram into a terminal screenshot; using it specifically for
ports / types / IDs creates visual hierarchy.

## Minimal example

Correct three-role usage:

```html
<!-- Title (serif italic, editorial feel) -->
<text x="40" y="40" font-family="Instrument Serif, Georgia, serif"
      font-size="16" font-weight="400" font-style="italic"
      fill="var(--ink)">
  The retry budget, visualized
</text>

<!-- Node name (sans) -->
<text x="120" y="216" text-anchor="middle" font-size="12"
      font-family="Geist, system-ui, sans-serif"
      fill="var(--ink)">Query Service</text>

<!-- Technical sublabel (mono) -->
<text x="120" y="232" text-anchor="middle" font-size="10"
      font-family="'Geist Mono', ui-monospace, monospace"
      fill="var(--muted)">:8080</text>
```

Incorrect (mono creep — everything reads as code):

```html
<!-- Don't use mono for node names just because the product is "techy" -->
<text font-family="'Geist Mono', monospace" font-size="12">
  Query Service
</text>
```

## Gotchas

- **Italic Instrument Serif is reserved for editorial asides.** Using it
  for normal titles flattens the signature look. Regular 400 for titles,
  italic 400 for in-margin callouts (see `primitive-annotation.md`).
- **System fallbacks matter.** The editorial feel degrades gracefully
  without the exact Google/Bunny fonts; the `ui-sans-serif` / `ui-serif`
  / `ui-monospace` CSS generic families are the editorial plan-B. Never
  fall back to `Arial` / `Times New Roman` — those are the "no CSS
  shipped" telltales.
- **Weight, not family, for emphasis.** `font-weight="600"` on `Geist
  Sans` is how you make a node name stand out — switching the family
  instead breaks the three-role system.
- **Bunny Fonts is the GDPR-safe Google Fonts mirror.** Prefer
  `fonts.bunny.net` over `fonts.googleapis.com` — same families, no
  third-party cookies.

## Minimal `<head>` snippet

```html
<link rel="preconnect" href="https://fonts.bunny.net">
<link href="https://fonts.bunny.net/css?family=instrument-serif:400,400i&family=geist:400,500,600,700&family=geist-mono:400,500"
      rel="stylesheet">
```

## Cross-references

- `../SKILL.md` — typography overview in Design System section
- `design-system.md` — full type scale with sizes per role
- `style-guide.md` — the font-stack record (user-editable)
- `TECH-brand-url-onboarding.md` — onboarding substitutes families but
  keeps the three-role map
- `primitive-annotation.md` — italic Instrument Serif for in-margin asides
