---
name: TECH-hyperframes-registry-blocks
category: hyperframes-registry
source: external/hyperframes/skills/hyperframes-registry/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Include pattern](#include-pattern)
  - [Required attributes on the include](#required-attributes-on-the-include)
  - [Verification](#verification)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH: Wiring registry blocks into host compositions

## What it does

Blocks are standalone sub-compositions — own dimensions, own duration, own GSAP timeline. They install to `compositions/<name>.html` and are included in a host composition (typically `index.html`) via the `data-composition-src` attribute.

## When to use

Whenever a registry block fits the needed sub-composition (data chart, decision tree, product mockup animation, etc.) — saves the 30-120 min of writing + testing a sub-composition from scratch.

## How it works

### Include pattern

```html
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="15"
  data-track-index="1"
  data-width="1920"
  data-height="1080"></div>
```

### Required attributes on the include

| Attribute | Role |
|---|---|
| `data-composition-src` | Path to the block HTML file |
| `data-composition-id` | Must match the block's internal ID (defined inside the block file) |
| `data-start` | When the block appears in the host timeline (seconds) |
| `data-duration` | How long the block plays |
| `data-width` / `data-height` | Block canvas dimensions |
| `data-track-index` | Layer ordering — higher index renders in front |

### Verification

After wiring:

1. `npx hyperframes lint` — confirms the `data-composition-id` matches the block file and paths resolve
2. `npx hyperframes preview` — the block appears at its `data-start` time

## Minimal example

Host `index.html`:

```html
<div data-composition-id="intro" data-width="1920" data-height="1080">
  <!-- Scene 1 content -->
  <h1 id="title">Acme Launch</h1>
  <p id="subtitle">The verified-address API</p>

  <!-- Block: data chart appears at t=8s, lasts 10s -->
  <div
    id="chart-block"
    data-composition-id="performance-chart"
    data-composition-src="compositions/performance-chart.html"
    data-start="8"
    data-duration="10"
    data-track-index="2"
    data-width="1920"
    data-height="1080"></div>

  <script>
    const tl = gsap.timeline({ paused: true });
    tl.from('#title',    { y: 60, opacity: 0, duration: 0.6 }, 0.3);
    tl.from('#subtitle', { y: 40, opacity: 0, duration: 0.5 }, 0.6);
    // Block's own timeline auto-nests — do NOT add it here
    window.__timelines['intro'] = tl;
  </script>
</div>
```

*Attributed to the hyperframes-registry skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes-registry/SKILL.md`.*

## Gotchas

- Framework auto-nests sub-composition timelines. Do NOT manually add the block's timeline to the parent — that double-plays the block.
- `data-composition-id` on the include must EXACTLY match the block's internal `data-composition-id`. Typos silently fail.
- Blocks can have different dimensions than the host. A 1080×1080 block inside a 1920×1080 host is valid; the block renders at its own size and the host scales/positions it.
- Nested blocks (block A includes block B) work but require identical dimensions throughout the chain, or explicit `data-width` / `data-height` on each include.

## Cross-references

- [TECH-hyperframes-registry-add](TECH-hyperframes-registry-add.md), [TECH-hyperframes-registry-components](TECH-hyperframes-registry-components.md)
  > [TECH-hyperframes-registry-components.md] What it does · When to use · How it works · Wiring process · Example component file · Merging into host · Minimal example · Gotchas · Cross-references
  > What it does · When to use · How it works · Blocks vs components · Paths (configurable in `hyperframes.json`) · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-composition-core](TECH-hyperframes-composition-core.md), [TECH-hyperframes-data-attributes](TECH-hyperframes-data-attributes.md)
  > [TECH-hyperframes-data-attributes.md] What it does · When to use · How it works · Clip attributes (all clips) · Composition-level attributes (on the root `data-composition-id`) · Relative timing · Banned / deprecated attributes · Minimal example · Sub-composition wrapping · Per-instance variable injection via `data-variable-values` · Gotchas · Cross-references
  > What it does · When to use · How it works · Approach (narrative order) · Single-file skeleton · Visual Identity Gate (MUST — before writing HTML) · Gotchas · Cross-references
- [SKILL](../SKILL.md)
