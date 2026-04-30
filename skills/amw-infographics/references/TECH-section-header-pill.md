---
name: TECH-section-header-pill
category: infographic-template
source: image-generation/create-infographics/resources/style-details.md
also-in:
---

# Section header pill badge (ecosystem signature)

## What it does

Section label inside a colored pill with a neon glow. THE signature
section header for ecosystem infographics (73% prevalence).

## CSS

```css
/* source: image-generation/create-infographics/resources/style-details.md */
.section-pill {
  display: inline-flex;
  align-items: center;
  background: rgba(var(--primary-rgb), 0.1);
  border: 1px solid rgba(var(--primary-rgb), 0.35);
  box-shadow: 0 0 8px rgba(var(--primary-rgb), 0.25);
  color: var(--primary);
  font-family: 'Bebas Neue', sans-serif;
  font-size: 13px;
  letter-spacing: 2px;
  padding: 4px 16px;
  border-radius: 4px;
  margin-bottom: 14px;
}
```

## HTML

```html
<div class="section-pill">INTEGRATIONS</div>
```

## The four visual layers

1. **Background** — `rgba(primary, 0.1)` — muted accent fill
2. **Border** — `rgba(primary, 0.35)` — visible colored edge
3. **Box shadow** — `0 0 8px rgba(primary, 0.25)` — subtle neon glow
4. **Text** — brand primary color, Bebas Neue uppercase, 2px
   letter-spacing

## When to use

- Ecosystem infographic section dividers (mandatory for the type).
- Category labels in partner directories.
- Callout badges in game / crypto explainers.

## Variants

### Without glow (cleaner)
```css
.section-pill-clean {
  box-shadow: none;
  /* other properties same */
}
```

Use on light backgrounds or when glow competes with other glowing
elements.

### Wider (title-sized)
```css
.section-pill-large {
  font-size: 16px;
  padding: 6px 20px;
  letter-spacing: 2.5px;
}
```

Use for primary section titles in hero headers.

## Gotchas

- `2px` letter-spacing is wide — matches the editorial uppercase
  signature.
- On light backgrounds, drop the glow — it looks wrong on white.
- Don't use more than 4-6 section pills per piece — loses impact.

## Cross-references

- `TECH-ecosystem-playbook.md` — where this pattern is mandatory.
- `TECH-section-band.md` — the full-width alternative.
- `TECH-glow-system.md` — the glow system this uses.
- [`../SKILL.md`](../SKILL.md) — parent skill

