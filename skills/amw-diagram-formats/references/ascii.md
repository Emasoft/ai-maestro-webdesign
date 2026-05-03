## Table of Contents

- [1. Format definition](#1-format-definition)
- [2. Dimensional constraints](#2-dimensional-constraints)
- [3. Parse rules](#3-parse-rules)
- [4. Emission rules](#4-emission-rules)
- [5. Validation rules](#5-validation-rules)
- [6. Per-source breakdown of the technique catalog](#6-per-source-breakdown-of-the-technique-catalog)
- [7. Technique catalog](#7-technique-catalog)
- [8. Migration note (2026-04-22)](#8-migration-note-2026-04-22)


# ASCII — canonical format reference

This file is the single authoritative spec for ASCII diagrams in the `ai-maestro-webdesign` plugin. Every skill that creates, modifies, validates, or converts ASCII pulls from this file. Format semantics, parsing rules, emission rules, validation rules, and the full technique catalog (95 techniques, migrated from `ascii-creator/` and `ascii-to-html/` into this canonical home) are all below.

**Consumers (cross-references):**
- [SKILL](../../amw-ascii-creator/SKILL.md) — single-artifact ASCII authoring (structured + freeform modes)
- [SKILL](../../amw-ascii-validator/SKILL.md) — validation gate for every ASCII emitter
- [SKILL](../../amw-ascii-sketch/SKILL.md) — plan-phase 3-variant loop
- [SKILL](../../amw-ascii-to-html/SKILL.md) — ASCII → HTML pipeline (consumes technique catalog S7-S9)
- [SKILL](../../amw-ascii-to-svg/SKILL.md) — ASCII → SVG pipeline
- [SKILL](../../amw-box-diagram/SKILL.md) — Unicode rounded-corner box author
- `../../text-visual-{workflows,arch,state,cheatsheets,retro}/SKILL.md` — specialized ASCII archetypes
- `../../bin/amw-ascii-parse.py` — tokenizer (IR input)
- `../../bin/amw-ascii-render.py` — renderer (4 JSON modes)
- `../../bin/amw-validate-ascii.py` — validator (Perl, mandatory gate)
- `../../bin/amw-validate-ascii.py` — validator (Python mirror)
- [ir-schema](./ir-schema.md) — when ASCII is a source of the diagram IR
  > Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Minimal flowchart (3 nodes, 2 edges) · Sequence (two actors, one message + note) · Architecture (3 layers) · Raw-source stub (MVP HTML → IR) · Validation · Consumers
- [conversion-matrix](./conversion-matrix.md) — ASCII → {HTML, SVG, Mermaid, PNG} cells
  > Full N×N table · Cell semantics · PNG-as-source refusal (mandatory) · PNG-as-target pipelines (all supported) · Dispatch algorithm · Per-cell implementation notes · Tools index (required backends) · Related references · ascii · html · svg · mermaid · png
- [modify-flow](./modify-flow.md) — edit flow applied to existing `.txt` / `.md` artifacts
  > The pipeline · Create vs modify dispatch · Step-by-step detail · Step 1 — Detect · Step 2 — Parse to IR · Step 3 — Patch · Step 4 — (loop point) · Step 5 — Emit · Step 6 — Re-validate · Work directory and file naming · Per-format guidance · 1 ASCII modify (MVP structural) · 2 HTML modify (MVP raw-source; Phase 1 structural) · 3 SVG modify (MVP raw-source; Phase 1 structural) · 4 Mermaid modify (MVP raw-source; Phase 1 structural) · Conversion is a modify-flow variant · Composition with round-trip skills · 1 `diagram-webpage-sync` (`/amw-modify-webpage-from-diagram`) · 2 `webpage-to-diagram` (`/amw-modify-diagram-of-webpage`) · Related references · `/amw-create-or-modify-ascii-diagram` → backed by `ascii-creator` · `/amw-create-or-modify-html-diagram` → backed by `html-diagram` · `/amw-create-or-modify-svg-diagram` → backed by `svg-diagram` · `/amw-create-or-modify-mermaid-diagram` → backed by `mermaid-diagram` · `diagram-webpage-sync` / `/amw-modify-webpage-from-diagram` · `webpage-to-diagram` / `/amw-modify-diagram-of-webpage`
- [validation-dispatcher](./validation-dispatcher.md) — unified validator output contract
  > Unified output contract · Dispatch algorithm · PNG refusal message (fixed) · Per-format validator specs · 1 ASCII — `bin/amw-validate-ascii.py` (primary) and `bin/amw-validate-ascii.py` (fallback) · 2 SVG — `bin/amw-validate-svg-diagram.sh` · 3 HTML — `bin/amw-validate-html-diagram.sh` · 4 Mermaid — `bin/amw-mermaid-lint.sh` · Caller integration patterns · 1 Post-create gate · 2 Post-convert gate · 3 Modify-flow loop · 4 Multi-format mode (ascii-validator) · Known limitations (Phase 0) · Related references

---

## 1. Format definition

ASCII diagrams in this plugin are **plain-text files** (`.txt` or `.md` with a fenced block) that use:

- **Unicode box-drawing** (recommended default): `╭ ╮ ╰ ╯ │ ─ ├ ┤ ┬ ┴ ┼ ╌ ╎`
- **Classic ASCII** (terminal/legacy fallback): `+ - |` with `v ^ < >` arrows
- **Rounded-corner Unicode** (for clean pipeline / workflow visuals): `╭ ╮ ╰ ╯ │ ─`

Both Unicode and classic may appear in the plugin, but **never mixed in the same artifact** (TECH-91 below). One file picks one style and stays with it.

### 1.1 Character repertoire

| Class | Unicode (default) | Classic ASCII |
|---|---|---|
| Corners | `╭ ╮ ╰ ╯` (rounded) or `┌ ┐ └ ┘` (square) | `+` (all four) |
| Walls | `│ ─` | `| -` |
| T-junctions | `├ ┤ ┬ ┴` | `+` |
| Cross | `┼` | `+` |
| Dashed (external) | `╌ ╎` | `- -` (spaced) |
| Vertical arrows (safe) | `▾ ▴` (1-col) | `v ^` |
| Horizontal arrows (safe) | `▸ ◂` or `→ ←` | `> <` |
| Dashed borders | `┌╌╌╌╌┐ ╎  ╎ └╌╌╌╌┘` | `+- - -+ \| + -- + \| +- - -+` |

### 1.2 Forbidden characters (validator rejects)

| Char | Why banned | Safe alternative |
|---|---|---|
| `▼` | Variable width in most monospace fonts | `▾` (1-col) or `v` |
| `▲` | Same | `▴` or `^` |
| `▶` | Same | `▸` or `>` |
| `◀` | Same | `◂` or `<` |
| `⟶` / `⇒` | Long-arrow glyphs wider than 1 col | `→` or `->` |
| CJK / emoji in body | Double-width in most fonts | Drop or transliterate |

### 1.3 State / status markers

Inline bracketed tokens carry semantic meaning (picked up by parsers and the HTML emitter):

| Marker | Meaning | HTML mapping |
|---|---|---|
| `[!]` | Alert / warning | `role="alert" aria-live="polite"` |
| `[*]` | Highlight / accent | `.highlight` or `<strong>` |
| `[x]` | Checked / done | `<input type="checkbox" checked>` |
| `[ ]` | Unchecked | `<input type="checkbox">` |
| `(*)` | Radio selected | `<input type="radio" checked>` |
| `( )` | Radio unselected | `<input type="radio">` |
| `(@alice)` | Owner / assignee | `<span class="owner">` |
| `<placeholder>` | Template variable | `<input placeholder>` |

---

## 2. Dimensional constraints

- **Max width**: `78` columns (PR-friendly), also accepts `66` / `72` / `79` profile widths (TECH-93). Renderer's `MAX_WIDTH` constant = 78 (see `../../bin/amw-ascii-render.py`).
- **Min horizontal spacing**: 5 chars between adjacent nodes (TECH-76).
- **Min vertical spacing**: 2 blank lines between stacked nodes (TECH-76).
- **Max label length**: 20 characters; truncate with `...` (TECH-77).

---

## 3. Parse rules

Parser: `../../bin/amw-ascii-parse.py`. Exposes these functions that produce IR ([ir-schema](./ir-schema.md)) for downstream emitters:
> [ir-schema.md] Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Validation · Consumers

| Function | Returns | Drives |
|---|---|---|
| `classify(grid)` | Per-char class (corner / rule / arrow / text) | Tokenization (TECH-93) |
| `detect_format(text)` | `unicode \| ascii \| mixed` | Format branch (TECH-94) |
| `find_boxes(grid)` | List of `{x, y, w, h, text}` | Node extraction (TECH-91) |
| `find_arrows(grid)` | List of `{row, col, symbol, direction}` | Edge extraction (TECH-92) |
| `find_wireframe_components(grid)` | Form / button / radio / check tokens | HTML emission (TECH-95) |
| `to_grid(text, MAX_GRID_DIM)` | 2D char array | Entry point (TECH-96) |

Pipeline emits intermediate JSON to `/tmp/amw-ascii-<slug>-layout.json` (TECH-97) — downstream emitters read the JSON, never the raw ASCII.

---

## 4. Emission rules

Renderer: `../../bin/amw-ascii-render.py`. Reads JSON from stdin, writes ASCII to stdout. **Alignment is guaranteed by construction** — the renderer builds a character grid and places glyphs by coordinate.

### 4.1 Four JSON modes

| Mode | Use case | Key fields |
|---|---|---|
| `diagram` | Freeform node-and-arrow | `nodes[]`, `edges[]`, `layout` |
| `table` | Data tables | `headers[]`, `rows[][]`, `align[]` |
| `layers` | Layered architecture | `layers[]`, each with `nodes[]` |
| `sequence` | Sequence diagrams | `actors[]`, `messages[]` |

All modes output ≤78 columns. All modes go through the same Grid primitive (TECH-88, TECH-89).

### 4.2 Key renderer invariants

- **Column-center arrow lands on first row of destination box, NOT below** (TECH-57)
- **Detour column bend uses `+` corners for L-turns** (TECH-58)
- **Header-to-body separator is a full-width rule row** (TECH-59)
- **Table cell padding = 1 space each side** (TECH-61)
- **Spanning cells suppress internal `+`** (TECH-60)
- **Auto-bus fan-out: `+---+---+---+` at mid-row + `|` drops + `v` heads** (TECH-54)

---

## 5. Validation rules

Validator: `../../bin/amw-validate-ascii.py` (canonical) + `../../bin/amw-validate-ascii.py` (Python mirror). Output contract per [validation-dispatcher](./validation-dispatcher.md).
> [validation-dispatcher.md] Unified output contract · Dispatch algorithm · PNG refusal message (fixed) · Per-format validator specs · Caller integration patterns · Known limitations (Phase 0) · Related references

### 5.1 Checks

1. **WIDTH_MISMATCH** — every line inside a frame has identical width (TECH-89)
2. **VERTICAL_MISALIGNED** — `│` walls share column across body rows (TECH-88)
3. **JUNCTION_ALIGN** — `├` on left aligns with `┤` on right (TECH-90)
4. **NESTED_BOX_CORNERS** — nested corners align vertically
5. **FORBIDDEN_CHAR** — banned glyphs (`▼▲▶◀⟶⇒`, CJK, emoji) → FAIL with `FIX:` hint
6. **WIDE_CHAR_LEAK** — detects double-width char in body

### 5.2 Validation is MANDATORY before delivery

Every skill that emits ASCII MUST pipe through `../../bin/amw-validate-ascii.py` and refuse to ship on FAIL. `mermaid-render` pipes ASCII output through the validator as warn-only (variable-width Mermaid labels are a known issue). All other emitters fail-fast.

---

## 6. Per-source breakdown of the technique catalog

| Src | Source material | TECH range | Focus |
|---|---|---|---|
| S1 | `box-diagram-master` (gold examples) | TECH-01 .. TECH-15 | Rounded-frame dashboards, fan-out, numbered stages |
| S2 | `ascii-diagrams-skill` (CHI'24 refs, 7 files) | TECH-16 .. TECH-36 | Classic `+-|` idioms, decisions, sequences, trees |
| S3 | `cc-plugin-text-visualizations` (5 skills) | TECH-37 .. TECH-53 | Swimlanes, heatmaps, timelines, cheatsheets |
| S4 | `perfect-ascii` renderer | TECH-54 .. TECH-62 | Render invariants, lane labels, bus fan-out |
| S5 | `diagram-skill/ASCII-STYLES.md` | TECH-63 .. TECH-72 | DB shapes, sync/async edges, grouping containers |
| S6 | `baybee-diagram` (SVG ASCII equivalents) | TECH-73 .. TECH-77 | Actors, decisions, spacing, label truncation |
| S7 | `diagram-design-editorial` | TECH-78 .. TECH-87 | 4px grid, one-accent, density, editorial masthead |
| S8 | `bin/amw-validate-ascii.py` (in-repo) | TECH-88 .. TECH-90 | Structural pairing rules enforced by validator |
| S9 | Cross-cutting style rules | TECH-91 .. TECH-95 | Mix bans, widths, blank gaps |

Total: **95 techniques**, 9 sources.

---

## 7. Technique catalog

Format: `TECH-NN <name>: <description> | source: <path>:<line> | applies-to: <use-case>`

### S1 — box-diagram-master (gold examples)

TECH-01 rounded-frame: outer `╭──╮ / │..│ / ╰──╯` as the dashboard / mockup shell | source: box-diagram-master/examples/microservices.txt:3 | applies-to: outer frame of every Mode B variant
TECH-02 3-line-rounded-button: `╭──────╮ / │ label │ / ╰──────╯` per CTA / dropdown / tab | source: ci-cd-pipeline.txt:3-5 | applies-to: Export, Submit, View All, Archive, Drill-down, env filter, week selector, user menu
TECH-03 multi-line-titled-box: rounded outer + `│ ──── │` separator row between title row and body rows | source: incident-response.txt:3-10 | applies-to: KPI cards, alert detail cards, LEAD story callout, stage cards, metric columns
TECH-04 separator-row-inside-box: `│ ──────────── │` (inner-only) row dividing title from body — NEVER extend past the box walls | source: incident-response.txt:5 | applies-to: any titled card, section header inside a box
TECH-05 fan-out-T-junction: `┌──────┬──────┐` horizontal bus + `│` drops + `▾` (safe arrowhead) heads | source: ci-cd-pipeline.txt:7-9 | applies-to: parallel branches, one-input-to-many targets
TECH-06 fan-in-T-junction: `└──────┼──────┘` bottom bus joins many branches back to a single target | source: ci-cd-pipeline.txt:14-16 | applies-to: join-point back to a single owner/action
TECH-07 safe-arrowheads-vertical: use `▾` `▴` (1-col in most monospace) NEVER `▼` `▲` (variable) | source: ci-cd-pipeline.txt:4-5,9 | applies-to: every vertical flow arrow
TECH-08 safe-arrowheads-horizontal: use `▸` `◂` or `>` `<` NEVER `▶` `◀` | source: ci-cd-pipeline.txt:4 | applies-to: every horizontal flow arrow
TECH-09 column-centered-chain: center-align stages vertically by padding left, so a top stage aligns mid-of-box with lower stages | source: microservices.txt:10-12 | applies-to: single-column vertical sequences
TECH-10 asymmetric-tier: a secondary box sits OFFSET from the main axis (side-channel / queue / worker) | source: microservices.txt:22-24 | applies-to: logging, queues, async workers in architecture
TECH-11 numbered-stage-labels: `1. ALERT TRIGGERED` / `2. TRIAGE` / `3a. MITIGATE` style prefixed labels | source: incident-response.txt:4,14,28 | applies-to: time-ordered procedures, numbered lists inside boxes
TECH-12 inline-route-arrow-body: `→ Error rate back to baseline` inside body-text of a box for sub-step cues | source: incident-response.txt:45-48 | applies-to: sub-bullets / verification steps inside a card
TECH-13 gap-line-inside-box: `│                  │` all-space row to visually separate body paragraphs within one card | source: incident-response.txt:17,49 | applies-to: breathing-room between sub-sections of a tall card
TECH-14 three-column-peer-row: three same-width rounded cards sitting side by side at same y, separated by `   ` (3 spaces) | source: incident-response.txt:27-36 | applies-to: parallel-workstream rows, 3-KPI horizontal sets
TECH-15 title-above-frame: plain text title `  CI/CD Pipeline` 2 spaces indented, sitting above the first box, NOT inside the frame | source: ci-cd-pipeline.txt:1 | applies-to: naming a free-standing diagram when no outer frame exists

### S2 — ascii-diagrams-skill (CHI'24 refs, 7 files)

TECH-16 classic-plus-corners: ASCII-only `+----+` / `|  |` / `+----+` for maximum terminal compatibility | source: flowcharts.md:7-9 | applies-to: when Unicode is banned, READMEs, code comments
TECH-17 decision-diamond-plus: `+------+` / `| Valid? |` / `+--+---+--+` with `yes|no` pair branching left-right | source: flowcharts.md:15-20 | applies-to: binary decisions, yes/no gates
TECH-18 v-arrow-into-box: vertical line lands ON the top border with `v` sitting on the `+` | source: flowcharts.md:11-13 | applies-to: vertical step-to-step transitions, any classic ASCII flow
TECH-19 label-on-branch-line: `yes|` `no|` inline adjacent to branch vertical lines | source: flowcharts.md:19 | applies-to: labelled decision branches
TECH-20 sequence-lifelines: vertical `|` columns per actor with horizontal `--> ` labelled messages between them | source: sequences-tables.md:9-16 | applies-to: request/response flows, OAuth handshakes
TECH-21 sequence-return-arrow: `<-- 200 OK ---` right-to-left reply arrow directly below the outbound one | source: sequences-tables.md:14 | applies-to: reply / response messages in a sequence
TECH-22 timeline-notched-axis: `t=0     t=100ms` labels above a `|         |` tick row above event labels | source: sequences-tables.md:19-23 | applies-to: timelines, time-series markers, release/timeline blocks
TECH-23 pipe-column-table: `Method | Path | Handler | Auth` with `----|----|----|----` rule row beneath | source: sequences-tables.md:31-36 | applies-to: data tables inside a frame — endpoints, KPI drilldown, top-N lists
TECH-24 compact-status-table: 2-col `Status | Meaning` with tight padding for enum/dictionary displays | source: sequences-tables.md:40-47 | applies-to: legend, status key, enum lookup
TECH-25 state-loop-arrow: `^` `+` upper-left corner with feedback edge routing back to start | source: state-machines.md:8-23 | applies-to: retry loops, close→reopen transitions
TECH-26 state-uppercase-label: bare UPPERCASE names `IDLE -----> RUNNING -----> COMPLETE` without boxes for compact state chains | source: state-machines.md:28-32 | applies-to: inline state machine summary, caption
TECH-27 bus-spanning-above: `+---+---+---+` horizontal bus feeding vertical `v` drops to three children | source: network-topology.md:16-21 | applies-to: K8s pod layout, router fan-out, horizontal rail diagrams
TECH-28 pod-with-subtext: `| Pod (1)    |` header + `| app:v2.1   |` subtext inside the same rectangular box | source: network-topology.md:18-21 | applies-to: entity with type + version, server cards, endpoint IP
TECH-29 namespace-container-box: outer `+--- NS0 namespace -----+` box containing inner `+-- ipsec0 ----+` boxes | source: network-topology.md:67-72 | applies-to: grouped contexts, logical zones, nested lifecycle scopes
TECH-30 dashed-separator-band: `+- - - - - -+` across a box boundary for external / dotted grouping | source: ASCII-STYLES.md:177 | applies-to: external systems, optional components
TECH-31 linked-list-chain: `+--+    +--+    +--+` boxes connected by `--->` arrows terminating in `NULL` | source: data-structures.md:19-23 | applies-to: queues, linked pipelines, ordered lists
TECH-32 stack-top-bottom: `TOP --> +-----+` / items stacked / `+-----+     BOTTOM` labels outside the box | source: data-structures.md:28-34 | applies-to: stack, queue visualisation
TECH-33 byte-offset-header: `Offset  0         4         8` ruler above a struct box with same-width fields | source: data-structures.md:7-11 | applies-to: data tables with fixed cell widths, field-layout diagrams
TECH-34 comparison-triptych: three `0) Before` / `1) After` / `2) Combined` labels heading vertical subtrees side-by-side | source: graphs-annotations.md:54-69 | applies-to: before/after, A/B/C variants inside one artifact
TECH-35 ui-mockup-sidebar-grid: `+---+---+---------+` with `Sidebar | Main | ...` cells, `Card 1  Card 2` sub-boxes inside the main area | source: graphs-annotations.md:77-90 | applies-to: dashboard / app-shell wireframe outer structure
TECH-36 tree-branch-pipes: `+-- src/` / `|   +-- utils/` / `|   |   +-- helpers.py` for indented hierarchy | source: trees.md:6-23 | applies-to: file trees, component hierarchy sidebars, nav trees

### S3 — cc-plugin-text-visualizations (5 skills)

TECH-37 swimlane-grid: `+------+------+` header row splitting two columns with named lanes `Went Well | Needs Attention` | source: tools-visual-retro/SKILL.md:19-24 | applies-to: retro grids, pros/cons, A/B comparison inside the frame
TECH-38 heatmap-intensity-markers: `[++]` / `[+]` / `[~]` / `[!]` inline markers for relative intensity | source: tools-visual-retro/SKILL.md:27 | applies-to: heat signals, severity key, quality grades
TECH-39 owner-tag: `(@alice)` appended right of action items for attribution | source: tools-visual-retro/SKILL.md:29 | applies-to: assigned alerts, task owners, responsibility indicators
TECH-40 metric-delta: `+12% DAU` / `-4% churn` inline adjacent to the label, sign-prefixed | source: tools-visual-retro/SKILL.md:28 | applies-to: change columns in KPI grids, trend callouts
TECH-41 protocol-label-arrow: `---- HTTP ---->` / `---- gRPC ---->` edge label on the arrow line | source: tools-visual-ascii-arch/SKILL.md:25 | applies-to: architecture edges, annotated service calls
TECH-42 async-squiggle: `~~>` on async events vs `==>` on sync calls | source: tools-visual-workflows/SKILL.md:24 | applies-to: event bus, pub/sub, webhooks
TECH-43 start-end-parens: `(start)` and `(end)` bare labels at flow extremes, no box | source: tools-visual-workflows/SKILL.md:22 | applies-to: compact flow start/end markers
TECH-44 decision-braces: `{ condition? }` inline curly-brace node for decision diamond in compact charts | source: tools-visual-workflows/SKILL.md:24 | applies-to: yes/no gates without drawing full diamond
TECH-45 yes-no-vee-branch: `  /   \ ` paired branches below a decision with `yes` `no` labels sitting on each branch | source: tools-visual-workflows/SKILL.md:33-36 | applies-to: decision fork diagrams
TECH-46 ascii-timeline-dashes: `|-----|-----|-----|` row with `Day 0  Day 3  Day 7` labels above and milestone names below | source: tools-visual-workflows/SKILL.md:38-42 | applies-to: roadmap, sprint calendar, release timeline
TECH-47 sla-suffix: `<24h` / `<200ms` suffix on owner/action labels for latency/duration budgets | source: tools-visual-workflows/SKILL.md:44 | applies-to: KPI rows, SLO displays, deadline markers
TECH-48 legend-block: `[STATE]` box definitions + `-->` arrow legend + `..>` dotted transition legend at top of diagram | source: tools-visual-state-machines/SKILL.md:19 | applies-to: state machines, any skill needing an explicit symbol key
TECH-49 guard-condition-inline: `[Activated] --fails SLA--> [Churn Risk]` with the guard sitting ON the arrow | source: tools-visual-state-machines/SKILL.md:26 | applies-to: labelled transitions
TECH-50 action-slash-block: `/{ send email }` curly block appended to a transition arrow for side-effect | source: tools-visual-state-machines/SKILL.md:31 | applies-to: transition effects, enqueue/notify triggers
TECH-51 table-with-macos-win: `+--------+` 3-column grid with `Action | macOS | Win` headers for platform-parity cheatsheets | source: tools-visual-cheatsheets/SKILL.md:18-24 | applies-to: multi-platform command reference, A/B/C comparison
TECH-52 placeholder-brackets: `<branch>` / `<path>` angle-bracket placeholders inline in text | source: tools-visual-cheatsheets/SKILL.md:32 | applies-to: form-field hints, template variables in code snippets
TECH-53 critical-flag-uppercase: `*` or UPPERCASE label on risky commands for flagging | source: tools-visual-cheatsheets/SKILL.md:29 | applies-to: danger callouts, primary-action emphasis

### S4 — perfect-ascii (renderer)

TECH-54 auto-bus-fan-out-render: 1-to-N rail uses `+---+---+---+` at mid-row with `|` drops and `v` heads — the renderer's `bus pattern` | source: perfect-ascii/bin/ascii-render:977-989 | applies-to: architecture fan-outs when hand-drawn
TECH-55 title-above-lane-margin: diagram title in column `label_margin`, boxes offset right of lane labels | source: perfect-ascii/bin/ascii-render:924 | applies-to: swimlane diagrams with left-side lane labels
TECH-56 lane-label-rightjust: `  Frontend |` right-justified lane name followed by a single `|` wall, rest-of-row is the lane content | source: perfect-ascii/bin/ascii-render:258-262 | applies-to: swimlanes, resource tracks, team rows
TECH-57 column-center-arrow: `v` arrow lands on the first row of the destination box, NOT below | source: perfect-ascii/bin/ascii-render:378-379 | applies-to: every vertical arrowhead placement
TECH-58 detour-column-bend: `+` corner at L-turns for hop-around-obstacle routing via an available column | source: perfect-ascii/bin/ascii-render:449-451 | applies-to: crossing lines that cannot go straight
TECH-59 separator-after-header-rule: `+-----+----+` full-width rule row after headers in a table | source: perfect-ascii/bin/ascii-render:766-773 | applies-to: header/body separator in any table
TECH-60 span-suppress-plus: in tables, `+` is suppressed at internal column boundaries when a cell spans multiple columns | source: perfect-ascii/bin/ascii-render:754-762 | applies-to: summary rows, spanning title cells, merged headers
TECH-61 pad-1-space-each-side: table cell padding is exactly 1 space left + 1 space right of content | source: perfect-ascii/bin/ascii-render:790-791 | applies-to: every table cell for consistent vertical line positions
TECH-62 align-tokens-left-right-center: per-column `align` list drives `.ljust/.rjust/.center` formatting | source: perfect-ascii/bin/ascii-render:784-790 | applies-to: numeric columns right-aligned, text left-aligned

### S5 — diagram-skill styles (ASCII-STYLES.md)

TECH-63 detallado-rounded-db: `╭──╮ / │ DB │ / ╰──╯` rounded-corner BOTTOM-ONLY for database nodes, square top for everything else | source: ASCII-STYLES.md:35-38 | applies-to: DB node in architecture diagrams
TECH-64 queue-squiggle-border: `≋≋≋≋≋≋≋  / ≋ Queue ≋ / ≋≋≋≋≋≋≋` wavy top/bottom border for queue types | source: ASCII-STYLES.md:164 | applies-to: message queue nodes — WARNING: check font support before using, or keep for `detallado` only
TECH-65 dashed-external-border: `┌╌╌╌╌╌╌┐ / ╎ ext ╎ / └╌╌╌╌╌╌┘` dashed border for external systems | source: ASCII-STYLES.md:165 | applies-to: third-party APIs, out-of-scope components
TECH-66 sync-vs-async-edge: solid `---->` sync; dashed `- - >` async; these render differently in every style | source: ASCII-STYLES.md:188-190 | applies-to: every architecture edge — must choose which one
TECH-67 bidi-arrow: `<--->` (classic) / `◀──▶` (detallado, but `◀/▶` are MEDIUM banned — prefer classic) | source: ASCII-STYLES.md:191 | applies-to: bidirectional pipes, socket, replication
TECH-68 dependency-arrow: `----D` classic / `───▷` detallado — hollow head for dependency not flow | source: ASCII-STYLES.md:192 | applies-to: UML-style dependency edges
TECH-69 compact-tee-fanout: `Client → Gateway ─┬─→ Service A` / `└─→ Service B` single-line horizontal fan-out | source: ASCII-STYLES.md:139-141 | applies-to: one-line caption summaries
TECH-70 group-container-box: `+------ Backend Services -----+` title-on-border box containing smaller service nodes | source: ASCII-STYLES.md:223-231 | applies-to: grouping containers, logical boundary, region
TECH-71 note-companion-box: primary `┌─ Service ─┐` + adjacent `┌─ Note: ... ─┐` floating note box | source: ASCII-STYLES.md:248-253 | applies-to: callouts, side-notes attached to a node
TECH-72 rate-limit-inline: `┌────┐ (Rate limit: 100/min)` parenthesis annotation to the right of the box | source: ASCII-STYLES.md:240-243 | applies-to: attribute callouts on a node without enlarging the box

### S6 — baybee-diagram (SVG patterns with ASCII equivalents)

TECH-73 user-circle-actor: for `actor`, render as `  O / /|\ / / \` stick figure OR `+---+ | User | +---+` boxed label — boxed is ASCII-safe | source: SKILLS-TO-INTEGRATE/diagrams-skills/baybee-diagram/SKILL.md:47 | applies-to: user-personas in flow diagrams
TECH-74 decision-diamond-unicode: `    ◇ / ╱ ╲ / ◇   ◇ / ╲ ╱ /  ◇` explicit Unicode diamond (heavier than classic `{}`); detallado-only | source: ASCII-STYLES.md:166 | applies-to: explicit yes/no gate with strong visual emphasis
TECH-75 connection-semantics-table: use different edge styles (solid=sync, dashed=async, hollow=dependency) and label them in a legend block | source: SKILLS-TO-INTEGRATE/diagrams-skills/baybee-diagram/SKILL.md:73-90 | applies-to: any multi-edge-type diagram needing semantic legend
TECH-76 minimum-horizontal-spacing: 5 chars between horizontal nodes, 2 blank lines between vertical nodes | source: ASCII-STYLES.md:262-264 | applies-to: enforce breathing room, readability minimums
TECH-77 label-max-20-char-truncate: labels > 20 chars must be truncated with `...` | source: ASCII-STYLES.md:259-261 | applies-to: long endpoint names, class names, long KPI labels

### S7 — diagram-design-editorial (editorial)

TECH-78 4px-grid-align: every coordinate divisible by 4 prevents AI-generated jitter (ASCII analog: lock every column offset to multiples of 4) | source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md:139 | applies-to: any multi-column grid, gap computation
TECH-79 one-accent-rule: exactly 1 accent node per diagram, rest are neutral; ASCII analog: one `[!]` / `*` marker, one only | source: diagram-design-editorial/SKILL.md:152-154 | applies-to: alert rows, status lists, priority highlights
TECH-80 4-of-10-density: 4-5 nodes max per diagram, 8+ is cluttered; ASCII analog: trim KPI grid, navigation items | source: diagram-design-editorial/SKILL.md:537-542 | applies-to: node count discipline, prevent-clutter hygiene
TECH-81 sparse-hairline-border: single-line `─│┌┐└┘` NEVER doubled `═║╔╗╚╝` unless explicitly editorial — single-line is always safer | source: diagram-design-editorial/SKILL.md:142 | applies-to: outer frame, KPI cards, section dividers
TECH-82 editorial-title-small-caps: `THE  MAESTRO  DAILY` with double spaces between words and uppercase for editorial masthead tone | source: Dashboard Experimental.txt:2 | applies-to: newspaper / magazine / poster variants
TECH-83 three-column-editorial-row: `├──────┬──────┬──────┤` row joins, T-junction tops/bottoms sharing a horizontal rule above and below | source: Dashboard Experimental.txt:9,17 | applies-to: three equal editorial columns sharing a horizontal rule (PERFORMANCE / COST / RELIABILITY)
TECH-84 lead-story-block: italic-weight title line `LEAD` + rule + 2-3 narrative sentences in a top position | source: Dashboard Experimental.txt:4-8 | applies-to: hero / primary-callout / above-the-fold summary
TECH-85 metric-arithmetic-in-cell: `compute  +$ 18` / `egress    -$ 6` name + right-padded delta inside the metric cell | source: Dashboard Experimental.txt:13-16 | applies-to: accounting tables, KPI breakdown rows
TECH-86 rail-with-filler-spaces: `·` (middle dot) as filler between navigation items: `Overview · Workloads · Alerts` | source: Dashboard Baseline.txt:2 | applies-to: nav bar, menu rail, breadcrumb
TECH-87 right-justified-user-slot: user profile badge `│...                     ╭──user──╮   │` pushed to far right of frame | source: Dashboard Baseline.txt:4 | applies-to: header bar, top-right user menu, context indicator

### S8 — Structural pairing rules (enforced by validator)

TECH-88 left-right-walls-same-col: every `│` on the left wall must sit in identical column across all body rows | source: bin/amw-validate-ascii.py (VERTICAL_MISALIGNED rule) | applies-to: any framed Mode B artifact
TECH-89 same-width-lines: pad trailing spaces so every line inside the frame has IDENTICAL width | source: bin/amw-validate-ascii.py (WIDTH_MISMATCH rule) | applies-to: everything framed
TECH-90 junction-char-align: `├` on the frame left aligns with `┤` on the same row, both aligned with vertical walls above/below | source: bin/amw-validate-ascii.py (VERTICAL_MISALIGNED rule) | applies-to: dashboard cross-rules, section dividers

### S9 — Cross-cutting style rules

TECH-91 dont-mix-ascii-and-unicode: pick `+---+` OR `┌──┐` for one artifact, never interleave | source: ascii-creator/SKILL.md:78 | applies-to: every variant, hard rule
TECH-92 comment-title-outside-frame: name / date / vol number OUTSIDE the frame, left-aligned with 2-space indent | source: ci-cd-pipeline.txt:1 | applies-to: diagram caption, file-level title above framed content
TECH-93 width-66-72-79-only: stick to 66 / 72 / 79 column widths (terminals, terminals-wider, PR-max) | source: perfect-ascii/bin/ascii-render:11 | applies-to: frame-width selection at authoring time
TECH-94 body-row-gap-blanks: 1 blank `│          │` row between each KPI card row and the next cross-rule, for breathing room | source: Dashboard Baseline.txt:7,13,28 | applies-to: vertical rhythm inside a framed dashboard
TECH-95 dot-separator-pair: `  ·  ` (space-dot-space, 3 chars) as semantic pause between list items | source: Dashboard Baseline.txt:31 | applies-to: status strips, meta bars, inline caption

---

## 8. Migration note (2026-04-22)

This file is the **canonical home** for the ASCII technique catalog. It supersedes (in migration order):
- `skills/amw-ascii-creator/references/techniques.md` (95 techniques, moved here in full)
- `skills/amw-ascii-to-html/references/techniques.md` (100 techniques → S7/S9 of [html](./html.md); ASCII-parse hooks S9 mirrored here in §3)
  > Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22) · ai-slop-avoid · `../../amw-design-principles/starter-components/*` — all 9 canonical chrome components · color-system · typography-system · SKILL · SKILL · SKILL · SKILL · SKILL · `../../bin/amw-html-export.py` — HTML → PNG/PDF rasterizer (Playwright) · `../../bin/amw-ascii-parse.py` — ASCII → layout JSON consumed by HTML emitter · ir-schema · conversion-matrix · modify-flow · validation-dispatcher
  > Format definition · 1 File structure (baseline) · 2 Semantic-HTML requirements · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · 1 Listener-before-announce · 2 Partial-keys only · 3 Valid JSON EDITMODE block · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · S1 — design-principles starter-components (canonical chrome) · S2 — ai-slop-avoid (output-ban gate) · S3 — ui-ux-pro-max-skill (industry patterns) · S4 — ux-designer + accessibility · S5 — create-infographics (editorial density) · S6 — diagram-design-editorial (self-contained HTML+SVG) · S7 — ascii-creator mirror (pattern recognition) · S8 — CHI'24 ASCII classics (mockup → HTML skeleton) · S9 — ascii-parse.py (in-repo tokenizer hooks) · Migration note (2026-04-22) · ai-slop-avoid · `../../amw-design-principles/starter-components/*` — all 9 canonical chrome components · color-system · typography-system · SKILL · SKILL · …(+9)

Both original files are preserved at `docs_dev/backups/<timestamp>-phase0-refs/` and now carry a 3-line pointer referencing this file. Future edits to technique catalogs go here, not in per-skill references.
