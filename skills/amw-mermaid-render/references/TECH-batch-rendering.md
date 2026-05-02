---
name: TECH-batch-rendering
category: mermaid-batch
source: diagrams-skills/Pretty-mermaid-skills-main/scripts/batch.mjs
also-in: diagrams-skills/Pretty-mermaid-skills-main/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Batch rendering — worker-pool directory mode

## What it does

Walks a directory of `.mmd` files, renders each one in parallel via
`Promise.allSettled()` worker batches, and writes matching output
files into a target directory. One theme per run, or one format per
run.

## When to use

- A docs site with dozens of architecture diagrams — render all of
  them as SVG during build.
- Generating both SVG and ASCII versions from the same sources for
  dual-output documentation.
- Migration — re-render every diagram with a new theme after a brand
  refresh.

## How it works

```js
// source: diagrams-skills/Pretty-mermaid-skills-main/scripts/batch.mjs
// FFD-style batching: slice files into worker-sized chunks
for (let i = 0; i < files.length; i += opts.workers) {
  const batch = files.slice(i, i + opts.workers);
  const results = await Promise.allSettled(
    batch.map(file => renderFile(file, opts.inputDir, opts.outputDir, opts, lib))
  );
  // Log ✓/✗ per file, track success/failure counts
}
```

Default parallelism: 4. Recommended: 8 for 10+ diagrams, 2 for
memory-tight environments.

## Minimal example

```bash
# source: diagrams-skills/Pretty-mermaid-skills-main/SKILL.md
node scripts/batch.mjs \
  --input-dir ./diagrams \
  --output-dir ./output \
  --format svg \
  --theme dracula \
  --workers 4
```

Typical output:
```
Found 3 diagram(s) to render...
✓ architecture.mmd
✓ workflow.mmd
✓ database.mmd

3/3 diagrams rendered successfully
```

## Gotchas

- `--workers` over ~16 will saturate Node's event loop and actually
  slow things down — Mermaid parsing is synchronous in parts.
- Failures are non-fatal per-file (uses `allSettled`), but the process
  exits 1 if ANY file failed. Check the stderr summary.
- The output filename is `{input}.svg` or `{input}.txt` — the script
  strips only `.mmd`. A file named `foo.mermaid` would be written as
  `foo.mermaid.svg`.

## Cross-references

- [TECH-svg-render-api](TECH-svg-render-api.md) — the per-file rendering function.
- [TECH-ascii-render-api](TECH-ascii-render-api.md) — when `--format ascii`.
- [TECH-built-in-themes](TECH-built-in-themes.md) — valid `--theme` values.
- [`../SKILL.md`](../SKILL.md) — parent skill

