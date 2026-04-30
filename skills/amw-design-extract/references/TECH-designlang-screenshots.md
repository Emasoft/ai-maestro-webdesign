---
name: TECH-designlang-screenshots
category: designlang-url-extract
source: SKILLS-TO-INTEGRATE/web-design/designlang-design-extract/SKILL.md
also-in:
---

# TECH: `--screenshots` — component screenshot capture

## What it does

Captures PNG screenshots of individual components — buttons, cards, navigation bars, hero sections — by locating them in the DOM and cropping the viewport to their bounding box. Output goes to a `components/` subfolder alongside the usual token files.

## When to use

- Reference boards where the user wants visual anchors for each extracted component (a CTA button's actual pixel look, not just its tokens).
- Handoff documents where the reverse-engineered spec includes both machine-readable tokens and a visual reference.
- Brand-comparison workflows when paired with `designlang brands` — each brand's component gallery is directly comparable.

Skip if the user only wants machine-readable tokens — screenshots add file size and don't feed downstream Tailwind/shadcn/React outputs.

## How it works

designlang runs a heuristic DOM walker that tags elements by role — `button`, `nav`, `[class*="card"]`, `[class*="hero"]`. For each tagged element, Playwright computes the bounding box and issues a clipped screenshot. Images land in `components/<role>-<index>.png` relative to the main output dir.

## Minimal example

```bash
npx designlang https://stripe.com --screenshots
```

Produces `components/button-0.png`, `components/button-1.png`, `components/card-0.png`, `components/nav-0.png`, etc.

*Attributed to designlang — `designlang-design-extract/SKILL.md`.*

## Gotchas

- Heuristic role-tagging has false positives — a `<div class="card">` that is actually a landing-page decoration will get captured as a "card".
- Cropping can miss elements with negative margins or transform-based positioning that place them outside their computed bounding box.
- Large images accumulate quickly. When extracting many URLs (brands mode), pipe `--screenshots` outputs to `$TMPDIR` rather than a project folder.

## Cross-references

- `TECH-designlang-full-mode.md`
- `TECH-designlang-brands.md` — pairs well when comparing brand component galleries
- `../SKILL.md`
