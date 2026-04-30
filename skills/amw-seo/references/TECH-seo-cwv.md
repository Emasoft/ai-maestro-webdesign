---
name: TECH-seo-cwv
category: seo-cwv
source: SKILLS-TO-INTEGRATE/web-design/seo-fundamentals/SKILL.md
also-in:
---

# TECH: Core Web Vitals — page-experience signals

## What it does

Core Web Vitals (CWV) measure **how users experience a page** — loading speed (LCP), interactivity latency (INP), and visual stability (CLS). They are a page-experience signal; they rarely override poor content but hold back otherwise-good pages.

## When to use

On every live-URL SEO evaluation and whenever the user asks about page performance, "why does this page rank", or CWV-adjacent terms (LCP, INP, CLS). Pair with `../amw-dev-browser/` for live capture.

## How it works

Three metrics, three thresholds:

| Metric | Target | What it reflects |
|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5 s | Loading performance — time until the largest above-fold element is visible |
| **INP** (Interaction to Next Paint) | < 200 ms | Interactivity — latency from a user interaction to the next paint |
| **CLS** (Cumulative Layout Shift) | < 0.1 | Visual stability — sum of unexpected layout shifts across the page's lifetime |

### Field data vs lab data

- **Field data** (CrUX — Chrome User Experience Report) is what Google uses for ranking signals. It's real-user data aggregated over 28 days.
- **Lab data** (Lighthouse, PageSpeed Insights) is synthetic — a single run under controlled conditions. Useful for diagnosing, not for judging ranking readiness.

### Important context

- CWV rarely override poor content. A page with A-grade CWV but empty content doesn't rank.
- They matter most when content quality is comparable — between two equally useful pages, the faster one wins.
- Failing CWV can HOLD BACK otherwise-good pages, not doom them.

## Minimal example

Evaluating a live page:

```bash
# Via dev-browser skill, with wait for SPA hydration
npx dev-browser ls https://example.com --wait 3000

# Measure LCP candidate — screenshot + performance API
npx dev-browser shot https://example.com --include-timing
```

Interpretation:

- LCP 3.1s → fail. Likely a large hero image not optimized; serve in AVIF, add `fetchpriority="high"`.
- INP 180ms → pass.
- CLS 0.18 → fail. Ads or embedded elements loading after initial paint; reserve space with explicit `width` / `height`.

*Attributed to the seo-fundamentals skill — `SKILLS-TO-INTEGRATE/web-design/seo-fundamentals/SKILL.md`.*

## Gotchas

- Lab CWV and field CWV can diverge significantly. A Lighthouse "100" site can have field data below threshold if real users have slow networks.
- CLS of 0.1 is the 75th percentile threshold. A single bad load can poison the whole month's field data.
- INP replaced FID (First Input Delay) in March 2024 as the interactivity metric. Older guides reference FID.
- Third-party scripts (ads, analytics, chat widgets) are the #1 cause of failing INP and CLS in practice.

## Cross-references

- `TECH-seo-eeat.md`, `TECH-seo-technical.md`, `TECH-seo-content-quality.md`
- `../SKILL.md`
- `../../amw-dev-browser/SKILL.md` — live capture for CWV diagnostics
