---
name: TECH-flowchart-grammar
category: mermaid-grammar
source: diagrams-skills/Pretty-mermaid-skills-main/references/DIAGRAM_TYPES.md
also-in: diagrams-skills/agent-skill-diagramming-flows-main/SKILL.md
---

# Flowchart grammar — nodes, shapes, direction

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Node shapes (authoritative list)](#node-shapes-authoritative-list)
- [Direction tokens](#direction-tokens)
- [Connections](#connections)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

The Mermaid `flowchart` (also `graph`) grammar authors a directed
graph of labeled nodes connected by arrows. It's the most common
Mermaid diagram type — processes, workflows, decision trees.

## When to use

- Documenting a process / workflow with one start and one end.
- Decision trees — `{Rhombus}` nodes for branches.
- System flows with 5-30 nodes.

## Node shapes (authoritative list)

```
[Text]      Rectangle             (default)
([Text])    Stadium               (rounded ends — start/end)
[[Text]]    Subroutine            (double border)
[(Text)]    Cylindrical           (database)
((Text))    Circle
>Text]      Asymmetric            (rarely used)
{Text}      Rhombus               (decision)
{{Text}}    Hexagon               (preparation)
[/Text/]    Parallelogram         (input/output)
[\Text\]    Trapezoid alt
```

## Direction tokens

```
flowchart LR     Left-to-right    (widescreen)
flowchart TD     Top-down         (portrait, default in many renderers)
flowchart TB     Top-to-bottom    (alias of TD)
flowchart BT     Bottom-to-top    (inverted)
flowchart RL     Right-to-left    (inverted)
```

## Connections

```
A --> B          Arrow
A --- B          Line (no arrow)
A -.-> B         Dotted arrow
A ==> B          Thick arrow
A --text--> B    Arrow with inline text
A -->|text| B    Arrow with text (alt syntax)
```

## Minimal example

```mermaid
%% source: diagrams-skills/Pretty-mermaid-skills-main/references/DIAGRAM_TYPES.md
flowchart LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
```

## Gotchas

- Use `LR` for wide screens — `TD` can cause 20-node diagrams to need
  vertical scrolling in a blog post.
- Decision nodes must be `{diamond}` — a regular `[rect]` node with
  the text "Decision" reads as a process, not a branch.
- `A-->B` (no spaces) works but `A -- B` (no arrow) fails silently —
  add the `--` explicitly. The renderer's error is cryptic.
- Limit nesting (subgraphs inside subgraphs) to 2 levels — readers
  lose the plot past that.

## Cross-references

- [TECH-subgraph-grouping](TECH-subgraph-grouping.md) — composite / nested flowcharts.
  > What it does · When to use · Syntax · With direction override per subgraph · Minimal example · Gotchas · Cross-references
- [TECH-edge-styles](TECH-edge-styles.md) — arrows, labels, line styles in depth.
  > What it does · Line-and-arrow combinations · Inline label — two syntaxes · Minimal example · Styling edges with `linkStyle` · Gotchas · Cross-references
- [TECH-sequence-grammar](TECH-sequence-grammar.md) — the Mermaid cousin for API/message flows.
  > What it does · When to use · Participants · Message arrow types · Activations — show processing time · Notes · Loops & alt/else · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

