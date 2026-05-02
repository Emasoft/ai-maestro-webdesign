---
name: TECH-seo-content-quality
category: seo-technical
source: SKILLS-TO-INTEGRATE/web-design/seo-fundamentals/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Page-level elements](#page-level-elements)
  - [Content quality signals](#content-quality-signals)
  - [Intent classification](#intent-classification)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Content SEO — page elements + quality signals

## What it does

Content SEO covers on-page elements (title, meta description, headings, alt text) and quality signals (depth, originality, accuracy, clarity, usefulness). Content quality is the highest-weighted ranking factor when pages are comparable on technical and trust dimensions.

## When to use

On every SEO audit. Content issues are often subtler than technical issues — a page can be technically perfect and rank poorly because it doesn't actually answer the query.

## How it works

### Page-level elements

| Element | Principle |
|---|---|
| Title tag | Clear topic + intent; 50-60 characters |
| Meta description | Click relevance (not a ranking signal but drives CTR); 150-160 chars |
| H1 | Page's primary subject; one per page |
| Headings (H2, H3) | Logical structure; reflect content outline |
| Alt text | Accessibility + context for image search |
| Internal links | Anchor text carries semantic signal |

### Content quality signals

| Dimension | What search engines look for |
|---|---|
| Depth | Fully answers the query; addresses follow-up questions |
| Originality | Adds unique value — not a rehash of existing articles |
| Accuracy | Factually correct, citations when claims are non-obvious |
| Clarity | Easy to understand for the target audience |
| Usefulness | Satisfies intent — navigational / informational / transactional |

### Intent classification

- **Informational** — user wants to learn ("what is SEO"). Content should be thorough, educational.
- **Navigational** — user wants a specific site ("stripe pricing"). Don't try to out-rank the brand's own page.
- **Transactional** — user wants to buy / sign up. Product / pricing pages win.
- **Commercial investigation** — user is comparing before buying ("best CRM for small business"). Comparison posts / reviews win.

A page ranks best when its structure matches the dominant intent of its target query.

## Minimal example

Title + H1 for a how-to article:

```html
<title>How to Install Node.js on macOS (2026 Guide)</title>
<meta name="description" content="Step-by-step guide to installing Node.js on macOS using nvm, Homebrew, or the official installer. Includes troubleshooting for common errors.">

<h1>How to Install Node.js on macOS</h1>
<h2>Method 1: Using nvm (recommended)</h2>
<h2>Method 2: Using Homebrew</h2>
<h2>Method 3: Official installer</h2>
<h2>Troubleshooting common errors</h2>
```

Every heading maps to a question the user might have. The outline reflects real user intent.

*Attributed to the seo-fundamentals skill — `SKILLS-TO-INTEGRATE/web-design/seo-fundamentals/SKILL.md`.*

## Gotchas

- "Keyword density" is a myth. Modern search engines use semantic similarity (embeddings), not term frequency.
- Thin content (fewer than 300 words on a purportedly in-depth topic) is a clear quality signal regardless of keywords.
- Duplicate content across a site hurts — canonical one version, redirect the rest.
- Meta descriptions don't affect ranking directly, but low CTR (indicated by click-through-rate in Search Console) is a signal that the result is irrelevant.

## Cross-references

- [TECH-seo-eeat](TECH-seo-eeat.md), [TECH-seo-ai-content](TECH-seo-ai-content.md), [TECH-seo-structured-data](TECH-seo-structured-data.md)
- `../SKILL.md`
