---
name: TECH-seo-relative-importance
category: seo-technical
source: SKILLS-TO-INTEGRATE/web-design/seo-fundamentals/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Approximate weight hierarchy](#approximate-weight-hierarchy)
  - [The operational rule](#the-operational-rule)
  - [Remediation priority](#remediation-priority)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH: Relative importance of SEO factors

## What it does

There is no fixed ranking-factor order. But when competing pages are comparable, the factor weight tends to follow a predictable pattern. This TECH documents the approximate hierarchy and cautions against treating it as gospel.

## When to use

When prioritizing an SEO remediation — what to fix first when time and budget are bounded. Also when explaining to a stakeholder why technical SEO alone will not rescue poor content.

## How it works

### Approximate weight hierarchy

| Relative weight | Factor |
|---|---|
| Highest | Content relevance + quality |
| High | Authority + trust signals (E-E-A-T) |
| Medium | Page experience (CWV, UX) |
| Medium | Mobile optimization |
| Baseline | Technical accessibility (crawlable, indexable, HTTPS) |

### The operational rule

> **Technical SEO enables ranking; content quality earns it.**

A page with perfect technical SEO and thin content does not rank above a page with good-enough technical SEO and excellent content. Conversely, excellent content with broken technical SEO doesn't get indexed.

### Remediation priority

When triaging a site with multiple SEO issues:

1. **Baseline first** — fix crawl blockers, HTTPS, canonical errors, 404s in sitemap
2. **Content next** — close gaps in depth, originality, accuracy
3. **Authority + trust third** — author bios, citations, backlink outreach
4. **Page experience fourth** — CWV, mobile usability, load times

Attempting #4 before #1 wastes effort because Google can't see the improvements if pages are uncrawlable.

## Minimal example

Triage for a 500-page site scoring poorly on all axes:

- Priority 1 (week 1): fix 120 broken canonicals, remove 80 noindexed-but-in-sitemap pages, switch 40 pages to HTTPS
- Priority 2 (week 2-6): rewrite 50 thinnest pages (below 400 words) with research-backed depth; consolidate 30 duplicate topic clusters
- Priority 3 (week 4-8): add author bios + credentials on 200 content pages; outreach for 20 topical backlinks
- Priority 4 (week 6-10): optimize LCP on 10 highest-traffic templates (image compression, preload hints, server response tuning)

This sequence ensures each tier's work is visible to Google before the next tier begins.

*Attributed to the seo-fundamentals skill — `SKILLS-TO-INTEGRATE/web-design/seo-fundamentals/SKILL.md`.*

## Gotchas

- "Just fix CWV" is common bad advice — fast pages with bad content don't rank.
- "Just write more content" is equally bad — 500 thin pages hurt the site's aggregate quality signal more than not publishing them at all.
- The weight hierarchy drifts over time. In 2013, backlinks were #1; in 2026, content quality + E-E-A-T are. Don't treat this as permanent.
- Local SEO, mobile-only queries, YMYL topics, and e-commerce each have category-specific weights (NAP consistency, local citations, review count for Local Pack; merchant feed quality for Shopping).

## Cross-references

- [TECH-seo-eeat](TECH-seo-eeat.md), [TECH-seo-cwv](TECH-seo-cwv.md), [TECH-seo-technical](TECH-seo-technical.md), [TECH-seo-content-quality](TECH-seo-content-quality.md)
  > [TECH-seo-cwv.md] What it does · When to use · How it works · Field data vs lab data · Important context · Minimal example · Gotchas · Cross-references
  > [TECH-seo-technical.md] What it does · When to use · How it works · Crawl & index control · Performance & accessibility (technical prerequisites for CWV) · Common technical failures · Minimal example · Gotchas · Cross-references
  > [TECH-seo-content-quality.md] What it does · When to use · How it works · Page-level elements · Content quality signals · Intent classification · Minimal example · Gotchas · Cross-references
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-seo-measurement](TECH-seo-measurement.md)
  > What it does · When to use · How it works · Cross-validation examples · KPIs worth tracking vs vanity metrics · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
