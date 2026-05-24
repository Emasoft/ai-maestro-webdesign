# Mermaid diagram technique catalog

Full per-technique reference catalog for `amw-mermaid-diagram`. The orchestrator should read only the file whose TOC matches its current need.

## Technique decision tree

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `mermaid-diagram` is the user asking about?
  - **sequence** (3 techniques)
    - [TECH-sequence-activations](./TECH-sequence-activations.md) — Sequence diagram activations
    - [TECH-sequence-grammar](./TECH-sequence-grammar.md) — Sequence diagram grammar
    - [TECH-sequence-notes-and-loops](./TECH-sequence-notes-and-loops.md) — Sequence diagram — notes, loops, alt/else blocks
  - **edge** (2 techniques)
    - [TECH-edge-best-practices](./TECH-edge-best-practices.md) — Edge best practices — when to use which arrow
    - [TECH-edge-styles](./TECH-edge-styles.md) — Edge styles — arrows, lines, labels
  - **er** (2 techniques)
    - [TECH-er-best-practices](./TECH-er-best-practices.md) — ER diagram best practices
    - [TECH-er-grammar](./TECH-er-grammar.md) — ER diagram grammar (`erDiagram`)
  - **flowchart** (2 techniques)
    - [TECH-flowchart-best-practices](./TECH-flowchart-best-practices.md) — Flowchart authoring best practices
    - [TECH-flowchart-grammar](./TECH-flowchart-grammar.md) — Flowchart grammar — nodes, shapes, direction
  - **class** (1 technique)
    - [TECH-class-grammar](./TECH-class-grammar.md) — Class diagram grammar
  - **diagram** (1 technique)
    - [TECH-diagram-file-organization](./TECH-diagram-file-organization.md) — Diagram file organization — folder layout for `.mmd` libraries
  - **state** (1 technique)
    - [TECH-state-grammar](./TECH-state-grammar.md) — State diagram grammar (`stateDiagram-v2`)
  - **subgraph** (1 technique)
    - [TECH-subgraph-grouping](./TECH-subgraph-grouping.md) — Subgraphs — grouped nodes in flowcharts
  - **terminal** (1 technique)
    - [TECH-terminal-ascii-wrapper](./TECH-terminal-ascii-wrapper.md) — Terminal ASCII authoring — Bun-style one-liner

## Per-technique TOC summary

Every TECH file in this skill's `references/` directory documents a single technique. The TOC bullets below summarize each file's structure — load the file when its TOC matches the current need.

### TECH-class-grammar
**Description:** Class diagram grammar
**TOC:** What it does · When to use · Class definition · Visibility markers · Relationship arrows (UML) · Cardinality · Abstract / interface / generic · Minimal example · Gotchas · Cross-references

### TECH-diagram-file-organization
**Description:** Diagram file organization — folder layout for `.mmd` libraries
**TOC:** What it does · When to use · Recommended layout · Why this works · Naming conventions · Minimal example — integrated with batch render · Gotchas · Cross-references

### TECH-edge-best-practices
**Description:** Edge best practices — when to use which arrow
**TOC:** What it does · When to use · The heuristic table · Label conventions · Arrow density rule · Minimal example — mixed arrows with purpose · Gotchas · Cross-references

### TECH-edge-styles
**Description:** Edge styles — arrows, lines, labels
**TOC:** What it does · Line-and-arrow combinations · Inline label — two syntaxes · Minimal example · Styling edges with `linkStyle` · Gotchas · Cross-references

### TECH-er-best-practices
**Description:** ER diagram best practices
**TOC:** What it does · When to use · The rules · Cardinality clarity · Minimal example — good style · Gotchas · Cross-references

### TECH-er-grammar
**Description:** ER diagram grammar (`erDiagram`)
**TOC:** What it does · When to use · Basic syntax · Cardinality crowsfeet · Attributes (optional but almost always used) · Attribute constraints · Minimal example · Gotchas · Cross-references

### TECH-flowchart-best-practices
**Description:** Flowchart authoring best practices
**TOC:** What it does · When to use · The rules · Anti-patterns to reject · Minimal example — good vs bad · Gotchas · Cross-references

### TECH-flowchart-grammar
**Description:** Flowchart grammar — nodes, shapes, direction
**TOC:** What it does · When to use · Node shapes (authoritative list) · Direction tokens · Connections · Minimal example · Gotchas · Cross-references

### TECH-sequence-activations
**Description:** Sequence diagram activations
**TOC:** What it does · When to use · Syntax · Nested activations — double-stacking · Manual activate/deactivate (alt syntax) · Minimal example · Gotchas · Cross-references

### TECH-sequence-grammar
**Description:** Sequence diagram grammar
**TOC:** What it does · When to use · Participants · Message arrow types · Activations — show processing time · Notes · Loops & alt/else · Minimal example · Gotchas · Cross-references

### TECH-sequence-notes-and-loops
**Description:** Sequence diagram — notes, loops, alt/else blocks
**TOC:** What it does · Notes · Loops · Alt/else · `opt` — optional block (one-sided alt) · `par` — parallel block · Minimal example — realistic API flow · Gotchas · Cross-references

### TECH-state-grammar
**Description:** State diagram grammar (`stateDiagram-v2`)
**TOC:** What it does · When to use · Basic syntax · Composite states — nested state machines · Choice pseudo-state — conditional branching · Concurrency — parallel regions · Notes · Minimal example · Gotchas · Cross-references

### TECH-subgraph-grouping
**Description:** Subgraphs — grouped nodes in flowcharts
**TOC:** What it does · When to use · Syntax · With direction override per subgraph · Minimal example · Gotchas · Cross-references

### TECH-terminal-ascii-wrapper
**Description:** Terminal ASCII authoring — Bun-style one-liner
**TOC:** What it does · When to use · The minimal wrapper · Usage patterns · The key convention — newlines not semicolons · Gotchas · Cross-references
