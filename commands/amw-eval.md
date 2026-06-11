---
name: amw-eval
description: "Shortcut for users who want a systematic UX and SEO evaluation against a specific HTML file directly — scored report on Position, Visual Weight, Spacing, contrast, Core Web Vitals. An agent in Main-agent mode may also invoke skills/amw-ux-evaluator/ and skills/amw-seo/ directly via the orchestrator as part of Phase B validation, applying the full framework beyond what this command exposes."
---

# /amw-eval

Evaluate a rendered HTML page against the `ux-evaluator` framework (Position / Visual Weight / Spacing — from Balsamiq + Nielsen heuristics) and the `seo` skill (Core Web Vitals hints). Produces a scored markdown report.

This command is read-only and **never rewrites the HTML**. It tells the user what to change, not makes the changes.

## Arguments

- Optional: a file path to a local `.html` (or a URL for a deployed page).
- If absent, find the latest-modified `.html` under the working directory (same logic as `/amw-preview`).
- If a URL is passed, confirm with the user before running (same etiquette as `/amw-extract-style`).

## Action

### 1. Render

Open the page in `dev-browser` at desktop 1440×900. If it's a URL, wait for network idle. If it's a local file, serve via `bin/amw-preview-server.py` when there are relative assets.

### 2. Three-dimension analysis (ux-evaluator)

Run the three-dimension framework from [SKILL](../skills/amw-ux-evaluator/SKILL.md):

**Position**
- Primary CTA location (Z-pattern terminal? F-pattern first-row?).
- Logo position (left-of-header convention per Jakob's Law).
- Navigation density and order (≤ 7 items per Hick / Miller).
- Content hierarchy visible in the top 600 pixels.

**Visual Weight**
- Hero text size vs body ratio (Major Third / Perfect Fourth / Golden? Per [typography-system](../skills/amw-design-principles/typography-system.md)).
> [typography-system.md] I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax · VIII. Forbidden AI-giveaway fonts (T-043)
- Color weight — primary accent occupies < 10% of page area?
- Figure-ground — exactly one focal element per viewport?
- Evidence of visual hierarchy depth ≥ 3 levels (size + weight + spacing + color combined, not any single dimension).

**Spacing**
- Spacing values on 4pt / 8pt grid per [spacing-rhythm](../skills/amw-design-principles/spacing-rhythm.md)? Scan computed styles for any non-grid values (13px, 7px, 17px) and flag.
> [spacing-rhythm.md] I. 8pt grid system · II. Fibonacci spacing rhythm (large-scale) · III. Vertical rhythm (baseline grid) · IV. Hit targets (tappable areas) · V. Alignment · VI. Three principles of whitespace · VII. Border radius · VIII. Shadow system · IX. Self-check
- Section gap > section-internal gap? (External > internal rule.)
- Alignment — is the body copy left-aligned (Chinese + Latin rule) and paginated against a baseline grid?

Each dimension gets a verdict: **Pass / Warn / Fail** with the evidence.

### 3. SEO + performance snapshot

From [SKILL](../skills/amw-seo/SKILL.md) evaluation framework + dev-browser inspection:

- `<title>` length, `<meta description>` presence.
- `<h1>` count (should be 1).
- Heading order (no skipped levels).
- Image `alt` coverage.
- Structured data present? (`application/ld+json` block).
- LCP candidate element identified; image dimensions and format; lazy-loading attrs.
- Largest CSS / JS resource sizes via console capture.
- Any layout-shift offenders visible on load.

These are hints, not a full Lighthouse run. Document the limitation.

### 4. AI-slop compliance

One-pass scan against [ai-slop-avoid](../skills/amw-design-principles/ai-slop-avoid.md):
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)

- Check the 26 items via DOM patterns (CSS selectors, style strings, text content signatures).
- List only matches — silent on passes.
- Common live hits: default Inter/Roboto font stack, 135deg-ish purple gradient, every-card-equal-size grid, fake testimonial names, "10x" stats, per-feature icon row.

### 5. Scoring

Produce a single verdict letter grade and the full breakdown:

```
# UX Evaluation — <filename or URL>
Overall grade: B   (pass thresholds met; two warn items, zero fail)

## Position
- Primary CTA: Pass (right-of-hero, Z-pattern terminal)
- Nav: Warn (9 items; consider collapsing to ≤ 7)
- Hierarchy depth: Pass

## Visual Weight
- Typography scale: Pass (Perfect Fourth)
- Accent coverage: Pass (8.2% of area)
- Focal element: Pass

## Spacing
- Grid compliance: Warn (two 13px values found in .card)
- External > internal: Pass
- Baseline: Pass

## SEO / performance hints
- Title: 52 chars — Pass
- Meta description: missing — Warn
- H1 count: 1 — Pass
- LCP candidate: /hero.webp (243 KB, no dimensions attr) — Warn
- Structured data: none detected

## AI-slop compliance
- 0 matches.

## Priority recommendations
1. Collapse nav to 6 items (Hick/Miller) — highest impact.
2. Snap the two 13px .card paddings to 12px or 16px (4/8-grid).
3. Add a ≤ 160-char <meta description> for SERP CTR.
4. Set width/height attributes on /hero.webp to stabilize LCP.
```

Write the full report to `/tmp/amw-eval-<slug>-report.md` and return only the grade line + report path to the user.

## Non-negotiables

- **dev-browser only** for live inspection.
- **No HTML edits.** This is pure evaluation.
- **Cite evidence.** Every Fail or Warn names a CSS selector, a computed-style value, or a DOM attribute.

## When to use `/amw-eval` vs `/amw-preview`

- `/amw-preview` → quick visual confirmation + 5-point self-check. Seconds.
- `/amw-eval` → full framework scoring. Minutes. Use before declaring a design "done."

## Failure modes

- JS-heavy page with client-side-only rendering → wait longer; if still not rendered, note it and proceed with what loaded.
- Page with auth wall → stop.
- Page with paywall overlay → evaluate what's visible, flag the rest as blocked.
