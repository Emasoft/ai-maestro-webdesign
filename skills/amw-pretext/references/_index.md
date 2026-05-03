---
name: pretext-tech-index
purpose: Full per-technique catalog for amw-pretext. Read this when you need the explicit one-line description of every TECH-NN file. SKILL.md links here directly.
---

# Pretext — Full Technique Catalog (78 entries)

> **Routing back:** [SKILL](../SKILL.md) · [Decision guide TECH-72](TECH-72-use-pretext-decision-guide.md)

## Table of Contents

- API functions (TECH-01 — TECH-13)
- Measurement prerequisites (TECH-14 — TECH-18)
- Layout patterns / obstacle routing (TECH-19 — TECH-31)
- Typography techniques (TECH-32 — TECH-44)
- Motion / interactive demos (TECH-45 — TECH-55)
- Tables (TECH-56 — TECH-58)
- Integration patterns (TECH-59 — TECH-66)
- Workflow assemblies (TECH-67 — TECH-71)
- Consult / decision-routing (TECH-72 — TECH-78)
- Cross-references

This catalog mirrors every `TECH-NN-<slug>.md` file in `./` with its
one-line description and shared TOC fingerprint. Use the decision tree in
[SKILL.md](../SKILL.md) to pick the right TECH file; this index exists for
direct lookup when you already know the technique number or slug.

All TECH files share the same TOC structure unless noted:
> What it does · When to use · How it works · Minimal example · Gotchas · Cross-references

## API functions (TECH-01 — TECH-13)

- [TECH-01-prepare-basics.md](TECH-01-prepare-basics.md) — `prepare()` — one-time text analysis (TOC adds: Configuration options · source: pretext-skill-master/SKILL.md)
- [TECH-02-prepare-with-segments.md](TECH-02-prepare-with-segments.md) — `prepareWithSegments()` — richer handle for line-level access (TOC adds: TypeScript types)
- [TECH-03-layout.md](TECH-03-layout.md) — `layout()` — fast height + line count (TOC adds: Return value)
- [TECH-04-layout-with-lines.md](TECH-04-layout-with-lines.md) — `layoutWithLines()` — materialize all lines at a fixed width (TOC adds: Return types)
- [TECH-05-layout-next-line.md](TECH-05-layout-next-line.md) — `layoutNextLine()` — iterator with variable width per line
- [TECH-06-walk-line-ranges.md](TECH-06-walk-line-ranges.md) — `walkLineRanges()` — geometry-only line iteration (no string allocation)
- [TECH-07-measure-line-stats.md](TECH-07-measure-line-stats.md) — `measureLineStats()` — aggregate line stats without string alloc
- [TECH-08-measure-natural-width.md](TECH-08-measure-natural-width.md) — `measureNaturalWidth()` — unconstrained text width
- [TECH-09-layout-next-line-range.md](TECH-09-layout-next-line-range.md) — `layoutNextLineRange()` + `materializeLineRange()` — variable-width iterator without strings (TOC adds: Return type)
- [TECH-10-clear-cache.md](TECH-10-clear-cache.md) — `clearCache()` — release global measurement cache
- [TECH-11-set-locale.md](TECH-11-set-locale.md) — `setLocale()` — global Intl.Segmenter locale override
- [TECH-12-profile-prepare.md](TECH-12-profile-prepare.md) — `profilePrepare()` — diagnostic timing breakdown
- [TECH-13-rich-inline.md](TECH-13-rich-inline.md) — `prepareRichInline()` — mixed-font inline flow (chips, mentions, code spans)

## Measurement prerequisites (TECH-14 — TECH-18)

- [TECH-14-dom-free-height.md](TECH-14-dom-free-height.md) — DOM-free paragraph height (the core pretext win)
- [TECH-15-textarea-prewrap.md](TECH-15-textarea-prewrap.md) — Textarea-compatible measurement (`whiteSpace: pre-wrap`)
- [TECH-16-cjk-keep-all.md](TECH-16-cjk-keep-all.md) — CJK keep-all word-break
- [TECH-17-font-loading-sync.md](TECH-17-font-loading-sync.md) — Font-loading sync point before `prepare()`
- [TECH-18-font-string-parity.md](TECH-18-font-string-parity.md) — Font-string parity between pretext and renderer

## Layout patterns / obstacle routing (TECH-19 — TECH-31)

- [TECH-19-shaped-container.md](TECH-19-shaped-container.md) — Shaped container (text inside a circle / polygon / outline)
- [TECH-20-polygon-obstacle-mask.md](TECH-20-polygon-obstacle-mask.md) — Polygon / obstacle mask routing
- [TECH-21-multi-column-handoff.md](TECH-21-multi-column-handoff.md) — Multi-column text handoff
- [TECH-22-text-around-floated-image.md](TECH-22-text-around-floated-image.md) — Text flowing around a floated image
- [TECH-23-animated-obstacle-reflow.md](TECH-23-animated-obstacle-reflow.md) — 60 fps text reflow around animated obstacles
- [TECH-24-carve-text-line-slots.md](TECH-24-carve-text-line-slots.md) — `carveTextLineSlots` — fill both sides of a mid-line obstacle
- [TECH-25-shrinkwrap-width.md](TECH-25-shrinkwrap-width.md) — Shrink-wrap container width (tightest multiline width)
- [TECH-26-balanced-headline.md](TECH-26-balanced-headline.md) — Balanced headline (widow-free multiline titles)
- [TECH-27-auto-fit-font-size.md](TECH-27-auto-fit-font-size.md) — Auto-fit font size (largest font that stays within N lines)
- [TECH-28-tapering-font-size.md](TECH-28-tapering-font-size.md) — Tapering / variable font size (big first line → small tail)
- [TECH-29-line-clamp-truncate-readmore.md](TECH-29-line-clamp-truncate-readmore.md) — Exact-line truncate with "Read more"
- [TECH-30-layout-shift-prevention.md](TECH-30-layout-shift-prevention.md) — Prevent layout shift (CLS) on dynamic content
- [TECH-31-overflow-prediction.md](TECH-31-overflow-prediction.md) — Overflow prediction (will this button's label wrap?)

## Typography techniques (TECH-32 — TECH-44)

- [TECH-32-multilingual-bidi.md](TECH-32-multilingual-bidi.md) — Multilingual / bidi / emoji measurement (TOC adds: Recommended practices · QA checklist)
- [TECH-33-kinetic-width-animation.md](TECH-33-kinetic-width-animation.md) — Kinetic typography (text reflows as width animates)
- [TECH-34-wavy-baseline.md](TECH-34-wavy-baseline.md) — Wavy / curved baseline
- [TECH-35-text-on-path.md](TECH-35-text-on-path.md) — Text on a path (glyph-level placement along a curve)
- [TECH-36-generative-poster-grid.md](TECH-36-generative-poster-grid.md) — Generative poster / text-block grid
- [TECH-37-typographic-ascii.md](TECH-37-typographic-ascii.md) — Typographic ASCII art (proportional-width characters)
- [TECH-38-calligram-shape.md](TECH-38-calligram-shape.md) — Calligram (word rendered in the shape of what it describes)
- [TECH-39-glyph-mask-calligram.md](TECH-39-glyph-mask-calligram.md) — Glyph-mask calligram (big letter filled with small text)
- [TECH-40-letterbox-gallery.md](TECH-40-letterbox-gallery.md) — Letterbox gallery (each character its own filled canvas)
- [TECH-41-illuminated-manuscript.md](TECH-41-illuminated-manuscript.md) — Illuminated manuscript (medieval page with living ornaments)
- [TECH-42-variable-font-waves.md](TECH-42-variable-font-waves.md) — Variable-font per-character waves (weight / width ripples)
- [TECH-43-glyph-morphing.md](TECH-43-glyph-morphing.md) — Glyph morphing (interpolate letterforms A → Z)
- [TECH-44-outline-calligram.md](TECH-44-outline-calligram.md) — Outline calligram (text fills the exact contour of a glyph)

## Motion / interactive demos (TECH-45 — TECH-55)

- [TECH-45-accordion-heights.md](TECH-45-accordion-heights.md) — Accordion panel height (expand/collapse with known height)
- [TECH-46-chat-bubbles.md](TECH-46-chat-bubbles.md) — Tight multiline chat bubbles (Bubbles demo family)
- [TECH-47-dynamic-layout-routing.md](TECH-47-dynamic-layout-routing.md) — Dynamic layout — fixed-height editorial spread with routed text
- [TECH-48-editorial-engine.md](TECH-48-editorial-engine.md) — Editorial engine (live multi-column reflow around animated geometry)
- [TECH-49-justification-comparison.md](TECH-49-justification-comparison.md) — Justification comparison (width probing workflow)
- [TECH-50-cycling-text-autofit.md](TECH-50-cycling-text-autofit.md) — Cycling text with auto-fit (rotating headline reveals)
- [TECH-51-collapse-expand-filter.md](TECH-51-collapse-expand-filter.md) — Animated filter (CSS collapse/expand, NOT virtualization)
- [TECH-52-glyph-path-art.md](TECH-52-glyph-path-art.md) — Glyph path art (SVG letterforms with stroke-draw animation)
- [TECH-53-threejs-text-wrapping.md](TECH-53-threejs-text-wrapping.md) — Three.js — text wrapping around 3D objects
- [TECH-54-splat-editor.md](TECH-54-splat-editor.md) — Splat editor — text wrapping around Gaussian splats in real time
- [TECH-55-variable-ascii-canvas.md](TECH-55-variable-ascii-canvas.md) — Variable Typographic ASCII (Canvas glyph field anchored to measured lines)

## Tables (TECH-56 — TECH-58)

- [TECH-56-pretext-tables-virtualized.md](TECH-56-pretext-tables-virtualized.md) — Virtualized table with pretext-measured row heights
- [TECH-57-pretext-tables-resizable.md](TECH-57-pretext-tables-resizable.md) — Resizable table (column + row resize with scroll anchor)
- [TECH-58-pretext-tables-grid.md](TECH-58-pretext-tables-grid.md) — Grid table (CSS Grid layout with sticky headers)

## Integration patterns (TECH-59 — TECH-66)

- [TECH-59-react-hooks-integration.md](TECH-59-react-hooks-integration.md) — React hook integration (`useMemo` prepared handles)
- [TECH-60-svelte-islands-integration.md](TECH-60-svelte-islands-integration.md) — Svelte / Astro islands integration (`client:load`)
- [TECH-61-vanilla-ts.md](TECH-61-vanilla-ts.md) — Vanilla TypeScript integration (no framework)
- [TECH-62-ssr-node-canvas.md](TECH-62-ssr-node-canvas.md) — SSR / Node.js integration (node-canvas shim)
- [TECH-63-progressive-enhancement.md](TECH-63-progressive-enhancement.md) — Progressive enhancement (pretext as feature gate)
- [TECH-64-wrapper-module.md](TECH-64-wrapper-module.md) — Wrapper module (line-height conversion + null fallback)
- [TECH-65-vendoring-esm.md](TECH-65-vendoring-esm.md) — Vendoring pretext as a single ESM file (no build step)
- [TECH-66-resize-observer-pattern.md](TECH-66-resize-observer-pattern.md) — ResizeObserver pattern (re-layout, not re-prepare)

## Workflow assemblies (TECH-67 — TECH-71)

- [TECH-67-masonry-grid.md](TECH-67-masonry-grid.md) — Masonry grid (Pinterest-style variable card heights)
- [TECH-68-virtualized-list.md](TECH-68-virtualized-list.md) — Virtualized list with variable-height text rows
- [TECH-69-smartpage-a4-autofit.md](TECH-69-smartpage-a4-autofit.md) — SmartPage — auto-fit Markdown to one A4 page
- [TECH-70-streaming-ai-chat.md](TECH-70-streaming-ai-chat.md) — Streaming AI chat (measure tokens as they arrive)
- [TECH-71-auto-height-textarea.md](TECH-71-auto-height-textarea.md) — Auto-height textarea (pre-wrap, no scroll bar)

## Consult / decision-routing (TECH-72 — TECH-78)

- [TECH-72-use-pretext-decision-guide.md](TECH-72-use-pretext-decision-guide.md) — **Read first.** Decision guide — when to use pretext (and when NOT)
- [TECH-73-design-consultation-route.md](TECH-73-design-consultation-route.md) — Full-pipeline design consultation (gstack design-html)
- [TECH-74-dragon-text-reflow.md](TECH-74-dragon-text-reflow.md) — Dragon text reflow (text flowing around an 80-segment creature)
- [TECH-75-rich-note-atomic-pills.md](TECH-75-rich-note-atomic-pills.md) — Rich note (mixed inline fragments with atomic pills)
- [TECH-76-postext-mobile-port.md](TECH-76-postext-mobile-port.md) — postext — pretext port for React Native / mobile runtimes (TOC adds: Suggested font pairings by mood)
- [TECH-77-font-strategy.md](TECH-77-font-strategy.md) — Font strategy for pretext (named families, load order, fallbacks)
- [TECH-78-style-profiles.md](TECH-78-style-profiles.md) — Style profiles (pick ONE aesthetic per pretext output)

## Cross-references

- [SKILL.md](../SKILL.md) — orchestrator routing surface (decision tree, trigger phrases, completion checklist)
- [TECH-72-use-pretext-decision-guide.md](TECH-72-use-pretext-decision-guide.md) — when to use pretext (and when NOT)
- [TECH-77-font-strategy.md](TECH-77-font-strategy.md) — font strategy + load order
- [../../amw-design-principles/typography-system.md](../../amw-design-principles/typography-system.md) — broader typography rules pretext extends
