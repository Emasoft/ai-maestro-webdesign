---
name: TECH-cli-usage
category: mermaid-render-cli
source: skills/amw-mermaid-render/SKILL.md
---
## Table of Contents

- [Full flag surface](#full-flag-surface)
- [stdin fallback and gotchas](#stdin-fallback-and-gotchas)
- [Common invocation patterns](#common-invocation-patterns)
- [Batch render](#batch-render)

## Usage

All invocations go through the shell wrapper `../../bin/amw-mermaid-render.sh`.
It handles the "external/mermaid-render/ is missing" case cleanly, adds
stdin input (the vendored render.mjs also supports `-i -`), and pipes
ASCII output through the alignment validator.

### Full flag surface

The wrapper forwards all flags verbatim to the vendored `render.mjs`. The backend accepts 17 flags. Core flags: `--input` / `-i` (file or `-` for stdin), `--out` / `-o`, `--format` (svg|ascii), `--theme`, `--bg`/`--fg` (Mono Mode), `--line`/`--accent`/`--muted`/`--surface`/`--border` (7-color enriched), `--font`, `--transparent` (SVG only), `--use-ascii` (pure ASCII), `--padding-x`/`--padding-y`/`--box-border-padding` (ASCII only, default 5/5/1).

Full per-flag detail: [TECH-custom-colors-override](TECH-custom-colors-override.md) and [TECH-ascii-padding-options](TECH-ascii-padding-options.md).

### stdin fallback and gotchas

If `--input` is omitted AND stdin is not a TTY, the wrapper reads Mermaid text from stdin into a temp file. Both `--input -` and the bare stdin form work.

Prefer newlines over semicolons in piped input — shells sometimes re-escape `;` in ways that mangle the parse tree.

```bash
# Reliable
printf 'graph LR\nA --> B\nB --> C\n' | bin/amw-mermaid-render.sh --format svg --out d.svg
```

### Common invocation patterns

```bash
# File → themed SVG
bin/amw-mermaid-render.sh --input diagram.mmd --format svg --theme tokyo-night --out diagram.svg

# Stdin → Unicode ASCII
echo 'graph LR; A --> B --> C' | bin/amw-mermaid-render.sh --input - --format ascii

# Stdin → pure ASCII for README
cat architecture.mmd | bin/amw-mermaid-render.sh --input - --format ascii --use-ascii --out architecture.txt

# Custom 2-color palette (no built-in theme)
bin/amw-mermaid-render.sh --input diagram.mmd --format svg --bg "#0f0f0f" --fg "#e0e0e0" --accent "#ff6b6b" --out diagram.svg

# Transparent background (SVG only)
bin/amw-mermaid-render.sh --input diagram.mmd --format svg --theme github-dark --transparent --out diagram.svg
```

For per-flag color overrides see [TECH-custom-colors-override](TECH-custom-colors-override.md); for ASCII padding flags see [TECH-ascii-padding-options](TECH-ascii-padding-options.md).

### Batch render

```bash
node external/mermaid-render/scripts/batch.mjs --input-dir ./diagrams --output-dir ./rendered --format svg --theme tokyo-night --workers 4
```

`--workers N` defaults to 4 (max ≈ CPU cores). Use for 3+ diagrams. `batch.mjs` has a different arg shape from the wrapper — invoke directly. Full details: [TECH-batch-rendering](TECH-batch-rendering.md).
