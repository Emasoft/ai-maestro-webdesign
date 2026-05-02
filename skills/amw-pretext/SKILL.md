---
name: amw-pretext
description: Pretext-driven typography, text measurement, layout, integration patterns, virtualized tables, ASCII-on-canvas, calligrams, and 3D/motion text — triggers on "pretext", "@chenglou/pretext", "text-on-path", "balanced headline", "shrink-wrap text", "virtualized list", "masonry", "text around obstacles", "kinetic typography", "auto-fit font", "DOM-free text", "pretext API". Does NOT claim generic design vocabulary — the orchestrator "design-principles" retains those triggers. Use when applying pretext-based typography, text measurement, or advanced layout techniques. Trigger with explicit "pretext" or "@chenglou/pretext" phrasing.
version: 0.1.0
---

# Pretext

> **Orchestrated by:** `../amw-design-principles/SKILL.md`. Do not activate for generic "make the type nice" requests — those stay in the base typography system. Activate only on the narrow triggers above.

## Overview

Precision text-layout engine for when CSS flow is insufficient. Wraps `@chenglou/pretext` — a headless, DOM-free text measurement library — across 78 technique files covering API functions, measurement prerequisites, layout patterns, obstacle-aware flow, kinetic typography, virtualized tables, 3D/motion text, integration patterns, and workflow assemblies. Routes each narrow trigger (shrink-wrap, text-on-path, balanced headline, virtualized list, etc.) to the matching TECH file. Output reuses existing project typography tokens; pretext never introduces new fonts or motion systems.

## Instructions

1. Walk the `## Technique selection` tree top-down to identify the matching technique category (API function, measurement prerequisite, layout pattern, obstacle routing, kinetic typography, virtualized tables, 3D/motion, integration, workflow assembly).
2. Open only the relevant `references/TECH-NN-<slug>.md` file — do not load the whole catalog.
3. Follow the TECH file's "How it works" section; call `prepare()` (or the appropriate pretext API function) exactly once before calling any layout function.
4. Reuse the project's existing typography tokens — do not introduce new fonts or motion systems; pretext exposes per-line metrics but does not own typographic decisions.
5. Handle the resize path explicitly: call `clearCache()` on font-change or after every `ResizeObserver` tick when measurement validity has changed.
6. Validate the font-string parity constraint (same CSS font string in both pretext and the renderer) before shipping; see `TECH-18-font-string-parity.md`.

See the `## How to use this skill` section below for the authoritative step-by-step decision workflow, and the `## Technique selection` tree to pick the relevant TECH reference file.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during **Phase B** when the approved design requires precision text layout beyond what CSS flow provides (virtualization, shrink-wrap, obstacle-aware flow, kinetic typography). Also callable directly when the user explicitly names `pretext` or its API.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT. Pretext is the precision text-layout engine the plugin reaches for when CSS flow is insufficient (variable-height virtualization, shrink-wrap bubbles, obstacle-aware editorial flow, kinetic typography, auto-fit font search). All pretext-powered output must reuse the project's existing typography tokens — pretext does NOT introduce new fonts or motion systems, it just exposes the per-line metrics.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `pretext` is the user asking about?
  - **01** (1 techniques)
    - [TECH-01-prepare-basics](./references/TECH-01-prepare-basics.md) — prepare() — one-time text analysis
  - **02** (1 techniques)
    - [TECH-02-prepare-with-segments](./references/TECH-02-prepare-with-segments.md) — prepareWithSegments() — richer handle for line-level access
  - **03** (1 techniques)
    - [TECH-03-layout](./references/TECH-03-layout.md) — layout() — fast height + line count
  - **04** (1 techniques)
    - [TECH-04-layout-with-lines](./references/TECH-04-layout-with-lines.md) — layoutWithLines() — materialize all lines at a fixed width
  - **05** (1 techniques)
    - [TECH-05-layout-next-line](./references/TECH-05-layout-next-line.md) — layoutNextLine() — iterator with variable width per line
  - **06** (1 techniques)
    - [TECH-06-walk-line-ranges](./references/TECH-06-walk-line-ranges.md) — walkLineRanges() — geometry-only line iteration (no string allocation)
  - **07** (1 techniques)
    - [TECH-07-measure-line-stats](./references/TECH-07-measure-line-stats.md) — measureLineStats() — aggregate line stats without string alloc
  - **08** (1 techniques)
    - [TECH-08-measure-natural-width](./references/TECH-08-measure-natural-width.md) — measureNaturalWidth() — unconstrained text width
  - **09** (1 techniques)
    - [TECH-09-layout-next-line-range](./references/TECH-09-layout-next-line-range.md) — layoutNextLineRange() + materializeLineRange() — variable-width iterat
  - **10** (1 techniques)
    - [TECH-10-clear-cache](./references/TECH-10-clear-cache.md) — clearCache() — release global measurement cache
  - **11** (1 techniques)
    - [TECH-11-set-locale](./references/TECH-11-set-locale.md) — setLocale() — global Intl.Segmenter locale override
  - **12** (1 techniques)
    - [TECH-12-profile-prepare](./references/TECH-12-profile-prepare.md) — profilePrepare() — diagnostic timing breakdown
  - **13** (1 techniques)
    - [TECH-13-rich-inline](./references/TECH-13-rich-inline.md) — prepareRichInline() — mixed-font inline flow (chips, mentions, code sp
  - **14** (1 techniques)
    - [TECH-14-dom-free-height](./references/TECH-14-dom-free-height.md) — DOM-free paragraph height (the core pretext win)
  - **15** (1 techniques)
    - [TECH-15-textarea-prewrap](./references/TECH-15-textarea-prewrap.md) — Textarea-compatible measurement (whiteSpace: pre-wrap)
  - **16** (1 techniques)
    - [TECH-16-cjk-keep-all](./references/TECH-16-cjk-keep-all.md) — CJK keep-all word-break
  - **17** (1 techniques)
    - [TECH-17-font-loading-sync](./references/TECH-17-font-loading-sync.md) — Font-loading sync point before prepare()
  - **18** (1 techniques)
    - [TECH-18-font-string-parity](./references/TECH-18-font-string-parity.md) — Font-string parity between pretext and renderer
  - **19** (1 techniques)
    - [TECH-19-shaped-container](./references/TECH-19-shaped-container.md) — Shaped container (text inside a circle / polygon / outline)
  - **20** (1 techniques)
    - [TECH-20-polygon-obstacle-mask](./references/TECH-20-polygon-obstacle-mask.md) — Polygon / obstacle mask routing
  - **21** (1 techniques)
    - [TECH-21-multi-column-handoff](./references/TECH-21-multi-column-handoff.md) — Multi-column text handoff
  - **22** (1 techniques)
    - [TECH-22-text-around-floated-image](./references/TECH-22-text-around-floated-image.md) — Text flowing around a floated image
  - **23** (1 techniques)
    - [TECH-23-animated-obstacle-reflow](./references/TECH-23-animated-obstacle-reflow.md) — 60 fps text reflow around animated obstacles
  - **24** (1 techniques)
    - [TECH-24-carve-text-line-slots](./references/TECH-24-carve-text-line-slots.md) — carveTextLineSlots — fill both sides of a mid-line obstacle
  - **25** (1 techniques)
    - [TECH-25-shrinkwrap-width](./references/TECH-25-shrinkwrap-width.md) — Shrink-wrap container width (tightest multiline width)
  - **26** (1 techniques)
    - [TECH-26-balanced-headline](./references/TECH-26-balanced-headline.md) — Balanced headline (widow-free multiline titles)
  - **27** (1 techniques)
    - [TECH-27-auto-fit-font-size](./references/TECH-27-auto-fit-font-size.md) — Auto-fit font size (largest font that stays within N lines)
  - **28** (1 techniques)
    - [TECH-28-tapering-font-size](./references/TECH-28-tapering-font-size.md) — Tapering / variable font size (big first line → small tail)
  - **29** (1 techniques)
    - [TECH-29-line-clamp-truncate-readmore](./references/TECH-29-line-clamp-truncate-readmore.md) — Exact-line truncate with "Read more"
  - **30** (1 techniques)
    - [TECH-30-layout-shift-prevention](./references/TECH-30-layout-shift-prevention.md) — Prevent layout shift (CLS) on dynamic content
  - **31** (1 techniques)
    - [TECH-31-overflow-prediction](./references/TECH-31-overflow-prediction.md) — Overflow prediction (will this button's label wrap?)
  - **32** (1 techniques)
    - [TECH-32-multilingual-bidi](./references/TECH-32-multilingual-bidi.md) — Multilingual / bidi / emoji measurement
  - **33** (1 techniques)
    - [TECH-33-kinetic-width-animation](./references/TECH-33-kinetic-width-animation.md) — Kinetic typography (text reflows as width animates)
  - **34** (1 techniques)
    - [TECH-34-wavy-baseline](./references/TECH-34-wavy-baseline.md) — Wavy / curved baseline
  - **35** (1 techniques)
    - [TECH-35-text-on-path](./references/TECH-35-text-on-path.md) — Text on a path (glyph-level placement along a curve)
  - **36** (1 techniques)
    - [TECH-36-generative-poster-grid](./references/TECH-36-generative-poster-grid.md) — Generative poster / text-block grid
  - **37** (1 techniques)
    - [TECH-37-typographic-ascii](./references/TECH-37-typographic-ascii.md) — Typographic ASCII art (proportional-width characters)
  - **38** (1 techniques)
    - [TECH-38-calligram-shape](./references/TECH-38-calligram-shape.md) — Calligram (word rendered in the shape of what it describes)
  - **39** (1 techniques)
    - [TECH-39-glyph-mask-calligram](./references/TECH-39-glyph-mask-calligram.md) — Glyph-mask calligram (big letter filled with small text)
  - **40** (1 techniques)
    - [TECH-40-letterbox-gallery](./references/TECH-40-letterbox-gallery.md) — Letterbox gallery (each character its own filled canvas)
  - **41** (1 techniques)
    - [TECH-41-illuminated-manuscript](./references/TECH-41-illuminated-manuscript.md) — Illuminated manuscript (medieval page with living ornaments)
  - **42** (1 techniques)
    - [TECH-42-variable-font-waves](./references/TECH-42-variable-font-waves.md) — Variable-font per-character waves (weight / width ripples)
  - **43** (1 techniques)
    - [TECH-43-glyph-morphing](./references/TECH-43-glyph-morphing.md) — Glyph morphing (interpolate letterforms A → Z)
  - **44** (1 techniques)
    - [TECH-44-outline-calligram](./references/TECH-44-outline-calligram.md) — Outline calligram (text fills the exact contour of a glyph)
  - **45** (1 techniques)
    - [TECH-45-accordion-heights](./references/TECH-45-accordion-heights.md) — Accordion panel height (expand/collapse with known height)
  - **46** (1 techniques)
    - [TECH-46-chat-bubbles](./references/TECH-46-chat-bubbles.md) — Tight multiline chat bubbles (Bubbles demo family)
  - **47** (1 techniques)
    - [TECH-47-dynamic-layout-routing](./references/TECH-47-dynamic-layout-routing.md) — Dynamic layout — fixed-height editorial spread with routed text
  - **48** (1 techniques)
    - [TECH-48-editorial-engine](./references/TECH-48-editorial-engine.md) — Editorial engine (live multi-column reflow around animated geometry)
  - **49** (1 techniques)
    - [TECH-49-justification-comparison](./references/TECH-49-justification-comparison.md) — Justification comparison (width probing workflow)
  - **50** (1 techniques)
    - [TECH-50-cycling-text-autofit](./references/TECH-50-cycling-text-autofit.md) — Cycling text with auto-fit (rotating headline reveals)
  - **51** (1 techniques)
    - [TECH-51-collapse-expand-filter](./references/TECH-51-collapse-expand-filter.md) — Animated filter (CSS collapse/expand, NOT virtualization)
  - **52** (1 techniques)
    - [TECH-52-glyph-path-art](./references/TECH-52-glyph-path-art.md) — Glyph path art (SVG letterforms with stroke-draw animation)
  - **53** (1 techniques)
    - [TECH-53-threejs-text-wrapping](./references/TECH-53-threejs-text-wrapping.md) — Three.js — text wrapping around 3D objects
  - **54** (1 techniques)
    - [TECH-54-splat-editor](./references/TECH-54-splat-editor.md) — Splat editor — text wrapping around Gaussian splats in real time
  - **55** (1 techniques)
    - [TECH-55-variable-ascii-canvas](./references/TECH-55-variable-ascii-canvas.md) — Variable Typographic ASCII (Canvas glyph field anchored to measured li
  - **56** (1 techniques)
    - [TECH-56-pretext-tables-virtualized](./references/TECH-56-pretext-tables-virtualized.md) — Virtualized table with pretext-measured row heights
  - **57** (1 techniques)
    - [TECH-57-pretext-tables-resizable](./references/TECH-57-pretext-tables-resizable.md) — Resizable table (column + row resize with scroll anchor)
  - **58** (1 techniques)
    - [TECH-58-pretext-tables-grid](./references/TECH-58-pretext-tables-grid.md) — Grid table (CSS Grid layout with sticky headers)
  - **59** (1 techniques)
    - [TECH-59-react-hooks-integration](./references/TECH-59-react-hooks-integration.md) — React hook integration (useMemo prepared handles)
  - **60** (1 techniques)
    - [TECH-60-svelte-islands-integration](./references/TECH-60-svelte-islands-integration.md) — Svelte / Astro islands integration (client:load)
  - **61** (1 techniques)
    - [TECH-61-vanilla-ts](./references/TECH-61-vanilla-ts.md) — Vanilla TypeScript integration (no framework)
  - **62** (1 techniques)
    - [TECH-62-ssr-node-canvas](./references/TECH-62-ssr-node-canvas.md) — SSR / Node.js integration (node-canvas shim)
  - **63** (1 techniques)
    - [TECH-63-progressive-enhancement](./references/TECH-63-progressive-enhancement.md) — Progressive enhancement (pretext as feature gate)
  - **64** (1 techniques)
    - [TECH-64-wrapper-module](./references/TECH-64-wrapper-module.md) — Wrapper module (line-height conversion + null fallback)
  - **65** (1 techniques)
    - [TECH-65-vendoring-esm](./references/TECH-65-vendoring-esm.md) — Vendoring pretext as a single ESM file (no build step)
  - **66** (1 techniques)
    - [TECH-66-resize-observer-pattern](./references/TECH-66-resize-observer-pattern.md) — ResizeObserver pattern (re-layout, not re-prepare)
  - **67** (1 techniques)
    - [TECH-67-masonry-grid](./references/TECH-67-masonry-grid.md) — Masonry grid (Pinterest-style variable card heights)
  - **68** (1 techniques)
    - [TECH-68-virtualized-list](./references/TECH-68-virtualized-list.md) — Virtualized list with variable-height text rows
  - **69** (1 techniques)
    - [TECH-69-smartpage-a4-autofit](./references/TECH-69-smartpage-a4-autofit.md) — SmartPage — auto-fit Markdown to one A4 page
  - **70** (1 techniques)
    - [TECH-70-streaming-ai-chat](./references/TECH-70-streaming-ai-chat.md) — Streaming AI chat (measure tokens as they arrive)
  - **71** (1 techniques)
    - [TECH-71-auto-height-textarea](./references/TECH-71-auto-height-textarea.md) — Auto-height textarea (pre-wrap, no scroll bar)
  - **72** (1 techniques)
    - [TECH-72-use-pretext-decision-guide](./references/TECH-72-use-pretext-decision-guide.md) — Decision guide — when to use pretext (and when NOT)
  - **73** (1 techniques)
    - [TECH-73-design-consultation-route](./references/TECH-73-design-consultation-route.md) — Full-pipeline design consultation (gstack design-html)
  - **74** (1 techniques)
    - [TECH-74-dragon-text-reflow](./references/TECH-74-dragon-text-reflow.md) — Dragon text reflow (text flowing around an 80-segment creature)
  - **75** (1 techniques)
    - [TECH-75-rich-note-atomic-pills](./references/TECH-75-rich-note-atomic-pills.md) — Rich note (mixed inline fragments with atomic pills)
  - **76** (1 techniques)
    - [TECH-76-postext-mobile-port](./references/TECH-76-postext-mobile-port.md) — postext — pretext port for React Native / mobile runtimes
  - **77** (1 techniques)
    - [TECH-77-font-strategy](./references/TECH-77-font-strategy.md) — Font strategy for pretext (named families, load order, fallbacks)
  - **78** (1 techniques)
    - [TECH-78-style-profiles](./references/TECH-78-style-profiles.md) — Style profiles (pick ONE aesthetic per pretext output)

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-01-prepare-basics.md](./references/TECH-01-prepare-basics.md)**
  - Description: prepare() — one-time text analysis
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-02-prepare-with-segments.md](./references/TECH-02-prepare-with-segments.md)**
  - Description: prepareWithSegments() — richer handle for line-level access
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-03-layout.md](./references/TECH-03-layout.md)**
  - Description: layout() — fast height + line count
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-04-layout-with-lines.md](./references/TECH-04-layout-with-lines.md)**
  - Description: layoutWithLines() — materialize all lines at a fixed width
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-05-layout-next-line.md](./references/TECH-05-layout-next-line.md)**
  - Description: layoutNextLine() — iterator with variable width per line
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-06-walk-line-ranges.md](./references/TECH-06-walk-line-ranges.md)**
  - Description: walkLineRanges() — geometry-only line iteration (no string allocation)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-07-measure-line-stats.md](./references/TECH-07-measure-line-stats.md)**
  - Description: measureLineStats() — aggregate line stats without string alloc
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-08-measure-natural-width.md](./references/TECH-08-measure-natural-width.md)**
  - Description: measureNaturalWidth() — unconstrained text width
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-09-layout-next-line-range.md](./references/TECH-09-layout-next-line-range.md)**
  - Description: layoutNextLineRange() + materializeLineRange() — variable-width iterator without strings
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-10-clear-cache.md](./references/TECH-10-clear-cache.md)**
  - Description: clearCache() — release global measurement cache
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-11-set-locale.md](./references/TECH-11-set-locale.md)**
  - Description: setLocale() — global Intl.Segmenter locale override
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-12-profile-prepare.md](./references/TECH-12-profile-prepare.md)**
  - Description: profilePrepare() — diagnostic timing breakdown
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-13-rich-inline.md](./references/TECH-13-rich-inline.md)**
  - Description: prepareRichInline() — mixed-font inline flow (chips, mentions, code spans)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-14-dom-free-height.md](./references/TECH-14-dom-free-height.md)**
  - Description: DOM-free paragraph height (the core pretext win)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-15-textarea-prewrap.md](./references/TECH-15-textarea-prewrap.md)**
  - Description: Textarea-compatible measurement (whiteSpace: pre-wrap)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-16-cjk-keep-all.md](./references/TECH-16-cjk-keep-all.md)**
  - Description: CJK keep-all word-break
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-17-font-loading-sync.md](./references/TECH-17-font-loading-sync.md)**
  - Description: Font-loading sync point before prepare()
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-18-font-string-parity.md](./references/TECH-18-font-string-parity.md)**
  - Description: Font-string parity between pretext and renderer
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-19-shaped-container.md](./references/TECH-19-shaped-container.md)**
  - Description: Shaped container (text inside a circle / polygon / outline)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-20-polygon-obstacle-mask.md](./references/TECH-20-polygon-obstacle-mask.md)**
  - Description: Polygon / obstacle mask routing
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-21-multi-column-handoff.md](./references/TECH-21-multi-column-handoff.md)**
  - Description: Multi-column text handoff
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-22-text-around-floated-image.md](./references/TECH-22-text-around-floated-image.md)**
  - Description: Text flowing around a floated image
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-23-animated-obstacle-reflow.md](./references/TECH-23-animated-obstacle-reflow.md)**
  - Description: 60 fps text reflow around animated obstacles
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-24-carve-text-line-slots.md](./references/TECH-24-carve-text-line-slots.md)**
  - Description: carveTextLineSlots — fill both sides of a mid-line obstacle
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-25-shrinkwrap-width.md](./references/TECH-25-shrinkwrap-width.md)**
  - Description: Shrink-wrap container width (tightest multiline width)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-26-balanced-headline.md](./references/TECH-26-balanced-headline.md)**
  - Description: Balanced headline (widow-free multiline titles)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-27-auto-fit-font-size.md](./references/TECH-27-auto-fit-font-size.md)**
  - Description: Auto-fit font size (largest font that stays within N lines)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-28-tapering-font-size.md](./references/TECH-28-tapering-font-size.md)**
  - Description: Tapering / variable font size (big first line → small tail)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-29-line-clamp-truncate-readmore.md](./references/TECH-29-line-clamp-truncate-readmore.md)**
  - Description: Exact-line truncate with "Read more"
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-30-layout-shift-prevention.md](./references/TECH-30-layout-shift-prevention.md)**
  - Description: Prevent layout shift (CLS) on dynamic content
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-31-overflow-prediction.md](./references/TECH-31-overflow-prediction.md)**
  - Description: Overflow prediction (will this button's label wrap?)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-32-multilingual-bidi.md](./references/TECH-32-multilingual-bidi.md)**
  - Description: Multilingual / bidi / emoji measurement
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-33-kinetic-width-animation.md](./references/TECH-33-kinetic-width-animation.md)**
  - Description: Kinetic typography (text reflows as width animates)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-34-wavy-baseline.md](./references/TECH-34-wavy-baseline.md)**
  - Description: Wavy / curved baseline
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-35-text-on-path.md](./references/TECH-35-text-on-path.md)**
  - Description: Text on a path (glyph-level placement along a curve)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-36-generative-poster-grid.md](./references/TECH-36-generative-poster-grid.md)**
  - Description: Generative poster / text-block grid
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-37-typographic-ascii.md](./references/TECH-37-typographic-ascii.md)**
  - Description: Typographic ASCII art (proportional-width characters)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-38-calligram-shape.md](./references/TECH-38-calligram-shape.md)**
  - Description: Calligram (word rendered in the shape of what it describes)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-39-glyph-mask-calligram.md](./references/TECH-39-glyph-mask-calligram.md)**
  - Description: Glyph-mask calligram (big letter filled with small text)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-40-letterbox-gallery.md](./references/TECH-40-letterbox-gallery.md)**
  - Description: Letterbox gallery (each character its own filled canvas)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-41-illuminated-manuscript.md](./references/TECH-41-illuminated-manuscript.md)**
  - Description: Illuminated manuscript (medieval page with living ornaments)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-42-variable-font-waves.md](./references/TECH-42-variable-font-waves.md)**
  - Description: Variable-font per-character waves (weight / width ripples)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-43-glyph-morphing.md](./references/TECH-43-glyph-morphing.md)**
  - Description: Glyph morphing (interpolate letterforms A → Z)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-44-outline-calligram.md](./references/TECH-44-outline-calligram.md)**
  - Description: Outline calligram (text fills the exact contour of a glyph)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-45-accordion-heights.md](./references/TECH-45-accordion-heights.md)**
  - Description: Accordion panel height (expand/collapse with known height)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-46-chat-bubbles.md](./references/TECH-46-chat-bubbles.md)**
  - Description: Tight multiline chat bubbles (Bubbles demo family)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-47-dynamic-layout-routing.md](./references/TECH-47-dynamic-layout-routing.md)**
  - Description: Dynamic layout — fixed-height editorial spread with routed text
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-48-editorial-engine.md](./references/TECH-48-editorial-engine.md)**
  - Description: Editorial engine (live multi-column reflow around animated geometry)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-49-justification-comparison.md](./references/TECH-49-justification-comparison.md)**
  - Description: Justification comparison (width probing workflow)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-50-cycling-text-autofit.md](./references/TECH-50-cycling-text-autofit.md)**
  - Description: Cycling text with auto-fit (rotating headline reveals)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-51-collapse-expand-filter.md](./references/TECH-51-collapse-expand-filter.md)**
  - Description: Animated filter (CSS collapse/expand, NOT virtualization)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-52-glyph-path-art.md](./references/TECH-52-glyph-path-art.md)**
  - Description: Glyph path art (SVG letterforms with stroke-draw animation)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-53-threejs-text-wrapping.md](./references/TECH-53-threejs-text-wrapping.md)**
  - Description: Three.js — text wrapping around 3D objects
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-54-splat-editor.md](./references/TECH-54-splat-editor.md)**
  - Description: Splat editor — text wrapping around Gaussian splats in real time
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-55-variable-ascii-canvas.md](./references/TECH-55-variable-ascii-canvas.md)**
  - Description: Variable Typographic ASCII (Canvas glyph field anchored to measured lines)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-56-pretext-tables-virtualized.md](./references/TECH-56-pretext-tables-virtualized.md)**
  - Description: Virtualized table with pretext-measured row heights
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-57-pretext-tables-resizable.md](./references/TECH-57-pretext-tables-resizable.md)**
  - Description: Resizable table (column + row resize with scroll anchor)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-58-pretext-tables-grid.md](./references/TECH-58-pretext-tables-grid.md)**
  - Description: Grid table (CSS Grid layout with sticky headers)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-59-react-hooks-integration.md](./references/TECH-59-react-hooks-integration.md)**
  - Description: React hook integration (useMemo prepared handles)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-60-svelte-islands-integration.md](./references/TECH-60-svelte-islands-integration.md)**
  - Description: Svelte / Astro islands integration (client:load)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-61-vanilla-ts.md](./references/TECH-61-vanilla-ts.md)**
  - Description: Vanilla TypeScript integration (no framework)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-62-ssr-node-canvas.md](./references/TECH-62-ssr-node-canvas.md)**
  - Description: SSR / Node.js integration (node-canvas shim)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-63-progressive-enhancement.md](./references/TECH-63-progressive-enhancement.md)**
  - Description: Progressive enhancement (pretext as feature gate)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-64-wrapper-module.md](./references/TECH-64-wrapper-module.md)**
  - Description: Wrapper module (line-height conversion + null fallback)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-65-vendoring-esm.md](./references/TECH-65-vendoring-esm.md)**
  - Description: Vendoring pretext as a single ESM file (no build step)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-66-resize-observer-pattern.md](./references/TECH-66-resize-observer-pattern.md)**
  - Description: ResizeObserver pattern (re-layout, not re-prepare)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-67-masonry-grid.md](./references/TECH-67-masonry-grid.md)**
  - Description: Masonry grid (Pinterest-style variable card heights)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-68-virtualized-list.md](./references/TECH-68-virtualized-list.md)**
  - Description: Virtualized list with variable-height text rows
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-69-smartpage-a4-autofit.md](./references/TECH-69-smartpage-a4-autofit.md)**
  - Description: SmartPage — auto-fit Markdown to one A4 page
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-70-streaming-ai-chat.md](./references/TECH-70-streaming-ai-chat.md)**
  - Description: Streaming AI chat (measure tokens as they arrive)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-71-auto-height-textarea.md](./references/TECH-71-auto-height-textarea.md)**
  - Description: Auto-height textarea (pre-wrap, no scroll bar)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-72-use-pretext-decision-guide.md](./references/TECH-72-use-pretext-decision-guide.md)**
  - Description: Decision guide — when to use pretext (and when NOT)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-73-design-consultation-route.md](./references/TECH-73-design-consultation-route.md)**
  - Description: Full-pipeline design consultation (gstack design-html)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-74-dragon-text-reflow.md](./references/TECH-74-dragon-text-reflow.md)**
  - Description: Dragon text reflow (text flowing around an 80-segment creature)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-75-rich-note-atomic-pills.md](./references/TECH-75-rich-note-atomic-pills.md)**
  - Description: Rich note (mixed inline fragments with atomic pills)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-76-postext-mobile-port.md](./references/TECH-76-postext-mobile-port.md)**
  - Description: postext — pretext port for React Native / mobile runtimes
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-77-font-strategy.md](./references/TECH-77-font-strategy.md)**
  - Description: Font strategy for pretext (named families, load order, fallbacks)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-78-style-profiles.md](./references/TECH-78-style-profiles.md)**
  - Description: Style profiles (pick ONE aesthetic per pretext output)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-pretext/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per `../amw-design-principles/ai-slop-avoid.md` (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. HTML pages (and/or JS modules) that use `@chenglou/pretext` for precise text layout). The output path is determined by **project inference**, NOT hardcoded. See [`../amw-design-principles/references/project-output-routing.md`](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/mockups/` created fresh)
   - Last-resort scratch: `/tmp/amw-pretext-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- <artifact-path> — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.

## How to use this skill

1. **Decide first:** read [TECH-72-use-pretext-decision-guide](references/TECH-72-use-pretext-decision-guide.md) — if CSS solves it (`line-clamp`, `text-overflow`, `text-wrap: balance`) there's no reason to add pretext.
2. **Pick the technique** from the catalog above — one TECH file, not a monolithic dump.
3. **Follow the exact API path** documented in that TECH file. Do NOT improvise — pretext has sharp gotchas (lineHeight-in-px, font-string-parity, `system-ui` drift).
4. **Build the wrapper module first** ([TECH-64](references/TECH-64-wrapper-module.md)) — this catches the #1 integration bug (lineHeight multiplier vs pixels).
5. **Handle resize** ([TECH-66](references/TECH-66-resize-observer-pattern.md)) — re-layout never re-prepare.
6. **Validate against the font strategy** ([TECH-77](references/TECH-77-font-strategy.md)) — named fonts, `document.fonts.ready`, no `system-ui`.

## Prerequisites

- **Runtime (user installs — NOT auto-installed by the plugin):** `@chenglou/pretext` via npm / bun — adds ~15 KB to the user's bundle. Documented in each TECH file; not mandatory for every design task.
- **Optional runtime companions:** `opentype.js@1.3.4` (glyph paths), `flubber@0.4.2` (glyph morph), `canvas` (Node SSR). All loaded conditionally by the TECH that needs them.
- **Plugin-side:** none — this skill is pure documentation / routing.

## Examples

Each TECH file under `./references/` contains a "Minimal example" section with near-runnable code. Start with `TECH-72-use-pretext-decision-guide.md` to determine if pretext is needed, then read the matching TECH file for the specific technique.

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| Measurement results differ from browser render | Font string mismatch between `prepare()` call and CSS/canvas renderer | Follow TECH-18: font-string parity — pass the exact same CSS font string to both. |
| Layout produces wrong line count after resize | `prepare()` called in the resize loop | `prepare()` must be called once at stable font load time; only call `layout()` on resize. See TECH-66. |
| Canvas text blurry on retina | Missing HiDPI backing-store scaling | Scale canvas by `devicePixelRatio` at setup. See TECH non-negotiables. |
| `@chenglou/pretext` not found | Library not installed in user's project | `npm install @chenglou/pretext` or `bun add @chenglou/pretext`. Not auto-installed by this plugin. |
| `system-ui` measurement drift across OS | Font resolved differently per OS | Use named, loaded fonts only. See TECH-77 (font strategy). |

## Resources

- [`../amw-design-principles/SKILL.md`](../amw-design-principles/SKILL.md) — orchestrator; pretext must reuse the design-principles typography tokens, not introduce new fonts.
- [`../amw-design-principles/typography-system.md`](../amw-design-principles/typography-system.md) — type scale + families pretext extends (never replaces).
- [`../amw-design-principles/ai-slop-avoid.md`](../amw-design-principles/ai-slop-avoid.md) — review every kinetic / calligram output against item 9 (over-cute effects).
- [`../amw-design-principles/starter-components/animations.html`](../amw-design-principles/starter-components/animations.html) — Stage + Sprite timeline; pretext kinetic work composes with this, not with Framer Motion / GSAP (banned plugin-wide).
- [`../amw-mermaid-render/SKILL.md`](../amw-mermaid-render/SKILL.md) — pretext is NOT a diagram skill. For diagrams, the plugin has dedicated ASCII / Mermaid / SVG paths.

## Non-negotiables

- Never activate on "make the type nice" / "pick a font" — those belong to `../amw-design-principles/typography-system.md`.
- No Framer Motion, no GSAP — plugin-wide ban. Pretext's frame-by-frame Canvas / SVG approach IS the approved kinetic-text alternative.
- The font string passed to `prepare()` MUST be loaded and byte-identical to what the renderer uses.
- `prepare()` MUST live outside animation / render loops. `layout()` is the hot path.
- HiDPI: scale the canvas backing store by `devicePixelRatio` at setup.
- No pseudocode — every code snippet in a TECH file is runnable or near-runnable.
- Responses stay in the user's language.
