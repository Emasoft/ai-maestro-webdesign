# Color System — hard rules

> Color is not picked by eye. It is picked by **color space + contrast numbers + a structured palette**.

---

## I. Always prefer oklch over rgb / hex / hsl

### Why

- **rgb / hex:** adjacent values look uneven in perceived brightness (e.g. #4169E1 looks darker than #FF6347, yet their RGB sums are similar).
- **hsl:** the L (lightness) channel is a mathematical value, not a perceptual one.
- **oklch:** a color space designed around **human perception** — an oklch(50%) red and an oklch(50%) blue actually look equally bright.

### Syntax

```css
oklch(L% C H)
/*    ↑  ↑ ↑
      │  │ └ Hue 0–360 (red 30, orange 60, yellow 90, green 130, cyan 200, blue 260, purple 300, pink 0/360)
      │  └── Chroma 0–0.4 (0 = gray, 0.2 = mid-saturation, 0.3+ = vivid)
      └───── Lightness 0–100% (0 = black, 100 = white) */

oklch(62% 0.19 40)    /* Equation orange */
oklch(98% 0.005 85)   /* off-white background */
oklch(25% 0.04 240)   /* deep blue-black ink */
```

### Comfort ranges

| Use | L (lightness) | C (chroma) |
|------|--------|---------|
| Bright background | 95–99% | 0–0.02 |
| Large light-tinted surfaces | 85–95% | 0.02–0.05 |
| Primary (buttons / emphasis) | 45–70% | 0.12–0.22 |
| Body text | 15–25% | 0–0.03 |
| High-saturation accent | 55–75% | 0.22–0.32 |
| **Never** | L < 10 or > 99 | C > 0.35 (screen-pure, harsh on the eye) |

---

## II. WCAG contrast — hard requirement

| Text size | AA pass | AAA pass |
|---------|---------|---------|
| Body (< 18px) | **≥ 4.5 : 1** | ≥ 7 : 1 |
| Large text (≥ 18px, or 14px bold) | **≥ 3 : 1** | ≥ 4.5 : 1 |
| Non-text UI (button borders, icons) | ≥ 3 : 1 | — |

### Checking tools

- Browser devtools color picker — built-in contrast indicator.
- Command line: `npx wcag-contrast "#1a1a1a" "#fafaf7"`
- Figma / Sketch plugin: Stark.

**Rule:** before declaring a design finished, the **primary text + background** pair must pass AA. If it doesn't, adjust L. No exceptions.

---

## III. Palette structure (cap at 5–7 colors)

### Standard 6-color framework

```css
:root {
  /* 1. Primary (brand color — minimal use, accent only) */
  --primary: oklch(62% 0.19 40);

  /* 2. Surface (background layering) */
  --surface-0: oklch(99% 0.005 85);   /* page base */
  --surface-1: oklch(97% 0.008 85);   /* cards */
  --surface-2: oklch(94% 0.012 85);   /* nested cards */

  /* 3. Text (primary → tertiary) */
  --text-1: oklch(18% 0.01 260);      /* body */
  --text-2: oklch(45% 0.01 260);      /* secondary */
  --text-3: oklch(65% 0.01 260);      /* auxiliary */

  /* 4. Border */
  --border: oklch(88% 0.01 85);

  /* 5. Semantic (success / warning / danger) */
  --success: oklch(62% 0.15 150);
  --warning: oklch(72% 0.16 70);
  --danger:  oklch(58% 0.20 25);
}
```

### Rules

- **At most 6 core colors** (1 primary + 3 surface + 3 text + 1 border + 2 semantic = 10 tokens, but visually only 6 base colors).
- Before inventing a seventh, **ask yourself: can this be solved with a lightness / chroma variant of an existing color?**
- Neutrals occupy 80–90% of surface area; primary 5–10%; accents under 5%.

---

## IV. Dark mode is not a simple inversion

### Wrong approach

```css
/* Inverting the L value directly */
--text: oklch(18% ...);       /* light mode */
--text: oklch(82% ...);       /* dark mode (breaks contrast + looks washed out) */
```

### Right approach

```css
/* Re-palette for dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --surface-0: oklch(14% 0.01 260);    /* not pure black */
    --surface-1: oklch(18% 0.015 260);   /* smaller step between layers */
    --text-1: oklch(92% 0.005 85);       /* not pure white (harsh) */
    --text-2: oklch(72% 0.01 85);
    --primary: oklch(70% 0.18 40);       /* primary needs to be lighter in dark mode or it disappears */
  }
}
```

Rules:
- Dark backgrounds **never use #000** — use oklch(14% 0.01 ...) with a slight color temperature.
- Dark-mode text **never uses #fff** — use oklch(92% 0.005 ...) to avoid eye strain.
- Primary color in dark mode needs **L + 8–10%** (a dark background requires a brighter primary to stand out).

---

## V. Color temperature

Keep project color temperature consistent. Mixing temperatures makes the composition feel dirty.

| Temperature | Hue range (H) | Fits |
|------|----------|------|
| Warm | 20–80 (red / orange / yellow) | Editorial, food, mood, arts |
| Near-neutral warm | 85 (beige family) | Paper feel, journaling, lifestyle |
| Cool | 200–270 (cyan / blue) | Tech, tools, productivity |
| Near-neutral cool | 250 (blue-gray) | Enterprise, finance, serious |

**Rule:** the H values of primary + background + neutrals **must not cross temperatures**. If the primary is H=60 (orange) but the neutrals are H=250 (cool gray), it looks dirty. Use neutrals at H=85 (warm gray) instead.

---

## VI. Palette inspiration libraries (use these instead of inventing)

- **Radix Colors** — 12-step scales, semantic naming.
- **Tailwind Palette** — 50–950 gradient scales.
- **Open Color** — Nordic-style neutrals.
- **TokyoNight / Everforest / Catppuccin** — code-editor palettes worth borrowing.
- Physical print swatch books (Pantone, DIC) — more tactile than any on-screen palette.

Rule: **find an existing palette first, tweak it next, invent only as a last resort.**

---

## VII. Self-check list

Before shipping any HTML, verify:

- [ ] All colors use oklch (or at least the primary does).
- [ ] Body text vs. background contrast ≥ 4.5:1.
- [ ] Total palette ≤ 7 core colors.
- [ ] Primary color occupies ≤ 10% of surface area.
- [ ] No direct use of #000 or #fff.
- [ ] Color temperature is consistent (all H values within a 30-unit spread, or the spread has a deliberate reason).
