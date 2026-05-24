# Skill completion + output contract (shared)

Every executor skill in this plugin (ASCII, HTML, SVG, Mermaid, infographic, diagram, etc.) shares the same completion-checklist + output-report contract. To keep each SKILL.md focused on its specific techniques, the boilerplate lives here and individual SKILL.md files link to it.

## Completion checklist (apply to every skill run)

Before reporting a job using a skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- **Inputs captured verbatim** — what the user provided (brief, URL, reference files) was captured without silent paraphrasing that changes meaning.
- **At least one `TECH-*.md` consulted** — the skill's own `references/TECH-*.md` library was used and is cited in the final report.
- **Skill non-negotiables PASS** — every item in the skill's own `## Non-negotiables` section.
- **No AI-slop** — output passes the [ai-slop-avoid](../ai-slop-avoid.md) checklist (no generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- **Output rendered/validated by the matching tool** — if the skill emits HTML/SVG/ASCII, the canonical validator ran (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, `bin/amw-validate-diagram.sh`, etc.) and returned PASS.
- **Cross-skill hand-offs documented** — if work routed through another skill, that skill's `SKILL.md` + TECH file are named in the report.
- **Descriptive English filename** — user-facing artifact files use clear names (`Login Flow.html`, `Dashboard Overview.txt`), never `output.html` / `diagram.txt`.

## Output contract (apply to every skill run)

This contract produces TWO kinds of output for every skill run:

### 1. Artifact(s)

The actual work product — the `.txt` / `.html` / `.svg` / `.png` / `.mp4` / `.md` file(s) the skill produces. The output path is determined by **project inference**, NOT hardcoded. See [project-output-routing](./project-output-routing.md) for the full detection rules. Summary of the priority order:

1. User-supplied path (honor verbatim).
2. Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.).
3. Existing `./design/<subtype>/` folder if present.
4. Generic fallback (`./design/<subtype>/` created fresh — e.g. `./design/wireframes/`, `./design/diagrams/`).
5. Last-resort scratch: `/tmp/<skill-name>-<slug>/`.

Every artifact file MUST be listed with its path in the job-completion report.

### 2. Job-completion report

A markdown file at:

```
$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md
```

The report must contain, in order:

- **Inputs** — what the user provided + any auto-detected context.
- **Method** — which TECH references were consulted, which pipeline steps ran.
- **Artifacts** — bullet list, one per produced file, formatted as:
  ```
  - <artifact-path> - <1-line description> - **How to use:** <usage tip> - **Next steps:** <suggested follow-up>
  ```
- **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A.
- **Deviations** — any step skipped or changed, with rationale.

The `<8-char-hash>` is a short content-addressed hash of the report body (first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via:

```bash
MAIN_ROOT="$(git worktree list | head -n1 | awk '{print $1}')"
```

(main-repo root, worktree-safe — never write to a linked worktree's local `reports/`).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.

## How to reference this file from a skill's SKILL.md

Replace the in-line `## Completion checklist` and `## Output` sections with:

```markdown
## Completion checklist + output

See [skill-completion-and-output-contract](../amw-design-principles/references/skill-completion-and-output-contract.md) for the standard completion checklist and the job-completion report contract. This skill's `## Non-negotiables` section below lists the skill-specific additions to that baseline.
```

Skills that have ADDITIONAL completion items beyond the baseline (e.g. "Mode A output must successfully execute `bin/amw-ascii-render.py`") add them under `## Non-negotiables` rather than duplicating the baseline.
