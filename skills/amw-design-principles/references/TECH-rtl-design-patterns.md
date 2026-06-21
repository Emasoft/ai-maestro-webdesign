---
name: TECH-rtl-design-patterns
category: design-principles-process
source: clean-room synthesis of RTL design practice (batch9 Wave 2 Round 4, T-170)
license: MIT (plugin-original under ../../../LICENSE)
also-in: TECH-cross-cultural-design.md (cultural design context for non-Western audiences); TECH-css-modern-syntax.md (logical properties: margin-inline-start, padding-block-end); TECH-css-variable-discipline.md (RTL-aware tokens); typography-system.md (Arabic / Hebrew / Persian font-stack rules)
---

<!-- Clean-room synthesis of right-to-left web-design practice (typographic + iconographic + bidirectional-text patterns) commonly documented in MDN, W3C i18n drafts, and major-vendor RTL handoffs. No copyrighted material reproduced. Authored for batch9 Wave 2 Round 4, T-170. -->

# RTL design patterns — beyond mirroring the layout

## Table of contents

- [What it does](#what-it-does)
- [When this file fires](#when-this-file-fires)
- [The four problem areas — overview](#the-four-problem-areas--overview)
- [Token block — RTL-aware design tokens](#token-block--rtl-aware-design-tokens)
- [Typography — Arabic / Hebrew / Persian needs](#typography--arabic--hebrew--persian-needs)
- [Iconography — what mirrors and what doesn't](#iconography--what-mirrors-and-what-doesnt)
- [Motion direction — entry / exit / progress](#motion-direction--entry--exit--progress)
- [Bidirectional text — numbers, dates, mixed scripts](#bidirectional-text--numbers-dates-mixed-scripts)
- [CSS logical properties — the safe way to write RTL-ready CSS](#css-logical-properties--the-safe-way-to-write-rtl-ready-css)
- [Worked example — an RTL-aware navbar](#worked-example--an-rtl-aware-navbar)
- [Breaks if](#breaks-if)
- [Cross-references](#cross-references)

## What it does

Most teams' RTL plan is "set `dir="rtl"` and let the browser flip the layout." This works for the easy 60% — flexbox direction, paragraph alignment, simple margins. The remaining 40% is where designs break: typography needs different fonts and tighter line-heights, half the icons must NOT mirror, motion direction inverts, bidirectional text (Arabic prose with embedded Latin product names or English numbers) needs explicit `unicode-bidi` handling, and number / date / currency display follows locale-specific conventions that don't follow the writing direction.

This file gives the patterns and the CSS for each of the four problem areas, with concrete code samples and a worked example.

## When this file fires

- The audience includes **Arabic** (Saudi Arabia, UAE, Egypt, Morocco, etc.), **Hebrew** (Israel), **Persian / Farsi** (Iran), **Urdu** (Pakistan, parts of India), **Sindhi**, **Yiddish**, **Pashto**, or any other RTL language.
- The brief mentions "internationalisation" / "i18n" / "right-to-left" / "Arabic version" / "Hebrew localisation"
- The product currently ships LTR-only and the team is planning RTL support
- Bidirectional text appears in the UI (a Hebrew customer's name in an English admin tool; an Arabic product description with English SKU codes)

Do NOT read this file for:
- LTR-only products with no localisation plan
- Products where the RTL audience is incidental and is served the LTR version (decide upfront whether to invest)

## The four problem areas — overview

| Area | What "set dir=rtl" handles | What it doesn't |
|---|---|---|
| **Typography** | Text alignment, paragraph direction | Font choice, line-height tuning, x-height/cap-height mismatch with LTR fonts |
| **Iconography** | Container flexbox direction | Which icons should and shouldn't mirror (chronology / brand / direction-of-progress) |
| **Motion** | Nothing | Entry-from-right becomes entry-from-left; toast slide-in direction; progress-bar fill direction |
| **Bidirectional text** | Basic paragraph-level direction | Mixed-script runs (Arabic + English + numbers); locale-specific number / date / currency formatting |

The browser handles the easy 60%. Your job is the 40%.

## Token block — RTL-aware design tokens

Stop using directional tokens (`--padding-left`, `--icon-margin-right`). Use logical-property tokens that flip with `dir`:

```css
:root {
  /* Direction-neutral logical tokens — flip automatically with dir */
  --inline-start-pad: 1rem;       /* was --pad-left */
  --inline-end-pad: 1rem;          /* was --pad-right */
  --block-start-pad: 0.75rem;     /* was --pad-top */
  --block-end-pad: 0.75rem;        /* was --pad-bottom */

  /* RTL font stacks — bind to language-specific fonts */
  --font-arabic: "Noto Sans Arabic", "Cairo", "Segoe UI Arabic", "Tahoma", sans-serif;
  --font-hebrew: "Noto Sans Hebrew", "Heebo", "Arial Hebrew", "Tahoma", sans-serif;
  --font-persian: "Noto Sans Persian", "Vazir", "IRANSans", "Tahoma", sans-serif;

  /* Line-height — RTL scripts need more vertical room */
  --line-height-rtl-body: 1.7;     /* vs 1.5 for Latin */
  --line-height-rtl-heading: 1.4;  /* vs 1.2 for Latin */

  /* Motion direction — flipped automatically below */
  --motion-x-enter: 8px;            /* enter from the inline-start direction */
  --motion-x-exit: -8px;
}

[dir="rtl"] {
  --motion-x-enter: -8px;
  --motion-x-exit: 8px;
}

[lang|="ar"] { font-family: var(--font-arabic); line-height: var(--line-height-rtl-body); }
[lang|="he"] { font-family: var(--font-hebrew); line-height: var(--line-height-rtl-body); }
[lang|="fa"] { font-family: var(--font-persian); line-height: var(--line-height-rtl-body); }
```

The `[lang|="ar"]` selector matches `lang="ar"` and any `lang="ar-EG"`, `lang="ar-SA"`, etc. — the regional Arabic variants.

## Typography — Arabic / Hebrew / Persian needs

Three rules:

1. **Use a script-specific font.** Latin-only fonts (Inter, Roboto, system-ui) fall back to platform Arabic/Hebrew fonts that may have a completely different feel, x-height, and weight axis. Always pair the Latin font with a matched script-specific stack.

2. **Increase line-height.** Arabic and Persian have descenders and connector loops that extend below the baseline; Hebrew vowel points (niqqud) extend above. Latin's 1.5 line-height feels cramped in Arabic; use 1.7. Headings need 1.4 instead of 1.2.

3. **Right-align body text** in RTL contexts. The browser does this automatically when `dir="rtl"` is set on the document or container. Don't force `text-align: left` anywhere in the cascade — use `text-align: start` (logical) and let the direction control it.

```html
<html lang="ar" dir="rtl">
<head><style>
  body {
    font-family: var(--font-arabic);
    line-height: var(--line-height-rtl-body);
  }
  h1, h2, h3 { line-height: var(--line-height-rtl-heading); }
  .article-body { text-align: start; }   /* logical: justifies right in RTL */
</style></head>
<body>
  <article class="article-body">
    <h1>تصميم الويب من أجل القراء العرب</h1>
    <p>هذا نص تجريبي مع <strong>تأكيد</strong> ومصطلح إنجليزي
       مدمج مثل <span lang="en">CSS Grid</span> داخل الفقرة.</p>
  </article>
</body>
</html>
```

The `<span lang="en">` annotation tells the browser to render that span in the LTR Latin font from the stack; without it, "CSS Grid" would render in the Arabic-script fallback, which is wrong.

## Iconography — what mirrors and what doesn't

The hardest part of RTL is iconography. The wrong icon-mirror choice produces brand damage on the RTL site that nobody notices on the LTR site.

### Mirror these icons

Icons whose meaning is direction-relative (the meaning depends on which way they point):

- **Back / forward arrows.** A "back" arrow points to where the user came from; in RTL, that's the right side. Mirror.
- **Pagination prev / next arrows.** Same reasoning. Mirror.
- **Breadcrumb separators (chevrons).** The chevron points forward in the reading direction. Mirror.
- **Progress bars and steppers.** Fill direction follows reading direction. Mirror via `transform: scaleX(-1)` on the fill or use logical CSS.
- **Chat-bubble tails.** "Sent" messages point inward to the user's side. The user's side is opposite in RTL. Mirror.
- **Sliders / range inputs.** Min on the start (right in RTL), max on the end (left in RTL). Browser handles this if you use the native input.
- **Quote marks.** Opening quote on the start, closing on the end. CSS `quotes` property handles this.

### Do NOT mirror these icons

Icons whose meaning is absolute (mirroring would invert or destroy the meaning):

- **Brand logos and product marks.** A logo is fixed. Mirroring "Coca-Cola" backwards is brand damage, not localisation.
- **Chronological / time-direction arrows.** "Past → Future" is a left-to-right metaphor in LTR but Arabic/Hebrew readers ALSO read time-charts left-to-right (it's a cross-cultural convention, not a reading-direction one). Don't mirror clocks, calendar timelines, history graphs, or rewind/forward media controls.
- **Media controls.** Play (▶), rewind, fast-forward all stay the same — the conventions are global. Audio waveforms are LTR even on Arabic sites.
- **Letters / numbers in the icon.** A "G" icon doesn't mirror. A "+1" notification doesn't mirror.
- **Real-world objects.** A pencil, a hammer, a key — all keep their original orientation. Mirroring a key icon makes it look broken.
- **Mathematical / scientific symbols.** ∑, ∫, →, mathematical operators stay LTR even in RTL contexts; this is the global convention.
- **Direction-of-progress in horizontal layouts where the progression is metaphorical, not reading-driven.** A flowchart of "input → process → output" stays LTR in RTL contexts unless the team has explicitly localised the conceptual direction.

### The decision tree

```
Does the icon's meaning depend on reading direction?
├── YES → mirror in RTL
│   Examples: back/next arrows, progress bars, chat-bubble tails
└── NO → do NOT mirror
    Examples: logos, clocks, media controls, mathematical symbols, real-world objects
```

### CSS for the cases that DO mirror

```css
/* Use a single rule with logical properties — flips automatically */
.icon-back svg {
  /* Points to inline-start direction; LTR=left, RTL=right */
}

/* Or explicitly flip via transform when the icon SVG is fixed */
[dir="rtl"] .icon-arrow-forward svg {
  transform: scaleX(-1);
}

/* The progress bar — fill from start to end */
.progress-bar__fill {
  width: var(--progress);
  inset-inline-start: 0;   /* anchors to start edge; flips */
  /* NOT: left: 0; — that's fixed in absolute space */
}
```

### CSS to LOCK an icon against mirroring

Use the `bdi` element or the `dir="ltr"` attribute to force LTR rendering of a child even in RTL contexts:

```html
<span dir="rtl">
  زيارة <bdi dir="ltr">github.com/Emasoft</bdi> للحصول على المصدر
</span>
```

Or with CSS:

```css
.brand-logo,
.media-play-button,
.clock-icon { direction: ltr; }
```

## Motion direction — entry / exit / progress

Motion in LTR animations assumes time flows left-to-right. RTL inverts this for direction-relative motion only — same rule as icons.

| Motion | LTR | RTL |
|---|---|---|
| Toast slide-in (from "edge") | right edge | left edge |
| Drawer slide-in | from one side | from the OTHER side |
| Page-transition slide | next page enters from right | next page enters from left |
| Progress bar fill | grows leftward to rightward | grows rightward to leftward |
| Confetti / fireworks (chronological) | particles fly upward + outward | same — direction-neutral |
| Loading spinner | clockwise | clockwise — keep |

Use logical CSS where possible:

```css
.toast {
  position: fixed;
  inset-inline-end: 1rem;   /* anchors to end edge; flips */
  inset-block-end: 1rem;
  transform: translateX(0);
  transition: transform 0.2s ease-out;
}
.toast--entering {
  /* Slide in from the inline-end direction */
  transform: translateX(var(--motion-x-enter));  /* flips via the dir override */
}
```

When `transform` is involved (which is direction-naive), bind the value to a token (`--motion-x-enter`) that you flip in the `[dir="rtl"]` selector. See the token block above.

## Bidirectional text — numbers, dates, mixed scripts

The hardest pattern. Arabic / Hebrew / Persian users see English product names, English-language SKU codes, ASCII URLs, English numbers (Western Arabic digits 0-9 vs Eastern Arabic-Indic digits ٠-٩) every day. Mixed-script text needs explicit annotation; otherwise the browser's Unicode Bidi Algorithm guesses, and guesses wrong.

### Numbers — three Arabic-numeral systems

| System | Digits | Used in |
|---|---|---|
| **Western Arabic** | 0 1 2 3 4 5 6 7 8 9 | Most Arab countries (Egypt, Morocco, Lebanon, Saudi Arabia for commerce / receipts) |
| **Eastern Arabic-Indic** | ٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩ | Religious / formal / literary contexts in Arabic; default in Iran (Persian) |
| **Bengali / Devanagari** | various | South Asian RTL contexts (Urdu uses Eastern Arabic-Indic) |

When showing numbers, the locale matters more than the script direction. UAE, Saudi Arabia, Egypt — most ecommerce and SaaS use Western Arabic digits. Iran and religious / literary Arabic content use Eastern Arabic-Indic. Don't guess; ask the localisation team or default to Western Arabic for commerce.

CSS:

```css
/* Force Western Arabic digits in a commercial context */
.price, .quantity, .order-number { font-feature-settings: "lnum" 1; }

/* Use Intl.NumberFormat for runtime locale-correct rendering */
```

```js
new Intl.NumberFormat("ar-EG", { useGrouping: true }).format(1234567);
// → "١٬٢٣٤٬٥٦٧" in Eastern Arabic-Indic (default for ar-EG)
new Intl.NumberFormat("ar-EG", { numberingSystem: "latn" }).format(1234567);
// → "1,234,567" in Western Arabic
```

### Dates — locale-correct formatting

`Intl.DateTimeFormat` handles the heavy lifting. Don't string-format dates manually.

```js
new Intl.DateTimeFormat("ar-SA", { dateStyle: "long" }).format(new Date());
// → "٢٧ مايو ٢٠٢٦" (Saudi Arabic, Eastern digits)

new Intl.DateTimeFormat("he-IL", { dateStyle: "long" }).format(new Date());
// → "27 במאי 2026" (Hebrew, Western digits)
```

### Currency — symbol placement

Currency symbol placement varies by locale, not just by script direction. `Intl.NumberFormat` handles it:

```js
new Intl.NumberFormat("ar-AE", { style: "currency", currency: "AED" }).format(99);
// → "د.إ.‏ ٩٩٫٠٠"

new Intl.NumberFormat("he-IL", { style: "currency", currency: "ILS" }).format(99);
// → "‏99.00 ₪"
```

Never hardcode `$99` or `€99` — wrap in `Intl.NumberFormat` even for LTR locales; the RTL flip will then be correct for free.

### Mixed-script paragraphs — the `dir="auto"` attribute

When user-generated content might be in either direction (a comment, a chat message, a product review), use `dir="auto"`. The browser uses the first strong-directional character to decide:

```html
<p dir="auto">User comment: this product is great!</p>
<p dir="auto">تعليق المستخدم: هذا المنتج رائع!</p>
<!-- Browser detects each correctly via the first strong character -->
```

### Mixed-script inline — the `bdi` element

When LTR content (a product name, a URL, a hashtag) appears inline inside an RTL paragraph, wrap it in `<bdi>` (Bidi Isolate) to prevent the surrounding bidi algorithm from rearranging punctuation around it:

```html
<p>
  لتنزيل المنتج، قم بزيارة <bdi>github.com/Emasoft/repo</bdi>
  أو ابحث عن <bdi>"my-awesome-product"</bdi> على الإنترنت.
</p>
```

Without `<bdi>`, the surrounding Arabic text can pull the punctuation (parens, periods, slashes) onto the wrong side of the Latin text.

## CSS logical properties — the safe way to write RTL-ready CSS

Stop using `margin-left` / `padding-right` / `left: 0` / `text-align: right`. Use logical properties. They flip automatically with `dir`.

| Don't use | Use |
|---|---|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-top` | `padding-block-start` |
| `padding-bottom` | `padding-block-end` |
| `left: 0` | `inset-inline-start: 0` |
| `right: 0` | `inset-inline-end: 0` |
| `top: 0` | `inset-block-start: 0` |
| `bottom: 0` | `inset-block-end: 0` |
| `text-align: left` | `text-align: start` |
| `text-align: right` | `text-align: end` |
| `border-left` | `border-inline-start` |
| `border-radius: 8px 0 0 8px` | `border-start-start-radius: 8px; border-end-start-radius: 8px;` |

Browser support is universal in modern browsers (Chrome 87+, Firefox 66+, Safari 14.1+). For older browsers, write the logical properties first and let a PostCSS plugin (`postcss-logical`) emit physical fallbacks.

Shorthand cheatsheet:

```css
/* inset = top/right/bottom/left */
.card { inset: 0; }  /* same in LTR and RTL */

/* inset-inline = start + end */
.card { inset-inline: 1rem; }  /* shorthand for inset-inline-start + inset-inline-end */

/* margin / padding shorthands have logical-block-axis versions */
.card { margin-block: 1rem 2rem; }  /* top in LTR/RTL, bottom in LTR/RTL */
.card { margin-inline: 1rem; }       /* both sides */
```

See `TECH-css-modern-syntax.md` for the wider CSS-modern feature list; logical properties are listed there as well, but this file goes deeper on the RTL motivation.

## Worked example — an RTL-aware navbar

A navbar with a logo, three nav links, a language toggle, and a primary CTA. Built to work in both LTR and RTL without duplicate CSS.

```html
<html lang="ar" dir="rtl">
<head><style>
  .nav {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding-block: 0.75rem;
    padding-inline: 1.5rem;
    border-block-end: 1px solid var(--border-color);
  }
  .nav__logo {
    /* Logo does NOT mirror — direction:ltr locks it */
    direction: ltr;
    margin-inline-end: auto;  /* pushes everything else to inline-end */
  }
  .nav__links {
    display: flex;
    gap: 1.5rem;
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .nav__cta {
    padding-block: 0.5rem;
    padding-inline: 1rem;
    background: var(--cta-bg);
    color: var(--cta-fg);
    border-radius: 6px;
  }
  .nav__lang-toggle {
    /* Toggle button shows the *other* language label */
  }
</style></head>
<body>
  <nav class="nav">
    <a href="/" class="nav__logo">
      <img src="/logo.svg" alt="Acme">
    </a>
    <ul class="nav__links">
      <li><a href="/features">المميزات</a></li>
      <li><a href="/pricing">الأسعار</a></li>
      <li><a href="/docs">الوثائق</a></li>
    </ul>
    <button class="nav__lang-toggle" dir="ltr">English</button>
    <a href="/signup" class="nav__cta">إبدأ مجاناً</a>
  </nav>
</body>
</html>
```

When the same template is used with `dir="ltr"` and English copy, it renders LTR with zero CSS changes. The logo stays LTR via `direction: ltr`. The language toggle button stays LTR because its label is English. The `margin-inline-end: auto` on the logo pushes everything else to the inline-end side; in LTR that's the right, in RTL that's the left. The `padding-block` / `padding-inline` are direction-neutral.

## Breaks if

- The team flips icons indiscriminately. Logo mirroring, clock mirroring, and play-button mirroring are brand damage that nobody flags during the LTR review.
- Latin-only fonts are used for Arabic / Hebrew content. The browser falls back to the OS default, which gives the page a different feel from the LTR site (often worse).
- `text-align: left` and `margin-left` are hardcoded in component CSS. RTL stylesheets become a forest of `[dir="rtl"]` overrides that go out of sync with new components.
- Number formatting is hand-coded ("$99") instead of `Intl.NumberFormat`. RTL locales get the wrong digit system or the wrong currency-symbol position; trust collapses for the local audience.
- Bidirectional text isn't wrapped in `<bdi>` or `dir="auto"`. Mixed-script comments / reviews render with punctuation in the wrong place; the bug is invisible to LTR-only reviewers.
- Motion direction isn't flipped. Toasts slide in from the wrong side; users perceive the site as "ported from a foreign template" rather than locally designed.

## Cross-references

- [TECH-cross-cultural-design.md](TECH-cross-cultural-design.md) — Wu-Xing palette + Fibonacci spacing for East Asian audiences; companion to RTL for cross-cultural design coverage.
- [TECH-css-modern-syntax.md](TECH-css-modern-syntax.md) — CSS logical properties + container queries; the technical foundation for RTL-ready CSS.
- [TECH-css-variable-discipline.md](TECH-css-variable-discipline.md) — token authoring rules; the RTL-aware token block in this file follows them.
- [typography-system.md](../typography-system.md) — type-scale rules; line-height needs to lift for RTL scripts (this file overrides).
- [spacing-rhythm.md](../spacing-rhythm.md) — spacing scale; logical properties (`margin-inline-start` etc.) sit on top of this.
- [ai-slop-avoid.md](../ai-slop-avoid.md) — rejects mirror-everything-blindly RTL templates.
- [authority-hierarchy.md](authority-hierarchy.md) — `amw-accessibility-auditor-agent` flags `text-align: left` hardcodes (WCAG 1.3.2 Meaningful Sequence) in RTL audits.
