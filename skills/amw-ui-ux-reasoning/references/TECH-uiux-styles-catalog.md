---
name: TECH-uiux-styles-catalog
category: uiux-style
source: SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md
also-in:
---

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

- Some styles in the raw catalog are ai-slop adjacent (purple-pink gradient AI-Native templates, rainbow Maximalist). Always filter against `../../amw-design-principles/ai-slop-avoid.md` before proposing.
- "Best for" is permissive — it lists industries where the style CAN work, not where it SHOULD be the default. Cross-check against the reasoning rule for the target industry.
- The catalog is upstream-sourced and the plugin does not vendor the raw data. Use the upstream CLI or upstream Python API to browse; treat this file as conceptual reference.

## Cross-references

- `TECH-uiux-rules-catalog.md` — 161 industry rules that reference this catalog
- `TECH-uiux-palettes-catalog.md`, `TECH-uiux-font-pairings-catalog.md`, `TECH-uiux-lp-patterns-catalog.md`
- `../SKILL.md`
- `../../amw-design-principles/ai-slop-avoid.md`
