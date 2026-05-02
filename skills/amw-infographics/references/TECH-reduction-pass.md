---
name: TECH-reduction-pass
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [The checklist](#the-checklist)
- [Per-aesthetic strictness](#per-aesthetic-strictness)
- [The rule](#the-rule)
- [Before / after — gridline removal](#before-after-gridline-removal)
  - [Before](#before)
  - [After](#after)
- [Before / after — legend to direct labels](#before-after-legend-to-direct-labels)
  - [Before](#before-1)
  - [After](#after-1)
- [Before / after — decoration removal](#before-after-decoration-removal)
  - [Before (everything shouting)](#before-everything-shouting)
  - [After (structure creates hierarchy, not decoration)](#after-structure-creates-hierarchy-not-decoration)
- [Decision rule](#decision-rule)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Reduction Pass — strip everything that doesn't encode data

## What it does

Final step before export. Strips everything that doesn't encode
data. The difference between a good infographic and a great one.

## The checklist

- [ ] Remove gridlines that aren't needed to read values
- [ ] Remove axis tick marks where direct labels already exist
- [ ] Replace decorative icons with whitespace, or remove entirely
- [ ] Does every color choice encode something? If not, make it gray
- [ ] Remove border/glow on elements already separated by whitespace
- [ ] Cut any text that repeats what the visual already shows
- [ ] Check data-to-ink ratio — is decoration competing with data?

## Per-aesthetic strictness

| Aesthetic | Strictness |
|-----------|------------|
| **Designer signature dark (default)** | **Loose** — dense info is the point; colored borders / neon / multi-color labeling all serve the style. Remove axis clutter + redundant text, but do NOT reduce density. |
| Editorial/Clean | Strict — every element must justify itself |
| Corporate/Trust | Strict — remove decoration, preserve structure |
| Premium/Luxury | Moderate — decoration earns place through refinement |
| Bold/Cyber | Loose — glows + texture serve brand identity |
| Playful/Loud | Loose — saturation + energy are the point |

## The rule

Remove axis clutter, redundant labels, unjustified blank space. Do
NOT reduce information density — the designer's work is dense and
that is intentional. Whitespace separates SECTIONS, not content
within sections.

## Before / after — gridline removal

### Before
```css
.chart-grid {
  background-image: repeating-linear-gradient(
    0deg, rgba(255,255,255,0.08) 0px, rgba(255,255,255,0.08) 1px,
    transparent 1px, transparent 40px
  );
}
.axis-tick { display: block; }
```

### After
```css
.chart-grid { background: none; }
.axis-tick  { display: none; }

.bar-value-label {
  position: absolute;
  right: 8px;
  font-size: 11px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}
```

## Before / after — legend to direct labels

### Before
```html
<div class="legend">
  <span class="legend-dot" style="background:#00D4FF"></span> Product A
  <span class="legend-dot" style="background:#F5A623"></span> Product B
</div>
```

### After
```html
<svg>
  <!-- line path ... -->
  <text x="580" y="42" fill="#00D4FF" font-size="11" font-weight="600">Product A</text>
  <!-- line path ... -->
  <text x="580" y="78" fill="#F5A623" font-size="11" font-weight="600">Product B</text>
</svg>
```

## Before / after — decoration removal

### Before (everything shouting)
```css
.card {
  border: 1px solid transparent;
  background: linear-gradient(#0D0D0D, #0D0D0D) padding-box,
              linear-gradient(135deg, var(--primary), var(--secondary)) border-box;
  box-shadow: 0 0 30px rgba(var(--primary-rgb), 0.5), 0 8px 32px rgba(0,0,0,0.4);
  background-image: url("pattern.svg");
}
.card-icon { font-size: 32px; margin-bottom: 8px; }  /* decorative only */
```

### After (structure creates hierarchy, not decoration)
```css
.card {
  border: 1px solid rgba(255, 255, 255, 0.10);
  box-shadow: none;
  background: rgba(255, 255, 255, 0.03);
}
/* Icon removed — heading already identifies the card */
```

## Decision rule

If two elements are separated by 16px+ of whitespace, they don't
need a border AND a glow AND a shadow. Pick ONE separation signal.
Usually border alone is enough.

## Gotchas

- Reduction pass runs AFTER the build, before export — not during.
- Don't reduce density. Density is intentional.
- Loose strictness doesn't mean "no reduction" — still remove
  redundant labels.

## Cross-references

- [TECH-annotation-first](TECH-annotation-first.md) — related: labels over legends.
- [TECH-anti-frontend-checklist](TECH-anti-frontend-checklist.md) — the pre-delivery check that
  includes this.
- [TECH-dense-editorial-dna](TECH-dense-editorial-dna.md) — the "don't reduce density" rule.
- [`../SKILL.md`](../SKILL.md) — parent skill

