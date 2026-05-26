---
id: S-026
name: Soft / Pastel
aesthetic_position: playful-consumer-bold
source_attribution: atelier-main/SKILL.md (tone B1 #10); frontend-design-main/SKILL.md
license: MIT
---

# S-026 — Soft / Pastel

**Filename:** `references/S-026-soft-pastel.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Soft / Pastel occupies the gentle corner of the playful-consumer spectrum: desaturated pastels (HSL saturation 30–50%) layered over near-white backgrounds create a nursery-fresh or wellness-calm register. Rounded grotesque typefaces (Nunito, DM Rounded) and generous radii (20–32px) soften every edge, while an ultra-light shadow (`0 8px 24px rgba(0,0,0,.06)`) provides just enough depth to keep cards from dissolving into the background. The intended audience is consumer apps, wellness platforms, children's products, and any brand where approachability outweighs authority.

## Token block

```css
/* S-026 Soft / Pastel — complete token block */
:root {
  /* Colors — desaturated pastels, 30-50% HSL saturation */
  --color-bg:          #FAFAF9;   /* near-white warm white */
  --color-surface:     #FFFFFF;   /* pure white card face */
  --color-text:        #2D2D35;   /* near-black — keeps WCAG-AA at small sizes */
  --color-text-muted:  #7A7A8C;   /* mid-grey muted prose */
  --color-primary:     #B5A4D4;   /* soft lavender — hsl(266,33%,73%) */
  --color-accent:      #F7A8B8;   /* pastel pink — hsl(348,82%,81%) desaturated to 40% eff. */
  --color-border:      #E8E4F0;   /* whisper lavender border */

  /* Extended palette (soft mint + peach for feature rows) */
  --color-mint:        #A8D8C8;   /* hsl(161,36%,75%) */
  --color-peach:       #F9C8A8;   /* hsl(25,88%,82%) — effective sat 38% */
  --color-sky:         #A8C8E8;   /* hsl(210,50%,78%) */

  /* Typography */
  --font-display:      'Nunito', 'DM Rounded', 'Varela Round', sans-serif;
  --font-body:         'Nunito', 'DM Rounded', 'Varela Round', sans-serif;
  --font-mono:         'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Spacing & shape */
  --spacing:           8px;
  --radius:            24px;   /* canonical soft-pastel radius: 20-32px range */

  /* Shadow — the signature ultra-light float */
  --shadow:            0 8px 24px rgba(0,0,0,0.06);

  /* Motion — gentle only */
  --motion-duration:   280ms;
  --motion-easing:     cubic-bezier(0.22, 1, 0.36, 1);   /* ease-out-quint: gentle settle */
}
```

```js
// Tailwind theme extension — S-026 Soft / Pastel
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        'sp-bg':       '#FAFAF9',
        'sp-surface':  '#FFFFFF',
        'sp-text':     '#2D2D35',
        'sp-muted':    '#7A7A8C',
        'sp-primary':  '#B5A4D4',
        'sp-accent':   '#F7A8B8',
        'sp-border':   '#E8E4F0',
        'sp-mint':     '#A8D8C8',
        'sp-peach':    '#F9C8A8',
        'sp-sky':      '#A8C8E8',
      },
      fontFamily: {
        display: ['Nunito', 'DM Rounded', 'Varela Round', 'sans-serif'],
        body:    ['Nunito', 'DM Rounded', 'Varela Round', 'sans-serif'],
        mono:    ['JetBrains Mono', 'Fira Code', 'Courier New', 'monospace'],
      },
      borderRadius: {
        sp: '24px',
        'sp-pill': '9999px',
      },
      boxShadow: {
        sp: '0 8px 24px rgba(0,0,0,0.06)',
      },
      transitionTimingFunction: {
        sp: 'cubic-bezier(0.22, 1, 0.36, 1)',
      },
      transitionDuration: {
        sp: '280ms',
      },
    },
  },
}
```

## "Breaks if" invariants

- breaks if any color HSL saturation exceeds 55% — the entire palette must stay in the 30–50% desaturated band; vivid high-chroma accents exit the preset
- breaks if `border-radius` drops below 16px — the pillow-softness of rounded corners is the primary structural signal; sharp corners contradict the aesthetic
- breaks if the shadow is changed to anything darker than `rgba(0,0,0,0.10)` or gains a colored tint — the ultra-light float shadow is identity-defining
- breaks if a dark or deeply saturated background is used — the near-white base is mandatory; dark-mode variants require a separate desaturated-dark token set
- breaks if typography switches to a geometric sans with sharp joints (e.g., Futura, Barlow) — only rounded grotesques (Nunito, DM Rounded, Varela Round) or soft calligraphic serifs are valid
- breaks if motion uses linear or abrupt easing — gentle ease-out is required; kinetic or spring-heavy motion overrides the calm register
- breaks if a second bold chromatic accent is added alongside the primary — the palette supports multiple pastels at low saturation, but never two high-saturation competing accents

## Canonical render-test pointer

Render-test: inject tokens from `## Token block` into `references/_test-skeleton.html` (substitute `{{BG}}=#FAFAF9`, `{{SURFACE}}=#FFFFFF`, `{{TEXT}}=#2D2D35`, `{{TEXT_MUTED}}=#7A7A8C`, `{{PRIMARY}}=#B5A4D4`, `{{ACCENT}}=#F7A8B8`, `{{BORDER}}=#E8E4F0`, `{{FONT_DISPLAY}}='Nunito',sans-serif`, `{{FONT_BODY}}='Nunito',sans-serif`, `{{FONT_MONO}}='JetBrains Mono',monospace`, `{{RADIUS}}=24px`, `{{SHADOW}}=0 8px 24px rgba(0,0,0,.06)`, `{{SPACING}}=8px`).

Upstream reference: `atelier-main/SKILL.md` tone B1 #10 "Soft / Pastel"; `reports/batch9-harvest/styles-A.md` "Soft / Pastel" section.

## Render-test verdict

JOD: pending

## Cross-references

- Sibling styles: S-024 Candy (higher saturation, pill radius, bounce physics), S-025 Playful Toy-Like (high-chroma primaries, bold weight), S-007 Claymorphism (3D inflate + inner highlight), S-005 Neumorphism (monochromatic extrusion)
- Source: `atelier-main/SKILL.md` (MIT); `reports/batch9-harvest/styles-A.md` "Soft / Pastel" entry; `frontend-design-main/SKILL.md` Anchor 6 (MIT).

## Attribution

Direct port from `atelier-main` (MIT license). Token values synthesized from the `styles-A.md` "Soft / Pastel" section and the task brief token notes (`reports/batch9-analysis/MASTER-LEDGER.md` S-026 row). Catalog summary and "breaks-if" invariants are original content authored for this plugin. License: MIT.
