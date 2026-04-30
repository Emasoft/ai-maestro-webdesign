---
name: TECH-bordered-section-component
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in:
---

# `bordered_section` — visible-border content panel

## What it does

Panel with a 2px colored border (left accent or full) containing
mixed content. Replaces naked card grids with something structurally
richer. The visible border is the signature — ghost borders
(`rgba(255,255,255,0.08)`) fail the Anti-Frontend Checklist.

## When to use

- Major content groupings where `bullet_panel` is not enough.
- Callout sections that need structural emphasis.
- Anywhere you'd reach for an invisible-border card grid.

## Left-accent variant (most common)

```css
/* source: image-generation/create-infographics/SKILL.md */
.bordered-section {
  border-left: 3px solid var(--primary);
  background: rgba(var(--primary-rgb), 0.04);
  border-radius: 0 8px 8px 0;
  padding: 14px 16px;
  margin-bottom: 16px;
}
```

## Full-border variant

```css
.bordered-section-full {
  border: 2px solid rgba(var(--primary-rgb), 0.3);
  border-radius: 8px;
  padding: 14px 16px;
  background: rgba(var(--primary-rgb), 0.04);
}
```

## Header styles

```css
.bordered-section h3 {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--primary);
  margin-bottom: 10px;
}
```

## HTML

```html
<div class="bordered-section">
  <h3>ELIGIBILITY OVERVIEW</h3>
  <ul class="bullet-list">
    <li>Hold 500+ $TKN at snapshot</li>
    <li>Active wallet for 30+ days</li>
    <li>Claim window: March 31 – April 30</li>
    <li>Tax implications: DYOR</li>
  </ul>
</div>
```

## Minimum border opacity

```
✅ border: 2px solid rgba(var(--primary-rgb), 0.3)   (visible)
❌ border: 1px solid rgba(255,255,255,0.08)          (ghost, fails checklist)
```

## Gotchas

- The left-accent variant is more "editorial" — the full-border
  variant is more "callout box".
- Combining `border-left` with `border-radius: 0 8px 8px 0` gives
  the signature look — rounded on 3 sides, flat on the left.
- Background tint (`rgba(var(--primary-rgb), 0.04)`) is barely
  visible but important — it separates the panel from the dark bg.

## Cross-references

- `TECH-bullet-panel-component.md` — simpler alternative for pure
  bullet content.
- `TECH-annotation-first.md` — styled insight callout box covered there.
- `TECH-dense-editorial-dna.md` — the visible-borders rule.
- [`../SKILL.md`](../SKILL.md) — parent skill

