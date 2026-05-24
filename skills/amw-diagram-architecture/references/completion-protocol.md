# Completion protocol — amw-diagram-architecture

## Table of Contents

- [Completion checklist](#completion-checklist)
- [Output protocol](#output-protocol)
- [Error Handling](#error-handling)

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

## Completion checklist

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-diagram-architecture/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section of SKILL.md).
- No AI-slop per [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output protocol

This skill produces TWO kinds of output:

### 1. Artifact(s)

The actual work product (e.g. graph JSON / layered SVG / PNG export). The output path is determined by **project inference**, NOT hardcoded. See [project-output-routing](../../amw-design-principles/references/project-output-routing.md) for the full detection rules.

Summary of the priority order:

- User-supplied path (honor verbatim)
- Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
- Existing `./design/<subtype>/` folder if present
- Generic fallback (`./design/diagrams/` created fresh)
- Last-resort scratch: `/tmp/amw-diagram-architecture-<slug>/`

Every artifact file is listed with its path in the report (next item).

### 2. Job-completion report

A markdown file at: `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

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

## Error Handling

- **Overloaded layer (> 5 nodes after generation)** — Stage 1.3 fix: move the least-essential node to an adjacent layer; if every adjacent layer is also full, re-run generation with an explicit merge instruction.
- **Too-few or too-many layers/nodes** — re-run generation. The skill does not silently stretch (too few) or truncate (too many) — it regenerates. Patching these conditions produces visually incoherent diagrams.
- **SVG text overflow** — a label longer than `NODE_W = 160px` at 13pt wraps visually ugly. Stage 1.4 fix: truncate to 3 title-case words. If that still overflows, re-run generation and ask the model for a shorter label.
- **Model timeout / parse failure** — the LLM returned prose instead of JSON, or the JSON is malformed. Apply the `repairAndParse` recipe from [prompts](./prompts.md) in order (strip fences → extract outermost braces → strip trailing commas → normalise newlines in string values). If both attempts fail, re-run generation once; on a second failure, surface the raw parse error to the caller rather than fabricate a graph.
- **Auth missing** (embedded / standalone callers only) — `ANTHROPIC_API_KEY` is not set; surface the error immediately, do not retry. Inside Claude.ai / Claude Code, the platform handles auth — this failure mode does not apply.
- **Empty / too-abstract description** — the caller gave one sentence or a single noun. The prompt explicitly says "infer a clean canonical architecture — do not ask"; the model produces a best-effort default. If the result feels wrong, the caller should re-invoke with more specifics rather than iterate inside this skill.
