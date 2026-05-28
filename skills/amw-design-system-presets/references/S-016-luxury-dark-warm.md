---
id: S-016
name: Luxury Dark Warm
aesthetic_position: editorial-warm-paper
source_attribution: https://github.com/frontend-design-engineer-skill (visual-directions.md #3 Luxury Dark Warm); https://github.com/claude-website-design-skills (claude-remix art-deco vocabulary)
license: MIT (inferred from source repo conventions)
---

# S-016 — Luxury Dark Warm

**Filename:** `skills/amw-design-system-presets/references/S-016-luxury-dark-warm.md`
**Tracked in:** this repo (design/tasks/ is git-tracked)

## Identity

Luxury Dark Warm encodes the aesthetic language of premium jewelry, haute couture, boutique hospitality, and fine wine — industries where the deepest near-black and 24-karat gold are the only grammar that conveys true rarity. The background is not black but a warm organic near-black (`#12100E`), a tone that reads as aged leather rather than void. Gold is the single chromatic accent: `#D4AF37` is mined gold, not tech-startup amber. Beige-white text (`#F5F5DC`) avoids the clinical harshness of pure white, keeping the surface warm even in body copy. The typographic pairing — Cinzel (Roman-inscribed capitals, lapidary) for display, Montserrat for body — reinforces the material quality without competing with the color hierarchy. This style serves premium product pages, invitation-only platforms, luxury real-estate, fine-dining brands, and any context where perceived value must be communicated in the absence of imagery.

## Token block

```css
:root {
  /* Colors */
  --color-bg:          #12100E;
  --color-surface:     #1C1916;
  --color-text:        #F5F5DC;
  --color-text-muted:  #A89B78;
  --color-primary:     #D4AF37;
  --color-accent:      #C5A059;
  --color-border:      #2E2A24;

  /* Typography */
  --font-display: 'Cinzel', 'Trajan Pro', 'Times New Roman', serif;
  --font-body:    'Montserrat', 'Gill Sans', 'Helvetica Neue', sans-serif;
  --font-mono:    'Courier New', 'Courier', monospace;

  /* Spacing */
  --spacing: 8px;

  /* Shape */
  --radius: 2px;

  /* Shadow */
  --shadow: 0 4px 20px rgba(0, 0, 0, 0.5);

  /* Motion */
  --motion-duration: 500ms;
  --motion-easing:   cubic-bezier(0.25, 0.46, 0.45, 0.94);

  /* Optional brand-specific */
  --gradient-gold: linear-gradient(135deg, #C5A059 0%, #D4AF37 50%, #B8962A 100%);
  --glow-gold:     0 0 20px rgba(212, 175, 55, 0.25);
}
```

```ts
// Tailwind theme extension
theme: {
  extend: {
    colors: {
      'lux-bg':        '#12100E',
      'lux-surface':   '#1C1916',
      'lux-text':      '#F5F5DC',
      'lux-muted':     '#A89B78',
      'lux-gold':      '#D4AF37',
      'lux-accent':    '#C5A059',
      'lux-border':    '#2E2A24',
    },
    fontFamily: {
      display: ['Cinzel', 'Trajan Pro', 'Times New Roman', 'serif'],
      body:    ['Montserrat', 'Gill Sans', 'Helvetica Neue', 'sans-serif'],
    },
    borderRadius: {
      DEFAULT: '2px',
      sm:      '1px',
      lg:      '4px',
    },
    boxShadow: {
      lux: '0 4px 20px rgba(0,0,0,0.5)',
    },
  },
},
```

## "Breaks if" invariants

- breaks if `--color-bg` is changed to pure `#000000` — the warmth disappears and the style collapses into generic dark mode
- breaks if the display typeface is replaced with a sans-serif or slab — the lapidary Roman quality (Cinzel) is the style's non-negotiable typographic signal
- breaks if a cool accent (blue, cyan, green, purple) is introduced — the entire palette is warm-spectrum; any cool hue creates a chromatic discord that reads as cheap
- breaks if `--radius` is raised above 4px — even 6px begins to read as approachable/modern rather than refined/formal; 2px is the architectural limit
- breaks if gold (`--color-primary`) is replaced with a muted amber or yellow — the hue must read as precious metal, not warm tone
- breaks if multiple competing shadows are added — the deep single shadow is a depth signal; stacking shadows turns it into SaaS-generic
- breaks if body copy uses pure white (`#FFFFFF`) — beige-white (`#F5F5DC`) maintains the warm chromatic temperature that unifies the page
- breaks if section padding drops below 64px — luxury communicates through generosity of space; tight layouts read as mass-market

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers with the values above.
Source parity: `frontend-design-engineer-skill-main/references/visual-directions.md` (direction #3, Luxury Dark Warm). Compare hero section, card row, and pricing table at 1440px desktop.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 107184 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- S-015 Fashion Luxury Editorial — sibling; lighter background, Didot/Bodoni, museum-frame; use when the aesthetic is contemporary luxury, not heritage warmth
- S-028 Art Deco / Geometric — related gold palette; differs in structured symmetry and geometric ornament rather than warm warmth; use for events and identity brands
- S-013 Industrial — opposing anchor; same dark bg but cold, utilitarian; use to understand the warm/cold axis for dark UI
- Source: `frontend-design-engineer-skill-main/.../visual-directions.md` (#3 Luxury Dark Warm); `claude-website-design-skills-main/skills/claude-remix/SKILL.md` (art-deco vocabulary cross-reference)
