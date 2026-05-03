---
name: TECH-designlang-diff
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


# TECH: `designlang diff` — pairwise brand comparison

## What it does

Takes two URLs (or a URL and a baseline token file) and emits a side-by-side comparison of colors, type scales, spacing, and shadow systems. Outputs Markdown and an interactive HTML visualization with color-overlap analysis.

## When to use

- Pairwise brand audits — "how does our site compare to Stripe's?".
- Tracking a design system's evolution over time — diff today's extraction against a stored baseline JSON.
- CI regression gates where a significant drift from a pinned baseline should fail the build.

Skip when comparing more than two sites — use `designlang brands` for N-way comparison instead.

## How it works

designlang extracts both sources (two live URLs, or one URL and a `design-tokens.json` baseline), then runs set diffs on:

- **Color palette** — colors exclusive to A, exclusive to B, shared (with hue-proximity clustering)
- **Typography** — font-family diffs, size-scale deltas, weight coverage
- **Spacing** — scale value comparison
- **Shadows** — elevation stack comparison
- **Border radii** — radius set diff

The HTML output renders a Venn-style overlap of colors and a side-by-side swatch grid.

## Minimal example

```bash
# Live vs live
npx designlang diff https://stripe.com https://paddle.com

# Live vs stored baseline
npx designlang diff https://vercel.com ./baselines/vercel-2025-01.design-tokens.json
```

*Attributed to designlang — `designlang-design-extract/SKILL.md`.*

## Gotchas

- Color-overlap analysis uses LCH proximity (within ΔE < 3) to treat near-identical hues as "shared". Sites that hand-tune for contrast may register drift even when the brand intent is unchanged.
- Font-family diffs will flag `-apple-system, BlinkMacSystemFont` stacks against `Inter` as different even though both resolve to system sans on macOS.
- For CI gating, always pin a JSON baseline — live-vs-live diffs are non-deterministic because competitor sites change between runs.

## Cross-references

- [TECH-designlang-score](TECH-designlang-score.md) — score both sides before diffing
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-designlang-brands](TECH-designlang-brands.md) — N-way version
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
