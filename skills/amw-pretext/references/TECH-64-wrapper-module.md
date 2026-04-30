---
name: TECH-64-wrapper-module
category: integrate
source: pretext-skills/amw-pretext-skill-main/pretext/skills/amw-pretext/references/patterns.md
also-in: 
---

# Wrapper module (line-height conversion + null fallback)

**Category:** integrate
**Status:** stable

## What it does

Create a thin wrapper that (a) converts `lineHeight` from the CSS multiplier developers naturally think in (e.g. `1.5`) to the absolute pixels pretext requires (`fontSize * 1.5`), and (b) returns `null` on failure so callers can implement graceful fallback. Eliminates the #1 integration bug in pretext usage.

## When to use

- ALWAYS — as the first file in any pretext integration
- Especially in large codebases where many developers will touch the API

## How it works

```js
// Source: pretext-skill-main/pretext/skills/amw-pretext/references/patterns.md — Wrapper Module
import { prepare, layout } from '@chenglou/pretext'
export function measureText(text, fontFamily, fontSize, maxWidth, lineHeight) {
  lineHeight = lineHeight || 1.5
  const lineHeightPx = fontSize * lineHeight
  const cssFont = fontSize + 'px ' + fontFamily
  try {
    const prepared = prepare(text, cssFont)
    const result = layout(prepared, maxWidth, lineHeightPx)
    return { width: maxWidth, height: result.height, lines: result.lineCount }
  } catch (e) {
    return null
  }
}
```

## Minimal example

See How-it-works — this IS the recommended wrapper.

## Gotchas

- Do NOT skip the multiplier-to-px conversion — passing `1.5` as `lineHeight` silently produces heights ~14x too small.
- Returning `null` on failure enables TECH-63 progressive enhancement.

## Cross-references

- Related: TECH-03-layout, TECH-63-progressive-enhancement
- API reference: [TECH-03-layout](TECH-03-layout.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
