---
name: TECH-flowchart-paren-bracket-glyphs
category: text-visual-workflow
source: cc-plugin-text-visualizations-main/skills/tools-visual-workflows/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-flowchart-paren-bracket-glyphs — `(start)` `[action]` `{decision?}`

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Uses lightweight ASCII punctuation as node-shape markers so a workflow
flowchart fits cleanly in plain-text chat, PRs, Slack, and GitHub
comments — no Unicode required. Different shapes map to different node
kinds: rounded-paren endpoints, square-bracket processes, curly-brace
decisions.

## When to use

- PR body flowcharts where Unicode rendering is inconsistent
- Slack-pasteable workflow sketches
- Lightweight sketches where a full `+--+` box is overkill
- Quick brainstorms in issue comments

## How it works

| Glyph | Meaning |
|---|---|
| `(start)` / `(end)` | Terminal nodes |
| `[ action ]` | Process step (verb + object) |
| `{ condition? }` | Decision point |
| `-->` | Sync transition |
| `==>` | Emphasized / primary path |
| `~~>` | Async transition |

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-workflows/SKILL.md lines 28-36
(start)
  |
[Step 1]
  |
{Decision?}
 /   \
yes   no
```

## Gotchas

- Paren / bracket / brace glyphs all render 1-col in every monospace
  font, so alignment is never an issue.
- Don't mix them with `+--+` boxes in the same diagram — pick one
  visual vocabulary per artifact.
- For workflows with many decision points, a pure-text flowchart gets
  messy; switch to `../../amw-ascii-creator/` Mode A with JSON and let the
  renderer handle alignment.

## Cross-references

- [TECH-timeline-with-anchors](./TECH-timeline-with-anchors.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-swimlane-parallel-tracks](./TECH-swimlane-parallel-tracks.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-render-mode-diagram](../../amw-ascii-creator/references/TECH-render-mode-diagram.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

