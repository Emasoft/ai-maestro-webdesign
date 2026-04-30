---
name: amw-box-diagram
description: Author clean Unicode rounded-corner box diagrams (╭╮╰╯│─) for pipeline diagrams, workflow charts, microservices topologies, and incident-response flows. Triggers on narrow technical intents only — "box diagram of", "Unicode pipeline diagram", "fan-out diagram", "fan-in diagram", "pipeline box diagram", "rounded-corner box diagram", "microservices box topology", "incident-response flow diagram", "workflow box chart". Does NOT trigger on broad design vocabulary ("design", "UI", "landing page", "mockup", "wireframe") — those belong to the `design-principles` orchestrator, which routes here when the user needs a rectangular-box flow with clean rounded corners. All output MUST pass `../../bin/amw-validate-ascii.py` before emission.
version: 0.1.0
---

# Box Diagram

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> Executor. Narrow technical triggers only — the orchestrator routes here for clean rectangular Unicode box diagrams (pipelines, fan-out/fan-in, layered service topologies).

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during Phase A (as a low-fi ASCII medium for pipeline/topology sketches) or Phase B (when the approved design requires a validated box diagram artifact). The orchestrator may apply any box-drawing and layout technique from this skill without command-layer restriction.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**OUTPUT.** Emits a monospaced Unicode box diagram composed of rounded corners (`╭ ╮ ╰ ╯`), straight rules (`─ │`), T-junctions (`┌ ┐ └ ┘ ┬ ┴ ├ ┤ ┼`), and triangle arrowheads (`▸ ▾ ▴ ◂`). Intended audiences: terminal output, markdown code fences in READMEs, ADRs, runbooks, chat transcripts. Not a wireframe skill — structured box-and-arrow flow only.

## Trigger conditions

- "draw a box diagram of <system>"
- "Unicode pipeline diagram"
- "fan-out diagram", "fan-in diagram"
- "show this as a rounded-corner box diagram"
- "microservices box topology", "service dependency boxes"
- "incident-response flow diagram"
- "build pipeline with boxes", "workflow box chart"
- "rewrite this ASCII `+--+` diagram with Unicode corners"

Do **not** activate on generic "design", "UI", "wireframe", "mockup", "landing page" — those route to `../amw-design-principles/` and `../amw-ascii-sketch/`. For freehand ASCII wireframe layouts use `../amw-ascii-sketch/`. For ASCII→SVG export use `../amw-ascii-to-svg/`. For structured JSON→ASCII rendering (sequence diagrams, tables, layered architectures) use `../amw-ascii-validator/` in render mode.

## Why rounded Unicode over ASCII `+--+`

Classic `+--+` diagrams render everywhere but look dated and noisy at the junctions. Rounded-corner Unicode:

- **Reads cleaner in modern terminals, editors, and chat.** The corner glyphs (`╭ ╮ ╰ ╯`) are single-width in every mainstream monospaced font and do not collide with surrounding text the way `+` does.
- **Distinguishes rounded outer frames from sharp inner junctions.** Outer boxes use `╭ ╮ ╰ ╯`; internal T-junctions use `┌ ┐ └ ┘ ┬ ┴ ├ ┤ ┼`. That visual hierarchy is load-bearing — it lets the reader follow branching flow without counting arrows.
- **Pairs with the plugin's ASCII-first plan phase.** `../amw-ascii-sketch/` produces wireframe layouts; this skill produces the flow diagrams that go alongside them in docs. Same output medium, same validation gate.

If the target context cannot render UTF-8 (old terminals, ancient CI log viewers, some Git blame tools), fall back to `+--+` via `../amw-ascii-diagrams-reference/` — that skill is the classic-ASCII counterpart.

## Non-negotiables

Every diagram this skill emits **MUST** pass `../../bin/amw-validate-ascii.py` before presentation to the user. See `../amw-ascii-validator/SKILL.md` for the validator contract — same gate `../amw-ascii-sketch/` uses.

```bash
python3 bin/amw-validate-ascii.py /tmp/box-diagram-<slug>.txt
```

The validator catches:

- Double-width characters (emoji, CJK) that break alignment
- Inconsistent box-frame widths within a row of parallel boxes
- Vertical connector (`│`, `╭`, `╰`) misalignment between rows
- Broken box borders (corners not matching their horizontal/vertical rules)
- Tab characters masquerading as spaces

If the validator fails, apply the emitted `FIX:` hints and re-validate. Do NOT show the user output that failed validation — LLMs cannot count characters, the validator is how this skill compensates.

Additional non-negotiables beyond the validator:

- **Never use emoji inside boxes** — all emoji are double-width in most monospaced fonts and break alignment.
- **Prefer Python generation** for diagrams with 3+ parallel boxes. Define helper functions for `box_line(text, w)`, `border_top(w)`, `border_bot(w)` — hand-counting spaces is error-prone.
- **Fixed-width boxes per row.** Every box in the same horizontal band must share the same outer width so vertical connectors line up.
- **Never re-type the diagram manually after validation.** Read the validated file and paste its exact bytes into the code fence. Even one lost space shifts every corner below it.
- **Max box width ≈ 60 chars.** Wider than that, split into two stacked boxes or use multi-line rich content (see Example C).

## Character set

| Element | Character | Code point |
|---------|-----------|------------|
| Outer rounded corners | `╭ ╮ ╰ ╯` | U+256D..U+256F |
| Inner sharp corners | `┌ ┐ └ ┘` | U+250C..U+2518 |
| Horizontal rule | `─` | U+2500 |
| Vertical rule | `│` | U+2502 |
| T-junctions | `┬ ┴ ├ ┤ ┼` | U+252C..U+253C |
| Arrow right | `▸` | U+25B8 |
| Arrow left | `◂` | U+25C2 |
| Arrow down | `▾` | U+25BE |
| Arrow up | `▴` | U+25B4 |
| Content inline arrow | `→ ← ↑ ↓` | U+2190..U+2193 |

`▼ ▲ ▶ ◀` (U+25BC, U+25B2, U+25B6, U+25C0) are BANNED — they render at variable width in many fonts. The validator rejects them.

## Extended connection-type vocabulary

The base unidirectional arrows above (`▸ ▾ ▴ ◂`) are sufficient for simple flows. For richer relationships (sequence-style returns, class/interface associations, async hand-offs) draw on this extended set — all survive `validate-ascii.py` because none introduce variable-width glyphs:

| Connection type | Unicode form | Classic-ASCII form | When to use |
|---|---|---|---|
| `sync` (default) | `───▸`   | `----->` | Request → response pairs, direct method calls, pipeline stages |
| `return` | `◂───` | `<-----` | Sequence-style return arrow after a synchronous call |
| `bidirectional` | `◂──▸` | `<---->` | Handshake, symmetric coupling, peer-to-peer |
| `async event` | `- - ▸` | `- - ->` | Message-queue publish, event emission, fire-and-forget (dashed emphasises async) |
| `dependency` (hollow) | `───▷` | `----D` | Class / interface depends on (hollow head = "knows about" not "owns") |
| `association` | `────` | `------` | Plain link with no directional semantics (composition, containment, loose coupling) |

The connector body is always the same horizontal (`─` or `-`); only the head changes. Keep one connector style per diagram unless the whole point of the diagram is to contrast sync vs async — mixed arrowheads without a clear legend become noise.

## Semantic node shapes (optional authoring conventions)

The default box in this skill is a rounded Unicode rectangle. For diagrams that need to distinguish **what kind of thing** each node is (database vs queue vs external dependency vs decision point), the following glyph conventions help the reader scan the diagram faster. These are **authoring conventions, not validator rules** — `validate-ascii.py` does not require them, but readers familiar with the style will decode the diagram faster.

- **Database** — rounded-corner "cylinder" using the same outer rounded corners as a normal box. The top/bottom separator rules are the same `─`. Width rules identical.

  ```
  ╭──────╮
  │ DB   │
  ╰──────╯
  ```

- **Queue / topic / stream** — tilde ribbon. `≋` is U+224B (TRIPLE TILDE) and is single-width in monospaced fonts, so it survives the validator. Use it on the top and bottom rule lines only; the sides stay vertical `│`.

  ```
  ≋≋≋≋≋≋≋≋
  │ Queue │
  ≋≋≋≋≋≋≋≋
  ```

- **External service** — dashed border using `╌` (U+254C, LIGHT DOUBLE DASH HORIZONTAL) on the rules and `╎` (U+254E, LIGHT DOUBLE DASH VERTICAL) on the sides. Signals "outside our system / we don't own this".

  ```
  ┌╌╌╌╌╌╌╌╌┐
  ╎ Stripe ╎
  └╌╌╌╌╌╌╌╌┘
  ```

- **Decision point** — diamonds are notoriously hard to render cleanly in ASCII (non-rectangular shapes break alignment). **Prefer a labelled rounded box with a question mark** (e.g. `│ Valid? │`) and branch with labelled connectors (`──yes──▸`, `──no──▸`). If a diamond is absolutely required for editorial reasons, use the `../amw-diagram-svg/` skill instead — the ASCII medium is the wrong tool.

When mixing shapes in one diagram, keep them in the same column grid so the connectors still line up. All of the examples below (A, B, C) use only the default rounded rectangle because most flow diagrams do not need more.

## Construction method

1. **Define the grid.** Assign exact column positions for each box (e.g. `col_A = 0`, `col_B = 25`, `col_C = 50`). Columns are sticky — every box in the same column has the same left-edge offset.
2. **Choose fixed box widths per row.** Within one horizontal band, all boxes share one width. Different rows can differ.
3. **Draw row by row.** Pad each content line to the border width: `│` + space + text + `' ' * (inner_width - len(text))` + space + `│`.
4. **Connectors.** Vertical `│` must sit under the center of the box above; horizontal `─` counts = gap between box edges; fan-out uses `┌ ─ ┬ ─ ┐` across the top of the child row; fan-in uses `└ ─ ┴ ─ ┘` across the bottom.
5. **Assert text fits BEFORE generating.** `assert len(text) <= inner_width` — one char overflow breaks everything.
6. **Validate.** Run `python3 bin/amw-validate-ascii.py` on the file. Fix any `FIX:` hint, re-validate.
7. **Output from the file, never from memory.** Read the validated file, paste verbatim into the reply.

### Python helper pattern

For any diagram with 3+ boxes, build the primitives in Python:

```python
H  = '─'   # ─
V  = '│'   # │
TL = '╭'   # ╭
TR = '╮'   # ╮
BL = '╰'   # ╰
BR = '╯'   # ╯

def border_top(inner_width): return TL + H * (inner_width + 2) + TR
def border_bot(inner_width): return BL + H * (inner_width + 2) + BR
def box_line(text, inner_width):
    assert len(text) <= inner_width, f"text too wide: {text!r}"
    return V + ' ' + text + ' ' * (inner_width - len(text)) + ' ' + V
```

Hand-authored diagrams (2 boxes, trivial layout) can skip Python — but still validate.

## Example A — Simple pipeline (3 sequential boxes)

CI/CD pipeline flow. Single horizontal line, `▸` arrowhead between boxes. All boxes same width so the horizontal rule is symmetric.

```
╭──────────────╮   ╭──────────────╮   ╭──────────────╮
│ git push     │──▸│ Build        │──▸│ Lint         │
╰──────────────╯   ╰──────────────╯   ╰──────────────╯
```

Trigger phrasing: *"show the CI pipeline as boxes"*, *"draw a box diagram of the build flow"*.

## Example B — Fan-out / fan-in (pipeline with parallel stages)

Three parallel test stages between Lint and Release. `├` on the right edge of Lint means "three branches leave from here"; matching `└ ┼ ┘` at the bottom rejoin into Release.

```
╭──────────────╮   ╭──────────────╮   ╭──────────────╮
│ git push     │──▸│ Build        │──▸│ Lint         │
╰──────────────╯   ╰──────────────╯   ╰──────────────╯
                                              │
        ┌──────────────────┬──────────────────┤
        │                  │                  │
        ▾                  ▾                  ▾
╭──────────────╮   ╭──────────────╮   ╭──────────────╮
│ Unit Tests   │   │ API Tests    │   │ E2E Tests    │
╰──────────────╯   ╰──────────────╯   ╰──────────────╯
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▾
                   ╭──────────────╮
                   │ Release      │
                   ╰──────────────╯
                           │
                  ┌────────┴────────┐
                  │                 │
                  ▾                 ▾
          ╭──────────────╮  ╭──────────────╮
          │ Staging      │  │ Production   │
          ╰──────────────╯  ╰──────────────╯
```

Trigger phrasing: *"fan-out to Unit/API/E2E then fan-in to Release"*, *"pipeline with three parallel test suites"*, *"deploy to staging AND production"*.

## Example C — Multi-line rich-content boxes

When each box needs more than a single label — title row + horizontal separator (`─` spanning the full inner width) + 2-5 body lines — use the multi-line form. Width must be consistent across all content lines AND match the frame.

```
            ╭──────────────────────────────────────────╮
            │ 1. ALERT TRIGGERED                       │
            │ ──────────────────────────────────────── │
            │ PagerDuty → #incident-channel            │
            │ Severity: P1 (user-facing)               │
            │ Source: Grafana alert rule               │
            │ Runbook: wiki/runbook/api-5xx            │
            ╰──────────────────────────────────────────╯
                                 │
                                 ▾
              ╭──────────────────────────────────────╮
              │ 2. TRIAGE                            │
              │ ──────────────────────────────────── │
              │ On-call engineer assesses:           │
              │                                      │
              │   1. Check error rate (Grafana)      │
              │   2. Review recent deploys           │
              │   3. Check dependent services        │
              │   4. Assign severity / commander     │
              ╰──────────────────────────────────────╯
```

Rules for multi-line content:

- Title on line 1, then a full-width `─` separator row (with leading/trailing spaces matching a normal content line — `│ ` + `─ * inner_width` + ` │`), then body lines.
- Blank content lines are allowed — they are `│` + `' ' * (inner_width + 2)` + `│`.
- Nested inline arrows (`→ ← ↑ ↓`) are safe inside the content; BANNED: `▼ ▲ ▶ ◀`, emoji, CJK.

Trigger phrasing: *"detailed incident-response flow"*, *"rich-content box diagram with multi-line steps"*, *"runbook as boxes with context"*.

## Canonical example files

The `examples/` subdirectory contains the three gold-standard reference artifacts this skill was adapted from. Each one passes `../../bin/amw-validate-ascii.py` verbatim. Use them as shape templates when building a new diagram — the column grid, fixed box widths, and junction spacing in each are non-trivial to reproduce by eye.

| File | Shape | Use as template for |
|---|---|---|
| [`examples/ci-cd-pipeline.txt`](examples/ci-cd-pipeline.txt) | Linear flow → 3-way fan-out → fan-in → 2-way fan-out | CI/CD pipelines, build stages, deploy gates, workflow charts |
| [`examples/microservices.txt`](examples/microservices.txt) | 2 entry points → load balancer → gateway → 3 parallel services (+ sidecar queue) → 3 datastores | Microservice topology maps, service dependency diagrams, architecture overviews |
| [`examples/incident-response.txt`](examples/incident-response.txt) | Multi-line rich-content boxes in sequence + 3-way parallel branch → rejoin → 2 final rich boxes | Runbooks, incident playbooks, detailed step-by-step procedure flows |

Before authoring a new diagram, open the closest example and match its column offsets, inner box widths, and junction patterns. When in doubt, copy the example and rename the labels — alignment stays correct as long as the new label fits inside the original `inner_width`.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `box-diagram` is the user asking about?
  - **arrow** (1 techniques)
    - [TECH-arrow-head-variants](./references/TECH-arrow-head-variants.md) — `▸ ▾ ▴ ◂` vs banned `▶ ▼ ▲ ◀`
  - **fan** (1 techniques)
    - [TECH-fan-out-fan-in-junctions](./references/TECH-fan-out-fan-in-junctions.md) — `┌┬┐` / `└┴┘` to diverge and rejoin
  - **multi** (1 techniques)
    - [TECH-multi-line-rich-content-box](./references/TECH-multi-line-rich-content-box.md) — title + separator + body lines
  - **output** (1 techniques)
    - [TECH-output-from-validated-file](./references/TECH-output-from-validated-file.md) — read back, never re-type
  - **python** (1 techniques)
    - [TECH-python-helper-pattern](./references/TECH-python-helper-pattern.md) — `border_top` / `border_bot` / `box_line`
  - **semantic** (1 techniques)
    - [TECH-semantic-node-shapes](./references/TECH-semantic-node-shapes.md) — DB / queue / external / decision glyphs
  - **unicode** (1 techniques)
    - [TECH-unicode-rounded-corner-set](./references/TECH-unicode-rounded-corner-set.md) — `╭ ╮ ╰ ╯ │ ─` box character set

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-arrow-head-variants.md](./references/TECH-arrow-head-variants.md)**
  - Description: `▸ ▾ ▴ ◂` vs banned `▶ ▼ ▲ ◀`
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-fan-out-fan-in-junctions.md](./references/TECH-fan-out-fan-in-junctions.md)**
  - Description: `┌┬┐` / `└┴┘` to diverge and rejoin
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-multi-line-rich-content-box.md](./references/TECH-multi-line-rich-content-box.md)**
  - Description: title + separator + body lines
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-output-from-validated-file.md](./references/TECH-output-from-validated-file.md)**
  - Description: read back, never re-type
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-python-helper-pattern.md](./references/TECH-python-helper-pattern.md)**
  - Description: `border_top` / `border_bot` / `box_line`
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-semantic-node-shapes.md](./references/TECH-semantic-node-shapes.md)**
  - Description: DB / queue / external / decision glyphs
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-unicode-rounded-corner-set.md](./references/TECH-unicode-rounded-corner-set.md)**
  - Description: `╭ ╮ ╰ ╯ │ ─` box character set
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
- At least one `TECH-*.md` file from `skills/amw-box-diagram/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per `../amw-design-principles/ai-slop-avoid.md` (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. Unicode rounded-corner box-diagram `.txt` files). The output path is determined by **project inference**, NOT hardcoded. See [`../amw-design-principles/references/project-output-routing.md`](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-box-diagram-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- [path/to/artifact.ext](./path/to/artifact.ext) — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.

## Dependencies

- **runtime_binaries:** `perl >= 5.10` (pre-installed on macOS and most Linux distros — `/amw-doctor` checks) **OR** `python3 >= 3.8` (Windows-friendly fallback — `bin/amw-validate-ascii.py` has identical behavior)
- **python_packages:** none (pure stdlib)
- **cpan / npm:** none

## Cross-references

- `../amw-ascii-validator/SKILL.md` — MANDATORY validation gate; defines the rule set
- `../../bin/amw-validate-ascii.py` — the validator (pure-Python, exits non-zero on failure, emits `FIX:` hints; Windows-compatible, group-aware width detection for multi-structure diagrams)
- `../amw-ascii-sketch/SKILL.md` — upstream peer for wireframe layouts; this skill handles the flow-diagram side of the same output medium
- `../amw-ascii-to-svg/SKILL.md` — downstream: convert an approved box diagram to SVG for editorial/print use
- `../amw-ascii-diagrams-reference/SKILL.md` — classic-ASCII (`+--+`) counterpart for legacy contexts that cannot render UTF-8
- `../amw-diagram-svg/SKILL.md` — when the caller wants an SVG output directly (skip the ASCII round trip)
- `../amw-design-principles/ai-slop-avoid.md` — misaligned boxes are a form of AI-slop

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Validator reports WIDE_CHAR on a working glyph | An emoji, `▼`, `▲`, `▶`, or `◀` slipped into the content | Replace with `v`, `^`, `>`, `<` or the correct triangle (`▾ ▴ ▸ ◂`) |
| Validator reports WIDTH_MISMATCH on a multi-line box | Content line is shorter/longer than the frame's inner width | Re-pad every content line with trailing spaces to match |
| Vertical `│` walks one column to the right between rows | Adjacent boxes in the upper row differ in width | Re-equalize the upper-row boxes (same `inner_width`) |
| Fan-out `┌ ┬ ┐` does not line up with the children below | Column offsets differ between parent row and child row | Fix the grid first — every box in a column shares one left-edge offset |
| Output looks right in the reply but breaks in the user's terminal | User's terminal is not UTF-8 or has a proportional font | Fall back to `../amw-ascii-diagrams-reference/` which uses only `+`, `-`, `|` |
