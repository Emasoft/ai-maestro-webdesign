---
name: TECH-uiux-palettes-catalog
category: uiux-palette
source: SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md
also-in:
---

# TECH: Color-palette catalog (161 industry-matched palettes)

## What it does

Ships 161 curated color palettes, each labeled by industry fit and emotional mood. Every palette slots five hex values into the plugin's five-role structure — primary, secondary, CTA, background, text — and carries:

- **Mood tag(s)** — calming / clinical / energetic / luxury / playful / bold / serene / trustworthy
- **Industry fit** — e.g. "medical clinic", "SaaS dashboard", "wellness spa"
- **Notes** — one-sentence explanation of what the palette communicates

## When to use

Fallback flow only. When `ui-ux-reasoning` is routed to and must return three palette candidates, this catalog is the source. Each candidate must be re-expressed in oklch (via `../../amw-design-principles/color-system.md`) before it reaches downstream output. Palettes that cannot be cleanly oklch-ified are dropped.

Do NOT use in the happy-path flow — there the brand tokens are already defined via `design-extract` or user input.

## How it works

```python
from uiuxpro import ColorEngine
colors = ColorEngine()

# By product type
palette = colors.get_for_product("medical clinic")
# palette.primary, palette.secondary, palette.cta, palette.background, palette.text, palette.notes

# By mood
calming = colors.get_by_mood("calming")
luxury = colors.get_by_mood("luxury")
```

Representative palettes (sample from the 161):

| Mood | Primary | Secondary | CTA | Background | Text | Industry fit |
|---|---|---|---|---|---|---|
| Clinical trust | `#2B7A9F` | `#E8F4FD` | `#0066CC` | `#FFFFFF` | `#1A2B3C` | Medical, healthcare |
| Luxury soft | `#E8B4B8` | `#A8D5BA` | `#D4AF37` | `#FFF5F5` | `#2D3436` | Wellness spa, beauty |
| Fintech trust | `#1A365D` | `#EDF2F7` | `#2F855A` | `#F7FAFC` | `#2D3748` | Fintech, banking |
| SaaS Indigo | `#6366F1` | `#EEF2FF` | `#8B5CF6` | `#FFFFFF` | `#1E1B4B` | SaaS dashboard |
| Warm dine | `#C53030` | `#FFF8F0` | `#DD6B20` | `#FDFCFB` | `#2D2015` | Restaurant, food |
| Editorial mono | `#0D0D0D` | `#F5F5F5` | `#B8860B` | `#FFFFFF` | `#1A1A1A` | Luxury ecom, publication |
| Calming sage | `#84A98C` | `#F1F6F1` | `#52796F` | `#FFFEFB` | `#354F52` | Wellness, mindfulness |

Full set: 161 palettes spanning every industry covered in `TECH-uiux-rules-catalog.md`.

## Minimal example

```python
ds = gen.generate(description="Luxury wellness spa booking site", stack="html")
print(ds.css_variables)
# :root {
#   --color-primary: #E8B4B8;
#   --color-secondary: #A8D5BA;
#   --color-cta: #D4AF37;
#   --color-background: #FFF5F5;
#   --color-text: #2D3436;
# }
```

*Attributed to ui-ux-pro-max-skill — `SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md`.*

## Gotchas

- Hex values in the raw catalog are sRGB — they must be converted to oklch (`../../amw-design-principles/color-system.md`) before entering the plugin's token pipeline.
- Some palettes include purple-pink gradients or neon accents that are on the ai-slop list. Filter before emission.
- Industry fit is a hint, not a constraint — a "clinical trust" palette can work for a B2B SaaS onboarding flow even though the catalog tags it for healthcare.
- Contrast is not guaranteed across all pairings. Always check `--background / --text` and `--cta / --background` against WCAG 4.5:1 before finalizing.

## Cross-references

- `TECH-uiux-rules-catalog.md` — rules that reference palette moods
- `TECH-uiux-styles-catalog.md` — styles that pair with palettes
- `../../amw-design-principles/color-system.md` — oklch structure all palettes conform to
- `../../amw-design-principles/ai-slop-avoid.md`
- `../SKILL.md`
