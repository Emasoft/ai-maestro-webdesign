---
id: S-025
name: Playful / Toy-Like
aesthetic_position: playful-consumer-bold toy-atelier
source_attribution: https://github.com/atelier-main (SKILL.md — tone B1 #6); Bexa landing archetype "Playful/Consumer"
license: MIT (inferred)
---

# S-025 — Playful / Toy-Like

**Filename:** `skills/amw-design-system-presets/references/S-025-playful-toy.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Playful / Toy-Like is the Atelier tone #6 archetype: high-chroma primary palette (red, blue, yellow, green as saturated working colors), Nunito or Poppins at heavy weights, large rounded containers, and colorful drop-shadows that function as elevation signals rather than neutral depth. The aesthetic registers as "joyful product for non-expert users" — visual energy without aggression. Bounce and spring easing reward interaction; confetti-ready success states are expected. Unlike Candy (which leans hot pink / purple / neon), Playful Toy uses the primary color wheel — crayon-box hues, not neon cosmetics. Intended audience: children's education apps, gamified consumer tools, casual games, creative-for-kids platforms, and products that explicitly want to feel fun and approachable.

## Token block

```css
:root {
  /* Colors — high-chroma primary wheel; no pastels, no neons */
  --color-bg:         #FFFFFF;
  --color-surface:    #FFF9F0;
  --color-text:       #1A1A1A;
  --color-text-muted: #555555;
  --color-primary:    #E63946;   /* crayon red */
  --color-secondary:  #1D70B8;   /* crayon blue */
  --color-accent:     #F4A900;   /* crayon yellow-amber */
  --color-accent-2:   #2DC653;   /* crayon green */
  --color-border:     #E8E8E8;

  /* Typography — heavy rounded grotesque */
  --font-display: 'Nunito', 'Poppins', 'DM Rounded', sans-serif;
  --font-body:    'Nunito', 'Poppins', 'Inter', sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace;

  /* Geometry — large rounded, generous touch targets */
  --spacing:      8px;
  --radius:       20px;          /* 16-24px; large = toy-like */
  --border-width: 2px;           /* slightly thicker borders add cartoon weight */

  /* Shadow — colorful, matching the nearest primary hue */
  --shadow:        0 6px 0 rgba(230, 57, 70, 0.20),
                   0 4px 16px rgba(230, 57, 70, 0.12);

  /* Motion — bounce + spring; interaction rewards */
  --motion-duration: 320ms;
  --motion-easing:   cubic-bezier(0.34, 1.46, 0.64, 1);   /* spring bounce */
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:           '#FFFFFF',
        surface:      '#FFF9F0',
        text:         '#1A1A1A',
        'text-muted': '#555555',
        primary:      '#E63946',
        secondary:    '#1D70B8',
        accent:       '#F4A900',
        'accent-2':   '#2DC653',
        border:       '#E8E8E8',
      },
      fontFamily: {
        display: ['Nunito', 'Poppins', '"DM Rounded"', 'sans-serif'],
        body:    ['Nunito', 'Poppins', 'Inter', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      fontWeight: {
        display: '800',
        body:    '600',
      },
      borderRadius: {
        DEFAULT: '20px',
        card: '20px',
        btn:  '16px',
        sm:   '12px',
        lg:   '24px',
        pill: '9999px',
      },
      borderWidth: { DEFAULT: '2px' },
      boxShadow: {
        DEFAULT: '0 6px 0 rgba(230,57,70,0.20), 0 4px 16px rgba(230,57,70,0.12)',
        blue:    '0 6px 0 rgba(29,112,184,0.20), 0 4px 16px rgba(29,112,184,0.12)',
        yellow:  '0 6px 0 rgba(244,169,0,0.20),  0 4px 16px rgba(244,169,0,0.12)',
        hover:   '0 8px 0 rgba(230,57,70,0.28), 0 6px 24px rgba(230,57,70,0.18)',
      },
      transitionDuration: { DEFAULT: '320ms' },
      transitionTimingFunction: {
        DEFAULT: 'cubic-bezier(0.34,1.46,0.64,1)',
        bounce: 'cubic-bezier(0.34,1.46,0.64,1)',
      },
    },
  },
};
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --color-bg:         #1A1A2E;
  --color-surface:    #232340;
  --color-text:       #F8F8F8;
  --color-text-muted: #AAAACC;
  --color-border:     #3A3A5C;
  --shadow:           0 6px 0 rgba(230, 57, 70, 0.35),
                      0 4px 16px rgba(230, 57, 70, 0.22);
}
```

## "Breaks if" invariants

- breaks if palette shifts to pastels, muted tones, or neutrals — high-chroma primary wheel is the invariant
- breaks if `border-radius` drops below `16px` — large rounding is structural to the toy register
- breaks if colored shadow is removed or replaced with neutral grey drop-shadow
- breaks if `--motion-easing` is changed to `ease` or `linear` — the spring bounce is the kinetic signature
- breaks if typography switches to a serif, condensed, or non-rounded sans
- breaks if font weight drops below 700 on display headings — heavy weight signals toy-store boldness
- breaks if layout becomes dense, grid-heavy, or data-table oriented — low-density generosity is required
- breaks if neutral grey is used as a primary background — warm or bright surface only

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `atelier-main/SKILL.md` (tone B1 #6 — Playful/Consumer archetype definition); Bexa landing archetype "Playful/Consumer".

## Render-test verdict

JOD: pending

## Cross-references

- **Sibling styles:** S-024 Candy (hot pink + neon palette, spring overshoot), S-023 Vibrant Friendly (softer multi-color, less bounce), S-007 Claymorphism (pastel + clay depth)
- **Source:** `atelier-main` — SKILL.md (tone B1 #6); Bexa landing archetype "Playful/Consumer"
- **Note:** Nunito at weight 800 is the ideal display face for this style; the rounded apertures reinforce the toy-like energy. Poppins Bold (700) is an acceptable alternative with slightly less rounding. Both are on Google Fonts.
