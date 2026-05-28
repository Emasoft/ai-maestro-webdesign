---
id: S-015
name: Fashion / Luxury Editorial
aesthetic_position: editorial-warm-paper
source_attribution: https://github.com/Emasoft/ai-maestro-webdesign (batch9 harvest, styles-B; web-designer-plugin Fashion Editorial)
license: original summary; color, typography, and timing values in the public domain
---

## Identity

Fashion / Luxury Editorial is the visual language of high-fashion print — Vogue, Harper's Bazaar, AnOther Magazine — translated to the web: near-white `#FAFAFA` pages with near-black `#0A0A0A` type, large-format Didot or Bodoni (or the web-native Cormorant Garamond) display type at 80-120px for hero headlines, and a single restrained gold `#C9A84C` accent that appears only at key inflection points (a hairline border on a hero image, a navigation active-state, a price display). Photography is the primary content medium; the typography frames it rather than competes with it. The gallery model is museum-frame: images sit on generous white space with no decorative borders, radius, or shadow — the image is the object, the page is the gallery wall. Transitions are long (750ms) and use a refined cubic-bezier easing that mimics the physical weight of high-quality print stock turning. Designed for luxury fashion brands, high-end jewelry, art galleries, fine dining establishments, and any context where refinement and restraint communicate exclusivity.

## Token block

```css
/* S-015 Fashion / Luxury Editorial — token block */
:root {
  /* Colors — near-white page, near-black type, one gold accent */
  --color-bg:           #FAFAFA;   /* near-white gallery wall */
  --color-surface:      #FFFFFF;   /* pure white for image frames */
  --color-text:         #0A0A0A;   /* near-black — all body and display */
  --color-text-muted:   #767676;   /* mid-grey for captions, credits, metadata */
  --color-primary:      #0A0A0A;   /* primary action — same as text (no colour in CTA) */
  --color-accent:       #C9A84C;   /* gold — single decorative chromatic note */
  --color-border:       transparent; /* no visible borders — whitespace does the work */

  /* Typography — high-contrast display serif + restrained body */
  --font-display: 'Cormorant Garamond', 'Bodoni MT', 'Didot', 'Playfair Display', Georgia, serif;
  --font-body:    'Cormorant Garamond', 'Garamond', Georgia, serif;
  --font-mono:    'JetBrains Mono', 'Courier New', monospace;

  /* Display sizing — hero type at extreme scale */
  --font-size-display: clamp(64px, 9vw, 120px);
  --font-size-body:    16px;
  --line-height:       1.6;
  --letter-spacing-display: 0.06em;   /* wide tracking on display headlines */
  --letter-spacing-caps:    0.18em;   /* all-caps nav and labels */

  /* Layout */
  --spacing:            12px;
  --column-width:       750px;
  --radius:             0px;   /* no rounding — ever */
  --border-width:       0px;

  /* Shadow — none */
  --shadow: none;

  /* Motion — slow and weighted */
  --motion-duration:        750ms;
  --motion-easing:          cubic-bezier(0.25, 0.46, 0.45, 0.94);   /* ease-out-quart feel */
  --motion-duration-quick:  400ms;   /* for hover states only */
}
```

```ts
// Tailwind theme extension — S-015 Fashion / Luxury Editorial
export default {
  theme: {
    extend: {
      colors: {
        fashion: {
          bg:      '#FAFAFA',
          white:   '#FFFFFF',
          black:   '#0A0A0A',
          muted:   '#767676',
          gold:    '#C9A84C',
        },
      },
      fontFamily: {
        display: ['Cormorant Garamond', 'Bodoni MT', 'Didot', 'Playfair Display', 'Georgia', 'serif'],
        body:    ['Cormorant Garamond', 'Garamond', 'Georgia', 'serif'],
        mono:    ['JetBrains Mono', 'Courier New', 'monospace'],
      },
      fontSize: {
        'fashion-display': ['clamp(64px, 9vw, 120px)', { letterSpacing: '0.06em', lineHeight: '1.05' }],
        'fashion-body':    ['16px', { lineHeight: '1.6' }],
      },
      maxWidth: {
        fashion: '750px',
      },
      borderRadius: {
        fashion: '0px',
      },
      boxShadow: {
        fashion: 'none',
      },
      transitionDuration: {
        fashion:       '750ms',
        'fashion-fast': '400ms',
      },
      transitionTimingFunction: {
        fashion: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
      },
    },
  },
};
```

## "Breaks if" invariants

- Breaks if `border-radius` is set above `0px` — rounded corners signal consumer-app design; in the luxury-editorial context they read as naivety.
- Breaks if `box-shadow` or `drop-shadow` is applied to any element — shadows add material depth that conflicts with the gallery-wall flatness; the image is the only three-dimensional object on the page.
- Breaks if any visible border is drawn around images or cards — borders enclose; the fashion editorial aesthetic requires images to float on whitespace with no containing frame.
- Breaks if `--motion-duration` falls below `500ms` — fast transitions read as low-cost consumer UI; the 750ms weighted motion communicates physical materiality and deliberateness.
- Breaks if a second chromatic color (beyond black and gold) is introduced — the single gold accent is the only permitted chromatic note; a second color (blue, red, green) destroys the refined near-monochrome palette.
- Breaks if body text is set in a sans-serif typeface — the serif body is load-bearing for the editorial identity; humanist sans-serif fonts read as contemporary SaaS, not luxury fashion.
- Breaks if display type is set below `64px` on desktop — the extreme headline scale is definitional to the style; scaled-down display type produces a conventional editorial layout, not a fashion-luxury one.
- Breaks if image whitespace margins are reduced to less than `8vw` on either side of full-bleed images — the gallery-wall presentation requires generous surrounding space; compressed image margins produce a stock-photography grid, not a museum installation.

## Canonical render-test pointer

Render-test: inject tokens into `skills/amw-design-system-presets/references/_test-skeleton.html` with the token block above. Parity source: styles-B "Fashion / Luxury Editorial" + web-designer-plugin Fashion Editorial (batch9 harvest).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 63837 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- S-014 Editorial Serif / Content-First — shares the serif-first editorial typographic ethic; Editorial Serif prioritizes readable prose at 18px/1.8 with a deep-red accent; Fashion Luxury scales display type to 80-120px and uses gold.
- S-016 Luxury Dark Warm — shares the luxury positioning and gold accent; Luxury Dark Warm uses `#D4AF37` gold on `#12100E` dark background with Cinzel; Fashion Luxury uses a lighter gold on near-white for a daytime editorial feeling.
- S-028 Art Deco / Geometric — shares Cormorant and gold accent; Art Deco adds geometric ornament (chevrons, symmetry) and deep-navy backgrounds; Fashion Luxury stays close to pure near-white/black with extreme minimalism.

## Attribution

Tokens derived from batch9 harvest: `styles-B` "Fashion / Luxury Editorial", `web-designer-plugin` Fashion Editorial. Display typography conventions (Didot/Bodoni/Cormorant at large scale, wide tracking, gold accent) are established luxury-fashion design conventions in the public domain.
