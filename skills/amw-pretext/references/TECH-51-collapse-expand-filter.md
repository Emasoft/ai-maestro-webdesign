---
name: TECH-51-collapse-expand-filter
category: motion
source: pretext-skills/amw-pretext-skill-main/patterns.md
also-in: 
---

# Animated filter (CSS collapse/expand, NOT virtualization)

**Category:** motion
**Status:** stable

## What it does

For filtering a visible list of items, render ALL items as normal DOM and use CSS `max-height` transitions + `scrollHeight` snapshotting to animate collapse/expand. This is the ANTI-pattern recommendation: do NOT reach for pretext + virtualization for simple filter/search UIs — CSS handles it better for <500 items.

## When to use

- List filters where < 500 items are visible
- Search-as-you-type UIs
- Anywhere pretext is tempting but CSS wins

## How it works

```js
// Source: pretext-skill-main/patterns.md — Animated Filter
function applyFilter(query) {
  items.forEach((item, i) => {
    const wrapper = wrappers[i]
    if (matches(item, query)) {
      wrapper.classList.remove('hidden')
      wrapper.style.maxHeight = wrapper.scrollHeight + 'px'
    } else {
      wrapper.style.maxHeight = wrapper.scrollHeight + 'px'
      wrapper.offsetHeight  // force reflow
      wrapper.style.maxHeight = '0'
      wrapper.classList.add('hidden')
    }
  })
}
```

## Minimal example

```css
.card-wrapper { overflow: hidden; transition: max-height 0.3s ease-out }
```

## Gotchas

- CSS class `max-height: 0` gets overridden by the inline `max-height` snapshot — use inline styles for collapse values.
- For 1000+ items, TECH-67 (virtualized list) is correct.

## Cross-references

- Related: TECH-67-virtualized-list
- API reference: none (CSS-only pattern)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
