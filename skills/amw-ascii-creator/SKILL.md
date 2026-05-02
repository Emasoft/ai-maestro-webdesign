---
name: amw-ascii-creator
description: >-
  Produce ONE validated perfect-ASCII artifact from a brief — structured diagrams via bin/amw-ascii-render.py (perfect-ascii JSON → ASCII), freeform wireframes via hand-author-validate-iterate loop using bin/amw-validate-ascii.py. Use when converting a finalized brief into a single validated ASCII file ready for ascii-to-html. Triggers on narrow authoring intents only — "ASCII diagram of", "ASCII wireframe of", "create an ASCII flowchart", "perfect ASCII of", "build an ASCII mockup", "finalize ASCII for a subject". Does NOT trigger on generic design intent — those go to design-principles → ascii-sketch (plan-phase, 3 variants). This is the FINISHING skill — one invocation, one validated .txt file delivered. ascii-to-html consumes its output.
version: 0.1.0
---

# ASCII Creator

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> **Single-artifact authoring skill.** The plugin's plan-phase is `../amw-ascii-sketch/` (iterates three variants). This skill is for the opposite case — the user already knows what diagram they want, and wants ONE perfect ASCII file delivered. It is the ASCII twin of `../amw-svg-creator/`.

## Overview

Produces ONE validated perfect-ASCII artifact from a brief. Uses `bin/amw-ascii-render.py` for structured diagrams (Mode A) or a hand-author-validate-iterate loop via `bin/amw-validate-ascii.py` (Mode B). The finishing skill — one invocation, one validated `.txt` file delivered.

## Activation

Callable directly via the `/amw-create-or-modify-ascii-diagram` command (user shortcut — fast path for single-artifact ASCII creation or modification). Also invoked by the `design-principles` orchestrator as a Phase B finisher after Phase A approval in Main-agent mode, when the user has committed to a specific ASCII artifact. In Main-agent mode the orchestrator may apply Mode A (structured via ascii-render.py) or Mode B (freeform validate-iterate) techniques from this skill beyond what the command exposes.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**OUTPUT (Phase B).** Takes a natural-language diagram brief → produces exactly one `.txt` file containing validated perfect-ASCII. Downstream of `../amw-design-principles/` for any "I know what I want, make it perfect" authoring request. Upstream of `../amw-ascii-to-html/` when the artifact is a wireframe and the user wants HTML next.

This skill does NOT:
- Iterate three variants (that is `../amw-ascii-sketch/`'s plan-phase role)
- Emit partial / un-validated drafts into chat
- Pick the format from design vocabulary ("design a dashboard") — that is `../amw-design-principles/`'s routing job; it will route here only when the user has already committed to an ASCII artifact

## Trigger conditions

- "ASCII diagram of <system>" / "perfect ASCII diagram of <flow>"
- "ASCII wireframe of <screen>" / "finalize this ASCII"
- "create an ASCII flowchart / table / sequence / layered architecture"
- "perfect ASCII of the <subject>"
- "build an ASCII mockup of <screen>" — single mockup, not a set
- After `/amw-sketch` approval, when the approved variant needs to be rendered to file (alternative path to `/amw-ascii-to-html` for ASCII-only deliverables)

Do NOT trigger on:
- "design a dashboard" / "mockup a UI" — broad design vocabulary, orchestrator's job
- "show me three options" / "iterate in ASCII" — plan-phase, `../amw-ascii-sketch/`'s job

## Instructions

1. Classify the brief as Mode A (structured: flowchart, table, layers, sequence) or Mode B (freeform rectangular wireframe/mockup).
2. For Mode A: build the JSON spec, run `bin/amw-ascii-render.py`, sanity-check the rendered output, fix JSON errors and re-render until correct.
3. For Mode B: author the ASCII frame, substitute banned characters before writing, save to `/tmp/ascii-creator-<slug>.txt`, run `bin/amw-validate-ascii.py`.
4. Iterate on FIX hints from the validator until the output reaches PASS status; apply every hint, re-validate.
5. Apply the matching style preset (`detallado`, `unicode`, `clasico`, or `compacto`) based on brief context or explicit request.
6. Save the validated artifact with a descriptive English filename; write the job-completion report to `reports/webdesigner/`.

## Two authoring modes (the skill classifies automatically)

### Mode A — Structured (flowchart, table, layers, sequence)

Use when the brief describes a STRUCTURE — nodes + edges, rows + columns, tiers, messages between actors. The renderer `../../bin/amw-ascii-render.py` draws it pixel-perfect from a JSON spec, so alignment is guaranteed by construction.

**Sub-modes:**

| Sub-mode | When to use | Example intent |
|---|---|---|
| `diagram` | Flowcharts, ER diagrams, state machines, block diagrams | "ASCII flowchart of the login flow" |
| `table`   | Data grids, comparison matrices | "ASCII table comparing A vs B vs C" |
| `layers`  | Layered architecture with bus connectors between tiers | "ASCII architecture of web / api / db tiers" |
| `sequence`| Sequence diagrams with lifelines | "ASCII sequence of the OAuth flow" |

**Workflow:**

1. Parse the brief. Identify sub-mode + extract entities (boxes, rows, connectors, etc.).
2. Build JSON matching the schema in `../../bin/amw-ascii-render.py`'s top-of-file docstring. Keep labels under ~15 chars (renderer constraint).
3. Run:
   ```bash
   echo '<JSON>' | python3 ../../bin/amw-ascii-render.py > /tmp/ascii-creator-<slug>.txt
   ```
   Non-zero exit → fix the JSON and retry. Typical errors: label too long, grid references a missing box id, connector refers to non-existent box, total width > 78 columns.
4. Open the rendered `.txt` and sanity-check it visually. If connections look wrong or the layout is cramped, adjust the `grid` / `connectors` / `lanes` in the JSON and re-render.
5. Save final: `cp /tmp/ascii-creator-<slug>.txt <working-dir>/<Descriptive Name>.txt`

Structured output from `ascii-render.py` is NOT expected to pass the frame-width validator (it's trimmed-line, not framed). Skip the frame validator for Mode A. If the user explicitly wants the structured diagram wrapped in a frame, switch to Mode B after rendering.

### Mode B — Freeform wireframe (framed rectangular UI mockup)

Use when the brief describes a RECTANGULAR artifact — dashboard, mobile frame, editorial poster, newspaper-column layout. The renderer cannot produce these; they are hand-authored, and alignment is enforced by `../../bin/amw-validate-ascii.py`.

**Workflow:**

1. Parse the brief. Determine:
   - Frame dimensions (target columns — common choices: 60 / 66 / 72 / 78).
   - Required elements (header, body regions, specific content blocks).
   - Banned chars to avoid (see below).
2. Substitute banned characters BEFORE authoring:
   - `▼ ▲ ▶ ◀` → `v ^ > <` (filled triangles render at variable width)
   - `⟶ ⇒` → `->` / `=>` / `→`
   - Emoji state markers → ASCII (`[!]`, `(*)`, `[x]`, `[ ]`, `*`)
   - CJK chars — avoid unless the user explicitly asks; they are 2-col in monospaced fonts
3. Author the ASCII. Use `+---+` ASCII or `┌─┐│└┘├┤┬┴┼` Unicode box-drawing. Mixing the two in the same artifact usually breaks alignment — pick one.
4. Write to `/tmp/ascii-creator-<slug>.txt`.
5. Validate:
   ```bash
   perl ../../bin/amw-validate-ascii.py /tmp/ascii-creator-<slug>.txt
   ```
6. If FAIL — read the `FIX:` hints. They are exact ("Move '│' on line 5 right by 1 position(s) to column 64"). Apply every hint, re-validate. Loop until PASS.
7. Save final: `cp /tmp/ascii-creator-<slug>.txt <working-dir>/<Descriptive Name>.txt`

Typical iteration counts:
- Simple wireframe (1-2 boxes, 1 screen): **1** iteration
- Dashboard with 3-5 framed regions: **2-3** iterations
- Dense editorial layout with nested cells: **3-5** iterations

Never present or save a FAILing artifact. The whole value of "perfect ASCII" is that it passes the validator.

### Technique catalog

The full technique catalog (95 validated patterns + the 12 JSON-render techniques migrated from `perfect-ascii`) is shared across skills under `../amw-diagram-formats/references/ascii.md`. For the JSON-rendering side specifically, this skill's own `references/` directory holds one `.md` per technique extracted from the `perfect-ascii` source:

| TECH-ID | Category | One-line description |
|---|---|---|
| [TECH-json-render-four-modes](./references/TECH-json-render-four-modes.md) | ascii-render | JSON → ASCII, four exclusive modes (diagram/table/layers/sequence) |
| [TECH-render-mode-diagram](./references/TECH-render-mode-diagram.md) | ascii-render | Grid-based flowchart / block-diagram renderer |
| [TECH-render-mode-table](./references/TECH-render-mode-table.md) | ascii-render | Data grids with cell-span and wrap |
| [TECH-render-mode-layers](./references/TECH-render-mode-layers.md) | ascii-render | Layered architecture with auto bus connectors |
| [TECH-render-mode-sequence](./references/TECH-render-mode-sequence.md) | ascii-render | Lifelines + messages + notes |
| [TECH-lane-labeled-diagrams](./references/TECH-lane-labeled-diagrams.md) | ascii-render | Swimlanes via `lanes[]` in diagram mode |
| [TECH-multi-line-box-body](./references/TECH-multi-line-box-body.md) | ascii-render | Rich multi-row boxes via `body[]` |
| [TECH-cell-spanning](./references/TECH-cell-spanning.md) | ascii-render | `{text, span: N}` for multi-column cells |
| [TECH-bus-connectors](./references/TECH-bus-connectors.md) | ascii-render | Auto fan-out / fan-in between tiers |
| [TECH-sequence-notes](./references/TECH-sequence-notes.md) | ascii-render | Inline boxed annotations between lifelines |
| [TECH-78-column-cap](./references/TECH-78-column-cap.md) | ascii-render | Hard 78-col rule and its consequences |
| [TECH-eval-rubric-six-axes](./references/TECH-eval-rubric-six-axes.md) | ascii-render | Score an ASCII diagram on six 1-5 axes |

Before authoring Mode B (freeform wireframe), still consult the 95-technique catalog at `../amw-diagram-formats/references/ascii.md` for patterns like `[!]` markers, `├──┤` band rules, three-column `├┬┬┤` editorial layouts. Pick at least 10 distinct TECH-IDs per variant so each diagram demonstrates deliberate construction rather than a single-source port.

Representative IDs the rebuilt demo variants apply:
- Baseline dashboard — TECH-02 (3-line buttons), TECH-03 (multi-line titled cards), TECH-23 (pipe-column table), TECH-38 (`[!]` markers), TECH-90 (`├──┤` band rules)
- Advanced dashboard — TECH-22 (timeline axis), TECH-46 (axis labels), TECH-82 (editorial brand), TECH-84 (hero narrative)
- Experimental dashboard — TECH-11 (UPPERCASE section labels), TECH-83 (three-column `├┬┬┤` editorial), TECH-84 (LEAD story), TECH-85 (in-cell metric arithmetic)

### Mode B gold-standard inspiration

<!-- Source: box-diagram-master/examples/*.txt (copied to skills/amw-box-diagram/examples/) -->

For non-trivial Mode B wireframes (multi-stage flows, fan-out/fan-in,
rich multi-line boxes), read the three canonical examples before
authoring:

- `../amw-box-diagram/examples/incident-response.txt` — 5-stage flow
  (ALERT / TRIAGE / MITIGATE·INVESTIGATE·COMMUNICATE / VERIFY /
  POST-MORTEM), each box 5-7 body lines, mid-flow 3-way fan-out then
  fan-in. Gold standard for "complex process" Mode-B diagrams.
- `../amw-box-diagram/examples/ci-cd-pipeline.txt` — 3-stage pipeline with
  fan-out to 3 parallel tests, fan-in to Release, 2-way fan-out to
  Staging + Production. Gold standard for "branching deploy" diagrams.
- `../amw-box-diagram/examples/microservices.txt` — Browser/Mobile → LB →
  API Gateway → 3 services (Auth / User / Order) → data stores
  (Redis / Postgres / MongoDB) + Queue → Worker → S3. Gold standard for
  "system architecture" diagrams.

Copy one, then edit the box labels and connector topology to match the
user's brief. The frame-width and vertical-alignment invariants are
already correct in the source, so the validator passes on first try for
minor label swaps — most iteration cost is on structural changes, not
cosmetic ones.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `ascii-creator` is the user asking about?
  - **render** (4 techniques)
    - [TECH-render-mode-diagram](./references/TECH-render-mode-diagram.md) — grid-based flowchart/block-diagram renderer
    - [TECH-render-mode-layers](./references/TECH-render-mode-layers.md) — layered architecture with bus connectors
    - [TECH-render-mode-sequence](./references/TECH-render-mode-sequence.md) — lifelines + messages + notes
    - [TECH-render-mode-table](./references/TECH-render-mode-table.md) — data grids with cell-span and wrap
  - **78** (1 techniques)
    - [TECH-78-column-cap](./references/TECH-78-column-cap.md) — hard 78-col rule and its consequences
  - **bus** (1 techniques)
    - [TECH-bus-connectors](./references/TECH-bus-connectors.md) — auto fan-out / fan-in between tiers
  - **cell** (1 techniques)
    - [TECH-cell-spanning](./references/TECH-cell-spanning.md) — `{text, span: N}` for multi-column cells
  - **eval** (1 techniques)
    - [TECH-eval-rubric-six-axes](./references/TECH-eval-rubric-six-axes.md) — score an ASCII diagram on six 1-5 axes
  - **json** (1 techniques)
    - [TECH-json-render-four-modes](./references/TECH-json-render-four-modes.md) — JSON → ASCII, four exclusive modes
  - **lane** (1 techniques)
    - [TECH-lane-labeled-diagrams](./references/TECH-lane-labeled-diagrams.md) — swimlanes via `lanes[]` in diagram mode
  - **multi** (1 techniques)
    - [TECH-multi-line-box-body](./references/TECH-multi-line-box-body.md) — rich multi-row boxes via `body[]`
  - **sequence** (1 techniques)
    - [TECH-sequence-notes](./references/TECH-sequence-notes.md) — inline boxed annotations between lifelines

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-78-column-cap.md](./references/TECH-78-column-cap.md)**
  - Description: hard 78-col rule and its consequences
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-bus-connectors.md](./references/TECH-bus-connectors.md)**
  - Description: auto fan-out / fan-in between tiers
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-cell-spanning.md](./references/TECH-cell-spanning.md)**
  - Description: `{text, span: N}` for multi-column cells
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-eval-rubric-six-axes.md](./references/TECH-eval-rubric-six-axes.md)**
  - Description: score an ASCII diagram on six 1-5 axes
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-json-render-four-modes.md](./references/TECH-json-render-four-modes.md)**
  - Description: JSON → ASCII, four exclusive modes
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-lane-labeled-diagrams.md](./references/TECH-lane-labeled-diagrams.md)**
  - Description: swimlanes via `lanes[]` in diagram mode
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-multi-line-box-body.md](./references/TECH-multi-line-box-body.md)**
  - Description: rich multi-row boxes via `body[]`
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-render-mode-diagram.md](./references/TECH-render-mode-diagram.md)**
  - Description: grid-based flowchart/block-diagram renderer
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-render-mode-layers.md](./references/TECH-render-mode-layers.md)**
  - Description: layered architecture with bus connectors
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-render-mode-sequence.md](./references/TECH-render-mode-sequence.md)**
  - Description: lifelines + messages + notes
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-render-mode-table.md](./references/TECH-render-mode-table.md)**
  - Description: data grids with cell-span and wrap
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-sequence-notes.md](./references/TECH-sequence-notes.md)**
  - Description: inline boxed annotations between lifelines
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-ascii-creator/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per `../amw-design-principles/ai-slop-avoid.md` (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. ASCII `.txt` files (flowcharts, tables, sequence diagrams, framed wireframes)). The output path is determined by **project inference**, NOT hardcoded. See [`../amw-design-principles/references/project-output-routing.md`](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/wireframes/` or `./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-ascii-creator-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- <artifact-path> — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.

## Style presets (orthogonal to mode selection)

<!-- Source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-skill-main/ASCII-STYLES.md lines 5-155 -->

The mode (`diagram` / `table` / `layers` / `sequence` / freeform) picks
**structure**. A style preset picks **aesthetic** — how much labeling,
how many Unicode glyphs, inline vs. boxed. These are an opt-in dial; the
default is `unicode` for Mode A and hand-author-as-you-go for Mode B.
You can name the style explicitly in the brief ("use the clasico style")
or the skill will infer it from context (target is a plain-text README
→ clasico; terminal screenshot for a docs site → detallado).

| Preset | Glyph set | Labels on edges | Width | Use when |
|---|---|---|---|---|
| `detallado` (detailed) | Unicode box-drawing + `▶ ▼ ╭╮╰╯` | Yes (numbered `1. Request`) | Widest | Docs/review artifacts, high clarity, labelled steps |
| `unicode` | Unicode box-drawing | No | Medium | Large diagrams where label clutter dominates |
| `clasico` (classic) | Pure ASCII (`+` `-` `|` `>` `<` `v` `^`) | Optional | Medium | READMEs, maximum compatibility, copy-paste-safe |
| `compacto` (compact) | One-line inline: `A → B → C` with `─┬─` / `└─` fan-outs | No | Narrowest | Linear flows, single-line summaries, captions |

### Preset examples

**`detallado`** — all boxes + labels + semantic shapes (`╭─╮` for DBs):

```
┌────────┐  1. Request   ┌──────────┐  2. Process   ┌─────────┐
│ Client │──────────────▶│ Gateway  │──────────────▶│ Service │
└────────┘               └──────────┘               └─────────┘
                               │
                               │ 3. Query
                               ▼
                         ╭──────────╮
                         │    DB    │
                         ╰──────────╯
```

**`unicode`** — boxes without edge labels:

```
┌────────┐     ┌──────────┐     ┌─────────┐
│ Client │────▶│ Gateway  │────▶│ Service │
└────────┘     └──────────┘     └─────────┘
```

**`clasico`** — pure ASCII:

```
+--------+     +----------+     +---------+
| Client |---->| Gateway  |---->| Service |
+--------+     +----------+     +---------+
```

**`compacto`** — inline:

```
Client → Gateway → Service → DB
```

**`compacto` with fan-out:**

```
Client → Gateway ─┬─→ Service A → DB-A
                  └─→ Service B → DB-B
```

The preset is orthogonal to the Mode A sub-mode:
`--style clasico` + `sub-mode: layers` produces ASCII-only layered
architecture; `--style detallado` + `sub-mode: sequence` produces a
sequence diagram with labelled messages and Unicode lifelines. Mode B
freeform wireframes usually imply `unicode` (box-drawing of a UI frame);
a user explicitly asking for a "retro terminal" look wants `clasico`.

## Banned characters (severity-rated — enforced by validate-ascii.py)

<!-- Source: bin/amw-validate-ascii.py lines 72-98 (%forbidden_chars table) -->

The validator flags these as forbidden because they render at variable
width in most monospaced fonts. They are tiered by severity so the FIX
iteration loop fixes **CRITICAL first** (definitely breaks alignment for
everyone), then **HIGH** (breaks on common fonts), then **MEDIUM** (may
break on some fonts). The validator reports the tier in the error code
(e.g. `FORBIDDEN_CHAR_CRITICAL`, `FORBIDDEN_CHAR_HIGH`,
`FORBIDDEN_CHAR_MEDIUM`) — address them in that order.

### CRITICAL — will definitely break alignment

| Banned | Approx. width | Use instead |
|---|---|---|
| `⟶` | 3-4x | `──→` or `-->` |
| `⟵` | 3-4x | `←──` or `<--` |
| `⟹` | 3-4x | `══→` or `==>` |
| `⟸` | 3-4x | `←══` or `<==` |
| `⟷` | 4-5x | `←─→` or `<->` |
| `⟺` | 4-5x | `←═→` or `<=>` |

### HIGH — likely to break alignment on common fonts

| Banned | Approx. width | Use instead |
|---|---|---|
| `⇒` | 1.5-2x | `=>` or `→` |
| `⇐` | 1.5-2x | `<=` or `←` |
| `⇔` | 2x | `<=>` or `↔` |
| `⇑` | 1.5x | `^` or `↑` |
| `⇓` | 1.5x | `v` or `↓` |
| `⇕` | 1.5x | `↕` or `^v` |

### MEDIUM — may break alignment on some fonts

| Banned | Approx. width | Use instead |
|---|---|---|
| `▶` | 1.2-1.5x | `>` or `→` |
| `◀` | 1.2-1.5x | `<` or `←` |
| `▲` | variable | `^` or `↑` |
| `▼` | variable | `v` or `↓` |
| `⇆` | 2x | `<>` or `←→` |
| `⇄` | 2x | `><` or `→←` |

### Always-banned regardless of tier

| Banned | Why | Use instead |
|---|---|---|
| `🔴 🟡 🟢 ⚠` and most emoji | 2-col in terminals | `[!]` `(*)` `[x]` `[ ]` `*` |
| CJK characters | 2-col in monospaced terminals | Romanized text, or account for +1 col per char on that row |

If the user insists on including an emoji or CJK char, account for its 2-col width explicitly in the frame (the frame right-edge shifts right by 1 for each 2-col char on that row).

## Prerequisites

- **runtime_binaries (system):** `python3 >= 3.8`, `perl >= 5.10` — both pre-installed on macOS and most Linux distros. `/amw-doctor` checks.
- **python_packages / npm / mcp:** none — both tools are pure-stdlib in their respective languages.
- **Shared scripts:** `../../bin/amw-ascii-render.py` (pure-Python renderer, 4 modes, 78-col max), `../../bin/amw-validate-ascii.py` (alignment + width + wide-char + forbidden-char validator).

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Resources

- `../amw-ascii-sketch/SKILL.md` — upstream when the user wants to ITERATE. Sketch produces 3 variants for plan-phase iteration; once a direction is chosen, the result can either (a) pass through this skill to finalize the ASCII artifact file, or (b) pass directly to `ascii-to-html` for conversion.
- `../amw-ascii-validator/SKILL.md` — documents the underlying validator tool-chain (`bin/amw-ascii-render.py`, `bin/amw-validate-ascii.py`) and the validation contract.
- `../amw-ascii-to-html/SKILL.md` — downstream when the freeform wireframe should become HTML. Consumes Mode B output directly.
- `../amw-ascii-to-svg/SKILL.md` — downstream when the structured diagram should become SVG. Consumes Mode A output.
- `../amw-design-principles/SKILL.md` — orchestrator that routes here when the brief implies a single ASCII artifact rather than a variant set.
- `../amw-box-diagram/examples/` — **gold-standard Mode B reference diagrams** (`incident-response.txt`, `ci-cd-pipeline.txt`, `microservices.txt`). Read before authoring non-trivial wireframes.
- `../../bin/amw-ascii-render.py` — renderer (JSON → ASCII)
- `../../bin/amw-validate-ascii.py` — validator (ASCII → PASS/FAIL + FIX hints)

## Non-negotiables

- One invocation emits **exactly one** `.txt` file. For multi-variant exploration, use `../amw-ascii-sketch/`.
- Mode B output must PASS `bin/amw-validate-ascii.py` before being saved to the working directory.
- Mode A output must successfully execute `bin/amw-ascii-render.py` (non-zero exit = not delivered).
- Banned characters are substituted BEFORE authoring, not during FIX iteration — don't rely on the validator to catch them.
- Descriptive English filename (`Login Flow.txt`, `Dashboard Overview.txt`), never `diagram.txt` / `output.txt`.
- If a FIX iteration hits 8+ retries, STOP — the brief may be structurally impossible at the chosen frame width; propose widening the frame or switching modes.

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| `ascii-render.py` exits with "width exceeds 78" | Label too long or too many columns in a horizontal layer | Shorten labels, split the diagram into two, or switch Mode A sub-mode (e.g. `layers` for wide architecture) |
| Validator reports "WIDTH_MISMATCH" on every line | Author is not padding trailing whitespace — every line in a frame must have the SAME column width | Pad each line with trailing spaces to the max line's width |
| Validator reports "VERTICAL_MISALIGNED" | Nested box corners drift by a column between rows | Lock each `│` / `|` to an explicit column number, re-check each row |
| Validator reports "WIDE_CHAR" on what you thought was 1-col | Emoji / CJK / filled triangle | Substitute per the banned-character table |
| Validator reports "FORBIDDEN_CHAR_MEDIUM" | Variable-width triangle or long arrow | Substitute per the banned-character table |
| Mode-classification wrong — LLM picks wrong sub-mode | Brief has both structural AND freeform aspects | Split into two invocations: first the structural sub-diagram, then embed its output inside the freeform frame |
| User wants THREE variants | Wrong skill — route to `../amw-ascii-sketch/` |
| User wants the diagram as HTML | Wrong skill — produce the ASCII here, then route to `../amw-ascii-to-html/` |

## Modify flow (shared)

When the user points at an existing `.txt` / `.ascii` / `.md` file and asks to edit it (rather than author from scratch), this skill runs the **shared modify pipeline** instead of Mode A or Mode B. The pipeline is: **detect format → parse to IR (`bin/amw-diagram-ir.py parse`) → diff-aware IR patch → re-render (`bin/amw-diagram-ir.py emit --format ascii`) → re-validate (`bin/amw-validate-ascii.py`)**. The full, authoritative 6-step spec — including retry budget, atomic-move semantics, and per-format emitter fast paths — lives at `../amw-diagram-formats/references/modify-flow.md`. Do NOT re-implement the pipeline locally; reference that file.

User intents that trigger the modify path (vs. create):

- "edit this ASCII diagram" / "modify this `.txt` file" / "update the ASCII at `<path>`"
- "change the label of box X" / "rename the `Login` node to `Auth`" / "replace `DB` with `Primary DB`"
- "add a connector from A to B" / "remove the edge between Gateway and Worker" / "insert a box between X and Y"

All three intents resolve to the same pipeline; the only thing that varies is step 3 (patch). MVP patching is text substitution on the parsed IR's `nodes[*].label` and `edges[*]` fields (see `../amw-diagram-formats/references/modify-flow.md` §5.1 for ASCII-specific guidance). Every modified artifact re-passes `bin/amw-validate-ascii.py` before save — a modify that would FAIL validation is rejected and the original file is left untouched.
