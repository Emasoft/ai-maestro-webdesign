---
name: TECH-output-contract
category: hyperframes-bridge
source: skills/amw-hyperframes-bridge/SKILL.md
---

# TECH: Output contract + completion checklist — amw-hyperframes-bridge

The skill produces TWO kinds of output. Both MUST be present for the run to be considered complete.

## 1. Artifacts (work product)

Hyperframes project folders + rendered MP4 videos. The output path is determined by **project inference** (NOT hardcoded):

1. **User-supplied path** — honor verbatim.
2. **Framework convention** — React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.
3. **Existing `./design/<subtype>/` folder** — use if present.
4. **Generic fallback** — `./design/videos/` (created fresh).
5. **Last-resort scratch** — `/tmp/amw-hyperframes-bridge-<slug>/`.

Full detection rules: [project-output-routing](../../amw-design-principles/references/project-output-routing.md).

## 2. Job-completion report (mandatory)

Path: `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>-amw-video-producer-<slug>-<8-char-hash>.md`

- The agent name in the path lets multi-agent runs in the same minute avoid collisions.
- The 8-char hash is the SHA-256 prefix of the inputs+artifacts list — disambiguates re-runs of the same agent on the same input.
- Grammar matches `agents/amw-video-producer-agent.md` §7.10 — both producers MUST emit the same shape.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

Report sections, in order:

- **Inputs** — what the user provided + any auto-detected context.
- **Method** — which TECH references were consulted, which pipeline steps ran.
- **Artifacts** — bullet list, one per produced file: `- <artifact-path> — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`.
- **Checklist** — each Completion-checklist item with PASS / FAIL / N/A.
- **Deviations** — any step skipped or changed, with rationale.

`reports/webdesigner/` is for user-facing job outputs from this plugin (distinct from `reports/audit/` for build-time audit artifacts). **Every artifact MUST be linked from the report**; if an artifact is produced but not listed, the skill run is incomplete.

## Completion checklist (FAIL on any → remediation loop, do not deliver partial work)

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-hyperframes-bridge/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section in SKILL.md).
- No AI-slop per [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) — generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template, etc.
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).
