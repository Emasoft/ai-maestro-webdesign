---
name: TECH-49-justification-comparison
category: motion
source: pretext-skills/amw-pretext-frontend-motion-main/core/bundle/blueprints/justification-comparison.md
also-in: pretext-frontend-motion-main demo-family-map
---

# Justification comparison (width probing workflow)

**Category:** motion
**Status:** stable

## What it does

Side-by-side comparison of a paragraph at multiple widths and justification strategies (ragged right vs justified vs balanced). Uses `walkLineRanges()` to probe candidate widths without allocating strings, then renders the chosen strategies for visual comparison.

## When to use

- Typography design tool pages
- Demos comparing line-break quality
- Internal QA for a text block

## How it works

```ts
// Source: pretext-frontend-motion-main/blueprints/justification-comparison.md
// 1. For a grid of candidate widths: walkLineRanges(prepared, w, l => ...)
// 2. Score each width (max variance, orphan count, total height)
// 3. Render the top 3 strategies side by side
```

## Minimal example

See `pretext-frontend-motion-main/blueprints/justification-comparison.md` — conceptual blueprint.

## Delivery shape (source: justification-comparison.md blueprint)

- Side-by-side comparison view showing 3 strategies at once.
- Visible explanation of rivers, spacing, and ragged/justified trade-offs.
- Clear statement that pretext is not pretending to be a full Knuth-Plass engine — it probes widths via `walkLineRanges()` and scores them, leaving hyphenation to the caller.
- CSS justified text, greedy line breaking / hyphenation, and balanced algorithm should all be represented.

## Gotchas

- Without a scoring function, "best width" is subjective — let the user pick from the top 3.
- At small widths (< 200 px), most strategies fail — clamp.

## Cross-references

- Related: TECH-06-walk-line-ranges, TECH-26-balanced-headline
- API reference: [TECH-06-walk-line-ranges](TECH-06-walk-line-ranges.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
