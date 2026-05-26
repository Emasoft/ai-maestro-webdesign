---
id: S-040
name: Chinese Elegant
aesthetic_position: editorial-warm-paper
source_attribution: >
  blocked-B.md seed table "Chinese Elegant" (10-style Wave 1 Track H8 seed);
  styles-B.md "Chinese Elegant" editorial-warm-paper position; tasteful-ui-skill-master
  catalog CJK-editorial entry (LXGW WenKai, generous line-height, first-paragraph indent).
  LICENSE: MIT (tasteful-ui-skill, web-designer-plugin).
license: MIT (all upstream sources)
---

# S-040 — Chinese Elegant

**Filename:** `skills/amw-design-system-presets/references/S-040-chinese-elegant.md`
**Tracked in:** this repo (design/tasks/ is git-tracked)

## Identity

Chinese Elegant is a refined editorial aesthetic calibrated for mixed CJK-Latin long-form reading. Its visual fingerprint is a warm rice-paper canvas (`#FAF9F4`), LXGW WenKai as the preferred display and body typeface (a handwriting-derived open-source font with warm ink character), generous line-height of 1.8 for comfortable CJK-dense reading, a traditional 2em first-paragraph text-indent per paragraph, and a single muted cinnabar or ink-red accent. Intended audience: literary magazines and blogs with Chinese-language content, cultural institution sites, art-book publishers, traditional medicine portals, and any long-form editorial platform where the reading experience of CJK text is the primary design concern.

## Token block

```css
/* S-040 Chinese Elegant — CSS custom properties */
:root {
  /* Color */
  --color-bg:          #FAF9F4;   /* warm rice-paper white */
  --color-surface:     #F3F1E8;   /* slightly deeper warm for cards */
  --color-surface-2:   #EAE7DC;   /* elevated surface (modal, aside) */
  --color-text:        #1A1610;   /* warm near-black — ink on paper */
  --color-text-muted:  #6E6558;   /* warm brown-grey — captions, dates */
  --color-primary:     #1A1610;   /* primary action = text colour */
  --color-accent:      #A8342B;   /* muted cinnabar / ink-red — one chromatic touch */
  --color-accent-dim:  #7D251E;   /* pressed/hover accent */
  --color-border:      #DDD8CC;   /* warm hairline */

  /* Typography — CJK-optimised font stack */
  --font-display: 'LXGW WenKai', 'Songti SC', 'STSong', 'SimSun', 'Noto Serif SC', Georgia, serif;
  --font-body:    'LXGW WenKai', 'Songti SC', 'STSong', 'SimSun', 'Noto Serif SC', Georgia, serif;
  --font-mono:    'LXGW WenKai Mono', 'Courier Prime', 'Courier New', monospace;

  /* Spacing */
  --spacing: 8px;   /* base unit */

  /* Shape */
  --radius: 4px;

  /* Shadow — warm-toned ink shadow */
  --shadow: 0 2px 12px rgba(26, 22, 16, 0.08);

  /* Motion — measured, deliberate */
  --motion-duration: 350ms;
  --motion-easing: cubic-bezier(0.4, 0, 0.2, 1);

  /* CJK-editorial extras */
  --line-height-body:  1.8;        /* generous CJK reading leading */
  --indent-para:       2em;        /* traditional first-paragraph indent */
  --border-width:      1px;
  --letter-spacing-heading: 0.05em;   /* slight spacing for display headings */
}
```

```ts
// S-040 Chinese Elegant — Tailwind theme extension
const chineseElegant = {
  colors: {
    bg:          '#FAF9F4',
    surface:     '#F3F1E8',
    'surface-2': '#EAE7DC',
    text:        '#1A1610',
    'text-muted':'#6E6558',
    primary:     '#1A1610',
    accent:      '#A8342B',
    'accent-dim':'#7D251E',
    border:      '#DDD8CC',
  },
  fontFamily: {
    display: ['"LXGW WenKai"', '"Songti SC"', 'STSong', 'SimSun', '"Noto Serif SC"', 'Georgia', 'serif'],
    body:    ['"LXGW WenKai"', '"Songti SC"', 'STSong', 'SimSun', '"Noto Serif SC"', 'Georgia', 'serif'],
    mono:    ['"LXGW WenKai Mono"', '"Courier Prime"', '"Courier New"', 'monospace'],
  },
  spacing: { base: '8px' },
  borderRadius: { DEFAULT: '4px' },
  boxShadow: {
    DEFAULT: '0 2px 12px rgba(26,22,16,0.08)',
  },
  transitionDuration: { DEFAULT: '350ms' },
  transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.4,0,0.2,1)' },
} as const;
```

## "Breaks if" invariants

- breaks if line-height falls below 1.7 (CJK character stacking requires generous leading)
- breaks if the first-paragraph text-indent is removed (2em indent is a typographic tradition that defines this style)
- breaks if a sans-serif or geometric font replaces the warm-ink serif/handwriting display stack
- breaks if the canvas colour becomes white (`#FFFFFF`) or cool-toned
- breaks if a second chromatic accent is introduced alongside the cinnabar ink-red
- breaks if border-radius exceeds 8px (the subtle radius should not dominate; this is editorial, not rounded-consumer)
- breaks if the accent is used as a page-wide decorative fill rather than reserved for links, emphasis, and singular CTA elements
- breaks if drop-shadows use a cool grey rather than the warm ink tint
- breaks if letter-spacing on body text exceeds 0.05em (CJK readability degrades with excessive tracking)
- breaks if the typography system substitutes a cold-white Western-serif fallback (Helvetica, Arial) as the effective rendered font without the CJK fonts being loaded

## Canonical render-test pointer

Render test: inject this file's tokens into `references/_test-skeleton.html` (substituting `{{BG}}` = `#FAF9F4`, `{{SURFACE}}` = `#F3F1E8`, `{{TEXT}}` = `#1A1610`, `{{TEXT_MUTED}}` = `#6E6558`, `{{PRIMARY}}` = `#1A1610`, `{{ACCENT}}` = `#A8342B`, `{{BORDER}}` = `#DDD8CC`, `{{FONT_DISPLAY}}` = `'LXGW WenKai', 'Songti SC', 'Noto Serif SC', Georgia, serif`, `{{FONT_BODY}}` = `'LXGW WenKai', 'Songti SC', Georgia, serif`, `{{FONT_MONO}}` = `'LXGW WenKai Mono', 'Courier Prime', monospace`, `{{RADIUS}}` = `4px`, `{{SHADOW}}` = `0 2px 12px rgba(26,22,16,.08)`, `{{SPACING}}` = `8px`).

Note: LXGW WenKai requires loading from the LXGW CDN (`https://cdn.jsdelivr.net/npm/lxgw-wenkai-webfont@1.7.0/style.css`) for web delivery. Without it, Songti SC (macOS) / SimSun (Windows) / Noto Serif SC (Android/Linux) serve as graceful fallbacks.

Upstream parity source: `blocked-B.md` seed table "Chinese Elegant" + `tasteful-ui-skill-master` catalog (MIT, inferred).

## Render-test verdict

JOD: pending

## Cross-references

- Siblings: S-043 Japanese Dark (dark mode CJK editorial with Noto Serif JP), S-014 Editorial Serif (Western editorial serif), S-037 Cream Editorial (cream Western book-publisher serif)
- Differentiators: S-040 is warm-light CJK-first editorial with LXGW WenKai and 2em indent; S-043 is dark-mode Japanese editorial; S-014 is Western editorial with mixed sans/serif; S-037 is Western-only serif at 0px radius
- Source: `blocked-B.md` seed table Wave 1 Track H8 + `tasteful-ui-skill-master` catalog (MIT)
