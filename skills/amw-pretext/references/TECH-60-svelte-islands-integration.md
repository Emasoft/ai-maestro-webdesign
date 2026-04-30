---
name: TECH-60-svelte-islands-integration
category: integrate
source: pretext-skills/use-pretext/SKILL.md
also-in: 
---

# Svelte / Astro islands integration (client:load)

**Category:** integrate
**Status:** stable

## What it does

Pretext needs `<canvas>` and `Intl.Segmenter` — both browser-only. In Astro projects, put pretext-powered components inside Svelte / React / Vue islands with `client:load` or `client:visible` directives. Use `onMount` to trigger the `document.fonts.ready.then(...)` sync before the first `prepare()` call.

## When to use

- Astro blogs with interactive pretext widgets
- Svelte kit apps with virtualized lists
- Any static-site + island architecture

## How it works

```svelte
<!-- Source: use-pretext/SKILL.md — Recipe 1 Masonry -->
<script>
  import { onMount } from 'svelte'
  import { prepare, layout } from '@chenglou/pretext'
  export let items = []
  const font = '16px Rubik'
  let positioned = []
  let containerEl
  onMount(() => {
    document.fonts.ready.then(() => {
      positioned = computeLayout(containerEl.clientWidth)
    })
    const ro = new ResizeObserver(e => {
      positioned = computeLayout(e[0].contentRect.width)
    })
    ro.observe(containerEl); return () => ro.disconnect()
  })
</script>
```

## Minimal example

```astro
<!-- Astro page — hydrate the island -->
<MasonryGrid items={data} client:visible />
```

## Gotchas

- `client:visible` delays prepare() until the island scrolls into view — first measurement is late, may cause CLS.
- Never call `prepare()` in Astro frontmatter (`.astro` body) — it runs at build time without Canvas.
- Font loading: `document.fonts.ready` is critical in SSR-hydrated islands.

## Cross-references

- Related: TECH-17-font-loading-sync, TECH-30-layout-shift-prevention
- API reference: [TECH-01-prepare-basics](TECH-01-prepare-basics.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
