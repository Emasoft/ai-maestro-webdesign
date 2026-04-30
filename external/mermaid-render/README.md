# external/mermaid-render

Vendored backend for the `skills/mermaid-render/` skill.

This directory contains three small wrapper scripts around the
[`beautiful-mermaid`](https://www.npmjs.com/package/beautiful-mermaid) npm
package. They consolidate the CLI surface of three upstream Claude skills
(`beautiful-mermaid`, `pretty-mermaid`, `agent-skill-diagramming-flows`)
into one entry point used by `bin/mermaid-render.sh`.

## Layout

```
external/mermaid-render/
├── package.json           Depends only on beautiful-mermaid@^0.1.3
├── LICENSE                MIT (covers wrappers; beautiful-mermaid is separately MIT)
├── README.md              This file
├── scripts/
│   ├── render.mjs         Render one Mermaid → SVG or ASCII
│   ├── batch.mjs          Render a directory of .mmd → a directory of .svg / .txt
│   └── themes.mjs         List the 15 built-in themes
└── examples/
    ├── flowchart.mmd
    ├── sequence.mmd
    ├── state.mmd
    ├── class.mmd
    └── er.mmd
```

## Runtime install

On first render, `render.mjs` will auto-run `npm install` inside this
directory if `node_modules/beautiful-mermaid` is missing. The resulting
`node_modules/` and any `dist/` artifacts are gitignored at the repo root
(see the top-level `.gitignore` — `external/*/node_modules/` + `dist/`).

If you prefer an explicit install, run:

```bash
cd external/mermaid-render
npm install --no-fund --no-audit
```

The plugin's `/wd-init` command includes an opt-in step that does this.

## Usage

Prefer the wrapper at `bin/mermaid-render.sh` in the plugin root — it adds
stdin support, the `validate-ascii.pl` post-check for ASCII output, and the
"run /wd-init" hint when this directory is missing.

Direct use (for debugging):

```bash
node external/mermaid-render/scripts/render.mjs \
  --input examples/flowchart.mmd \
  --format svg \
  --theme tokyo-night \
  --out /tmp/flowchart.svg

node external/mermaid-render/scripts/render.mjs \
  --input examples/flowchart.mmd \
  --format ascii \
  --use-ascii
```

## Themes

15 built-in themes (all dark + light variants):

```
zinc-light, zinc-dark,
tokyo-night, tokyo-night-storm, tokyo-night-light,
catppuccin-mocha, catppuccin-latte,
nord, nord-light,
dracula,
github-light, github-dark,
solarized-light, solarized-dark,
one-dark
```

List them at runtime: `node scripts/themes.mjs`.

## Provenance

Upstream sources (MIT):

- https://github.com/lukilabs/beautiful-mermaid (TS API, 15 themes)
- Pretty-mermaid-skills (author: Alex) — CLI + batch
- agent-skill-diagramming-flows (Bun ASCII-only CLI)

The npm package `beautiful-mermaid@^0.1.3` (also MIT) is **not** vendored —
it is fetched by npm at install time. This keeps the plugin repo reviewable
and lets upstream security patches flow through normal npm channels.
