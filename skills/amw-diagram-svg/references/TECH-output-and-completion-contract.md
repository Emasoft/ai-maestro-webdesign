---
name: TECH-output-and-completion-contract
category: contract
source: skills/amw-diagram-svg/SKILL.md
also-in:
---
## Table of Contents

- [Output — artifacts and report](#output--artifacts-and-report)
- [Completion checklist](#completion-checklist)
- [Error handling](#error-handling)
- [Cross-references](#cross-references)

# TECH-output-and-completion-contract

The delivery contract for this skill: where artifacts land, what the
job-completion report must contain, the pre-delivery checklist, and the
error-handling table.

## Output — artifacts and report

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. standalone `.svg` diagrams). The output path is determined by **project inference**, NOT hardcoded. See [project-output-routing](../../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-diagram-svg-<slug>/`

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
- At least one `TECH-*.md` file from `skills/amw-diagram-svg/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section in the SKILL).
- No AI-slop per [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Error handling

| Symptom | Likely cause | Fix |
|---|---|---|
| SVG fails to parse | Unclosed tag, stray `&`, missing `xmlns` | Close all tags; include `xmlns="http://www.w3.org/2000/svg"` on the root. |
| Labels overflow nodes | Font too large or label too long | `font-size=18` is expressed in viewBox units, not rendered px — when the SVG ships inside a slide at 1920×1080 (viewBox 0–1000, factor ≈1.92×) it renders ≈35px, safely above the 24px slide floor; when inlined at <600px width it falls below 16px. Prefer splitting via `<tspan>` or shortening the label before dropping below 18 viewBox units. |
| Arrowheads invisible | `<marker>` absent, or `marker-end` URL typo | Verify `<marker id="arrow">` in `<defs>` and `marker-end="url(#arrow)"` id match. |
| Edges tangle / cross nodes | Spacing < 120 units or too dense | Increase spacing, reflow, or switch to grid. |
| Decision branches unclear | Diamond outputs unlabelled | Label edges `yes` / `no` or domain-specific. |
| Animation saturates diagram | Too many concurrent animations | Keep to one or two subtle pulses; prefer static when ambiguous. |
| Render script shows blank | `cairosvg` missing, or content outside `0–1000` viewBox | Install via `/amw-init`; reposition inside canvas. |
| User wanted a layered architecture | Wrong skill | Hand off to [SKILL](../../amw-diagram-architecture/SKILL.md). |

## Cross-references

- [SKILL](../SKILL.md) — the orchestration layer that routes here
- [project-output-routing](../../amw-design-principles/references/project-output-routing.md) — full artifact-path detection rules
  > When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
- [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) — the anti-slop checklist the output is graded against
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
