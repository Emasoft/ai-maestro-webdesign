---
name: TECH-77-font-strategy
category: typography
source: pretext-skills/amw-pretext-frontend-motion-main/core/bundle/references/font-strategy.md
also-in: SKILL-11.md, SKILL-23.md
---

# Font strategy for pretext (named families, load order, fallbacks)

**Category:** typography
**Status:** stable

## What it does

A project-level policy for which fonts pretext should measure against and how to avoid measurement drift. Core rules:
1. Always use named families — never `system-ui` (macOS Canvas/DOM drift).
2. Load fonts before the first `prepare()` (`document.fonts.ready`).
3. Keep the font string identical on both sides (pretext + renderer).
4. Cache prepared handles by `(text, font, options, locale)`.
5. For display type, prefer variable fonts with explicit `wght` / `wdth` axes pinned in the shorthand.

## When to use

- Every production pretext project
- Before the first `prepare()` call — set the strategy, don't improvise

## How it works

See rules above. The SKILL-11 "Anti-Patterns / Pretext" block reinforces this:
- Never use `system-ui` — macOS canvas/DOM diverge
- Never pure black `#000000` — off-blacks like `#06060a`, `#08080e`
- Never omit `document.fonts.ready.then(...)`

## Minimal example

```ts
// Source: pretext-frontend-motion-main/references/font-strategy.md (concept)
export const BODY_FONT = '18px/1.5 "Inter", sans-serif'
export const DISPLAY_FONT = 'bold 48px "Playfair Display", serif'
await document.fonts.ready
```

## Suggested font pairings by mood (source: pretext-frontend-motion-main/references/font-strategy.md)

| Mood | Display | Text |
|---|---|---|
| Editorial / literary | Cormorant Garamond, Playfair Display, Iowan Old Style | Source Serif 4, Georgia |
| Modern premium | Sora, Manrope | Inter, Source Sans 3 |
| Experimental poster | Space Grotesk, Archivo, Bebas Neue | IBM Plex Sans, IBM Plex Mono |
| Technical / ASCII / code-poetry | IBM Plex Mono, Geist Mono | Inter, IBM Plex Sans |
| Technical / lab white | Sora, IBM Plex Sans | IBM Plex Sans, Inter, Source Sans 3 |

Style-profile-specific advice:
- `editorial-paper`: display face can be visibly expressive; body face stays classical.
- `technical-lab-white`: avoid heavy serif display type; use mono sparingly for satellite labels only.
- `kinetic-dark-poster`: louder display face is fine; body must stay legible against motion backgrounds.

## Gotchas

- Google Fonts TTF CDN URLs return 404 for programmatic access (SKILL-11 anti-patterns) — use `@fontsource` via jsdelivr.
- `.woff2` is unsupported by opentype.js — if glyph paths are in the pipeline, load `.woff` or `.ttf`.

## Cross-references

- Related: TECH-17-font-loading-sync, TECH-18-font-string-parity
- API reference: [TECH-01-prepare-basics](TECH-01-prepare-basics.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
