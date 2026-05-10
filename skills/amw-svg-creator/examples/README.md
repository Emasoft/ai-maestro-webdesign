# svg-creator examples — in-scope only

## Table of Contents

- [Reference](#reference)

## Reference

This folder holds in-scope examples for the `svg-creator` skill (icons, logos,
patterns, data-vis primitives, SVG animations). It is intentionally empty at
the moment — real in-scope examples will be added as they are produced by
successful render-verify-finish loops via `../../../bin/amw-svg-render.py`.

## What this skill ships (in-scope categories)

- 24×24 stroke icons
- Geometric logos and badges (gradient / multi-stop)
- SVG patterns (repeating tiles via `<pattern>`)
- Data-visualisation primitives (computed geometry + gradient fills)
- SVG animations (CSS / SMIL + reduced-motion fallback)

When adding real examples, use filenames that make the category obvious
(e.g. `icon-home-24.svg`, `logo-acme-badge.svg`, `pattern-dots-tile.svg`,
`spinner-animated.svg`). Each example must be the output of a successful
render-verify-finish loop — no freehand hand-edited SVG.

## Archived character examples — moved out of this folder

The upstream skill shipped two character illustrations
(`cat-astronaut.svg`, `fox-yoga-static.svg`) as its canonical examples.
Those files have been moved to
`docs_dev/examples_archive/svg-creator-characters/` (outside the published
plugin) because:

- The output category they represent — AI-drawn character / scene / mascot
  illustrations — is explicitly banned by `../../amw-design-principles/ai-slop-avoid.md`
  item 3 ("AI-drawn SVG illustrations / mascots / scenes"). The plugin's
  `svg-creator` skill refuses those requests and routes the user to a
  placeholder box + real asset.
- Keeping them inside `examples/` sent a mixed message — even with a
  "not templates" caveat, a downstream Claude reading the folder would
  pattern-match on the cats/foxes before reading the caveat. They are an
  attractive nuisance for a skill whose entire job is to refuse that exact
  output.

Attribution and license traceability for the upstream skill (Apache 2.0,
retained in `../LICENSE`) is preserved in the archived folder's own
`README.md`. If the plugin's policy on AI-drawn characters ever changes
(it will not, as of this version), those archived files can be re-evaluated.
