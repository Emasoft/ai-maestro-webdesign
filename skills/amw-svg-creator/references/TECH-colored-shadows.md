---
name: TECH-colored-shadows
category: svg-lighting
source: image-generation/svg-creator/SKILL.md
also-in: image-generation/svg-creator/references/advanced-techniques.md
---

# Colored shadows (never pure black)

## What it does

The single most common digital-illustration mistake is using pure
black (`#000`) or gray for shadows. Professional shadows carry a
cool-shifted hue — dark blue, purple, teal. This single change lifts
an SVG from "looks generated" to "looks illustrated".

## The palette

| Color | Hex | Best for |
|-------|-----|----------|
| Dark blue | `#1a1a4e` | Universal — warm subjects (skin, fire, organic) |
| Deep purple | `#2d1b4e` | Dramatic scenes, twilight, cool subjects |
| Teal | `#0d3b4f` | Water scenes, underwater, underside of cool objects |
| Deep navy | `#1e1b4b` | Drop shadows, cast shadows on warm-lit scenes |

**Never:** `#000`, `#111`, `#222`, `#333`, `gray`, `black`. These
read as holes in the image, not shadows.

## Where the color goes

- `<feFlood flood-color="#1e1b4b" flood-opacity="0.30"/>` in drop
  shadow filters.
- `<ellipse fill="#3b1764" opacity="0.2" style="mix-blend-mode:multiply"/>`
  for form shadows overlaid on a subject.
- Radial gradient shadow stops (`#7c2d12` → `#431407` in the
  five-zone model).

## Drop-shadow filter with colored shadow

```xml
<!-- source: image-generation/svg-creator/SKILL.md -->
<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"
  color-interpolation-filters="linearRGB">
  <feGaussianBlur in="SourceAlpha" stdDeviation="4" result="blur"/>
  <feOffset in="blur" dx="3" dy="5" result="offset"/>
  <feFlood flood-color="#1e1b4b" flood-opacity="0.30" result="color"/>
  <feComposite in="color" in2="offset" operator="in" result="shadow"/>
  <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
```

The `feFlood flood-color="#1e1b4b"` is the key line — classic
drop-shadow filters use `#000` here, which is the amateur mistake.

## Opacity rules

- Drop shadow: 0.25–0.35
- Contact shadow (tight under object): 0.35–0.45
- Cast shadow (large, soft): 0.15–0.25
- Form shadow (on subject, overlay): 0.15–0.25

## Gotchas

- If your scene has a warm light source (sunset, fire), pick blue
  shadows. If the light is cool (moon, twilight), pick warm
  shadows. Colored shadows are the complement of the light color.
- Over-saturating the shadow color (opacity > 0.50) cancels the
  subtlety — shadows should recede, not dominate.

## Cross-references

- `TECH-five-zone-lighting.md` — where shadows live in the bigger model.
- `TECH-drop-shadow-filter.md` — the full filter chain.
- `TECH-vignette-overlay.md` — scene-level darkening at edges.
- [`../SKILL.md`](../SKILL.md) — parent skill

