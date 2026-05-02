---
name: TECH-section-band
category: infographic-template
source: image-generation/create-infographics/resources/style-details.md
also-in: image-generation/create-infographics/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [The CSS](#the-css)
- [HTML](#html)
- [Numbered section headers with icon prefix](#numbered-section-headers-with-icon-prefix)
- [When to use](#when-to-use)
- [The color choice](#the-color-choice)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Full-width section separator bands

## What it does

The most common section-divider pattern in the body of work. NOT
just a text label — a full-width solid-background strip containing
the section number and title. Distinguishes sections visually
without relying on whitespace.

## The CSS

```css
/* source: image-generation/create-infographics/resources/style-details.md */
.section-band {
  width: 100%;
  background: #111520;                /* slightly lighter than page bg */
  border-top: 1px solid rgba(255,255,255,0.08);
  border-bottom: 1px solid rgba(255,255,255,0.08);
  padding: 8px 48px;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.section-band-num {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 11px;
  color: var(--primary);
  letter-spacing: 1px;
}

/* Optional diamond prefix */
.section-band-num::before {
  content: '◆ ';
  color: var(--primary);
}

.section-band-title {
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: var(--text-muted);
}

/* Trailing line to fill the rest of the row */
.section-band-line {
  flex: 1;
  height: 1px;
  background: var(--border);
}
```

## HTML

```html
<div class="section-band">
  <span class="section-band-num">1</span>
  <span class="section-band-title">OVERVIEW</span>
  <span class="section-band-line"></span>
</div>
```

## Numbered section headers with icon prefix

A related pattern — diamond `◆` or colored circle before the
section number + name (e.g., `◆1 OVERVIEW`). Common in game guides
and mechanic breakdowns.

## When to use

- Every section break in a Stacked Reference archetype — this is
  the dominant separator pattern.
- Multi-chapter infographics where section numbering aids navigation.
- When a thin horizontal rule doesn't provide enough visual weight.

## The color choice

- Band background: `#111520` — barely lighter than page background
  `#0D0D0D`. Subtle but visible.
- Number: brand primary color.
- Title: muted text color with wide letter-spacing (2.5px).
- Trailing line: border color, fills remaining row width.

## Gotchas

- Don't use section bands alongside colored-border containers on
  every section — one strong separator per section.
- The `2.5px` letter-spacing on titles is wide on purpose — it
  matches the editorial / magazine section-title convention.
- Band padding `8px 48px` feels tight vertically — intentional;
  the band signals "new section starting", not "decorative strip".

## Cross-references

- [TECH-stacked-reference-archetype](TECH-stacked-reference-archetype.md) — where this pattern lives.
- [TECH-section-header-pill](TECH-section-header-pill.md) — the pill alternative.
- [TECH-dense-editorial-dna](TECH-dense-editorial-dna.md) — why structural separators
  matter.
- [`../SKILL.md`](../SKILL.md) — parent skill

