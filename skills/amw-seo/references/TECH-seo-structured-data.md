---
name: TECH-seo-structured-data
category: seo-technical
source: SKILLS-TO-INTEGRATE/web-design/seo-fundamentals/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Structured data (Schema.org / JSON-LD)

## What it does

Structured data helps search engines **understand meaning** — not boost rankings directly, but enable rich-result eligibility (recipe cards, FAQ accordions, product prices in results, review stars, breadcrumb trails). The dominant format is JSON-LD injected via `<script type="application/ld+json">`.

## When to use

On every content-heavy page that has an addressable entity type — articles, products, reviews, events, people, organizations, how-tos, FAQs, breadcrumbs. Also on homepages for Organization / WebSite markup.

## How it works

Key types:

| Type | Purpose | Common rich result |
|---|---|---|
| Article | Content classification | Article top stories, publisher badge |
| Organization | Entity identity (company, brand) | Sitelinks, knowledge panel eligibility |
| Person | Author identity | Author attribution, knowledge panel |
| FAQPage | Q&A clarity | FAQ accordion in SERP |
| Product | Commerce details | Price, availability, review stars in results |
| Review | Ratings context | Star rating display |
| BreadcrumbList | Site structure | Breadcrumb trail above snippet |
| HowTo | Step-by-step guides | HowTo carousel (some queries) |
| Event | Conferences, launches | Event date + venue in result |
| Recipe | Cooking content | Recipe card with calories, time, rating |

**Validation**

- Google Rich Results Test → [search.google.com/test/rich-results](https://search.google.com/test/rich-results)
- Schema.org validator → [validator.schema.org](https://validator.schema.org)
- Search Console → "Enhancements" section shows which pages are eligible for which rich-result types

## Minimal example

FAQ schema on a product page:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Do you offer a free trial?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, a 14-day free trial is available for all plans. No credit card required."
      }
    },
    {
      "@type": "Question",
      "name": "Can I cancel any time?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Cancel from your account settings; no fees or contracts."
      }
    }
  ]
}
</script>
```

When eligible, Google renders an expandable FAQ accordion below the page's search snippet.

*Attributed to the seo-fundamentals skill — `SKILLS-TO-INTEGRATE/web-design/seo-fundamentals/SKILL.md`.*

## Gotchas

- Schema enables rich-result eligibility but does not guarantee it. Google's algorithm decides per-query whether to show the rich result.
- Markup that doesn't match the visible page content is a manual-action risk. If your FAQ schema lists questions, those questions must be visible on the page.
- JSON-LD is the preferred format (Google's recommendation). Microdata and RDFa still work but are less common.
- Nested schemas can conflict (having both Organization and WebSite at the root can cause the validator to merge incorrectly). Use `@graph` to define multiple top-level entities cleanly.

## Cross-references

- [TECH-seo-technical](TECH-seo-technical.md), [TECH-seo-content-quality](TECH-seo-content-quality.md)
  > [TECH-seo-content-quality.md] What it does · When to use · How it works · Page-level elements · Content quality signals · Intent classification · Minimal example · Gotchas · Cross-references
  > What it does · When to use · How it works · Crawl & index control · Performance & accessibility (technical prerequisites for CWV) · Common technical failures · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
