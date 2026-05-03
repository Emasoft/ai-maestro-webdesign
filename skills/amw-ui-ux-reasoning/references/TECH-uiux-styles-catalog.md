---
name: TECH-uiux-styles-catalog
category: uiux-style
source: SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Representative styles (partial list — full 67 are in the upstream corpus)](#representative-styles-partial-list-full-67-are-in-the-upstream-corpus)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: UI-styles catalog (67 named visual languages)

## What it does

Ships 67 named visual languages ("UI styles"), each with a four-field spec:

- **Keywords** — short phrases that describe the look ("frosted glass, transparency, depth" for Glassmorphism)
- **Best for** — industries / product types where the style actually works
- **CSS variables** — starter token set (primary colors, shadows, radii) to inherit
- **Tailwind config** — drop-in theme extension

## When to use

During the fallback flow when design-principles routes to `ui-ux-reasoning` and the agent needs to propose **three** style candidates screened against ai-slop. The catalog is also the target of the reasoning rules' `style_priority` field — a rule like "Fintech → Professional Minimalism, Data-Dense UI" references two entries from this catalog.

Skip when a brand anchor exists — the style choice is already made.

## How it works

Each style entry is queryable by name or keyword-similarity:

```python
from uiuxpro import StyleLibrary
styles = StyleLibrary()
glass = styles.get("Glassmorphism")
# glass.keywords, glass.best_for, glass.css_variables, glass.tailwind_config
```

## Representative styles (partial list — full 67 are in the upstream corpus)

| Style | Keywords | Best for |
|---|---|---|
| Glassmorphism | frosted glass, transparency, depth, backdrop blur | SaaS dashboards, tech products, overlays |
| Brutalism | raw, unstyled, exposed grid, monospace, high contrast | Dev tools, portfolios, editorial |
| Neumorphism | soft shadows, tactile surfaces, embossed | Calm products, wellness, non-critical UI |
| Claymorphism | pillowy, soft, rounded, friendly colors | Consumer apps, kids products, casual |
| Bento Grid | modular tiles, card-based, dense info, consistent radii | Dashboards, Apple-style product pages |
| Editorial | magazine-grid, large type, generous whitespace | Luxury ecom, publications, portfolios |
| Swiss Minimalism | grid-strict, mono-ink, rhythmic type | Design agencies, corporate |
| Maximalist | busy, layered, color-riot | Fashion, entertainment, creative agencies |
| Skeuomorphic | real-world textures, dials, knobs | Audio products, niche hobby apps |
| Material Design | elevation system, Roboto-era, FAB pattern | Android-first, utility apps |
| Flat Design | no shadows, color blocks, generous margin | Early-web nostalgia, budget brand |
| Dark Mode Pro | oklch-deep, cyan accents, monospace numerals | Dev tools, crypto, terminals |
| AI-Native UI | chat bubbles, gradient accents, shimmer loaders | AI products, agents |
| Soft UI | gentle pastels, soft shadows, generous radius | Wellness, spa, beauty |
| Data-Dense UI | compact rows, tabular-nums, micro-type | Finance, analytics, ops |
| Retro 90s | pixel edges, neon, solid shadows | Entertainment, nostalgia campaigns |
| Y2K / Frutiger Aero | chrome, aqua, glossy gradient | Experimental / fashion / music |
| Vaporwave | pink/cyan, VHS lines, geometric grids | Music / entertainment / art |
| Cyberpunk | neon on black, mono + sans, HUD overlays | Gaming, crypto edge cases |
| Warm Minimalism | cream surfaces, earth palette, serif headlines | Food, craft, hospitality |

Full set: 67 styles — the upstream library provides CSS-variable + Tailwind-config stubs for each.

## Minimal example

```python
from uiuxpro import StyleLibrary
styles = StyleLibrary()

# All 67
all_styles = styles.list_all()

# Keyword search
candidates = styles.search("glass transparent blur")
# Returns: Glassmorphism, Frosted Depth, Translucent Material

# Get full spec
gm = styles.get("Glassmorphism")
print(gm.css_variables)
print(gm.tailwind_config)
```

*Attributed to ui-ux-pro-max-skill — `SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md`.*

## Gotchas

- Some styles in the raw catalog are ai-slop adjacent (purple-pink gradient AI-Native templates, rainbow Maximalist). Always filter against [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) before proposing.
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- "Best for" is permissive — it lists industries where the style CAN work, not where it SHOULD be the default. Cross-check against the reasoning rule for the target industry.
- The catalog is upstream-sourced and the plugin does not vendor the raw data. Use the upstream CLI or upstream Python API to browse; treat this file as conceptual reference.

## Cross-references

- [TECH-uiux-rules-catalog](TECH-uiux-rules-catalog.md) — 161 industry rules that reference this catalog
  > What it does · When to use · How it works · Minimal example · Gotchas · Top 10 distinctive rules — broken out as individual TECH files · Cross-references
- [TECH-uiux-palettes-catalog](TECH-uiux-palettes-catalog.md), [TECH-uiux-font-pairings-catalog](TECH-uiux-font-pairings-catalog.md), [TECH-uiux-lp-patterns-catalog](TECH-uiux-lp-patterns-catalog.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
- [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md)
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
