---
name: amw-ascii-validator
description: Render pixel-perfect ASCII diagrams from structured JSON and/or validate hand-authored ASCII wireframes for alignment bugs before they ship. Triggers on narrow technical intents only — "validate this ASCII", "check my ASCII alignment", "render this as perfect ASCII", "ASCII diagram from JSON", "fix ASCII box alignment", "why is my ASCII misaligned". Does NOT trigger on generic design intent ("design a page", "wireframe a dashboard") — those belong to ascii-sketch / design-principles. This is the MANDATORY validation gate for any ASCII emitted by ascii-sketch or /amw-sketch. Use when validating or rendering pixel-perfect ASCII diagrams for alignment correctness. Trigger with /amw-sketch (auto-runs on every loop turn) or /amw-validate-any-diagram-format (explicit ASCII-or-other-format validation entry).
version: 0.1.0
---

# ASCII Validator + Renderer

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> **Mandatory validation gate.** Every ASCII variant emitted by `ascii-sketch` / `/amw-sketch` MUST pass the validator before being shown to the user. LLMs cannot count characters — this skill is how the plugin compensates.

## Overview

Mandatory validation gate that every ASCII variant must pass before being shown to the user. Provides two tools: `bin/amw-validate-ascii.py` (alignment checker with FIX hints) and `bin/amw-ascii-render.py` (JSON→ASCII renderer). LLMs cannot count characters; this skill compensates.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked automatically by the orchestrator as a **mandatory gate** inside `ascii-sketch` / Phase A: every ASCII variant must pass this validator before being shown to the user. Also callable directly when the user explicitly asks to validate or render ASCII (`"validate this ASCII"`, `"render from JSON"`).


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

VALIDATION + OUTPUT. Two modes:

1. **Render mode** (`perfect-ascii`): caller describes the diagram in structured JSON → tool emits perfectly-aligned ASCII. Four sub-modes — `diagram`, `table`, `layers`, `sequence`. 78-column max. Use this when the diagram is a STRUCTURED flowchart / table / architecture / sequence.

2. **Validate mode** (`ascii-diagram-validator`): caller authored ASCII by hand (or mixed) → tool reports alignment bugs with actionable `FIX:` hints. Use this for WIREFRAMES (framed rectangular UI mockups — the case ascii-sketch produces).

Both tools ship as scripts in `../../bin/`.

## Trigger conditions

- "validate this ASCII diagram"
- "check my ASCII alignment"
- "render this as perfect ASCII"
- "ASCII diagram from JSON"
- "fix ASCII box alignment"
- "why is my ASCII misaligned"
- "perfect-ascii render"
- Automatic: invoked by `ascii-sketch` before emitting any variant

Do NOT activate on generic design / wireframe / UI intent — those belong to `../amw-ascii-sketch/` (plan-phase) and `../amw-design-principles/` (orchestrator).

## Tools

### `../../bin/amw-ascii-render.py` (perfect-ascii)

Pure-Python stdin→stdout. Reads JSON from stdin, writes ASCII to stdout. Exits non-zero on invalid input or a width-overflow.

```bash
echo '{"diagram": {"boxes": [{"id": "a", "label": "Hello"}, {"id": "b", "label": "World"}], "grid": [["a"], ["b"]], "connectors": [{"from": "a", "to": "b"}]}}' \
  | python3 bin/amw-ascii-render.py
```

Four top-level JSON modes (exactly one required):

| Key | Use for |
|-----|---------|
| `diagram`  | Flowcharts, ER diagrams, state machines, block diagrams |
| `table`    | Data grids, comparison matrices (auto-splits at 78 chars) |
| `layers`   | Layered architecture diagrams with bus connectors |
| `sequence` | Sequence diagrams with lifelines and message arrows |

Constraints: 78-col max, rectangular boxes only, labels under ~15 chars. Full JSON schema reference is embedded in the `render_ascii` docstring at the top of `bin/amw-ascii-render.py`.

## Lane-labeled diagrams (git graphs, CI pipelines)

`diagram` mode accepts an optional top-level `lanes: ["label1", "label2", ...]` array that renders left-margin track labels next to each grid row — the same pattern `layers` mode uses, but driven by arbitrary lane names instead of an automatic `"Presentation / API / Services / Data"` style. Use this for git-branch graphs, CI-pipeline swimlanes, or any diagram where each horizontal row represents a distinct track with a name.

Concrete git-merge example:

```json
{
  "diagram": {
    "lanes": ["main", "feature"],
    "boxes": [
      {"id": "m1", "label": "v1.0"},
      {"id": "m2", "label": "v1.1"},
      {"id": "f1", "label": "auth"},
      {"id": "f2", "label": "tests"}
    ],
    "grid": [
      ["m1", null, "m2"],
      [null, "f1", "f2"]
    ],
    "connectors": [
      {"from": "m1", "to": "m2"},
      {"from": "m1", "to": "f1", "label": "branch"},
      {"from": "f1", "to": "f2"},
      {"from": "f2", "to": "m2", "label": "merge"}
    ]
  }
}
```

Rendered output shows `main` / `feature` labels at the left margin of each row and routes the branch/merge connectors with elbowed L-shapes between lanes. Works the same way for CI pipelines (`["build", "test", "deploy"]`), or for any two-or-three-track flow that would be cramped on a single linear row.

### Sequence-mode inline notes

`sequence` mode supports a `notes` array alongside `messages`. Each note is `{"between": [actor1, actor2], "text": "...", "after_message": N}` where `N` is the 0-based index of the message after which to place the note. The renderer draws a boxed text block spanning the two actors, positioned between the outgoing message and the next interaction. Use notes to annotate timeouts, preconditions, side effects, or anything a plain message arrow cannot convey.

Concrete example — a timeout annotation between a request and its response:

```json
{
  "sequence": {
    "actors": ["User", "Frontend", "API", "DB"],
    "messages": [
      {"from": "User", "to": "Frontend", "label": "Click checkout", "style": "solid"},
      {"from": "Frontend", "to": "API", "label": "POST /checkout", "style": "solid"},
      {"from": "API", "to": "DB", "label": "INSERT order", "style": "solid"},
      {"from": "DB", "to": "API", "label": "OK", "style": "dashed"},
      {"from": "API", "to": "Frontend", "label": "200 OK", "style": "dashed"}
    ],
    "notes": [
      {"between": ["Frontend", "API"], "text": "Timeout after 30s", "after_message": 1}
    ]
  }
}
```

The note appears as a small boxed block between the Frontend and API lifelines right after message 1 (`POST /checkout`), reading `Timeout after 30s`. Keep note text under ~30 chars per line to respect the 78-col overall width cap; the renderer errors out if a note overflows.

### `../../bin/amw-validate-ascii.py` — ASCII diagram validator

Pure-Python 3.8+ stdlib validator. Checks framed ASCII wireframes for:

1. **Consistent line widths** — per structural box group (group-aware — avoids false positives on multi-structure diagrams)
2. **Box corner alignment** — nested boxes must have vertically-aligned corners
3. **Vertical line continuity** — `│` characters must align across rows
4. **Horizontal connections** — corners must connect properly to horizontal lines
5. **Wide-character detection** — flags CJK / emoji (2-col) that break alignment
6. **Forbidden characters** — flags long/double arrows (`⟶ ⇒`) and variable-width triangles (`▼ ▲ ▶ ◀`)

Exits 0 on PASS, 1 on FAIL. Every finding includes `FIX:` instructions.

```bash
python3 bin/amw-validate-ascii.py /tmp/variant-a.txt
```

**Group-detection algorithm:** the validator groups consecutive lines that share box-char column positions into one structural group, computes the expected width per group, and only flags intra-group deviations. The three canonical `box-diagram/examples/*.txt` PASS this validator. This is the canonical behavior target for all ASCII output.

## Mandatory integration with `ascii-sketch`

Every variant `ascii-sketch` produces MUST pass the validator before the orchestrator shows it to the user. The flow is:

```
1. Generate variant → write to /tmp/amw-sketch-<slug>-<variant>.txt
2. python3 bin/amw-validate-ascii.py /tmp/amw-sketch-<slug>-<variant>.txt
   - If PASS → proceed.
   - If FAIL → apply the emitted `FIX:` hints, re-validate. Loop until PASS.
3. Present the validated variant to the user.
```

Never show the user ASCII that failed validation. The validator's alignment-bug-count is NOT acceptable as "close enough" — the whole point of ASCII-first is that the user reads exactly what they'd read in production, and a 1-column-off rectangle erodes trust in every subsequent variant.

## Ban list (enforced by the validator)

The validator flags these characters as "forbidden" because they render at variable width in most monospaced fonts:

- `▼ ▲ ▶ ◀` — variable-width filled triangles → use `v ^ > <` or arrow characters
- `⟶ ⇒` — long/double arrows → use `->` / `=>` / `→`
- CJK characters — 2-col in terminals, usually 1-col in some proportional fonts
- Most emoji — 2-col; for state indicators prefer `[!]`, `[x]`, `[ ]`, `(*)`, `*`

Wireframes that must include emoji (e.g. user-content mockups) should escape the validator by accounting for the double-width in the frame explicitly.

## Instructions

1. Understand the two validator tools: `bin/amw-ascii-render.py` (JSON → ASCII renderer) and `bin/amw-validate-ascii.py` (ASCII → PASS/FAIL validator with FIX hints).
2. For rendering, pass a JSON spec to `amw-ascii-render.py`; it guarantees alignment by construction for structured diagram types.
3. For validation, run `bin/amw-validate-ascii.py <file>` against any hand-authored ASCII; PASS means the artifact is alignment-safe.
4. When the output is FAIL, read each `FIX:` hint (they are exact column-level instructions); apply every hint, then re-validate.
5. Iterate until PASS; never deliver or commit a FAIL artifact.
6. For multi-format workflows, reference the technique selection tree below to pick the relevant TECH reference file.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `ascii-validator` is the user asking about?
  - **box** (1 techniques)
    - [TECH-box-corner-alignment](./references/TECH-box-corner-alignment.md) — nested boxes share corner columns
  - **fix** (1 techniques)
    - [TECH-fix-hint-actionable-format](./references/TECH-fix-hint-actionable-format.md) — every finding carries a mechanical FIX:
  - **forbidden** (1 techniques)
    - [TECH-forbidden-chars-banlist](./references/TECH-forbidden-chars-banlist.md) — ban long/double arrows + filled triangles
  - **group** (1 techniques)
    - [TECH-group-aware-width-detection](./references/TECH-group-aware-width-detection.md) — per-structure width, not global mode
  - **safe** (1 techniques)
    - [TECH-safe-char-palette](./references/TECH-safe-char-palette.md) — the characters that always render 1-col
  - **validate** (1 techniques)
    - [TECH-validate-before-emit](./references/TECH-validate-before-emit.md) — never show un-validated ASCII
  - **vertical** (1 techniques)
    - [TECH-vertical-line-continuity](./references/TECH-vertical-line-continuity.md) — `│` / `|` align across consecutive rows
  - **wide** (1 techniques)
    - [TECH-wide-character-detection](./references/TECH-wide-character-detection.md) — flag CJK/emoji double-width chars
  - **width** (1 techniques)
    - [TECH-width-mismatch-rule](./references/TECH-width-mismatch-rule.md) — every frame line shares one display width

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-box-corner-alignment.md](./references/TECH-box-corner-alignment.md)**
  - Description: nested boxes share corner columns
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-fix-hint-actionable-format.md](./references/TECH-fix-hint-actionable-format.md)**
  - Description: every finding carries a mechanical FIX:
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-forbidden-chars-banlist.md](./references/TECH-forbidden-chars-banlist.md)**
  - Description: ban long/double arrows + filled triangles
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-group-aware-width-detection.md](./references/TECH-group-aware-width-detection.md)**
  - Description: per-structure width, not global mode
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-safe-char-palette.md](./references/TECH-safe-char-palette.md)**
  - Description: the characters that always render 1-col
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-validate-before-emit.md](./references/TECH-validate-before-emit.md)**
  - Description: never show un-validated ASCII
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-vertical-line-continuity.md](./references/TECH-vertical-line-continuity.md)**
  - Description: `│` / `|` align across consecutive rows
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-wide-character-detection.md](./references/TECH-wide-character-detection.md)**
  - Description: flag CJK/emoji double-width chars
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-width-mismatch-rule.md](./references/TECH-width-mismatch-rule.md)**
  - Description: every frame line shares one display width
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
- At least one `TECH-*.md` file from `skills/amw-ascii-validator/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per `../amw-design-principles/ai-slop-avoid.md` (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. validated ASCII `.txt` output + a `validate-ascii.py` PASS log). The output path is determined by **project inference**, NOT hardcoded. See [`../amw-design-principles/references/project-output-routing.md`](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-ascii-validator-<slug>/`

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

## Prerequisites

- **runtime_binaries:** `python3 >= 3.8` (system-required per plugin contract)
- **python_packages:** none (pure stdlib)
- **cpan / npm:** none

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Resources

- `../amw-ascii-sketch/SKILL.md` — upstream consumer: calls this validator before emitting variants
- `../amw-ascii-to-html/SKILL.md` — upstream consumer: validates the approved ASCII one last time before HTML conversion
- `../amw-ascii-to-svg/SKILL.md` — upstream consumer: validates the ASCII input before parse
- `../../bin/amw-ascii-render.py` — perfect-ascii renderer (pure Python, 78-col max, 4 modes)
- `../../bin/amw-validate-ascii.py` — alignment validator (Python; group-aware width detection, FIX hints)
- `../amw-design-principles/ai-slop-avoid.md` — misaligned ASCII is a form of AI-slop visible in tokens

## Non-negotiables

- Every variant `ascii-sketch` emits MUST pass `validate-ascii.py` before presentation
- Forbidden characters (`▼ ▲ ▶ ◀ ⟶ ⇒`) must be substituted BEFORE emission, not after
- CJK / emoji inclusion requires explicit double-width accounting in the frame
- `perfect-ascii` output is trimmed-line (no fixed width per line); the frame validator does NOT apply to its output — route to one or the other depending on shape

## Multi-format mode (shared)

This skill is also the entry point for **ALL diagram formats** when routed through `bin/amw-validate-diagram.sh`. The dispatcher sniffs the format first (`bin/amw-diagram-detect-format.sh`) and routes accordingly:

| Format | Backend |
|---|---|
| ASCII | `bin/amw-validate-ascii.py` |
| SVG | `bin/amw-validate-svg-diagram.sh` (wraps `xmllint --noout` + namespace check) |
| HTML | `bin/amw-validate-html-diagram.sh` (wraps `xmllint --html` + optional `tidy -e -q`) |
| Mermaid | `bin/amw-mermaid-lint.sh` (wraps `mmdc` dry-run, parses stderr for errors) |
| **PNG** | **Hardcoded refusal — exit 2** |

PNG-as-input is unconditionally refused:

```
REFUSE: PNG is output-only by plugin directive; validate the source artifact instead.
        Provide the ASCII / HTML / SVG / Mermaid source that produced this PNG.
```

All per-format validators conform to the same unified output contract — `PASS: <path>` on success or `FAIL: <line>: <message> [FIX: <hint>]` per finding — making `bin/amw-validate-diagram.sh` the single surface callers invoke regardless of format.

Full routing rules and per-format validator specs: `../amw-diagram-formats/references/validation-dispatcher.md`.

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| Validator reports WIDTH_MISMATCH on every line | Author is counting `│` as taking 1 col but the frame includes trailing whitespace | Pad every line to the max line's width with trailing spaces |
| Validator reports WIDE_CHAR on a working emoji | Terminal shows emoji as 2-col, author assumed 1 | Replace emoji with ASCII state marker (`[!]`, `(*)`, etc.) |
| `perfect-ascii` errors "width exceeds 78" | Labels too long for horizontal stacking | Shorten labels, split into multiple sub-diagrams, or switch to `layers` mode |
| `ascii-sketch` variants fail validation every iteration | Variant produced by raw LLM without the validator loop | The skill MUST NOT skip Step 3 of the loop — validation is non-skippable |
| `bin/amw-validate-diagram.sh` returns exit 2 for a non-PNG file | Format sniffer returned `unknown` | Ensure the file has a recognized extension or content signature (see `../amw-diagram-formats/references/detect-format.md`) |
| `bin/amw-validate-diagram.sh` returns exit 3 | `xmllint`, `tidy`, or `mmdc` not installed | Run `/amw-init` or `/amw-doctor` to install missing tools |
