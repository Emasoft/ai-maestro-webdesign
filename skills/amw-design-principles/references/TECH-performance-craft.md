---
name: TECH-performance-craft
category: design-principles-quality-gate
source: clean-room reimplementation (T-057 batch9 Wave 2; Core Web Vitals thresholds are published by Google web.dev (CC-BY-4.0 documentation); image-format guidance is common knowledge in modern web-perf practice — no verbatim copy)
license: this file = MIT (plugin license); NO verbatim copy from any GPL-2.0 source — thresholds cite the Google web.dev public spec
also-in: `agents/amw-browser-tester-agent.md` (runs Lighthouse / scenario tests against these targets); `agents/amw-wireframe-builder-agent.md` (validates page budget at HTML emit time); `agents/amw-asset-generator-agent.md` (image format decision tree)
---

# Performance craft — hard limits, budgets, and the format decision tree

## Table of Contents

- [What this is](#what-this-is)
- [Core Web Vitals — hard limits](#core-web-vitals--hard-limits)
- [Page weight budget](#page-weight-budget)
- [Image format decision tree](#image-format-decision-tree)
- [Picture element pattern](#picture-element-pattern)
- [Font loading strategy](#font-loading-strategy)
- [The competitor-median minus 20% rule](#the-competitor-median-minus-20-rule)
- [Cross-references](#cross-references)

## What this is

A hard quality gate for every page the plugin emits. Performance is treated as a craft discipline, not a "we'll optimize later" item. If a page fails any of the limits below, `amw-browser-tester-agent` returns a non-passing report and `amw-wireframe-builder-agent` must remediate before delivery.

The targets are 2024–2026 conventions: Core Web Vitals from Google's public web.dev documentation, page budget aligned with the HTTPArchive p75 trend, image-format decisions consistent with current browser support.

## Core Web Vitals — hard limits

These are non-negotiable. Every page the plugin ships must pass all four on **mobile 4G simulation** (Lighthouse default).

| Metric | Limit | What it measures |
|---|---|---|
| **LCP** (Largest Contentful Paint) | **< 2.5 s** | Time from navigation start until the largest above-the-fold element finishes painting. Usually the Hero image, headline, or product screenshot. |
| **INP** (Interaction to Next Paint) | **< 200 ms** | Time from a user interaction (click, tap, key press) until the next paint. Replaces FID as of 2024. |
| **CLS** (Cumulative Layout Shift) | **< 0.1** | Sum of unexpected layout shifts across the page lifecycle. Caused by images without dimensions, web fonts loading late, ad insertions, dynamic content above existing content. |
| **TTI** (Time to Interactive) | **< 3.8 s** | Time from navigation until the main thread is idle long enough to respond to input. Driven by JS parse/eval. |

**Common failure modes and fixes:**

| Failing metric | Common cause | Standard fix |
|---|---|---|
| LCP > 2.5 s | Hero image is the LCP element and isn't preloaded | `<link rel="preload" as="image" href="hero.webp" fetchpriority="high">` + serve from same origin |
| LCP > 4 s | Web font on H1 + no `font-display: swap` | Use `font-display: swap`; preload the font file with `<link rel="preload" as="font">` |
| INP > 200 ms | Heavy main-thread work on click (chart render, full-state sync) | Break work into smaller chunks with `requestIdleCallback` or `scheduler.yield()` |
| CLS > 0.1 | Images without `width` + `height` attributes | Always set explicit dimensions; use `aspect-ratio` CSS as a fallback |
| CLS > 0.25 | Web fonts loading and shifting text | `font-display: optional` for non-critical fonts; use `size-adjust` to match fallback metrics |
| TTI > 3.8 s | JS > 200KB gzipped | Code-split; defer non-critical JS; consider whether a JS framework is needed at all for this page |

A passing report from `amw-browser-tester-agent` includes the four metric values, the device profile they were measured on (default: Lighthouse mobile 4G), and the LCP element identified.

## Page weight budget

These caps apply to the **total transferred bytes** across the page lifecycle, measured on initial load (no warm cache):

| Resource type | Cap | Notes |
|---|---|---|
| **Total transferred** | **< 1.5 MB** | Above this, mobile users on 4G see > 5 s LCP regardless of optimization |
| **JavaScript (gzipped)** | **< 200 KB** | Above this, TTI risk on mid-tier devices; framework choice becomes a perf concern |
| **CSS (gzipped)** | **< 50 KB** | Above this, render-blocking parse delay; consider critical-CSS inlining |
| **Images (total)** | **< 800 KB** | Above this, LCP suffers; consider format change or lazy-loading below the fold |
| **Web fonts (total)** | **< 100 KB** | 2 weights × 2 styles is typically enough; ban full-family imports |
| **Requests (initial)** | **< 50** | Each request adds latency on 4G; consolidate via bundling, sprites, inlined SVG |
| **Third-party requests** | **≤ 5** | Above this, the page's perf is held hostage by third parties; audit each one |

These caps are aligned with the HTTPArchive 2024–2026 p25 — i.e., the top 25% of pages by performance. Hitting them puts a page in the top-quarter, not the median.

**Hard "you have to ship under this" caps:**

- Total transferred < 1.5 MB on initial load
- JS < 200 KB gzipped
- Image total < 800 KB

The other caps are guidelines — if you bust them but stay under the three hard caps AND pass Core Web Vitals, that's acceptable. Bust the three hard caps and the page fails the gate regardless of CWV.

## Image format decision tree

For any image the plugin emits or embeds, use this decision tree. It encodes 2024–2026 browser support and quality trade-offs.

```
START
  │
  ├─ Is the image a photograph / illustration with smooth gradients?
  │      │
  │      ├─ YES
  │      │     │
  │      │     ├─ Need transparency?      ───►  AVIF  (fallback WebP for older browsers)
  │      │     │                                with <picture> fallback chain
  │      │     │
  │      │     └─ No transparency needed  ───►  AVIF  (fallback WebP, fallback JPEG)
  │      │                                       — AVIF gives ~30–50% smaller than WebP
  │      │
  │      └─ NO (graphic / logo / icon)
  │            │
  │            ├─ Vector available?       ───►  SVG  (inline if < 4 KB, else <img>)
  │            │
  │            ├─ Need transparency?      ───►  PNG  (or AVIF/WebP if photo-like)
  │            │                                use lossy PNG (pngquant) when possible
  │            │
  │            └─ Solid color + no transparency ─►  JPEG  (rarely correct; usually want SVG or WebP)
  │
  └─ Special case: animated image?
        │
        ├─ Short loop (< 3 s, < 30 frames)  ───►  WebP  animated  (NOT GIF — GIF is 5–10× larger)
        │
        └─ Long playback                     ───►  MP4 / WebM video  with poster image
                                                  + autoplay muted playsinline
```

**Format quality settings (defaults the plugin uses):**

| Format | Quality setting | Tool |
|---|---|---|
| AVIF | 65 (perceptually equal to JPEG 85) | `cavif` / Squoosh |
| WebP | 80 | `cwebp -q 80` |
| JPEG | 85 (only when fallback needed) | `mozjpeg` |
| PNG | pngquant 8-bit palette where possible | `pngquant --quality=65-80` |
| SVG | minified, no metadata, no editor cruft | SVGO with default plugin set |

**Banned formats in 2024–2026:**

- **GIF** for anything — animated WebP or MP4 is always smaller.
- **BMP, TIFF** — never web-targets.
- **JPEG 2000 / JPEG XR** — Safari-only, never the right choice when AVIF + WebP cover all targets.

## Picture element pattern

Every above-the-fold image uses the `<picture>` element with the format chain, NOT `<img src>` alone. The chain handles older browsers gracefully:

```html
<picture>
  <source type="image/avif" srcset="hero.avif">
  <source type="image/webp" srcset="hero.webp">
  <img src="hero.jpg"
       alt="Descriptive alt text here"
       width="1200" height="800"
       fetchpriority="high"
       loading="eager">
</picture>
```

Below-the-fold images use `loading="lazy"` and drop `fetchpriority="high"`:

```html
<picture>
  <source type="image/avif" srcset="feature.avif">
  <source type="image/webp" srcset="feature.webp">
  <img src="feature.jpg"
       alt="Descriptive alt text"
       width="600" height="400"
       loading="lazy">
</picture>
```

**The always-required attributes on every `<img>`:**

- `alt` — descriptive (or `alt=""` if purely decorative)
- `width` and `height` — explicit, in pixels (prevents CLS)
- `loading="lazy"` for below-the-fold; `loading="eager"` for above-the-fold (default, omit)
- `fetchpriority="high"` on the LCP candidate ONLY (typically 1–2 images per page)

## Font loading strategy

Web fonts are the second-biggest CLS and LCP risk after images. The plugin's strategy:

1. **Subset to used characters.** A 400 KB full family with all weights becomes ~30 KB with just the characters you use. Use `fonttools subset` or a service like Bunny Fonts that does this automatically.
2. **Preload the critical font(s).** Hero typeface only — never preload more than 2 font files.
   ```html
   <link rel="preload" href="/fonts/inter-regular.woff2" as="font" type="font/woff2" crossorigin>
   ```
3. **Use `font-display: swap`** for all fonts. Visitors see fallback text immediately, then the web font swaps in when ready. No invisible-text period.
4. **Match fallback metrics with `size-adjust` and `ascent-override`** to minimize the layout shift when the swap happens:
   ```css
   @font-face {
     font-family: 'Inter';
     src: url('inter-regular.woff2') format('woff2');
     font-display: swap;
     size-adjust: 100%;
     ascent-override: 90%;
   }
   ```
5. **Cap weights/styles at 4 total** (e.g., Regular, Medium, Bold + Italic if used). Each additional weight is a separate request and adds ~25 KB.

## The competitor-median minus 20% rule

For a project's perf target, the orchestrator sets the budget at **20% under the competitor median** on every relevant metric. This is read from `amw-brand-researcher-agent`'s output during Phase A.

| Metric | If competitor median is | Your budget |
|---|---|---|
| LCP | 2.8 s | 2.24 s |
| Total transferred | 1.6 MB | 1.28 MB |
| JS gzipped | 220 KB | 176 KB |
| Lighthouse Perf score | 78 | 94 |

Two reasons for the 20% rule:

1. **Visitors notice 20% performance differences.** A page that's "as fast as the competition" feels equivalent; a page 20% faster feels noticeably better, especially on mobile.
2. **It forces a real perf decision.** "Match competitor" usually means defaulting to the same framework, image sizes, font stack. "Beat by 20%" forces at least one substantive choice — smaller hero image, drop the framework, subset fonts, switch image format.

The 20% rule is a starting point; for some markets (e.g., mobile-first in developing economies, conversion-critical SaaS funnels) the rule tightens to 40%.

## Cross-references

- `agents/amw-browser-tester-agent.md` — runs Lighthouse and scenario tests against the limits in this file; emits a pass/fail report per page.
- `agents/amw-wireframe-builder-agent.md` — validates the page weight budget at HTML emit time before delivery; rejects pages that bust the three hard caps.
- `agents/amw-asset-generator-agent.md` — applies the image format decision tree when emitting any image asset.
- `agents/amw-motion-designer-agent.md` — motion choices have INP cost; reads this file to know the 200 ms INP budget caps complex interaction animations.
- `agents/amw-brand-researcher-agent.md` — captures competitor median CWV during competitive research so the 20%-rule budget can be set.
- `skills/amw-design-principles/SKILL.md` — performance is rule 0 in the implicit hierarchy: a beautiful page that fails CWV is not a deliverable.
- `references/TECH-dial-configuration.md` — high MOTION_DRAMA and high INTERACTION_DEPTH push INP toward the cap; the dial config implicitly governs perf budget allocation.
- `references/runtime-conventions.md` — bundling, code-splitting, and asset-pipeline conventions that make these caps achievable.
