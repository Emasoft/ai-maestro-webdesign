---
name: TECH-65-vendoring-esm
category: integrate
source: pretext-skills/amw-pretext-skill-main/pretext/skills/amw-pretext/references/patterns.md
also-in: 
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Vendoring pretext as a single ESM file (no build step)

**Category:** integrate
**Status:** stable

## What it does

If your project doesn't use a bundler, pretext's multiple ES modules with relative imports won't work standalone. Bundle pretext into a single ESM file with `esbuild` once, ship the result alongside your HTML, and import it without a build step — works in static hosting, GitHub Pages, plain file:// previews.

## When to use

- Static-site / plain HTML pages
- GitHub Pages / Vercel static deploys
- Offline-capable demos
- When esm.sh is not acceptable (network dependency)

## How it works

```bash
# One-time bundle
npx esbuild node_modules/@chenglou/pretext/index.js \
  --bundle --format=esm \
  --outfile=vendor/pretext.js
```

```html
<!-- Then import without bundler -->
<script type="module">
  import { prepare, layout } from './vendor/pretext.js'
</script>
```

## Minimal example

See commands above.

## Gotchas

- Re-bundle on pretext upgrades.
- Source maps omitted for production — add `--sourcemap=linked` if needed.

## Cross-references

- Related: TECH-63-progressive-enhancement
- API reference: [TECH-01-prepare-basics](TECH-01-prepare-basics.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
