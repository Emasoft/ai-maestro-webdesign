---
name: amw-seo
description: SEO + Core Web Vitals evaluation framework (E-E-A-T quality signals, LCP/INP/CLS, structured data, technical foundations). Triggers on "SEO", "core web vitals", "E-E-A-T", "structured data", "schema markup", "page performance ranking", "search ranking", NOT generic design intent. Use when evaluating or improving a webpage's SEO, Core Web Vitals, or structured data markup. Trigger with explicit "SEO", "core web vitals", or "structured data" phrasing.
---

# SEO Evaluation Reference

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

SEO evaluation and Core Web Vitals interpretation framework. Knowledge-base only — interprets measurements from `amw-dev-browser` or user-supplied data; does not capture metrics itself. Covers 8 evaluation areas: E-E-A-T quality signals, Core Web Vitals (LCP/INP/CLS), technical SEO, content SEO, structured data / JSON-LD, AI-assisted content principles, relative importance of factors, and multi-signal measurement. Pairs with `amw-ux-evaluator` for combined UX + SEO scoring.

## Instructions

1. Classify the user's SEO concern into one of the 8 evaluation areas (E-E-A-T, Core Web Vitals, Technical SEO, Content SEO, Structured Data, AI-assisted content, Relative importance, Measurement).
2. Walk the `## Technique selection` tree top-down and open only the single TECH reference file whose TOC matches the current concern.
3. Gather live metrics when needed via [SKILL](../amw-dev-browser/SKILL.md) (LCP candidate identification, resource sizes, layout shift observation, interaction latency); interpret them through the framework — this skill does not capture metrics itself.
4. Score against the relevant thresholds (LCP < 2.5s, INP < 200ms, CLS < 0.1 for Core Web Vitals; E-E-A-T signals for content quality) and produce a prioritized list of findings.
5. When a combined UX + SEO audit is requested, pair with [SKILL](../amw-ux-evaluator/SKILL.md) — run both evaluations and merge the finding lists by priority.

Walk the `## Technique selection` tree to pick the matching TECH reference for the user's SEO concern. Read only the file whose TOC matches the current need.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during **Phase B** when the user requests SEO scoring alongside design work, or when `/amw-eval` triggers an SEO + UX combined audit. Also callable directly when the user explicitly names SEO, Core Web Vitals, E-E-A-T, or structured data.

This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow
VALIDATION / REFERENCE. Evaluation framework used alongside `ux-evaluator` when the user wants SEO + design quality scored together. Knowledge-base only — interprets measurements; does not capture them.

## Trigger conditions
- "audit SEO", "SEO review", "SEO score"
- "core web vitals", "LCP", "INP", "CLS", "page experience"
- "E-E-A-T", "experience expertise authoritativeness trust"
- "structured data", "schema markup", "JSON-LD", "rich results"
- "search ranking factors", "why does this page rank"
- "is this page SEO-ready"

Does NOT trigger on: generic "make this look better", pure visual critique, copywriting requests without search-intent framing.

## Prerequisites
- runtime_binaries: none (framework is prose-encoded)
- Pairs with [SKILL](../amw-dev-browser/SKILL.md) for live capture: LCP candidate identification, resource sizes, layout shift observation, interaction latency
- Pairs with [SKILL](../amw-ux-evaluator/SKILL.md) when user requests combined UX + SEO scoring

## Evaluation framework sections

1. **E-E-A-T** — Experience, Expertise, Authoritativeness, Trust. Quality lens, not a direct ranking factor; weighted heavily on YMYL topics.
2. **Core Web Vitals** — LCP < 2.5s, INP < 200ms, CLS < 0.1. Rarely override poor content but hold back otherwise-good pages.
3. **Technical SEO** — Crawl/index control (sitemap, robots.txt, canonical, status codes, HTTPS), performance, semantic HTML.
4. **Content SEO** — Page elements (title, meta, H1, headings, alt) + quality signals (depth, originality, accuracy, clarity, usefulness).
5. **Structured data** — Schema.org / JSON-LD types enable rich-result eligibility; do not boost rankings directly.
6. **AI-assisted content** — Output quality matters, not authorship method. Unedited AI output with factual errors or thin value is the failure mode.
7. **Relative importance** — No fixed order. When pages compete closely: content quality > authority/trust > page experience > mobile > technical accessibility.
8. **Measurement** — Multi-signal validation: visibility, engagement, performance (CWV field data), coverage, authority.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Is the user asking about this skill's domain?
  - For "AI-assisted content principles" -> [TECH-seo-ai-content](./references/TECH-seo-ai-content.md)
> [TECH-seo-ai-content.md] What it does · When to use · How it works · Effective use · Risky use · Minimal example · Gotchas · Cross-references
  - For "Content SEO — page elements + quality signals" -> [TECH-seo-content-quality](./references/TECH-seo-content-quality.md)
> [TECH-seo-content-quality.md] What it does · When to use · How it works · Page-level elements · Content quality signals · Intent classification · Minimal example · Gotchas · Cross-references
  - For "Core Web Vitals — page-experience signals" -> [TECH-seo-cwv](./references/TECH-seo-cwv.md)
> [TECH-seo-cwv.md] What it does · When to use · How it works · Field data vs lab data · Important context · Minimal example · Gotchas · Cross-references
  - For "E-E-A-T — Quality Evaluation Framework" -> [TECH-seo-eeat](./references/TECH-seo-eeat.md)
  - For "Measurement — multi-signal SEO validation" -> [TECH-seo-measurement](./references/TECH-seo-measurement.md)
> [TECH-seo-measurement.md] What it does · When to use · How it works · Cross-validation examples · KPIs worth tracking vs vanity metrics · Minimal example · Gotchas · Cross-references
  - For "Relative importance of SEO factors" -> [TECH-seo-relative-importance](./references/TECH-seo-relative-importance.md)
> [TECH-seo-relative-importance.md] What it does · When to use · How it works · Approximate weight hierarchy · The operational rule · Remediation priority · Minimal example · Gotchas · Cross-references
  - For "Structured data (Schema.org / JSON-LD)" -> [TECH-seo-structured-data](./references/TECH-seo-structured-data.md)
  - For "Technical SEO principles" -> [TECH-seo-technical](./references/TECH-seo-technical.md)
> [TECH-seo-technical.md] What it does · When to use · How it works · Crawl & index control · Performance & accessibility (technical prerequisites for CWV) · Common technical failures · Minimal example · Gotchas · Cross-references

## References

Every technique in this skill is documented as a single reference file under `./references/`. Each file follows the standard TOC: What it does · When to use · How it works · Minimal example · Gotchas · Cross-references. The technique-selection tree above is the authoritative router — open only the file whose tree branch matches the current need.

- [TECH-seo-ai-content](./references/TECH-seo-ai-content.md) — AI-assisted content principles
> [TECH-seo-ai-content.md] What it does · When to use · How it works · Effective use · Risky use · Minimal example · Gotchas · Cross-references
- [TECH-seo-content-quality](./references/TECH-seo-content-quality.md) — Content SEO: page elements + quality signals
> [TECH-seo-content-quality.md] What it does · When to use · How it works · Page-level elements · Content quality signals · Intent classification · Minimal example · Gotchas · Cross-references
- [TECH-seo-cwv](./references/TECH-seo-cwv.md) — Core Web Vitals: page-experience signals
> [TECH-seo-cwv.md] What it does · When to use · How it works · Field data vs lab data · Important context · Minimal example · Gotchas · Cross-references
- [TECH-seo-eeat](./references/TECH-seo-eeat.md) — E-E-A-T Quality Evaluation Framework
> [TECH-seo-eeat.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-seo-measurement](./references/TECH-seo-measurement.md) — Multi-signal SEO validation
> [TECH-seo-measurement.md] What it does · When to use · How it works · Cross-validation examples · KPIs worth tracking vs vanity metrics · Minimal example · Gotchas · Cross-references
- [TECH-seo-relative-importance](./references/TECH-seo-relative-importance.md) — Relative importance of SEO factors
> [TECH-seo-relative-importance.md] What it does · When to use · How it works · Approximate weight hierarchy · The operational rule · Remediation priority · Minimal example · Gotchas · Cross-references
- [TECH-seo-structured-data](./references/TECH-seo-structured-data.md) — Structured data (Schema.org / JSON-LD)
> [TECH-seo-structured-data.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-seo-technical](./references/TECH-seo-technical.md) — Technical SEO principles
> [TECH-seo-technical.md] What it does · When to use · How it works · Crawl & index control · Performance & accessibility (technical prerequisites for CWV) · Common technical failures · Minimal example · Gotchas · Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-seo/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. SEO evaluation report `.md` files; interpretation only — no measurements taken). The output path is determined by **project inference**, NOT hardcoded. See [project-output-routing](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/references/` or `./reports/webdesigner/` created fresh)
   - Last-resort scratch: `/tmp/amw-seo-<slug>/`

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

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`.

**Every artifact MUST be linked from the report.** `reports/webdesigner/` is for user-facing job outputs; `reports/audit/` is for build-time audits — keep them separate.

## Examples

See each TECH file under `./references/` for the "Minimal example" section. E.g. `TECH-seo-cwv.md` shows a PageSpeed Insights interpretation workflow; `TECH-seo-structured-data.md` shows a JSON-LD Article schema snippet.

## Resources
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator
- [SKILL](../amw-dev-browser/SKILL.md) — live page inspection for CWV capture
- [SKILL](../amw-ux-evaluator/SKILL.md) — pairs for combined UX + SEO scoring
- `/amw-eval` — user-facing command that runs ux-evaluator + seo together

## Non-negotiables
- Does NOT claim generic design / UI work.
- Knowledge-base only — does NOT run measurements itself; pairs with `dev-browser` for live capture.
- Does NOT substitute for Lighthouse / PageSpeed Insights / CrUX — those measure; this skill interprets.
- Does NOT promise ranking outcomes. SEO is probabilistic; factor weights shift over time.

## Error Handling
- JS-heavy SPA that does not render without JS → CWV capture misleading; flag and request SSR / pre-rendered variant before scoring.
- Auth wall / paywalled page → cannot observe what crawlers see; request public-equivalent URL or admit evaluation is partial.
- Offline environment → no live CWV, no structured-data validator access; restrict output to static-analysis findings and mark dynamic claims as unverified.
- User asks for guaranteed ranking lift → decline; SEO evaluation reports quality signals, not predictions.
