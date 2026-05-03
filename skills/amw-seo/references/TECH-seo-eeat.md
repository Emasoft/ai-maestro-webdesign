---
name: TECH-seo-eeat
category: seo-eeat
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


# TECH: E-E-A-T — Quality Evaluation Framework

## What it does

E-E-A-T is the framework search engines use to evaluate content quality — Experience, Expertise, Authoritativeness, Trustworthiness. It is **not** a direct ranking factor but a quality lens that weighs more heavily on sensitive, high-impact topics (health, finance, legal — "YMYL" = your-money-or-your-life).

## When to use

During SEO audits for content-heavy sites, especially YMYL categories. During competitive content analysis — when pages of comparable keyword targeting are differentiated by trust and experience signals, not keywords.

## How it works

Four dimensions:

| Dimension | What it represents | Common signals |
|---|---|---|
| **Experience** | First-hand, real-world involvement | Original examples, lived experience, demonstrations, photos of the author using the thing |
| **Expertise** | Subject-matter competence | Credentials, depth, accuracy, author bios with qualifications |
| **Authoritativeness** | Recognition by others | Mentions, citations, links from authoritative sources |
| **Trustworthiness** | Reliability and safety | HTTPS, transparency, accuracy, clear contact info, cited sources |

Pages competing in the same space are differentiated by **trust and experience**, not keyword matching. A page from a reviewed medical clinic outranks an anonymous content farm even if the content-farm page has better keyword density.

## Minimal example

Auditing an "intermittent fasting for weight loss" page:

| Dimension | Signal present? | Evidence |
|---|---|---|
| Experience | Partial | Author describes personal 30-day experiment; no photos or measurable data |
| Expertise | Missing | No author bio, no credentials, no medical review note |
| Authoritativeness | Missing | No backlinks visible; page is on a generic wellness site with no topical authority |
| Trust | Weak | HTTPS present but no author bio, no citations, no published date |

Recommendations: add author bio with qualifications, medical-review byline, link to primary sources (PubMed IDs, not blog citations), date + last-updated.

*Attributed to the seo-fundamentals skill — `SKILLS-TO-INTEGRATE/web-design/seo-fundamentals/SKILL.md`.*

## Gotchas

- E-E-A-T is not a score you can measure — it's a lens the evaluator applies. Tools that claim an "E-E-A-T score" are guessing.
- The "Experience" dimension was added to E-A-T in 2022. Older SEO guides still reference E-A-T.
- YMYL topics (health, finance, legal, safety) have the highest E-E-A-T weight. Entertainment blogs can rank with weaker E-E-A-T.
- E-E-A-T signals live on the page AND on the author's / site's broader web presence. A one-off page on a site with no brand trust cannot out-rank an established brand regardless of content quality.

## Cross-references

- [TECH-seo-cwv](TECH-seo-cwv.md) — page experience signals (CWV)
  > What it does · When to use · How it works · Field data vs lab data · Important context · Minimal example · Gotchas · Cross-references
- [TECH-seo-content-quality](TECH-seo-content-quality.md), [TECH-seo-technical](TECH-seo-technical.md), [TECH-seo-structured-data](TECH-seo-structured-data.md)
  > [TECH-seo-technical.md] What it does · When to use · How it works · Crawl & index control · Performance & accessibility (technical prerequisites for CWV) · Common technical failures · Minimal example · Gotchas · Cross-references
  > What it does · When to use · How it works · Page-level elements · Content quality signals · Intent classification · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
