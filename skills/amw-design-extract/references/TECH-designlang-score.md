---
name: TECH-designlang-score
category: designlang-score
source: SKILLS-TO-INTEGRATE/web-design/designlang-design-extract/SKILL.md
also-in:
---

# TECH: `designlang score` — design-quality scoring

## What it does

Evaluates a live URL across 7 design-discipline categories and returns an A-F grade plus a 0-100 score per category. Categories: color discipline, typography, spacing system, shadows, border radii, accessibility (WCAG 2.1 contrast), tokenization (CSS custom property usage).

## When to use

- Quick triage of whether a site has a coherent design system worth reverse-engineering. A D or F on tokenization means the site uses inline/computed styles and the extracted token file will be a noisy dump.
- Competitor benchmarking as a prelude to `designlang brands`.
- Auditing the user's own site — does it meet the same bar as its references?

Skip when the user wants tokens (use the default extraction) — scoring does not emit the eight token files.

## How it works

designlang runs a standard extraction, then applies rubrics:

- **Color discipline** — palette size, hue harmony (LCH clustering), per-role consistency
- **Typography** — number of distinct sizes/weights, scale ratio regularity
- **Spacing system** — whether spacing values cluster to a base unit (4 / 8 / 16 px)
- **Shadows** — elevation system coherence (few distinct depths, consistent offsets)
- **Border radii** — radius scale regularity
- **Accessibility** — pass/fail rate on WCAG 2.1 AA contrast for all fg/bg pairs
- **Tokenization** — ratio of CSS custom properties to inline computed values

Each category gets a 0-100 numeric score; the letter grade is banded (A 90+, B 75+, C 60+, D 45+, F <45).

## Minimal example

```bash
npx designlang score https://vercel.com
```

Output:

```
DESIGN SCORE: https://vercel.com  Grade A  (91/100)

  Color discipline:  A (94)
  Typography:        A (96)
  Spacing:           B (82)
  Shadows:           A (90)
  Border radii:      A (93)
  Accessibility:     B (78)
  Tokenization:      A (95)
```

*Attributed to designlang — `designlang-design-extract/SKILL.md`.*

## Gotchas

- Sites with heavy third-party embeds (Segment, Intercom, hCaptcha) drop several letter grades because the third-party CSS pollutes the palette and spacing clusters. Use `--depth 0` to limit scoring to the main frame if needed.
- The accessibility category checks contrast only — it does NOT substitute for an axe-core or Lighthouse a11y audit.
- Score is not a ranking signal; it's a heuristic. A site can score A and still have an incoherent product — the score measures discipline, not taste.

## Cross-references

- `TECH-designlang-diff.md` — score two sites and compare
- `TECH-designlang-brands.md` — score N brands in a matrix
- `../SKILL.md`
- `../../amw-ux-evaluator/SKILL.md` — complementary UX scoring
