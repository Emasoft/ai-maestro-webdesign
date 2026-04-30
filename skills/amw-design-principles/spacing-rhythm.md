# Spacing and rhythm — hard rules

> Spacing is not "whatever feels comfortable." You **pick from a fixed set of numbers**. Any spacing value not in the table is forbidden.

---

## I. 8pt grid system

Every spacing value must be a **multiple of 4 or 8**. Pick one cadence and apply it to the whole project.

### Allowed spacing values

```
4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 160, 192, 256
```

### T-shirt naming (use tokens)

```css
:root {
  --space-xs:  4px;
  --space-sm:  8px;
  --space-md:  16px;   /* base unit */
  --space-lg:  24px;
  --space-xl:  32px;
  --space-2xl: 48px;
  --space-3xl: 64px;
  --space-4xl: 96px;
  --space-5xl: 128px;
}
```

### Forbidden

- `padding: 13px`, `margin: 7px` (off-grid values)
- Mixing values inside one component like `padding: 16px 17px` (breaks symmetry)
- Inventing new spacing values (reach for an existing token first)

---

## II. Fibonacci spacing rhythm (large-scale)

For large compositions — slides, posters, hero sections — use Fibonacci:

```
8, 13, 21, 34, 55, 89, 144, 233
```

Why: **adjacent values differ sharply, giving the composition dramatic rhythm** instead of the uniform flatness an 8pt grid produces at large sizes.

Where it fits:

- Slide title vs body spacing
- Poster hero visual vs copy block
- Magazine / book-style editorial layouts

---

## III. Vertical rhythm (baseline grid)

### Core rule

**Every paragraph and component height** should be an **integer multiple of the base line-height**.

```css
:root {
  --baseline: 24px;   /* base line-height */
}

p  { line-height: 24px; margin-bottom: 24px; }     /* 1 × baseline */
h3 { line-height: 32px; margin-bottom: 48px; }     /* 2 × baseline */
h2 { line-height: 48px; margin-bottom: 72px; }     /* 3 × baseline */
```

### Result

Every line of text on the page **baseline-aligns to the same invisible grid**. This is how professional print typography works.

---

## IV. Hit targets (tappable areas)

| Platform | Minimum | Recommended |
|------|------|------|
| Mobile | **44 × 44 px** | 48 × 48 px |
| Desktop | **32 × 32 px** | 40 × 40 px |
| Dense toolbar | 24 × 24 px | 28 × 28 px |

**Rule:** the visible icon can be ≤ 24px, but the **hit target (icon plus padding) must meet the minimum**.

---

## V. Alignment

### Left vs centered vs justified

| Case | Choice |
|------|------|
| Body paragraphs | **Left-aligned** |
| Title (≤ 2 lines) | Center is OK |
| Title (> 2 lines) | **Left-aligned** |
| Number columns / prices | Right-aligned |
| Tables | Per column type: text left, numbers right |
| Mixed Latin + CJK body copy | **Left-aligned**, never justified (width mismatch between scripts produces ugly gaps) |

### Forbidden

- Centered multi-line titles (eye has to jump)
- Justified short body copy (creates white rivers)

---

## VI. Three principles of whitespace

### 1. The most important element gets the most whitespace around it

```
Hero section padding 128px top/bottom
Between sections 64-96px
Card inner padding 24-32px
Line spacing 8-12px
```

The more important → the more room to breathe.

### 2. Related elements cluster, unrelated elements separate (Gestalt proximity)

```css
/* Correct */
.card {
  title       → 8px to description
  description → 16px to metadata
  metadata    → 48px to the next card
}

/* Wrong: every gap is identical */
.card {
  all gaps 16px  /* no way to see what groups together */
}
```

### 3. Outer whitespace > inner whitespace

Space between cards should be **larger** than the padding inside each card. Otherwise the grid reads as one mass.

```css
.card { padding: 24px; }
.card-grid { gap: 48px; }   /* gap 2x padding */
```

---

## VII. Border radius

One scale across the whole project. Do not invent a new radius per component.

```css
:root {
  --radius-sm:   4px;   /* small tag */
  --radius-md:   8px;   /* buttons, inputs */
  --radius-lg:   12px;  /* cards */
  --radius-xl:   20px;  /* large panels */
  --radius-full: 9999px; /* circles / pills */
}
```

### Rules

- **Same hierarchy level → same radius** (every card is 12px)
- Nesting: **inner < outer** (outer card 12px → inner badge 6px)
- Minimalist style: **all 0 or all 8px**, never mix
- Forbidden: asymmetric corners like `border-radius: 16px 4px 16px 4px` (a 2010-era tic)

---

## VIII. Shadow system

Three tiers at most. Do not mint a new shadow per element.

```css
:root {
  /* soft, realistic shadows (not Material Design's heavy style) */
  --shadow-sm: 0 1px 2px rgba(0,0,0,.04), 0 1px 3px rgba(0,0,0,.06);
  --shadow-md: 0 4px 12px rgba(0,0,0,.06), 0 2px 4px rgba(0,0,0,.04);
  --shadow-lg: 0 12px 40px rgba(0,0,0,.08), 0 4px 12px rgba(0,0,0,.06);
}
```

### Rules

- Shadows are **always multi-layer** (a single hard shadow looks cheap)
- `rgba` alpha ≤ 0.12, otherwise too heavy
- In dark mode, soften shadows drastically or replace with borders

---

## IX. Self-check

- [ ] Every padding/margin is a multiple of 4 or 8
- [ ] 3-5 spacing tokens defined; no inline magic numbers
- [ ] Hit target ≥ 44px (mobile) or 32px (desktop)
- [ ] Related spacing < unrelated spacing (at least 2x ratio)
- [ ] Outer spacing > inner spacing
- [ ] Border radius tokens unified; no mixing
- [ ] Shadows capped at 3 tiers
