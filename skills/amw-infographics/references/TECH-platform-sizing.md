---
name: TECH-platform-sizing
category: infographic-export
source: image-generation/create-infographics/resources/platform-sizes.md
also-in: image-generation/create-infographics/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [The size table](#the-size-table)
- [Safe zones per platform](#safe-zones-per-platform)
- [CSS — fixed-aspect platforms](#css-fixed-aspect-platforms)
- [Font size scaling by platform](#font-size-scaling-by-platform)
- [Density by format](#density-by-format)
- [Watermark / attribution per platform](#watermark-attribution-per-platform)
- [Export commands](#export-commands)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Platform sizing — Twitter, Instagram, LinkedIn, Pinterest

## What it does

Canvas size defaults by platform, with CSS overrides and
export-script width flags. Default is portrait-medium (1080×1440) —
the most common format (41% of 175 pieces).

## The size table

| Platform | Width | Height | Aspect | CSS pattern | `--width` |
|----------|-------|--------|--------|-------------|-----------|
| **Portrait-medium (default)** | 1080 | 1440 | 3:4 | `width:1080px; height:1440px; overflow:hidden` | 1080 |
| Twitter/X card | 1200 | 675 | 16:9 | `width:1200px; height:675px; overflow:hidden` | 1200 |
| Twitter/X portrait | 1080 | 1350 | 4:5 | `width:1080px; height:1350px` | 1080 |
| Instagram post | 1080 | 1080 | 1:1 | `width:1080px; height:1080px` | 1080 |
| Instagram portrait | 1080 | 1350 | 4:5 | `width:1080px; height:1350px` | 1080 |
| Instagram story / TikTok | 1080 | 1920 | 9:16 | `width:1080px; min-height:1920px` | 1080 |
| LinkedIn post | 1200 | 627 | ~2:1 | `width:1200px; height:627px` | 1200 |
| LinkedIn article | 1200 | 800 | 3:2 | `width:1200px; height:800px` | 1200 |
| Pinterest | 1000 | 1500 | 2:3 | `width:1000px; height:1500px` | 1000 |
| Website | 1100 | auto | flexible | `max-width:1100px` | 1100 |

## Safe zones per platform

| Platform | Inset |
|----------|-------|
| Twitter/X | 60px all sides (Twitter crops previews) |
| Instagram square | 48px all sides |
| Instagram story | 150px top + 250px bottom (UI chrome) |
| LinkedIn | 40px all sides |
| Print/A4 | 48px all sides |

## CSS — fixed-aspect platforms

```css
/* Twitter 16:9 fixed height */
.infographic {
  width: 1200px;
  height: 675px;
  overflow: hidden;   /* strict crop */
}

/* Story / TikTok canvas */
.infographic {
  width: 1080px;
  min-height: 1920px;
  padding: 150px 56px 250px;  /* safe zones */
}

/* Instagram square with mobile-boosted font */
.infographic {
  width: 1080px;
  height: 1080px;
  overflow: hidden;
  padding: 48px;
}
:root {
  --text-body: clamp(15px, 1.6vw, 18px);
  --text-caption: clamp(12px, 1.2vw, 14px);
}
```

## Font size scaling by platform

Default type scale is calibrated at **1100px width**. Scale factor:

| Platform | Width | Scale | `--text-body` override |
|----------|-------|-------|-----------------------|
| Pinterest | 1000px | 0.91× | `clamp(12px, 1.4vw, 14px)` |
| Default | 1100px | 1.0× | default |
| Twitter/LinkedIn | 1200px | 1.09× | auto-scales |
| Instagram (mobile) | 1080px | boost | `clamp(15px, 1.6vw, 18px)` |

## Density by format

```
Portrait-medium (1080×1440):  8–15 content blocks
Portrait-tall   (1080×1920): 12–20 content blocks
Landscape       (1200×675):   4–8  content blocks
Square          (1080×1080):  5–10 content blocks
```

## Watermark / attribution per platform

| Platform | Recommendation |
|----------|---------------|
| Twitter/X | Footer URL, small, bottom-left |
| Instagram | Semi-transparent watermark, bottom-right |
| LinkedIn | Footer with company handle + date |
| Pinterest | URL prominent in middle or footer |
| TikTok | Top-right watermark (bottom covered by UI) |

## Export commands

```bash
# source: image-generation/create-infographics/resources/platform-sizes.md

# Twitter 16:9
python scripts/export.py -i infographic.html -o output/twitter -f png --width 1200

# Instagram Square
python scripts/export.py -i infographic.html -o output/instagram -f png --width 1080

# Story / TikTok
python scripts/export.py -i infographic.html -o output/story -f png --width 1080

# LinkedIn
python scripts/export.py -i infographic.html -o output/linkedin -f png --width 1200

# Pinterest
python scripts/export.py -i infographic.html -o output/pinterest -f png --width 1000
```

## Gotchas

- Fixed-height formats (Twitter 16:9, Instagram square) must use
  `overflow: hidden` — content overflow gets cropped.
- Instagram story / TikTok need big top+bottom padding for UI
  chrome.
- Mobile-viewed formats (Instagram) need boosted font sizes —
  smaller screens, same viewing distance.

## Cross-references

- [TECH-export-pipeline](TECH-export-pipeline.md) — the export script.
  > What it does · When to use · Install · Basic invocation · With local server (recommended) · Width and scale · Per-platform widths · Wait-for-render helper · SVG export · Gotchas · Cross-references
- [TECH-design-brief](TECH-design-brief.md) — platform is Question 3 in the brief.
  > What it does · The 3 minimum questions · The 5 full-brief questions · Aesthetic direction mapping (Question 2) · Rules · Skip-brief defaults · Thesis extraction (from data) · Thesis formula · Tone → palette mapping · Audience sophistication → density · Gotchas · Cross-references
- [TECH-dense-editorial-dna](TECH-dense-editorial-dna.md) — density targets by format.
  > What it does · The success state · The failure mode · The Anti-Frontend Checklist (run before delivery) · Density targets by canvas · Spacing rules (THE signature) · Content format hierarchy (top = prefer) · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

