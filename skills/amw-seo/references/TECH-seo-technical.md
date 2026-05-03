---
name: TECH-seo-technical
category: seo-technical
source: SKILLS-TO-INTEGRATE/web-design/seo-fundamentals/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Crawl & index control](#crawl-index-control)
  - [Performance & accessibility (technical prerequisites for CWV)](#performance-accessibility-technical-prerequisites-for-cwv)
  - [Common technical failures](#common-technical-failures)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Technical SEO principles

## What it does

Technical SEO ensures pages are accessible, understandable, and stable for search engines. Crawl control, index signals, HTTP correctness, HTTPS, semantic HTML, mobile-friendliness — the plumbing that lets content be discovered and ranked.

## When to use

On every SEO audit. Technical issues are usually binary (present/absent, correct/incorrect) and block ranking regardless of content quality.

## How it works

### Crawl & index control

| Element | Purpose |
|---|---|
| XML sitemaps | Help discovery of new + updated content |
| robots.txt | Control crawl access + crawl budget |
| Canonical tags | Consolidate duplicate URLs |
| HTTP status codes | Communicate page state (200 ok, 301 moved, 404 gone, 410 deleted) |
| HTTPS | Security + trust — HTTP-only sites are effectively uncompetitive |
| `noindex` / `nofollow` | Selective exclusion from index |
| hreflang | Multi-region/language coordination |

### Performance & accessibility (technical prerequisites for CWV)

| Factor | Why it matters |
|---|---|
| Page speed | User satisfaction + CWV |
| Mobile-friendly design | Mobile-first indexing — Google crawls mobile version as primary |
| Clean URLs | Crawl clarity, user comprehension |
| Semantic HTML | Accessibility + content understanding |
| Schema.org / JSON-LD | Rich-result eligibility (see [TECH-seo-structured-data](TECH-seo-structured-data.md)) |
| Internal linking | Link equity flow, discoverability |

### Common technical failures

- Trailing-slash vs no-trailing-slash duplicates without canonicals
- Pagination pages indexed without rel=prev/next hints (deprecated but still useful signals)
- Infinite scroll without paginated URL alternatives
- JavaScript-rendered content without SSR or pre-rendering — crawlers see empty HTML
- 404s returning 200 status codes (soft 404s)

## Minimal example

Auditing a site with JavaScript-rendered pages:

```bash
# Check what Googlebot sees
curl -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" \
  https://example.com/product

# If the response is <html><body><div id="root"></div></body></html> — that's what Google indexes.
# Pre-rendering, SSR, or Static Site Generation is required.
```

*Attributed to the seo-fundamentals skill — `SKILLS-TO-INTEGRATE/web-design/seo-fundamentals/SKILL.md`.*

## Gotchas

- `noindex` in robots.txt does NOT work — `noindex` is a meta-robots / HTTP-header directive, not a robots.txt directive.
- Canonicalizing to a URL that then canonicals somewhere else creates a canonical chain; Google may ignore chained canonicals.
- Mobile-first indexing means the mobile version of the page is the canonical. If mobile has less content than desktop (hidden behind tabs, removed from the DOM), you lose that content for ranking.
- A sitemap listing URLs that return 404 damages crawl budget. Keep sitemaps clean and current.

## Cross-references

- [TECH-seo-cwv](TECH-seo-cwv.md), [TECH-seo-structured-data](TECH-seo-structured-data.md), [TECH-seo-content-quality](TECH-seo-content-quality.md)
  > [TECH-seo-content-quality.md] What it does · When to use · How it works · Page-level elements · Content quality signals · Intent classification · Minimal example · Gotchas · Cross-references
  > What it does · When to use · How it works · Field data vs lab data · Important context · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
