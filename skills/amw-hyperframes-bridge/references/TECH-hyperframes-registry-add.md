---
name: TECH-hyperframes-registry-add
category: hyperframes-registry
source: external/hyperframes/skills/hyperframes-registry/SKILL.md
also-in:
---

# TECH: `hyperframes add` — install registry blocks + components

## What it does

Installs reusable blocks (standalone sub-compositions) and components (effect snippets) from the hyperframes registry into the current project. After install, the CLI prints which files were written and a wiring snippet to paste into the host composition.

## When to use

When a composition needs a complex sub-composition (data chart, decision tree, kinetic type) or an effect overlay (grain, shimmer, glow) that's already implemented in the registry — rather than rebuilding from scratch.

## How it works

```bash
# Install a block (standalone sub-composition)
hyperframes add data-chart

# Install a component (effect snippet)
hyperframes add grain-overlay

# Target a specific project directory
hyperframes add shimmer-sweep --dir .

# Machine-readable output
hyperframes add data-chart --json

# Skip clipboard (CI / headless — the snippet is printed to stdout)
hyperframes add data-chart --no-clipboard
```

### Blocks vs components

| Type | What it is | Install location | Wiring |
|---|---|---|---|
| **Block** | Standalone sub-composition with own dimensions, duration, timeline | `compositions/<name>.html` | Include via `data-composition-src` in host |
| **Component** | Effect snippet — no own dimensions | `compositions/components/<name>.html` | Paste HTML + CSS + JS into host composition |

### Paths (configurable in `hyperframes.json`)

```json
{
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": {
    "blocks": "compositions",
    "components": "compositions/components",
    "assets": "assets"
  }
}
```

Note: `hyperframes add` only installs blocks and components. For shipped examples, use `hyperframes init <dir> --example <name>`.

## Minimal example

```bash
# Install a data chart block
$ hyperframes add data-chart
✓ Installed compositions/data-chart.html
Clipboard: wiring snippet copied

# Paste into index.html:
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="15"
  data-track-index="1"
  data-width="1920"
  data-height="1080"></div>
```

*Attributed to the hyperframes-registry skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes-registry/SKILL.md`.*

## Gotchas

- The snippet printed after install is a starting point — you still need to set `data-start`, `data-track-index`, and (for blocks) `data-composition-id` matching the block's internal ID.
- Installing the same block twice overwrites the first install. Back up customizations before re-installing.
- Registry URL points to `heygen-com/hyperframes/main/registry` by default. To use a fork or private registry, override `registry` in `hyperframes.json`.

## Cross-references

- `TECH-hyperframes-registry-blocks.md` — detailed block-wiring rules
- `TECH-hyperframes-registry-components.md` — detailed component-wiring rules
- `TECH-hyperframes-cli-init.md`
- `../SKILL.md`
