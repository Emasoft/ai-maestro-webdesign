---
name: TECH-article-template
category: ascii-to-html-content-templates
source: amw-wireframe-builder-agent §9 (article-template routing rows)
also-in: ../../amw-seo/SKILL.md (Article JSON-LD schema)
---

# Article / blog post template

## What it does

Structural contract for long-form article and blog-post pages:
semantic markup, byline + reading-time, Open Graph + Twitter Card meta,
and JSON-LD Article schema. Pairs with `amw-seo` for the SEO
metadata authoring and with `amw-multilanguage-copywriter-agent` for
locale-specific copy.

## Semantic structure

```html
<article itemscope itemtype="https://schema.org/Article">
  <header>
    <p class="kicker" itemprop="articleSection">Engineering</p>
    <h1 itemprop="headline">How we cut LCP from 4.2s to 1.1s</h1>
    <p class="dek" itemprop="description">
      A pragmatic teardown of font-loading, image-preloading, and
      server-push tradeoffs.
    </p>

    <div class="byline">
      <span itemprop="author" itemscope itemtype="https://schema.org/Person">
        By <a href="/authors/jane-doe" itemprop="url">
          <span itemprop="name">Jane Doe</span>
        </a>
      </span>
      &middot;
      <time datetime="2026-04-22T10:00:00+02:00" itemprop="datePublished">
        Apr 22, 2026
      </time>
      &middot;
      <span class="reading-time">8 min read</span>
    </div>

    <figure class="hero">
      <img src="/img/hero-1200.avif"
           srcset="/img/hero-600.avif 600w,
                   /img/hero-1200.avif 1200w,
                   /img/hero-2000.avif 2000w"
           sizes="(min-width: 1024px) 1200px, 100vw"
           alt="Performance graph showing LCP improvement"
           width="1200" height="630"
           loading="eager"
           fetchpriority="high"
           decoding="async"
           itemprop="image">
      <figcaption>Before / after LCP traces</figcaption>
    </figure>
  </header>

  <div itemprop="articleBody">
    <!-- Paragraphs, code blocks, headings, figures, lists, blockquotes... -->
  </div>

  <footer>
    <ul class="tags">
      <li><a href="/tags/performance" rel="tag">performance</a></li>
      <li><a href="/tags/lcp" rel="tag">lcp</a></li>
    </ul>

    <nav class="related" aria-label="Related articles">
      <h2>Related</h2>
      <!-- 3 cards, each with its own article schema -->
    </nav>
  </footer>
</article>
```

Element rules:
- ONE `<h1>` per article — it is the title; no other H1s on the page
- `<header>` and `<footer>` here are scoped to the `<article>`, not the
  page (a blog index has its own page-level header/footer)
- `<time datetime>` is REQUIRED — bots use it for freshness signals
- `<figure>` for any image with caption; bare `<img>` for inline images
- `<aside>` for callout boxes, pull-quotes, "key takeaways" boxes
- `<blockquote cite="<url>">` for external quotes; include the URL

## Reading-time computation

Compute on the build step, not at runtime:

```js
function readingTime(plainText) {
  const wordsPerMinute = 200; // average adult silent reading speed
  const words = plainText.trim().split(/\s+/).length;
  const minutes = Math.max(1, Math.round(words / wordsPerMinute));
  return `${minutes} min read`;
}
```

For locales with character-based reading speeds:
- Japanese: ~400-600 chars/min
- Chinese: ~250-400 chars/min
- Korean: similar to Japanese
- Arabic: ~180-200 words/min (similar to English)

If the brief includes multiple locales, compute per-locale; do not
translate "8 min read" without re-computing.

## Open Graph + Twitter Card meta

In `<head>`:

```html
<!-- Open Graph (Facebook, LinkedIn, Slack, Discord) -->
<meta property="og:type"        content="article">
<meta property="og:title"       content="How we cut LCP from 4.2s to 1.1s">
<meta property="og:description" content="A pragmatic teardown of font-loading, image-preloading, and server-push tradeoffs.">
<meta property="og:url"         content="https://brand.com/blog/cut-lcp-to-1-1s">
<meta property="og:site_name"   content="Brand Engineering Blog">
<meta property="og:image"       content="https://brand.com/og/cut-lcp-to-1-1s.png">
<meta property="og:image:alt"   content="Performance graph showing LCP improvement">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale"      content="en_US">
<meta property="article:published_time" content="2026-04-22T10:00:00+02:00">
<meta property="article:modified_time"  content="2026-04-25T14:30:00+02:00">
<meta property="article:author" content="https://brand.com/authors/jane-doe">
<meta property="article:section" content="Engineering">
<meta property="article:tag"    content="performance">
<meta property="article:tag"    content="lcp">

<!-- Twitter Card -->
<meta name="twitter:card"        content="summary_large_image">
<meta name="twitter:site"        content="@brand">
<meta name="twitter:creator"     content="@janedoe">
<meta name="twitter:title"       content="How we cut LCP from 4.2s to 1.1s">
<meta name="twitter:description" content="A pragmatic teardown of font-loading, image-preloading, and server-push tradeoffs.">
<meta name="twitter:image"       content="https://brand.com/og/cut-lcp-to-1-1s.png">
<meta name="twitter:image:alt"   content="Performance graph showing LCP improvement">
```

Image rules:
- OG image: 1200×630 (1.91:1) is the canonical size; minimum 600×315
  per Open Graph spec
- Twitter `summary_large_image`: 1200×628 (essentially identical;
  reuse the OG image)
- File format: PNG or JPG; AVIF/WebP are NOT supported by Slack /
  Discord image previews — always ship a JPG/PNG fallback for OG
- Alt text on `og:image:alt` for screen-reader-friendly preview reads
- Absolute URL on `og:image` — relative paths fail on most platforms

## JSON-LD Article schema

Inside `<head>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How we cut LCP from 4.2s to 1.1s",
  "description": "A pragmatic teardown of font-loading, image-preloading, and server-push tradeoffs.",
  "image": [
    "https://brand.com/og/cut-lcp-to-1-1s.png"
  ],
  "datePublished": "2026-04-22T10:00:00+02:00",
  "dateModified": "2026-04-25T14:30:00+02:00",
  "author": {
    "@type": "Person",
    "name": "Jane Doe",
    "url": "https://brand.com/authors/jane-doe"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Brand",
    "logo": {
      "@type": "ImageObject",
      "url": "https://brand.com/logo-org.png",
      "width": 600,
      "height": 60
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://brand.com/blog/cut-lcp-to-1-1s"
  },
  "articleSection": "Engineering",
  "wordCount": 1620,
  "keywords": "performance, lcp, web vitals"
}
</script>
```

For more specific article subtypes (per schema.org):
- `NewsArticle` — news stories
- `BlogPosting` — informal blog posts
- `TechArticle` — technical / how-to content
- `ScholarlyArticle` — academic publications
- `Review` — review articles

`amw-seo-strategist-agent` decides the subtype from the brief; this
template defaults to `Article` (the supertype).

## Body copy patterns

- Line length: 65-75 characters per line at 18px (CSS:
  `max-width: 70ch`)
- Paragraph spacing: 1em vertical
- Headings: `<h2>` for section, `<h3>` for sub-section; never skip a
  level (no `<h2>` followed by `<h4>`)
- Code blocks: `<pre><code class="language-js">` for syntax-highlighted
  blocks; inline `<code>` for inline references
- Pull quotes: `<aside class="pullquote">` with the quote duplicated
  from body text (visual emphasis, not new content)
- Lists: `<ul>` for unordered, `<ol>` for ordered; nested up to 3 levels

## Accessibility

- Skip link: `<a class="skip" href="#main">Skip to article</a>` first
  thing in `<body>`
- `<main id="main">` wrapping the `<article>` for the skip target
- Headings hierarchy: H1 → H2 → H3, never skipped
- Image `alt` text: descriptive for content images, `alt=""` for
  decorative ones (figure decorations, dividers)
- `prefers-reduced-motion` reset on any animations
- Code blocks: `<pre>` retains whitespace and is not horizontally
  scrolled offscreen (overflow-x: auto with visible scrollbar OR
  word-wrap break-word)

## RSS / Atom feed

For a blog index, generate `/feed.xml` (Atom 1.0):

```xml
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Brand Engineering Blog</title>
  <link href="https://brand.com/blog"/>
  <link href="https://brand.com/feed.xml" rel="self" type="application/atom+xml"/>
  <id>https://brand.com/blog</id>
  <updated>2026-04-25T14:30:00+02:00</updated>
  <author>
    <name>Brand Engineering Team</name>
  </author>
  <entry>
    <title>How we cut LCP from 4.2s to 1.1s</title>
    <link href="https://brand.com/blog/cut-lcp-to-1-1s"/>
    <id>https://brand.com/blog/cut-lcp-to-1-1s</id>
    <updated>2026-04-25T14:30:00+02:00</updated>
    <published>2026-04-22T10:00:00+02:00</published>
    <author>
      <name>Jane Doe</name>
    </author>
    <summary>A pragmatic teardown of font-loading, image-preloading, and server-push tradeoffs.</summary>
    <content type="html">
      <![CDATA[Full HTML body here, sanitized.]]>
    </content>
  </entry>
</feed>
```

Link from `<head>`:

```html
<link rel="alternate"
      type="application/atom+xml"
      title="Brand Engineering Blog Atom Feed"
      href="/feed.xml">
```

For RSS 2.0 (older readers):

```xml
<?xml version="1.0"?>
<rss version="2.0">
  <channel>
    <title>Brand Engineering Blog</title>
    <link>https://brand.com/blog</link>
    <description>Engineering posts</description>
    <language>en-US</language>
    <pubDate>Sat, 25 Apr 2026 14:30:00 +0200</pubDate>
    <item>
      <title>...</title>
      <link>...</link>
      <description>...</description>
      <pubDate>...</pubDate>
      <guid isPermaLink="true">...</guid>
    </item>
  </channel>
</rss>
```

## Multi-locale considerations

Each locale gets its own URL: `/en/blog/<slug>`, `/fr/blog/<slug>`,
`/de/blog/<slug>`. Cross-link with `<link rel="alternate" hreflang>`:

```html
<link rel="alternate" hreflang="en" href="https://brand.com/en/blog/cut-lcp-to-1-1s">
<link rel="alternate" hreflang="fr" href="https://brand.com/fr/blog/reduire-lcp-a-1-1s">
<link rel="alternate" hreflang="de" href="https://brand.com/de/blog/lcp-auf-1-1s-senken">
<link rel="alternate" hreflang="x-default" href="https://brand.com/en/blog/cut-lcp-to-1-1s">
```

Set `<html lang="..">` per locale.

## What the agent MUST do

1. Use semantic `<article>` / `<header>` / `<footer>` / `<time>` / `<figure>` markup
2. Compute reading-time per locale on build (not runtime)
3. Emit `og:image` with absolute URL, 1200×630 PNG/JPG (no AVIF/WebP-only)
4. Emit Twitter Card meta paired with OG (twitter falls back to OG, but explicit is better)
5. Emit JSON-LD Article schema (or proper subtype) — coordinate with `amw-seo-strategist-agent` for subtype choice
6. Emit `<link rel="alternate" hreflang>` for every locale variant
7. Generate `/feed.xml` (Atom) for blog indexes; link from `<head>`

## What the agent MUST NOT do

- Skip `width`/`height` on images (CLS killer)
- Use `<h1>` more than once per article
- Translate "8 min read" without recomputing per locale
- Use AVIF or WebP as the only OG image format (Slack/Discord break)
- Mix RSS 2.0 and Atom feeds without explicit reason
- Embed third-party tracking scripts inside the article body without
  consent management (legal-expert + accessibility-auditor concerns)
