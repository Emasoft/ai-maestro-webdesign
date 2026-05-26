---
id: S-023
name: Vibrant Friendly / Playful SaaS
aesthetic_position: playful-consumer-bold saas-energy
source_attribution: https://github.com/tasteful-ui-skill-master (catalog.md — Lovable + Figma archetypes); https://github.com/swiftui-design-skill-main (SKILL.md — Expressive school)
license: MIT (inferred)
---

# S-023 — Vibrant Friendly / Playful SaaS

**Filename:** `skills/amw-design-system-presets/references/S-023-vibrant-friendly.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Vibrant Friendly is the canonical SaaS landing-page aesthetic: a bright brand-primary blue or purple, complemented by two or three cheerful secondary hues that are related but not identical, all on a white surface. DM Sans or Nunito supplies the approachable letterforms; card grids organize the feature sections; soft colored shadows (tinted to the nearest primary hue) add just enough depth without resorting to neutral grey. The style signals "professional product that humans actually enjoy using" — confident whitespace, warm illustration accents, and 8–16px radius on every interactive element. Intended audience: developer-tool SaaS, consumer productivity apps, B2C platforms, and any startup in the Lovable/Linear/Notion family of aesthetics.

## Token block

```css
:root {
  /* Colors — brand-primary + 2-3 complementary accents on white */
  --color-bg:         #FFFFFF;
  --color-surface:    #F7F8FF;
  --color-text:       #1A1A2E;
  --color-text-muted: #6B7280;
  --color-primary:    #5B4AE8;   /* brand blue-purple */
  --color-secondary:  #F59E0B;   /* amber accent */
  --color-accent:     #10B981;   /* emerald tertiary */
  --color-accent-2:   #EC4899;   /* pink fourth — optional; use sparingly */
  --color-border:     #E5E7EB;

  /* Typography */
  --font-display: 'DM Sans', 'Nunito', 'Inter', sans-serif;
  --font-body:    'Inter', 'DM Sans', 'Helvetica Neue', sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace;

  /* Geometry */
  --spacing:      8px;
  --radius:       12px;          /* 8-16px range; 12px is the comfortable default */
  --border-width: 1px;

  /* Shadow — soft, tinted to primary hue */
  --shadow:       0 4px 16px rgba(91, 74, 232, 0.12);

  /* Motion — enthusiastic but not chaotic */
  --motion-duration: 280ms;
  --motion-easing:   cubic-bezier(0.22, 0.61, 0.36, 1);  /* ease-out */
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:           '#FFFFFF',
        surface:      '#F7F8FF',
        text:         '#1A1A2E',
        'text-muted': '#6B7280',
        primary:      '#5B4AE8',
        secondary:    '#F59E0B',
        accent:       '#10B981',
        'accent-2':   '#EC4899',
        border:       '#E5E7EB',
      },
      fontFamily: {
        display: ['"DM Sans"', 'Nunito', 'Inter', 'sans-serif'],
        body:    ['Inter', '"DM Sans"', '"Helvetica Neue"', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      borderRadius: { DEFAULT: '12px', sm: '8px', lg: '16px' },
      boxShadow: {
        DEFAULT: '0 4px 16px rgba(91,74,232,0.12)',
        card:    '0 2px 8px rgba(91,74,232,0.08)',
        hover:   '0 8px 32px rgba(91,74,232,0.18)',
      },
      transitionDuration: { DEFAULT: '280ms' },
      transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.22,0.61,0.36,1)' },
    },
  },
};
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --color-bg:         #0F0E1A;
  --color-surface:    #1A1930;
  --color-text:       #F3F4F6;
  --color-text-muted: #9CA3AF;
  --color-border:     #2D2B4E;
  --shadow:           0 4px 16px rgba(91, 74, 232, 0.25);
}
```

## "Breaks if" invariants

- breaks if palette drops to monochrome — the multi-color energy is the signature; one accent is insufficient
- breaks if a dark background replaces the white/near-white surface — this is a light-mode-first style
- breaks if `border-radius` drops below `8px` — clinical sharp corners exit the friendly register
- breaks if font switches to a geometric or condensed sans without rounded terminals
- breaks if colored shadow is replaced with a neutral black/grey drop-shadow
- breaks if layout density shifts to data-grid or information-dense mode — spacious card grids are structural
- breaks if illustration accents are stripped entirely — some decorative color presence is expected between sections
- breaks if `--motion-duration` exceeds 400ms — enthusiasm turns sluggish above this threshold

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `tasteful-ui-skill-master/catalog.md` (Lovable archetype: "playful gradients, friendly dev aesthetic"; Figma archetype: "vibrant multi-color"); `swiftui-design-skill-main/SKILL.md` (Expressive school — bold colour, motion).

## Render-test verdict

JOD: pending

## Cross-references

- **Sibling styles:** S-024 Candy (hotter palette + bouncy spring), S-025 Playful Toy-Like (high-chroma primaries, heavier weight), S-007 Claymorphism (pastel + depth)
- **Source:** `tasteful-ui-skill-master` — catalog.md; `swiftui-design-skill-main` — SKILL.md
- **Note:** DM Sans and Nunito are available on Google Fonts (free for commercial use). The `--color-primary` slot is designed for brand-color substitution — the multi-color palette structure remains intact when only the primary hue changes.
