---
name: TECH-hyperframes-composition-core
category: hyperframes-composition
source: external/hyperframes/skills/hyperframes/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Approach (narrative order)](#approach-narrative-order)
  - [Single-file skeleton](#single-file-skeleton)
  - [Visual Identity Gate (MUST — before writing HTML)](#visual-identity-gate-must-before-writing-html)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Composition authoring — core model

## What it does

Hyperframes treats HTML as the source of truth for video. A composition is an HTML file with `data-*` attributes for timing, a GSAP timeline for animation, and CSS for appearance. The framework handles clip visibility, media playback, and timeline sync — the author writes declarative HTML + a paused GSAP timeline, nothing else.

## When to use

On every hyperframes composition. This TECH is the entry-point doc for the "how do I write a composition" question. Related TECHs cover specific sub-topics (layout-before-animation, timeline contract, data attributes, transitions).

## How it works

### Approach (narrative order)

Before writing HTML, think at a high level:

1. **What** — what should the viewer experience? Identify narrative arc, key moments, emotional beats.
2. **Structure** — how many compositions, which are sub-compositions vs inline, what tracks carry video / audio / overlays / captions.
3. **Timing** — which clips drive the duration, where do transitions land, what's the pacing.
4. **Layout** — build the end-state first (see [TECH-hyperframes-layout-before-animation](TECH-hyperframes-layout-before-animation.md)).
  > What it does · When to use · How it works · Why this matters · Minimal example · Wrong pattern (hardcoded dimensions + absolute positioning) · Layered + temporal intent · Gotchas · Cross-references
5. **Animate** — then add motion using the rules.

For small edits (fix a color, adjust timing), skip straight to the rules.

### Single-file skeleton

> **Note:** Compositions do NOT use `data-duration` — their duration is determined by `tl.duration()`. Setting `data-duration` on the root composition element is silently ignored.

```html
<div data-composition-id="my-scene" data-width="1920" data-height="1080">
  <style>
    [data-composition-id="my-scene"] {
      width: 100%; height: 100%;
      display: flex; flex-direction: column;
      justify-content: center;
      padding: 120px 160px;
      box-sizing: border-box;
      background: var(--surface, #0F172A);
      color: var(--text, #F8FAFC);
      font-family: var(--font-heading, sans-serif);
    }
    .title { font-size: 120px; font-weight: 600; }
    .subtitle { font-size: 42px; margin-top: 24px; }
  </style>
  <h1 class="title" id="title">Headline</h1>
  <p class="subtitle" id="subtitle">Supporting copy</p>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    tl.from('#title',    { y: 60, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.3);
    tl.from('#subtitle', { y: 40, opacity: 0, duration: 0.5, ease: "power3.out" }, 0.6);
    window.__timelines['my-scene'] = tl;
  </script>
</div>
```

### Visual Identity Gate (MUST — before writing HTML)

Every composition reads, in order:

1. **DESIGN.md** in the project root (if present)
2. **visual-style.md** (project-specific file — NOTE: distinct from `visual-styles.md`, the library with 8 named presets)
3. **User-named style** (e.g. "Swiss Pulse", "dark and techy") → read `visual-styles.md` for the preset, generate a minimal DESIGN.md from it
4. **None of the above** → ask 3 questions (mood / light-or-dark / brand colors/fonts) before writing any HTML

No composition uses `#333`, `#3b82f6`, or `Roboto` — those indicate the gate was skipped.

*Attributed to the hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes/SKILL.md`.*

## Gotchas

- Writing HTML before reading DESIGN.md produces brand-drifted output every time. The gate is non-negotiable.
- Standalone compositions (root `index.html`) DO NOT use `<template>` — they put `data-composition-id` directly in `<body>`. Sub-compositions loaded via `data-composition-src` DO use `<template>`.
- Inline nested compositions (defined directly in the parent, no external file) put `data-composition-id` directly on a nested `<div>` inside the parent — they do NOT use `<template>` or `data-composition-src`.
- Mixing the two patterns (template on a standalone file, or data-composition-src on an inline sub-composition) hides all content from the browser and breaks rendering.
- House style (`house-style.md` in the hyperframes repo) provides motion / sizing / palette defaults when DESIGN.md is minimal. Read on demand.

## Cross-references

- [TECH-hyperframes-identity-gate](TECH-hyperframes-identity-gate.md) — the hard-gate rule applied here
  > What it does · When to use · How it works · DESIGN.md exists in the project? · visual-style.md exists? · User named a style (e.g. "Swiss Pulse", "dark and techy", "luxury brand")? · None of the above? · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-layout-before-animation](TECH-hyperframes-layout-before-animation.md) — positioning strategy
  > What it does · When to use · How it works · Why this matters · Minimal example · Wrong pattern (hardcoded dimensions + absolute positioning) · Layered + temporal intent · Gotchas · Cross-references
- [TECH-hyperframes-data-attributes](TECH-hyperframes-data-attributes.md) — full attribute reference
  > What it does · When to use · How it works · Clip attributes (all clips) · Composition-level attributes (on the root `data-composition-id`) · Relative timing · Banned / deprecated attributes · Minimal example · Sub-composition wrapping · Per-instance variable injection via `data-variable-values` · Gotchas · Cross-references
- [TECH-hyperframes-timeline-contract](TECH-hyperframes-timeline-contract.md) — GSAP timeline rules
  > What it does · When to use · How it works · Required pattern · Banned patterns · Allowed GSAP properties · Minimal example · Use `tl.set()` for later-scene clips · Gotchas · Cross-references
- [TECH-hyperframes-scene-transitions](TECH-hyperframes-scene-transitions.md) — inter-scene rules
  > What it does · When to use · How it works · Rule 1 — ALWAYS use transitions between scenes · Rule 2 — ALWAYS use entrance animations on every scene · Rule 3 — NEVER use exit animations except on the final scene · Rule 4 — Final scene only may fade elements out · Wrong pattern · Right pattern · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-non-negotiables](TECH-hyperframes-non-negotiables.md) — banned patterns
  > What it does · When to use · How it works · The twelve rules · Determinism clause · Animation scope clause · Animation conflict clause · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
