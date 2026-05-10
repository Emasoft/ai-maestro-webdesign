# Typography system — hard rules

## Table of Contents

- [I. Modular type scale](#i-modular-type-scale)
- [II. Font-weight hierarchy (only 2–3 levels)](#ii-font-weight-hierarchy-only-23-levels)
- [III. Line-height](#iii-line-height)
- [IV. Letter-spacing](#iv-letter-spacing)
- [V. Font-pairing rules](#v-font-pairing-rules)
- [VI. Recommended font stacks (avoiding AI slop)](#vi-recommended-font-stacks-avoiding-ai-slop)
- [VII. Fallback-stack syntax](#vii-fallback-stack-syntax)

> Font size, weight, line-height, and letter-spacing are all numbers — there is no "aesthetic debate," only **scale selection**.

---

## I. Modular type scale

Every type size is derived from **one base** value using a fixed ratio. No improvising on the fly.

| Ratio | Name | Value | Best for |
|------|------|------|------|
| Minor Second | Minor Second | 1.067 | Ultra-conservative, high information density |
| Major Second | Major Second | 1.125 | Body-copy-heavy layouts |
| Minor Third | Minor Third | 1.2 | Standard web pages |
| **Major Third** | **Major Third** | **1.25** | **Default recommendation** |
| **Perfect Fourth** | **Perfect Fourth** | **1.333** | **Display work (landing pages, slides)** |
| Augmented Fourth | Augmented Fourth | 1.414 | High-contrast |
| Perfect Fifth | Perfect Fifth | 1.5 | Dramatic |
| Golden Ratio | Golden Ratio | 1.618 | Headline-driven visual impact |

### Default recommendation (Perfect Fourth, base = 16px)

```css
:root {
  --text-xs:  10px;   /* supporting */
  --text-sm:  12px;   /* labels */
  --text-base: 16px;  /* body */
  --text-lg:  21px;   /* emphasised paragraph */
  --text-xl:  28px;   /* subheading */
  --text-2xl: 37px;   /* H2 */
  --text-3xl: 50px;   /* H1 */
  --text-4xl: 66px;   /* Hero */
  --text-5xl: 88px;   /* Mega Hero */
}
```

> Pick one ratio and **use it for the entire project**. Do not mix 1.2 and 1.5.

---

## II. Font-weight hierarchy (only 2–3 levels)

| Role | Recommended weight |
|------|---------|
| Body | 400 (Regular) |
| Emphasis | 500 (Medium) or 600 (SemiBold) |
| Heading | 600–700 |
| Display (mega headings) | 700–900 |

**Forbidden**: shipping 300 / 400 / 500 / 600 / 700 all on the same page — visual control collapses.

---

## III. Line-height

| Context | Recommended line-height |
|------|---------|
| Body paragraphs | **1.5–1.7** |
| UI components (buttons, form fields) | 1.2–1.4 |
| Subheadings | 1.2–1.35 |
| Large headings / Display | 1.0–1.15 |
| Mixed Latin + CJK | +0.1 (10% extra over pure Latin) |

Rule: **the smaller the type, the taller the line; the larger the type, the tighter the line.**

---

## IV. Letter-spacing

| Context | Recommended |
|------|------|
| Large headings | **-0.02em to -0.03em** (negative, tighter) |
| Body | 0 (default) |
| Small ALL CAPS | +0.05em to +0.1em |
| CJK text | 0 by default; at very small sizes (≤10px) you can add +0.02em |

---

## V. Font-pairing rules

### Successful combinations

| Body | Heading | Effect |
|------|------|------|
| Sans-serif | Serif | Classic editorial (New Yorker) |
| Serif | Sans-serif | Modern authority (FT) |
| Sans-serif | Display from same family | Clean brand identity (Stripe) |
| Serif | Bold weight of same family | Literary texture |
| Two weights of one family | Two weights of one family | Content-driven, disciplined |

### Failure modes

- Serif + another Serif (visual conflict)
- Sans + another Sans (unless they are display variants from the same family)
- Three or more type families in one design — anything past two starts to smear

---

## VI. Recommended font stacks (avoiding AI slop)

### Latin

| Context | Recommended |
|------|-----|
| Editorial / storytelling | GT Alpina, Tiempos Text, Söhne, Untitled Sans |
| Tech / tooling | Suisse Int'l, Neue Haas Grotesk, Inter Display (NOT Inter) |
| Art / mood-driven | PP Editorial New, Reckless, Authentic Sans |
| Monospace accents | JetBrains Mono, Berkeley Mono, IBM Plex Mono |

### CJK / other scripts

Chinese-language fonts out of scope for this English-only plugin; keep your project's existing CJK stack.

### Banned list (AI slop)

- Inter (overused)
- Roboto (Android default)
- Arial / Helvetica (featureless)
- system-ui (unless deliberately chosen)
- Pacifico / Comic Sans (childish)

---

## VII. Fallback-stack syntax

```css
font-family:
  'Suisse Int\'l',              /* paid font */
  'Neue Haas Grotesk Text Pro', /* backup 1 */
  -apple-system, BlinkMacSystemFont,
  'Segoe UI', system-ui,         /* system final fallback */
  sans-serif;
```

Rule: **paid font → free font → system font → generic sans/serif.**
