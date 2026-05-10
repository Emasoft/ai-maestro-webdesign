---
name: TECH-uiux-font-pairings-catalog
category: uiux-font-pairing
source: SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH: Font-pairings catalog (57 heading+body combos)

## What it does

Ships 57 curated heading+body font pairings. Each pairing has:

- **Heading font** — serif, sans, display, or mono family
- **Body font** — complementary family selected for size-scale harmony
- **Google Fonts URL** — ready-to-paste `<link>` / `@import`
- **Mood/tone** — elegant / tech / editorial / friendly / luxurious / minimal / playful
- **Stack compatibility** — confirmed working in React, Next.js, Astro, Vue, etc.

## When to use

Fallback flow only (`ui-ux-reasoning`). When the user cannot name a font stack, this catalog supplies three candidates filtered against ai-slop. Pairings that include Inter, Roboto, Arial, or system-default stacks are pre-excluded because they trigger design-principles' slop rules.

Do NOT use when brand typography already exists (extracted via `design-extract` or provided by the user).

## How it works

```python
from uiuxpro import TypographyEngine
typography = TypographyEngine()

# By mood
pairing = typography.get_for_mood("elegant sophisticated")
# pairing.heading, pairing.body, pairing.google_url, pairing.css_import

# By stack
react_pairs = typography.get_for_stack("react")
```

Representative pairings (sample from 57):

| Tone | Heading | Body | Stack notes |
|---|---|---|---|
| Elegant | Cormorant Garamond | Montserrat | Luxury spa, beauty, editorial |
| Tech / editorial | IBM Plex Serif | IBM Plex Sans | Dev tools, fintech, data products |
| Warm minimalist | Fraunces | Inter Tight | Food, hospitality, design agencies |
| Editorial statement | Playfair Display | Source Sans 3 | Publications, portfolios |
| Geometric confident | Space Grotesk | Inter | SaaS, tech startups |
| Humanist soft | EB Garamond | Nunito | Wellness, non-profits |
| Monospace pro | JetBrains Mono | IBM Plex Sans | Developer tools, dashboards |
| Playful bold | Fredoka | Poppins | Kids products, entertainment |
| Neutral editorial | Manrope | Manrope | Modern utility apps |
| Retro-warm | Recoleta | DM Sans | Craft brands, boutique ecom |

Full set: 57 pairings covering serif/sans, display/body, tech/humanist, editorial/minimalist combinations.

## Minimal example

```python
pair = typography.get_for_mood("elegant sophisticated")
# pair.heading = "Cormorant Garamond"
# pair.body = "Montserrat"
# pair.google_url = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:..."
```

Resulting HTML:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Montserrat:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root {
    --font-heading: 'Cormorant Garamond', Georgia, serif;
    --font-body: 'Montserrat', system-ui, sans-serif;
  }
</style>
```

*Attributed to ui-ux-pro-max-skill — `SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md`.*

## Gotchas

- Some raw pairings contain `Inter` or `Roboto` on the body side — filter against the plugin's ai-slop list before proposing.
- Heading and body from the same superfamily (Inter + Inter, IBM Plex Serif + IBM Plex Sans) are fine and common — they count as a "pair" by design.
- Always confirm weight availability in Google Fonts — some families in the catalog only ship 4-5 weights, breaking the plugin's typography-system requirement of full weight coverage.
- `font-display: swap` is not in the catalog URLs; add it manually.

## Cross-references

- [TECH-uiux-rules-catalog](TECH-uiux-rules-catalog.md), [TECH-uiux-styles-catalog](TECH-uiux-styles-catalog.md), [TECH-uiux-palettes-catalog](TECH-uiux-palettes-catalog.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Top 10 distinctive rules — broken out as individual TECH files · Cross-references
- [typography-system](../../amw-design-principles/typography-system.md) — full weight coverage rule
  > I. Modular type scale · Default recommendation (Perfect Fourth, base = 16px) · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · Successful combinations · Failure modes · VI. Recommended font stacks (avoiding AI slop) · Latin · CJK / other scripts · Banned list (AI slop) · VII. Fallback-stack syntax
- [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) — Inter/Roboto filter
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- [SKILL](../SKILL.md)
