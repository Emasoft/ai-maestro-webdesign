---
name: TECH-63-progressive-enhancement
category: integrate
source: pretext-skills/amw-pretext-skill-main/pretext/skills/amw-pretext/references/patterns.md
also-in: SKILL-11.md
---

# Progressive enhancement (pretext as feature gate)

**Category:** integrate
**Status:** stable

## What it does

Load pretext only when both `<canvas>` and ES modules are available, so the page works without pretext (CSS fallback) and gets the enhanced layout only where supported. Use `<script type="module">` as the natural feature gate — older browsers ignore it, modern browsers run it.

## When to use

- Content-first sites that must render with or without JS
- Pages where pretext adds polish but isn't critical
- Universal pages served to a mix of user agents

## How it works

```html
<!-- Source: pretext-skill-main/patterns.md Progressive Enhancement -->
<div class="card" data-text="Long text that may wrap">
  <p>Long text that may wrap</p> <!-- CSS fallback renders this -->
</div>
<script type="module">
  import { prepare, layout } from 'https://esm.sh/@chenglou/pretext'
  document.querySelectorAll('.card').forEach(card => {
    // enhance with precise measurement
  })
</script>
```

## Minimal example

```js
// Wrapper from TECH-64 returns null on failure
const result = measureText(text, family, size, maxW, lh)
if (result === null) return  // fall back to CSS-only layout
```

## Gotchas

- If you depend on pretext's output for layout structure, you lose that in the fallback — design the base state to work without it.
- `esm.sh` availability affects progressive enhancement — consider vendoring (TECH-65).

## Cross-references

- Related: TECH-64-wrapper-module, TECH-65-vendoring-esm
- API reference: [TECH-03-layout](TECH-03-layout.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
