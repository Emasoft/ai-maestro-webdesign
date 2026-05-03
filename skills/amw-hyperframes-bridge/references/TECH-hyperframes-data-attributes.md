---
name: TECH-hyperframes-data-attributes
category: hyperframes-composition
source: external/hyperframes/skills/hyperframes/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Clip attributes (all clips)](#clip-attributes-all-clips)
  - [Composition-level attributes (on the root `data-composition-id`)](#composition-level-attributes-on-the-root-data-composition-id)
  - [Relative timing](#relative-timing)
  - [Banned / deprecated attributes](#banned-deprecated-attributes)
- [Minimal example](#minimal-example)
  - [Sub-composition wrapping](#sub-composition-wrapping)
  - [Per-instance variable injection via `data-variable-values`](#per-instance-variable-injection-via-data-variable-values)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Data attributes — clip + composition schema

## What it does

Hyperframes compositions are HTML files annotated with `data-*` attributes that the framework reads at compile time. Two categories of attributes exist: clip-level (on video / audio / img / div elements) and composition-level (on the `data-composition-id` root).

## When to use

On every element that should appear in the timeline. Missing or wrong attributes are the most common composition error.

## How it works

### Clip attributes (all clips)

| Attribute | Required | Values |
|---|---|---|
| `id` | Yes | Unique identifier |
| `class="clip"` | Yes (visible elements) | Required on all timed visible elements (`img`, `div`) so the runtime manages their visibility lifecycle. Omit on `<audio>` and `<video>` — the framework manages those directly. |
| `data-start` | Yes | Seconds (`"0"`, `"5.5"`) or a clip ID reference for relative timing (`"intro"`, `"intro + 2"`, `"intro - 0.5"`) |
| `data-duration` | Required for `img` / `div` | Seconds. `video` and `audio` default to source duration from `data-media-start`. NOT used on nested compositions. |
| `data-track-index` | Yes | Integer. Controls z-ordering (higher index renders in front). Same-track clips cannot overlap in time. |
| `data-media-start` | No | Trim offset into source file (seconds, default `0`) |
| `data-volume` | No | 0–1 (default 1) |
| `data-has-audio` | No | `"true"` on `<video>` elements with an audio track |

### Composition-level attributes (on the root `data-composition-id`)

| Attribute | Required | Values |
|---|---|---|
| `data-composition-id` | Yes | Unique composition ID — must match the `window.__timelines` key |
| `data-start` | Yes | Start time (root composition: use `"0"`) |
| `data-width` / `data-height` | Yes | Pixel dimensions (1920×1080 or 1080×1920) |
| `data-composition-src` | No | Path to external HTML file (for sub-compositions) |
| `data-variable-values` | No | JSON object of per-instance values to pass into a sub-composition (e.g. `'{"title":"Hello","color":"#ff0"}'`). The framework carries the attribute through to the composition's DOM; the composition's own script must read and apply the values manually (see worked example below). |
| `data-composition-variables` | No | Optional declarative metadata for tooling — describes the variable schema expected by this composition. Readable via `extractCompositionMetadata()` from `@hyperframes/core`. Does NOT auto-apply values; use `data-variable-values` on the host for actual injection. |

> Compositions do NOT use `data-duration` — duration is determined by the GSAP timeline's `tl.duration()`.

### Relative timing

Reference another clip's `id` in `data-start` to mean "start when that clip ends":

```html
<video id="intro" data-start="0" data-duration="10" data-track-index="0" src="..."></video>
<video id="main"  data-start="intro" data-duration="20" data-track-index="0" src="..."></video>
```

Offsets for gaps and overlaps:

```html
<!-- 2-second gap after intro -->
<video id="main" data-start="intro + 2" data-duration="20" data-track-index="0" src="..."></video>

<!-- 0.5-second overlap with intro (crossfade zone) -->
<video id="b" data-start="intro - 0.5" data-duration="20" data-track-index="1" src="..."></video>
```

Relative references resolve within the same composition only. Circular references and references to clips with no known duration are rejected by the linter.

### Banned / deprecated attributes

| Banned | Use instead |
|---|---|
| `data-layer` | `data-track-index` |
| `data-end` | `data-duration` |

## Minimal example

Video + overlay + audio:

```html
<!-- Video clip — no class="clip", no muted required but recommended -->
<video
  id="el-v"
  data-start="0"
  data-duration="30"
  data-track-index="0"
  src="video.mp4"></video>

<!-- Overlay div — class="clip" required for visibility management -->
<div
  id="el-overlay"
  class="clip lower-third"
  data-start="5"
  data-duration="3"
  data-track-index="1">Headline</div>

<!-- Audio (separate element, no class="clip") -->
<audio
  id="el-a"
  data-start="0"
  data-duration="30"
  data-track-index="2"
  src="narration.mp3"
  data-volume="1"></audio>
```

### Sub-composition wrapping

Sub-compositions loaded via `data-composition-src` use `<template>` in the external file:

```html
<!-- compositions/my-comp.html -->
<template id="my-comp-template">
  <div data-composition-id="my-comp" data-width="1920" data-height="1080">
    <!-- content + style + script here -->
  </div>
</template>
```

Referenced from root `index.html`:

```html
<div id="el-1"
     data-composition-id="my-comp"
     data-composition-src="compositions/my-comp.html"
     data-start="0"
     data-track-index="1"></div>
```

Inline nested compositions (defined directly in the parent, no external file) do NOT use `<template>` or `data-composition-src` — they put `data-composition-id` directly on the nested `<div>`.

### Per-instance variable injection via `data-variable-values`

To inject per-instance values into a composition, pass a JSON object via `data-variable-values` on the host element. The composition's own script must read and apply the values — the framework carries the attribute to the DOM and applies nothing automatically.

```html
<!-- index.html — host side: single card slot with variable values -->
<div data-composition-id="card"
     data-composition-src="compositions/card.html"
     data-variable-values='{"title":"Launch Day","color":"#6366f1"}'
     data-start="0"
     data-track-index="1"></div>
```

```html
<!-- compositions/card.html — composition side: read and apply values manually -->
<template id="card-template">
  <div data-composition-id="card" data-width="1920" data-height="1080">
    <style>
      .card-title { color: var(--card-color, #fff); }
    </style>

    <div class="clip card-title" data-start="0" data-duration="5" data-track-index="0">
      Title
    </div>

    <script>
      (function () {
        // Hyperframes does NOT auto-bind data-variable-values into DOM or CSS.
        // The composition reads its own root via its unique data-composition-id.
        const rootEl = document.querySelector('[data-composition-id="card"]');
        const vars = JSON.parse(rootEl.getAttribute("data-variable-values") || "{}");

        // Apply values — CSS custom property + text content
        if (vars.color) rootEl.style.setProperty("--card-color", vars.color);
        if (vars.title) rootEl.querySelector(".card-title").textContent = vars.title;
      })();
    </script>
  </div>
</template>
```

To use the **same composition template for multiple distinct slots**, each slot must have a unique `data-composition-id` (the attribute is required to be unique per composition instance, per `external/hyperframes/docs/concepts/data-attributes.mdx:28`). Use distinct IDs (e.g. `data-composition-id="card-1"` and `data-composition-id="card-2"`) and match the composition's `querySelector` selector accordingly, or use a class-based selector inside the composition.

Key rules:
- `data-variable-values` is a **host-side** attribute on the element that references the composition (not inside the composition template itself).
- The value must be a valid JSON object string (double-quoted keys, string values).
- The composition's script is responsible for reading, parsing, and applying the values. The framework only carries the attribute to the DOM — it applies nothing automatically.
- Use `document.querySelector('[data-composition-id="<id>"]')` to find the composition root; `document.currentScript.closest(...)` is fragile when compositions are loaded asynchronously.
- CSS custom properties (`var(--card-color, fallback)`) are the cleanest way to apply color tokens.
- **`data-var-*` (e.g. `data-var-title`) is NOT auto-bound.** Hyperframes explicitly does not auto-bind these attributes into the composition DOM or CSS. `data-variable-values` + manual script application is the only supported variable injection path.

*Attributed to the hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes/SKILL.md`.*

## Gotchas

- Missing `class="clip"` on a timed `<div>` or `<img>` — element is always visible, ignoring `data-start` / `data-duration`. The linter catches this.
- Forgetting `data-track-index` on a clip silently fails — the framework picks a default and overlap errors appear.
- Using `data-layer` or `data-end` (both banned) produces lint errors. Always run `hyperframes lint` after edits.
- Compositions do NOT take `data-duration` — their duration equals `tl.duration()`. Setting `data-duration` on a composition element is silently ignored and is a common source of confusion.
- Same `data-track-index` + overlapping `data-start` / `data-duration` = lint error (not runtime failure).

## Cross-references

- [TECH-hyperframes-composition-core](TECH-hyperframes-composition-core.md), [TECH-hyperframes-timeline-contract](TECH-hyperframes-timeline-contract.md)
  > [TECH-hyperframes-timeline-contract.md] What it does · When to use · How it works · Required pattern · Banned patterns · Allowed GSAP properties · Minimal example · Use `tl.set()` for later-scene clips · Gotchas · Cross-references
  > What it does · When to use · How it works · Approach (narrative order) · Single-file skeleton · Visual Identity Gate (MUST — before writing HTML) · Gotchas · Cross-references
- [TECH-hyperframes-non-negotiables](TECH-hyperframes-non-negotiables.md)
  > What it does · When to use · How it works · The twelve rules · Determinism clause · Animation scope clause · Animation conflict clause · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
