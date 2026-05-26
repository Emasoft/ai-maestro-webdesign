---
id: S-002
name: Brutalism (classic)
aesthetic_position: classical-modernist
source_attribution: "styles-B §Brutalism/Neo-Brutalism (DSIAYN, frontend-design Anchor 3); styles-A §Brutalist/Raw (atelier-main MIT). MIT per source repos."
license: MIT
---

# S-002 — Brutalism (classic)

## Identity

Classic web Brutalism applies the architectural manifesto to the browser: raw structural expression over visual comfort, system fonts only, primary-colour primaries with no tuning, thick black borders, and the signature hard-offset box-shadow with zero blur. It is anti-decoration on principle. Reach for it when the brief demands an oppositional stance — art agencies, counter-cultural platforms, portfolio sites that weaponise "wrong" as a statement.

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  --primary: #FF0000;           /* the brand-defining color — pure system red */
  --accent: #0000FF;            /* secondary accent — pure system blue */
  --bg: #FFFFFF;                /* page background — pure white, no cream */
  --surface: #FFFFFF;           /* card/elevated surface — no elevation in classic Brutalism */
  --text: #000000;              /* primary text */
  --text-muted: #333333;        /* secondary/muted text */
  --border: #000000;            /* border color — thick black border is the signature */
  --font-display: 'Times New Roman', 'Courier New', serif; /* system serif display — no webfonts */
  --font-body: Arial, Helvetica, sans-serif;               /* system sans body — no webfonts */
  --font-mono: 'Courier New', Courier, monospace;          /* system mono */
  --radius: 0px;                /* corner radius — zero is absolute */
  --shadow: 8px 8px 0 #000000; /* hard-offset box-shadow, zero blur — the Brutalism signature */
  --spacing: 16px;              /* base spacing unit */
}
```

Tailwind theme extension (equivalent):
```js
{
  theme: {
    extend: {
      colors: {
        primary: '#FF0000',
        accent: '#0000FF',
        bg: '#FFFFFF',
        surface: '#FFFFFF',
        text: '#000000',
        'text-muted': '#333333',
        border: '#000000',
      },
      fontFamily: {
        display: ['"Times New Roman"', '"Courier New"', 'serif'],
        body: ['Arial', 'Helvetica', 'sans-serif'],
      },
      borderRadius: { DEFAULT: '0px' },
      boxShadow: { DEFAULT: '8px 8px 0 #000000' },
    }
  }
}
```

## "Breaks if" invariants

- Breaks if any webfont replaces system fonts (Times New Roman, Arial, Helvetica, Courier are the only permitted faces).
- Breaks if `border-radius` exceeds 0px.
- Breaks if the box-shadow gains any blur radius (shadow must be `X Y 0 #000`, not `X Y 8px #000`).
- Breaks if a tuned/custom hex colour replaces the system primaries (`#FF0000`, `#0000FF`, `#FFFF00`, black, white only).
- Breaks if soft gradients, background textures, or grain overlays appear.
- Breaks if the border weight drops below 2px (hairline borders are the Swiss idiom, not Brutalism).
- Breaks if a centered layout replaces the off-grid stacking or asymmetric columns.

## Canonical render-test pointer

Skeleton: `references/_test-skeleton.html`
Source render: no standalone upstream demo — tokens direct-ported from `frontend-design-main/SKILL.md` Anchor 3, `design-system-is-all-you-need-main/brutalism.md`, `atelier-main/SKILL.md` tone B1 #8
Parity threshold: A-class justified (no renderable upstream demo)

## Render-test verdict

JOD: pending

## Cross-references

- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- [_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- [_harness-wiring.md](./_harness-wiring.md) — parity verification pipeline
- Source attribution: `reports/batch9-harvest/styles-B.md` §Brutalism / Neo-Brutalism; `reports/batch9-harvest/styles-A.md` §Brutalist/Raw

## Attribution

Token values direct-ported from styles-B.md §Brutalism/Neo-Brutalism (design-system-is-all-you-need, frontend-design Anchor 3) and styles-A.md §Brutalist/Raw (atelier-main). All source repos carry MIT license. Original distillation by the batch9 harvest team.
