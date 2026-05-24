# Technique Index — amw-diagram-architecture

## Table of Contents

- [Decision tree (top-down)](#decision-tree-top-down)
- [Per-file TOC summary](#per-file-toc-summary)

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

## Decision tree (top-down)

Which aspect of `diagram-architecture` is the user asking about?

- **arrow** (1 technique)
  - [TECH-arrow-vocabulary](./TECH-arrow-vocabulary.md) — 6-type connection taxonomy
- **assistant** (1 technique)
  - [TECH-assistant-prefill-json](./TECH-assistant-prefill-json.md) — assistant prefill `{` to force JSON-first output
- **edge** (1 technique)
  - [TECH-edge-budget-rule](./TECH-edge-budget-rule.md) — edges = floor(n × 0.8) rule
- **export** (1 technique)
  - [TECH-export-mermaid-plantuml-d2](./TECH-export-mermaid-plantuml-d2.md) — one YAML, four output formats
- **graph** (1 technique)
  - [TECH-graph-json-schema](./TECH-graph-json-schema.md) — canonical graph JSON schema
- **json** (1 technique)
  - [TECH-json-repair-recipe](./TECH-json-repair-recipe.md) — strip fences / extract braces / strip trailing commas / normalise newlines
- **layer** (1 technique)
  - [TECH-layer-palette-5-colors](./TECH-layer-palette-5-colors.md) — five-layer oklch + hex palette
- **png** (1 technique)
  - [TECH-png-export-bridge](./TECH-png-export-bridge.md) — SVG-as-source plus optional cairosvg path
- **stage1** (1 technique)
  - [TECH-stage1-graph-validation](./TECH-stage1-graph-validation.md) — every Stage 1 check + fix
- **style** (1 technique)
  - [TECH-style-presets](./TECH-style-presets.md) — `detallado` / `unicode` / `clasico` / `compacto`
- **svg** (1 technique)
  - [TECH-svg-layered-layout](./TECH-svg-layered-layout.md) — 820px canvas + 160×64 cards + cubic-bezier edges
- **version** (1 technique)
  - [TECH-version-history-yaml](./TECH-version-history-yaml.md) — v1 / v2 / ... + history.yaml + rollback
- **yaml** (1 technique)
  - [TECH-yaml-canonical-schema](./TECH-yaml-canonical-schema.md) — `meta / nodes / edges / groups / notes`

## Per-file TOC summary

Each reference file has a consistent TOC structure:

- **What it does**
- **When to use**
- **How it works**
- **Minimal example**
- **Gotchas**
- **Cross-references**

Some files additionally include **Constraints** (e.g. TECH-graph-json-schema.md).

Read the specific TECH-*.md file when its decision-tree branch matches the user's intent.
