---
name: TECH-seo-measurement
category: seo-technical
source: SKILLS-TO-INTEGRATE/web-design/seo-fundamentals/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Cross-validation examples](#cross-validation-examples)
  - [KPIs worth tracking vs vanity metrics](#kpis-worth-tracking-vs-vanity-metrics)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Measurement — multi-signal SEO validation

## What it does

Evaluating SEO correctly means validating against **multiple signals**, never a single metric. Organic traffic alone, keyword rank alone, or CWV alone will each produce misleading conclusions. The measurement framework pairs five signal categories so that gaps in one surface through another.

## When to use

On every SEO audit, retrospective, or quarterly review. When someone asks "is our SEO working?", the answer requires data from multiple signal categories, not one.

## How it works

Five signal areas:

| Area | What to observe | Typical tools |
|---|---|---|
| **Visibility** | Indexed pages, impressions, rank distributions | Search Console, Ahrefs, Semrush |
| **Engagement** | Click-through, dwell time, bounce, scroll depth | GA4, Hotjar, Search Console |
| **Performance** | CWV field data, mobile usability, speed metrics | PageSpeed Insights, CrUX, Search Console |
| **Coverage** | Indexing status, crawl errors, sitemap health | Search Console, log-file analysis |
| **Authority** | Mentions, backlinks, brand search volume | Ahrefs, Majestic, brand tools |

### Cross-validation examples

- **Ranks up, traffic flat** → the keyword isn't actually driving clicks. Check SERP features (featured snippet, People Also Ask) cannibalizing the query.
- **Impressions up, CTR down** → ranking for the wrong intent. Rewrite for alignment with searcher goal.
- **Indexed pages down** → Google dropped thin pages; audit which were dropped and why.
- **Mentions up, rank flat** → authority is growing but content relevance lags.
- **Traffic up, conversion flat** → SEO is working but the page is off-intent; the user left because the content didn't match their query.

### KPIs worth tracking vs vanity metrics

- **Track:** organic traffic to key pages, rank for priority queries, CWV field data, branded search volume
- **Ignore:** "domain authority" (third-party synthetic score), keyword density, bounce rate in isolation, "Alexa rank"

## Minimal example

Quarterly review dashboard:

```
Q1 2026
 Impressions      +18%    (Search Console)
 Clicks           +12%    (Search Console) — CTR slight drop 3.2% → 3.0%
 Indexed pages     -3%    (Search Console — removed thin tag pages, intentional)
 CWV good URLs   +22%     (CrUX field data)
 Referring domains +8%    (Ahrefs)
 Branded search  +35%     (Google Trends, internal analytics)
 Top-10 ranks    +14%     (Ahrefs)
```

Narrative: impressions up faster than clicks (CTR drop) suggests ranking for queries with weaker match; worth auditing the 10 highest-impression queries for intent alignment.

*Attributed to the seo-fundamentals skill — `SKILLS-TO-INTEGRATE/web-design/seo-fundamentals/SKILL.md`.*

## Gotchas

- "Organic traffic is up" with no cross-check can hide query-mix shifts — you might be ranking for lower-value queries while losing high-value ones.
- Search Console's 16-month data limit means historical trending requires exporting to a data warehouse (BigQuery connector is free for Search Console).
- CWV field data lags by 28 days — a fix today won't show in CrUX until next month.
- Third-party "authority" scores (DA, DR) are black-box proxies, not Google's signal. They correlate but do not cause ranking.

## Cross-references

- [TECH-seo-relative-importance](TECH-seo-relative-importance.md)
- [TECH-seo-eeat](TECH-seo-eeat.md), [TECH-seo-cwv](TECH-seo-cwv.md), [TECH-seo-technical](TECH-seo-technical.md)
- `../SKILL.md`
