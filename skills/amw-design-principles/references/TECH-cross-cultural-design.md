---
name: TECH-cross-cultural-design
category: design-principles-process
source: cross-cultural design literature (clean-room synthesis, batch9 Wave 2 Round 3, T-174)
license: MIT (plugin-original under ../../../LICENSE)
also-in: TECH-named-color-shadow-techniques.md (Wu-Xing maps to perceptual hue families differently than HSL); spacing-rhythm.md (Fibonacci is one of several spacing scales); typography-system.md (waterfall is one of several type-scale strategies)
---

<!-- Clean-room rewrite from cross-cultural design literature (Five Phases color theory, Fibonacci spacing in Renaissance typography, Swiss-school typographic-waterfall scales). No upstream source code or proprietary content copied. Synthesised for batch9 Wave 2 Round 3, T-174. -->

<!-- CJK exception: This TECH file contains Chinese characters (五行) by design, as linguistic subject matter for the Wu-Xing five-phase palette section. The plugin-wide CJK-clean check exempts this file (parallel to the existing exemption for skills/amw-pretext/references/TECH-80-ja-typography.md and skills/amw-pretext/references/TECH-16-cjk-keep-all.md). Document this carve-out in any future ai-slop-check.py update. -->

# Cross-cultural design — Wu-Xing palette, Fibonacci spacing, typographic waterfall

## Table of contents

- [What it does](#what-it-does)
- [When this file fires](#when-this-file-fires)
- [Wu-Xing five-phase palette framework](#wu-xing-five-phase-palette-framework)
  - [The five phases and their hue families](#the-five-phases-and-their-hue-families)
  - [The 5 × 8 = 40-shade palette](#the-5--8--40-shade-palette)
  - [Cultural pairings — when to use, when to skip](#cultural-pairings--when-to-use-when-to-skip)
- [Fibonacci spacing scale](#fibonacci-spacing-scale)
  - [The values](#the-values)
  - [Why Fibonacci over 4 / 8 px linear scales](#why-fibonacci-over-4--8-px-linear-scales)
  - [Implementation as CSS variables](#implementation-as-css-variables)
- [Typographic waterfall scale](#typographic-waterfall-scale)
  - [The 0.75× ratio](#the-075-ratio)
  - [The reference waterfall](#the-reference-waterfall)
  - [Swiss 12 / 16-column grid pairing](#swiss-12--16-column-grid-pairing)
- [Worked example — Asian-market editorial site](#worked-example--asian-market-editorial-site)
- [Breaks if](#breaks-if)
- [Cross-references](#cross-references)

## What it does

Three cross-cultural design systems the plugin can mix into a design when the audience or aesthetic demands it. Each is independently useful; together they yield a palette + spacing + type system aligned with a non-Western or Swiss-modernist tradition rather than the default Material / Tailwind defaults.

The three are:
1. **Wu-Xing (五行) five-phase palette** — Five hue families (Wood / Fire / Earth / Metal / Water) × eight shades = a 40-shade palette anchored in East Asian color theory. Useful for products serving Chinese, Japanese, Korean, or Vietnamese audiences when a culturally-resonant palette beats the default tech-blue.
2. **Fibonacci spacing scale** — Geometric spacing values (8, 13, 21, 34, 55, 89, 144 px) instead of the linear 4 / 8 / 16 / 24 / 32 / 48 family. The accelerating step size mirrors the way the eye reads scale.
3. **Typographic waterfall** — Type-size scale built on a 0.75× ratio (64 → 48 → 36 → 27 → 20 → 15 → 12). Sharper hierarchy than the 1.25× (major-third) or 1.333× (perfect-fourth) modular scales typical in Western tools.

These are **alternative** systems, not replacements. The plugin's default tokens (Tailwind / spacing-rhythm.md / typography-system.md) cover most projects; reach for these when the project explicitly calls for them.

## When this file fires

Read this file when:
- The audience is **explicitly East Asian** (mainland China, Taiwan, HK, Japan, Korea, Vietnam, Singapore) and the brand wants culturally-resonant color choices.
- The brief asks for a **classical / editorial / Swiss-modernist** aesthetic (think large display type, generous whitespace, asymmetric grids).
- A previous variant felt "too Material" or "too generic SaaS" and the team wants a palette / spacing / type scale that signals craft.
- The site is information-dense (long-form editorial, museum, archive, government portal) and needs more hierarchy resolution than the default 1.25× scale provides.

Do NOT use this file for:
- Generic Western B2B SaaS (use the plugin defaults).
- Children's / consumer-playful brands (Wu-Xing reads serious / classical).
- Anything where the team cannot maintain the discipline a 0.75× waterfall demands (every screen needs deliberate type-size choice).

## Wu-Xing five-phase palette framework

The Five Phases (五行 *wǔ xíng*) classify color into five families. The plugin uses this as a *palette framework*, not as a metaphysical claim — the cultural resonance is what makes the palette feel right in East Asian markets.

### The five phases and their hue families

| Phase | Char | Element | Hue family (LCH H°) | Typical role |
|---|---|---|---|---|
| Wood | 木 | (sprouting, growth) | 110–140° (green) | Growth, vitality, "go" semantic |
| Fire | 火 | (heat, brightness) | 10–30° (red-orange) | Action, alert, "urgent" semantic |
| Earth | 土 | (ground, soil) | 60–85° (yellow-ochre) | Stability, "neutral warm" semantic |
| Metal | 金 | (refined, clarity) | 200–230° (cool grey-blue) | Precision, structure, "info" semantic |
| Water | 水 | (depth, flow) | 250–280° (deep blue / navy) | Wisdom, depth, "brand primary" default |

**Important constraint.** When using Wu-Xing as a literal cultural reference (e.g. a Lunar New Year campaign for a Chinese-language audience), all five phases appear together. When using it as a *palette structure* for general East Asian aesthetic, pick 2–3 phases and ignore the rest — five primary hues on a single screen is too noisy regardless of culture.

### The 5 × 8 = 40-shade palette

Each phase generates 8 shades, named by traditional Chinese color names where they exist. The plugin uses OKLCH internally for perceptual uniformity; the table below gives starting OKLCH triples that you'll then tune per brand.

```
Wood (木) — 110–140° hue band:
  --wood-50   oklch(96% 0.04 130)   /* 葱白 cōng-bái — onion white */
  --wood-100  oklch(92% 0.07 130)   /* 嫩绿 nèn-lǜ — tender green */
  --wood-200  oklch(86% 0.10 130)
  --wood-300  oklch(78% 0.13 130)
  --wood-400  oklch(68% 0.15 130)   /* 翠绿 cuì-lǜ — kingfisher green */
  --wood-500  oklch(58% 0.16 130)   /* primary */
  --wood-600  oklch(48% 0.16 130)
  --wood-700  oklch(38% 0.14 130)
  --wood-800  oklch(28% 0.10 130)
  --wood-900  oklch(18% 0.06 130)   /* 墨绿 mò-lǜ — ink green */

Fire (火) — 10–30° hue band:
  --fire-50   oklch(96% 0.04 25)
  ...
  --fire-500  oklch(60% 0.20 25)    /* 朱红 zhū-hóng — vermilion */
  ...
  --fire-900  oklch(20% 0.10 25)

(Earth 70°, Metal 215°, Water 265° — same pattern.)
```

Final per-brand calibration is mandatory — the OKLCH triples above are starting points, not specifications. Tune chroma and lightness to the specific product (a financial product wants Metal more desaturated; a food brand wants Fire more saturated).

### Cultural pairings — when to use, when to skip

| Pairing | Reads as | Use for |
|---|---|---|
| Water + Metal (deep blue + cool grey-blue) | Calm, precise, institutional | Fintech, B2B SaaS, professional services targeting EA |
| Wood + Earth (green + ochre) | Natural, traditional, grounded | Wellness, food, tea, organic / artisan |
| Fire + Earth (red-orange + ochre) | Festive, ceremonial, warm | Hospitality, dining, celebrations, Lunar New Year |
| Fire + Water (red + deep blue) | High-contrast, classical | Editorial, museum, scholarly |
| All five together | Literal Wu-Xing reference | Cultural campaigns, education, ceremonial only |

Do **not** pair Wood + Fire (green + red) without a strong neutral between them — that combination reads as "Christmas" in Western and Western-adjacent markets, which usually overrides the Wu-Xing reference.

## Fibonacci spacing scale

### The values

```
4   px  (extra-tight, hairline detail)
8   px
13  px
21  px
34  px
55  px
89  px
144 px
233 px (page-level only)
```

The leading 4 px (= F(3) doubled, or simply a hairline detail value) is included because pure Fibonacci starts at 1 / 1 / 2 / 3, which is too cramped to be useful in UI. Treat 4 px as an optional half-step before 8 px.

### Why Fibonacci over 4 / 8 px linear scales

A linear 8 px scale (8 / 16 / 24 / 32 / 40 / 48 / 56) gives near-uniform contrast between adjacent steps; everything feels evenly spaced.

A Fibonacci scale gives **accelerating** contrast — the jump from 21 → 34 is bigger than 8 → 13, and 89 → 144 is huge. This matches how the eye reads scale: small differences read as the same; only large gaps register as hierarchy. The result is **more obvious section breaks** without needing larger absolute spacing budgets.

The trade-off: Fibonacci spacing is harder to align to a strict 8-px grid. Use it when the design has a strong editorial / asymmetric character and the grid is loose; stick with 4 / 8 / 16 when the design needs tight 12-column or 16-column alignment with components from a library like shadcn or Material.

### Implementation as CSS variables

```css
:root {
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  13px;
  --space-4:  21px;
  --space-5:  34px;
  --space-6:  55px;
  --space-7:  89px;
  --space-8:  144px;
  --space-9:  233px; /* hero / page-level only */
}

/* Tailwind v4 — extend in CSS not JS */
@theme {
  --spacing-1:  4px;
  --spacing-2:  8px;
  --spacing-3:  13px;
  --spacing-4:  21px;
  --spacing-5:  34px;
  --spacing-6:  55px;
  --spacing-7:  89px;
  --spacing-8:  144px;
}
```

Use `--space-3` (13 px) for inline element gaps, `--space-5` (34 px) for component-to-component, `--space-7` (89 px) for section-to-section. The jumps are intentional and large.

## Typographic waterfall scale

A waterfall is a **steeply contrasting** type scale, named after the historic specimen sheets typesetters used to show off a face at multiple sizes from one block of text. The plugin's waterfall uses a 0.75× ratio (= 1.333⁻¹), reversed from the common "perfect fourth" modular scale.

### The 0.75× ratio

Each step is **75% of the previous one** as you read down the scale (or 1/0.75 ≈ 1.333× as you read up). At this ratio, three consecutive sizes never feel adjacent — every step is unmistakably bigger or smaller than the next. The cost is fewer levels of hierarchy available before sizes become unusable: a 0.75× waterfall offers ~6 usable steps from 64 px down to 12 px; a 1.25× modular scale would give ~10.

### The reference waterfall

```
64 px     /* H1 / display — page title */
48 px     /* H2 — section opener */
36 px     /* H3 — sub-section */
27 px     /* H4 — paragraph-lead */
20 px     /* H5 / large body */
15 px     /* body */
12 px     /* caption / metadata */
```

Use no more than **5 of the 7** levels on any single page — the entire point of this scale is contrast, and contrast disappears when every step is in use. Typical landing-page selection: 64 (hero H1) + 36 (section H2) + 20 (lead) + 15 (body) + 12 (caption).

### Swiss 12 / 16-column grid pairing

The waterfall scale pairs naturally with **12-column** (general purpose) or **16-column** (editorial / asymmetric) grids. Use the 16-column grid when you need columns of unequal width (1 col label + 11 col content + 4 col annotation, for instance) — this is the canonical Swiss editorial pattern.

```
Container: max-width 1440px, 32px gutters, 8px column-gap
12-column: column = (1440 - 32*2 - 8*11) / 12 ≈ 109 px
16-column: column = (1440 - 32*2 - 8*15) / 16 ≈ 79 px
```

For mobile, collapse to 4-column (default for small screens) or single-column for narrow phones. Do not try to scale the 12 / 16 grid down — restart from a smaller column count.

## Worked example — Asian-market editorial site

Brief: A Hong Kong design studio's portfolio. Audience: international + East Asian art directors. Aesthetic: high-craft, scholarly, restrained.

**Palette.** Water + Metal pair (institutional, calm).
- `--water-700` (#1a3a5c-equivalent OKLCH) for headings and primary CTA.
- `--metal-300` (#9aaeb8-equivalent) for keylines and dividers.
- `--metal-50` (off-white #f4f6f7) as background.
- Pure black (`#000`) for body text — the Water+Metal pair gives enough chromatic warmth that pure black does not read cold.

**Spacing.** Fibonacci. Page padding 89 px desktop / 34 px mobile. Section breaks 55 px. Paragraph gap 21 px. List-item gap 13 px.

**Type.** Waterfall — display Noto Serif TC at 64 px / regular weight; body Noto Sans TC at 15 px; captions Inter at 12 px / 600 weight. The display face does the heavy lifting; the rest is restrained.

**Grid.** 16-column, 1440 px max. The asymmetry of the 16-column grid lets the layout place small annotations in narrow side columns (a 3-col block of metadata next to a 10-col block of project description), which is the Swiss editorial signature.

The page reads simultaneously as "international design studio" and "East Asian craft tradition" without explicit cultural ornament. That is the goal of using this file's three systems together.

## Breaks if

- The team picks two adjacent Wu-Xing phases (e.g. Wood + Water) without a neutral between them. Adjacent phases in the Five-Phase cycle have a "destruction" relationship (相剋); the eye reads the pair as competing. Pair non-adjacent phases or use a strong neutral.
- Fibonacci spacing is applied to a component library that expects 4 / 8 px grids (shadcn, Material, IBM Carbon). Components break because their internal padding / line-height tables assume a linear scale.
- The waterfall is used at all 7 levels on one page. Three to five levels is the cap; more breaks the "every step is unmistakably different" promise.
- Wu-Xing is used decoratively as "Asian flavor" without understanding the cultural pairings table above. The classical pairings carry meaning; combining them randomly reads as kitsch in the target market.
- The team treats this file as the *default*. It is not — the plugin defaults (Tailwind tokens, 8 px spacing, 1.25× type scale) cover most projects. Reach for Wu-Xing / Fibonacci / waterfall only when the brief explicitly calls for a culturally-grounded or Swiss-modernist aesthetic.

## Cross-references

- [color-system.md](../color-system.md) — the default palette tokens this file's Wu-Xing palette replaces.
- [spacing-rhythm.md](../spacing-rhythm.md) — the default 4 / 8 px spacing scale this file's Fibonacci replaces.
- [typography-system.md](../typography-system.md) — the default 1.25× type scale this file's waterfall replaces.
- [TECH-named-color-shadow-techniques.md](TECH-named-color-shadow-techniques.md) — historical / culturally-named colors usable as Wu-Xing shade names.
- [TECH-css-modern-syntax.md](TECH-css-modern-syntax.md) — `oklch()` syntax used in the palette specifications above.
- `skills/amw-pretext/references/TECH-80-ja-typography.md` — Japanese-specific typography rules; pairs with Wu-Xing when the audience is Japanese.
- `skills/amw-pretext/references/TECH-16-cjk-keep-all.md` — CJK word-break rules for Chinese / Japanese / Korean content.
- [authority-hierarchy.md](authority-hierarchy.md) — `amw-multilanguage-copywriter-agent` and `amw-brand-researcher-agent` collaborate on Wu-Xing palette selection.
