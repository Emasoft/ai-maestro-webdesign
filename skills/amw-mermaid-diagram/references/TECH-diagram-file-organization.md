---
name: TECH-diagram-file-organization
category: mermaid-grammar
source: diagrams-skills/Pretty-mermaid-skills-main/references/DIAGRAM_TYPES.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Recommended layout](#recommended-layout)
- [Why this works](#why-this-works)
- [Naming conventions](#naming-conventions)
- [Minimal example — integrated with batch render](#minimal-example-integrated-with-batch-render)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Diagram file organization — folder layout for `.mmd` libraries

## What it does

Filesystem convention for organizing a collection of `.mmd` diagram
sources. Mirrors the structure of the content — architecture /
workflows / database — and plays nicely with batch rendering.

## When to use

- Docs repo with 10+ Mermaid diagrams.
- Design system that ships diagram sources alongside component code.
- Multi-service project where each service has its own architecture
  diagram.

## Recommended layout

```
diagrams/
├── architecture/
│   ├── system-overview.mmd
│   └── data-flow.mmd
├── workflows/
│   ├── user-registration.mmd
│   └── checkout-process.mmd
└── database/
    ├── schema-users.mmd
    └── schema-orders.mmd
```

## Why this works

- **Topic folders** group diagrams that share context — readers don't
  have to hunt.
- **Short names** — `system-overview.mmd`, not
  `our-full-system-overview-diagram-v2.mmd`.
- **Play with batch** — `node scripts/batch.mjs --input-dir
  diagrams/architecture -o output/architecture` works per-folder.

## Naming conventions

- Use lowercase kebab-case filenames — `user-flow.mmd`, not
  `UserFlow.mmd` or `user_flow.mmd`.
- Don't embed the diagram type in the filename
  (`user-flow-flowchart.mmd`) — the file extension and opening
  keyword (`flowchart LR`) carry that info.
- Date prefixes (`2026-04-auth-flow.mmd`) are overkill — use git
  history.

## Minimal example — integrated with batch render

```bash
# source: diagrams-skills/Pretty-mermaid-skills-main/SKILL.md — adapted
# Render the whole folder tree in parallel
for dir in diagrams/*/; do
  node scripts/batch.mjs \
    --input-dir "$dir" \
    --output-dir "output/${dir#diagrams/}" \
    --format svg \
    --theme tokyo-night \
    --workers 4
done
```

## Gotchas

- `batch.mjs` is not recursive — you need one invocation per
  subfolder.
- Paths with spaces require quoting everywhere.
- If you also have `.mermaid` extensions, the batch script only picks
  up `.mmd` by default — rename or extend the filter.

## Cross-references

- [TECH-batch-rendering](../../amw-mermaid-render/references/TECH-batch-rendering.md) — the
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  batch script.
- [TECH-flowchart-grammar](TECH-flowchart-grammar.md) — what goes inside each file.
  > What it does · When to use · Node shapes (authoritative list) · Direction tokens · Connections · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

