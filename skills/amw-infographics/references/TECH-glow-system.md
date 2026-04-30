---
name: TECH-glow-system
category: infographic-archetype
source: image-generation/create-infographics/resources/style-details.md
also-in:
---

# Glow system — neon box-shadow + text-shadow

## What it does

Neon glow effects used in 57-75% of infographics (confirmed 57% via
GPT-5.4; Claude over-detected at 75%). Standard especially for
ecosystem (73%), crypto-explainer (69%), game-overview (60%),
token-economics (53%).

## The glow system

```css
/* source: image-generation/create-infographics/resources/style-details.md */

/* Standard neon glow — most common */
.glow-primary {
  box-shadow: 0 0 20px rgba(var(--primary-rgb), 0.4),
              0 0 40px rgba(var(--primary-rgb), 0.2);
}

/* Subtle glow — for cards */
.glow-card {
  box-shadow: 0 0 12px rgba(var(--primary-rgb), 0.25);
}

/* Text glow — for stat numbers, headers */
.glow-text {
  text-shadow: 0 0 20px rgba(var(--primary-rgb), 0.6),
               0 0 40px rgba(var(--primary-rgb), 0.3);
}

/* No glow — for tables and dense layouts */
.no-glow {
  box-shadow: none;
}
```

## Double-layer glow pattern

The signature is two box-shadows stacked — a tighter inner glow
(20px, 0.4 opacity) and a wider outer glow (40px, 0.2 opacity).
Creates a diffused, neon-sign feel.

## Top confirmed glow colors

```
#F5A623  amber       — 7 pieces
#FFD700  gold        — 6 pieces
#00D4FF  cyan        — 8 pieces
#E63946  red         — 4 pieces
#FF69B4  pink        — 3 pieces
#00E5A0  emerald     — 3 pieces
#7CFC00  lime        — 3 pieces
#9B5DE5  purple      — 2 pieces
```

## When to use each

| Style | Use on |
|-------|--------|
| `.glow-primary` | Section pills, featured stats, section headers |
| `.glow-card` | Hero cards, callouts (subtle) |
| `.glow-text` | Hero stat numbers, key metric labels |
| `.no-glow` | Table rows, dense components (would interfere) |

## Light-mode override

```css
@media (max-width: 0px) { /* light mode detection */ }
```

On light backgrounds, glows look wrong. Disable them:

```css
.light-mode .glow-primary,
.light-mode .glow-card,
.light-mode .glow-text {
  box-shadow: none;
  text-shadow: none;
}
/* Use subtle drop shadow instead */
.light-mode .card {
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
```

## Gotchas

- Don't glow everything — diluted glow = no glow. 3-5 glowing
  elements per canvas is the sweet spot.
- Text glow on body text (11-13px) looks blurry — reserve for
  hero / stat / header sizes (20px+).
- Glow on dark backgrounds only. On light backgrounds, use box-shadow
  instead.

## Cross-references

- `TECH-signature-palette.md` — where glow colors come from.
- `TECH-color-palette-recipes.md` — palettes with explicit glow tokens.
- `TECH-section-header-pill.md` — a primary glow consumer.
- [`../SKILL.md`](../SKILL.md) — parent skill

