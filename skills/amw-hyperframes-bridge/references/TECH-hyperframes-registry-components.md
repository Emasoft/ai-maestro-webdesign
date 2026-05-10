---
name: TECH-hyperframes-registry-components
category: hyperframes-registry
source: external/hyperframes/skills/hyperframes-registry/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Wiring process](#wiring-process)
  - [Example component file](#example-component-file)
  - [Merging into host](#merging-into-host)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH: Wiring registry components into host compositions

## What it does

Components are effect snippets — no own dimensions, no own timeline, they live inside an existing composition. They install to `compositions/components/<name>.html` and are **pasted into** the host composition's HTML, CSS, and JS sections.

## When to use

When a composition needs a pre-built visual effect (grain overlay, shimmer sweep, glow pulse, film burn, chromatic aberration) rather than rebuilding it manually.

## How it works

### Wiring process

1. **Read the installed file** (e.g. `compositions/components/grain-overlay.html`)
2. **Copy the HTML elements** into the host composition's `<div data-composition-id="...">`
3. **Copy the `<style>` block** into the host's style block
4. **Copy any `<script>` content** into the host's script, BEFORE the timeline code
5. **If the component exposes GSAP timeline integration** (look for the comment block inside the snippet), add those calls to the host's timeline

### Example component file

`compositions/components/grain-overlay.html`:

```html
<!-- HTML: grain overlay element -->
<div class="grain-overlay" aria-hidden="true"></div>

<!-- CSS: grain styling -->
<style>
  .grain-overlay {
    position: absolute; inset: 0; pointer-events: none; mix-blend-mode: overlay;
    background-image: url('data:image/png;base64,...');
    opacity: 0.06;
  }
</style>

<!-- JS / GSAP integration (optional) -->
<script>
  // If you want the grain to fade in with the scene:
  //   tl.from('.grain-overlay', { opacity: 0, duration: 0.8 }, 0);
</script>
```

### Merging into host

Host composition after merge:

```html
<div data-composition-id="hero" data-width="1920" data-height="1080">
  <style>
    [data-composition-id="hero"] { /* ... */ }
    /* Merged from grain-overlay component */
    .grain-overlay { position: absolute; inset: 0; /* ... */ }
  </style>

  <h1 id="title">Hero</h1>
  <!-- Merged from grain-overlay component -->
  <div class="grain-overlay" aria-hidden="true"></div>

  <script>
    const tl = gsap.timeline({ paused: true });
    tl.from('#title', { y: 60, opacity: 0, duration: 0.6 }, 0.3);
    // Merged from grain-overlay component:
    tl.from('.grain-overlay', { opacity: 0, duration: 0.8 }, 0);
    window.__timelines['hero'] = tl;
  </script>
</div>
```

## Minimal example

```bash
# Install grain overlay
hyperframes add grain-overlay

# File written: compositions/components/grain-overlay.html
# Clipboard: wiring snippet

# Paste the snippet into host composition's HTML + CSS + JS sections
```

*Attributed to the hyperframes-registry skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes-registry/SKILL.md`.*

## Gotchas

- Components are copy-paste, not include. The source file in `components/` is reference; the live version is inside the host composition.
- Re-installing a component doesn't update previously-merged copies — they have to be manually re-merged.
- Some components require specific CSS-variable names on the host (e.g. a shimmer component expects `--accent`). Read the comment block inside the component file.
- Z-index matters — grain overlays, chromatic aberration, scanlines are mix-blend layers that must be above content. Use `z-index: 10` or higher if your content has explicit z-indices.

## Cross-references

- [TECH-hyperframes-registry-add](TECH-hyperframes-registry-add.md), [TECH-hyperframes-registry-blocks](TECH-hyperframes-registry-blocks.md)
  > [TECH-hyperframes-registry-blocks.md] What it does · When to use · How it works · Include pattern · Required attributes on the include · Verification · Minimal example · Gotchas · Cross-references
  > What it does · When to use · How it works · Blocks vs components · Paths (configurable in `hyperframes.json`) · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-composition-core](TECH-hyperframes-composition-core.md)
  > What it does · When to use · How it works · Approach (narrative order) · Single-file skeleton · Visual Identity Gate (MUST — before writing HTML) · Gotchas · Cross-references
- [SKILL](../SKILL.md)
