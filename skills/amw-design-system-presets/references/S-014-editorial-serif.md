---
id: S-014
name: Editorial Serif / Content-First
aesthetic_position: editorial-warm-paper
source_attribution: https://github.com/Emasoft/ai-maestro-webdesign (batch9 harvest, styles-A/B "Editorial Serif"; frontend-design-engineer #1; generate-design-md editorial-minimal; blocked-A #6 WIRED)
license: original summary; typography and color values in the public domain
---

## Identity

Editorial Serif is a content-first reading experience modeled after long-form print journalism: The New Yorker, The Atlantic, WIRED's feature layouts, and classic book typography. The background is warm paper-white `#F9F9F7`; the text is near-black `#111111`; the single accent is a deep editorial red `#B22222`. Display headings use Playfair Display (or Cormorant Garamond as an alternative) — a high-contrast, classically-proportioned display serif with strong horizontal strokes. Body text uses Lora or Georgia, both optimized for screen reading at the 18px / 1.8 line-height values that define comfortable long-form reading. Column width is capped at `720px` (approximately 65 characters per line) — the optimal reading measure for prose. Horizontal rule dividers (`<hr>`) replace decorative elements. No border-radius, no shadows: the page surface is the paper.

## Token block

```css
/* S-014 Editorial Serif / Content-First — token block */
:root {
  /* Colors */
  --color-bg:           #F9F9F7;   /* warm paper-white */
  --color-surface:      #FFFFFF;   /* pure white for inset cards/quote blocks */
  --color-text:         #111111;   /* near-black for maximum contrast */
  --color-text-muted:   #555555;   /* secondary text — captions, metadata, bylines */
  --color-primary:      #B22222;   /* deep editorial red — links, CTAs, headings accent */
  --color-accent:       #8B1A1A;   /* darker red for pressed/visited states */
  --color-border:       #DDDDDD;   /* light grey — horizontal rules and table lines */

  /* Typography */
  --font-display: 'Playfair Display', 'Cormorant Garamond', Georgia, 'Times New Roman', serif;
  --font-body:    'Lora', Georgia, 'Times New Roman', serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Layout */
  --spacing:        8px;
  --column-width:   720px;   /* max-width for prose column */
  --font-size-body: 18px;
  --line-height:    1.8;
  --radius:         0px;

  /* Shadow — none */
  --shadow: none;

  /* Motion — slow, deliberate */
  --motion-duration: 300ms;
  --motion-easing:   ease-in-out;

  /* Rule dividers */
  --border-width:   1px;
  --rule-color:     #CCCCCC;
}
```

```ts
// Tailwind theme extension — S-014 Editorial Serif
export default {
  theme: {
    extend: {
      colors: {
        editorial: {
          bg:      '#F9F9F7',
          surface: '#FFFFFF',
          ink:     '#111111',
          muted:   '#555555',
          red:     '#B22222',
          'red-dark': '#8B1A1A',
          rule:    '#CCCCCC',
        },
      },
      fontFamily: {
        display: ['Playfair Display', 'Cormorant Garamond', 'Georgia', 'serif'],
        body:    ['Lora', 'Georgia', 'Times New Roman', 'serif'],
        mono:    ['JetBrains Mono', 'Fira Code', 'Courier New', 'monospace'],
      },
      maxWidth: {
        editorial: '720px',
      },
      fontSize: {
        editorial: ['18px', { lineHeight: '1.8' }],
      },
      borderRadius: {
        editorial: '0px',
      },
      boxShadow: {
        editorial: 'none',
      },
      transitionDuration: {
        editorial: '300ms',
      },
    },
  },
};
```

## "Breaks if" invariants

- Breaks if body font is set to a sans-serif typeface — the style's entire rationale is the optical warmth and reading rhythm of a high-quality serif; sans-serif produces a corporate or tech-product feel.
- Breaks if `border-radius` exceeds `0px` — the style emulates paper and print; rounded corners introduce GUI-product softness that conflicts with the typographic authority.
- Breaks if `box-shadow` is applied to any element — shadows in this context imply skeuomorphic depth, which conflicts with the flat paper-page model.
- Breaks if body `font-size` falls below `16px` or `line-height` falls below `1.6` — comfortable long-form reading requires both; reducing either produces a cramped newsletter, not a magazine feature.
- Breaks if prose column `max-width` exceeds `760px` — lines longer than ~70 characters per line impose measurable reading fatigue; the 720px constraint is not decorative.
- Breaks if a second chromatic color is introduced alongside the deep-red accent — editorial design relies on one controlled color moment against near-neutral ink; a second accent color turns the page into a branded product rather than a publication.
- Breaks if decorative graphics (illustrations, gradient backgrounds, hero images with text overlays) replace horizontal rule dividers as section breaks — rule dividers are the structure; they impose the visual hierarchy that images distract from.
- Breaks if the background color is set to pure white `#FFFFFF` and text to pure black `#000000` — the slight warmth of `#F9F9F7` and the softness of `#111111` are intentional to reduce eye strain in long-form reading; pure values are too harsh.

## Canonical render-test pointer

Render-test: inject tokens into `skills/amw-design-system-presets/references/_test-skeleton.html` with the token block above. Parity source: styles-A/B "Editorial Serif" + frontend-design-engineer #1 + generate-design-md editorial-minimal + blocked-A #6 WIRED (batch9 harvest).

## Render-test verdict

JOD: pending

## Cross-references

- S-015 Fashion / Luxury Editorial — shares the serif-display category and editorial whitespace ethic; Fashion Editorial uses Didot/Bodoni/Cormorant at 80-120px and gold accent vs. Editorial Serif's measured 18px body copy and deep-red accent.
- S-037 Cream Editorial — adjacent style using Cormorant Garamond on `#FAF8F4` with 0px radius; Editorial Serif carries a richer token set including the deep-red accent and explicit rule-divider treatment.
- S-044 Dashboard Magazine / FT-style — shares the broadsheet lineage but adds a 3-column grid, IBM Plex Sans alongside the serif, and paper-grain texture; Editorial Serif is single-column pure prose.

## Attribution

Tokens derived from batch9 harvest: `styles-A/B` "Editorial Serif", `frontend-design-engineer` #1, `generate-design-md` editorial-minimal, `blocked-A` #6 (WIRED reference). Typography choices (Playfair Display + Lora) and color values are established editorial-design conventions in the public domain.
