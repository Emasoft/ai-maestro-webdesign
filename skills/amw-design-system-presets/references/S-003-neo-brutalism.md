---
id: S-003
name: Neo-Brutalism
aesthetic_position: classical-modernist
source_attribution: "styles-B §Brutalism/Neo-Brutalism (design-system-is-all-you-need, frontend-design-engineer); blocked-A #9 (claude-skill-ui-ux-pro-max). MIT per source repos."
license: MIT
---

# S-003 — Neo-Brutalism

## Identity

Neo-Brutalism softens classic Brutalism by exactly one move: it replaces the pure-system-colour palette with a single scream colour (acid yellow, hot pink, or safety orange) on a white or off-white ground, and the hard shadow shrinks to 4px offset instead of 8px. Everything else — zero radius, black borders, Space Grotesk or heavy grotesque, raw grid-breaking layout — remains. The result is confrontational but commercially legible, which is why it colonised the 2022-era startup product space. Reach for it when the brief wants "edgy but readable."

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  --primary: #FFE500;           /* the brand-defining color — acid yellow scream colour */
  --accent: #000000;            /* secondary accent — black on yellow = maximum contrast */
  --bg: #FFFFFF;                /* page background — pure white */
  --surface: #FFE500;           /* card/elevated surface — scream colour as surface */
  --text: #000000;              /* primary text */
  --text-muted: #333333;        /* secondary/muted text */
  --border: #000000;            /* border color — 2-3px solid black */
  --font-display: 'Space Grotesk', 'Arial Black', sans-serif; /* display font family with fallbacks */
  --font-body: 'Space Grotesk', Arial, sans-serif;            /* body font family with fallbacks */
  --font-mono: 'Courier New', monospace;                      /* mono */
  --radius: 0px;                /* corner radius — Neo-Brutalism is always 0 */
  --shadow: 4px 4px 0 #000000; /* hard-offset box-shadow, zero blur — smaller than classic */
  --spacing: 16px;              /* base spacing unit */
}
```

Tailwind theme extension (equivalent):
```js
{
  theme: {
    extend: {
      colors: {
        primary: '#FFE500',
        accent: '#000000',
        bg: '#FFFFFF',
        surface: '#FFE500',
        text: '#000000',
        'text-muted': '#333333',
        border: '#000000',
      },
      fontFamily: {
        display: ['"Space Grotesk"', '"Arial Black"', 'sans-serif'],
        body: ['"Space Grotesk"', 'Arial', 'sans-serif'],
      },
      borderRadius: { DEFAULT: '0px' },
      boxShadow: { DEFAULT: '4px 4px 0 #000000' },
    }
  }
}
```

## "Breaks if" invariants

- Breaks if `border-radius` exceeds 0px.
- Breaks if the box-shadow gains any blur radius (must be `4px 4px 0 #000`, not blurred).
- Breaks if a second chromatic colour is introduced alongside the scream colour (one scream colour maximum).
- Breaks if the scream colour is replaced with a tuned palette colour — it must be a saturated primary (acid yellow `#FFE500`, hot pink `#FF2D55`, safety orange `#FF6B00`, or equivalent high-chroma primary).
- Breaks if the border disappears or drops below 2px weight.
- Breaks if a soft gradient or decorative texture appears anywhere on the page.
- Breaks if the display font becomes decorative, serif, or rounded — must be a heavy grotesque.

## Canonical render-test pointer

Skeleton: `references/_test-skeleton.html`
Source render: no standalone upstream demo — tokens direct-ported from `design-system-is-all-you-need-main/brutalism.md`, `frontend-design-engineer-skill-main/visual-directions.md` #6, `blocked-A #9`
Parity threshold: A-class justified (no renderable upstream demo)

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 68416 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- [_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- [_harness-wiring.md](./_harness-wiring.md) — parity verification pipeline
- Source attribution: `reports/batch9-harvest/styles-B.md` §Brutalism / Neo-Brutalism; `reports/batch9-harvest/blocked-A.md` §9 Neubrutalism

## Attribution

Token values direct-ported from styles-B.md §Brutalism/Neo-Brutalism (design-system-is-all-you-need rawness levels, frontend-design-engineer Neo-Brutalist token block) and blocked-A.md #9 (claude-skill-ui-ux-pro-max). All source repos carry MIT license. Original distillation by the batch9 harvest team.
