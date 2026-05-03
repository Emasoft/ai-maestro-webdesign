---
name: TECH-designlang-brands
category: designlang-diff
source: SKILLS-TO-INTEGRATE/web-design/designlang-design-extract/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: `designlang brands` — N-way brand comparison matrix

## What it does

Takes N URLs (or domain shorthands) and emits a comparison matrix across all of them — colors, typography, spacing, shadow systems — with a Markdown report and an interactive HTML grid that highlights shared vs unique tokens per brand.

## When to use

- Competitive design audits for a full category — comparing fintech primary colors across Stripe / Braintree / Paddle / Adyen.
- Visual mood boards anchored in real data — "show me what five luxury fashion brands actually use for body type".
- Generating a reference library for a new design system by observing what a chosen cohort of brands has in common.

Skip for pairwise comparison — `designlang diff` is faster and produces a tighter report.

## How it works

designlang runs a full extraction on each URL, then performs:

- **Palette matrix** — every brand's palette plotted side-by-side; shared hues flagged with a per-brand legend
- **Type matrix** — each brand's heading + body font pair stacked for visual scan
- **Spacing matrix** — base-unit comparison (4px cohort vs 8px cohort)
- **Shadow matrix** — elevation stacks side-by-side

Output is two files: `brands.md` (Markdown summary) and `brands.html` (interactive grid).

## Minimal example

```bash
npx designlang brands stripe.com vercel.com github.com linear.app
```

*Attributed to designlang — `designlang-design-extract/SKILL.md`.*

## Gotchas

- Runtime is linear in N — four brands is ~4x a single-URL extraction. Cap at ~10 brands per invocation or the HTML grid becomes unreadable.
- Domain shorthand (`stripe.com`) is expanded to `https://stripe.com`. Sites that require `www.` or a specific subpath must be passed as full URLs.
- The HTML grid relies on inline SVG for swatches — files can exceed 5 MB for N > 8.

## Cross-references

- [TECH-designlang-diff](TECH-designlang-diff.md) — pairwise version
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-designlang-score](TECH-designlang-score.md) — rank the N brands before comparing
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
