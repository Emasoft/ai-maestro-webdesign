# Pipeline detail — the 5 steps that match shared modify-flow

Authoritative execution sequence for the `amw-mermaid-diagram` skill. Matches the shared 6-step modify-flow at [../amw-diagram-formats/references/modify-flow.md](../../amw-diagram-formats/references/modify-flow.md) (step 4 — `(loop point)` — is collapsed in the per-skill sequence).

## The 5 steps

1. **Detect** source shape. If `$ARGUMENTS` is a path to an existing `.mmd` / `.mermaid` OR content starts with a Mermaid grammar header (`flowchart|graph|sequenceDiagram|stateDiagram|stateDiagram-v2|classDiagram|erDiagram|gantt|pie|journey|mindmap|quadrantChart|gitGraph|C4Context`) → **modify path**. If it's a natural-language brief → **create path**.

2. **Parse** (modify path only) via `bin/amw-parse-mermaid-diagram.py` → IR (schema: [ir-schema](../../amw-diagram-formats/references/ir-schema.md)). Regex-based per-grammar parsing. Create path skips this step.

3. **IR operation:**
   - Create path → select the grammar type from the brief (flowchart is default for "flow" / "process" intent; sequenceDiagram for "request/response" / "handshake"; erDiagram for "schema" / "database relationships"; etc — see [mermaid](../../amw-diagram-formats/references/mermaid.md) §2). Emit grammar directly.
   - Modify path → apply the user's requested edit to the IR (text substitution on `nodes[*].label` / `edges[*].label` for MVP; grammar-aware structural operations once Phase 1 parsers land — see [modify-flow](../../amw-diagram-formats/references/modify-flow.md) §5.4).

4. **Re-render** (to Mermaid source, not SVG/PNG) via `bin/amw-diagram-ir.py emit --format mermaid`. Per-kind grammar emitters map IR back to the appropriate Mermaid syntax.

5. **Re-validate** via `bin/amw-mermaid-lint.sh` (wraps `mmdc -i <file> -o /tmp/_mermaid_lint.svg` dry-run — exit 0 = valid; unified PASS/FAIL contract per [validation-dispatcher](../../amw-diagram-formats/references/validation-dispatcher.md)). A FAIL aborts and leaves the original file untouched. Retry budget = 3.

## Component detection table (most common dispatch cues)

Full 9-grammar + node-shape + edge + theme + flag catalog lives in [mermaid](../../amw-diagram-formats/references/mermaid.md) §2 + §8 (40 techniques). The 8 rows below are the most common dispatch cues — consult the ref for the rest.

| Mermaid construct | IR node/edge kind | Ref |
|---|---|---|
| `A[Text]` | `node{shape:rect, kind:process}` | mermaid TECH-MM-24 |
| `A([Text])` | `node{shape:stadium, kind:start-end}` | mermaid §2.1 |
| `A[(Text)]` | `node{shape:cylinder, kind:database}` | mermaid §2.1 |
| `A{Text}` | `node{shape:diamond, kind:decision}` | mermaid §2.1 |
| `A --> B` | `edge{style:solid, kind:sync}` | mermaid TECH-MM-25 |
| `A -.-> B` | `edge{style:dotted, kind:async}` | mermaid TECH-MM-25 |
| `A -->\|label\| B` | `edge{label:"label"}` | mermaid TECH-MM-26 |
| `subgraph Name ... end` | group container (`layout:nested`) | mermaid TECH-MM-27 |

## Output contract

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. `.mmd` Mermaid source files). The output path is determined by **project inference**, NOT hardcoded. See [project-output-routing](../../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-mermaid-diagram-<slug>/`

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

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-mermaid-diagram/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables.
- No AI-slop per [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).
