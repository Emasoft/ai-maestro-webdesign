---
name: amw-pretext
description: Pretext-driven typography, text measurement, layout, virtualized tables, ASCII-on-canvas, calligrams, 3D/motion text. Triggers on "pretext", "@chenglou/pretext", "text-on-path", "balanced headline", "shrink-wrap text", "virtualized list", "kinetic typography", "auto-fit font". Does NOT claim generic design vocabulary — design-principles retains those. Use when applying pretext-based typography or layout. Trigger with "pretext".
version: 0.1.0
---

# Pretext

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). Do not activate for generic "make the type nice" requests — those stay in the base typography system. Activate only on the narrow triggers above.

## Overview

Precision text-layout engine for when CSS flow is insufficient. Wraps `@chenglou/pretext` — a headless, DOM-free text measurement library — across 78 technique files covering API functions, measurement prerequisites, layout patterns, obstacle-aware flow, kinetic typography, virtualized tables, 3D/motion text, integration patterns, and workflow assemblies. Routes each narrow trigger (shrink-wrap, text-on-path, balanced headline, virtualized list, etc.) to the matching TECH file. Output reuses existing project typography tokens; pretext never introduces new fonts or motion systems.

## Instructions

1. Walk the `## Technique selection` decision tree below to identify the matching technique category (API function, measurement prerequisite, layout pattern, obstacle routing, kinetic typography, virtualized tables, 3D/motion, integration, workflow assembly).
2. Open ONLY the relevant `references/TECH-NN-<slug>.md` file — do not load the whole catalog. The full per-tech index lives in [_index](references/_index.md).
3. Follow the TECH file's "How it works" section; call `prepare()` (or the appropriate pretext API function) exactly once before calling any layout function.
4. Reuse the project's existing typography tokens — do not introduce new fonts or motion systems; pretext exposes per-line metrics but does not own typographic decisions.
5. Handle the resize path explicitly: call `clearCache()` on font-change or after every `ResizeObserver` tick when measurement validity has changed.
6. Validate the font-string parity constraint (same CSS font string in both pretext and the renderer) before shipping; see `TECH-18-font-string-parity.md`.

See the `## How to use this skill` section below for the authoritative step-by-step decision workflow, and the `## Technique selection` tree to pick the relevant TECH reference file.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during **Phase B** when the approved design requires precision text layout beyond what CSS flow provides (virtualization, shrink-wrap, obstacle-aware flow, kinetic typography). Also callable directly when the user explicitly names `pretext` or its API.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT. Pretext is the precision text-layout engine the plugin reaches for when CSS flow is insufficient (variable-height virtualization, shrink-wrap bubbles, obstacle-aware editorial flow, kinetic typography, auto-fit font search). All pretext-powered output must reuse the project's existing typography tokens — pretext does NOT introduce new fonts or motion systems, it just exposes the per-line metrics.

## Technique selection

Pick a technique category below, then look up the specific `TECH-NN-<slug>.md`
file by slug or technique number in the catalog at
[_index](references/_index.md). Each TECH file shares the
same TOC structure (What it does · When to use · How it works · Minimal
example · Gotchas · Cross-references), with category-specific extras.

**Always start with the decision guide** — if CSS already solves the
problem (`line-clamp`, `text-overflow`, `text-wrap: balance`), skip pretext
entirely. See [TECH-72-use-pretext-decision-guide](references/TECH-72-use-pretext-decision-guide.md).
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references

Then route by category — every technique number listed below is one TECH file inside the catalog:

- **API functions** — `prepare()`, `layout()`, `walkLineRanges()`, `measureLineStats()`, `clearCache()`, `setLocale()`, `prepareRichInline()`, `profilePrepare()` (TECH-01 through TECH-13).
- **Measurement prerequisites** — DOM-free paragraph height, textarea pre-wrap parity, CJK keep-all, font-loading sync, font-string parity (TECH-14 through TECH-18).
- **Layout / obstacle patterns** — text flowing around shapes, fitting into a container, multi-column handoff, balanced headline, auto-fit font, line-clamp truncate, layout-shift prevention, overflow prediction (TECH-19 through TECH-31).
- **Typography techniques** — multilingual/bidi/emoji, kinetic width animation, wavy baseline, text-on-path, generative poster, typographic ASCII, calligrams, glyph mask, illuminated manuscript, variable-font waves, glyph morphing, outline calligram (TECH-32 through TECH-44).
- **Motion / interactive demos** — accordion heights, chat bubbles, dynamic editorial spread, live multi-column engine, justification comparison, cycling text auto-fit, animated CSS filter, glyph path art, Three.js text-wrapping, splat editor, variable Typographic ASCII Canvas (TECH-45 through TECH-55).
- **Tables** — virtualized table with measured row heights, resizable table, grid table with sticky headers (TECH-56 through TECH-58).
- **Integration patterns** — React hooks, Svelte/Astro islands, vanilla TypeScript, SSR/Node-canvas, progressive enhancement, wrapper module, single-file ESM vendoring, ResizeObserver re-layout (TECH-59 through TECH-66).
- **Workflow assemblies** — Masonry grid, variable-height virtualized list, SmartPage A4 auto-fit, streaming AI chat, auto-height textarea (TECH-67 through TECH-71).
- **Consult / route / mobile** — full design-pipeline consultation, dragon text reflow, rich note with atomic pills, postext (React Native port), font strategy, style profiles (TECH-73 through TECH-78).

For one-line descriptions of every TECH file by category, open
[_index](references/_index.md).
  > Table of Contents · API functions (TECH-01 — TECH-13) · Measurement prerequisites (TECH-14 — TECH-18) · Layout patterns / obstacle routing (TECH-19 — TECH-31) · Typography techniques (TECH-32 — TECH-44) · Motion / interactive demos (TECH-45 — TECH-55) · Tables (TECH-56 — TECH-58) · Integration patterns (TECH-59 — TECH-66) · Workflow assemblies (TECH-67 — TECH-71) · Consult / decision-routing (TECH-72 — TECH-78) · Cross-references

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-pretext/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. HTML pages and/or JS modules that use `@chenglou/pretext` for precise text layout). The output path is determined by **project inference**, NOT hardcoded. See [project-output-routing](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/mockups/` created fresh)
   - Last-resort scratch: `/tmp/amw-pretext-<slug>/`

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

## How to use this skill

1. **Decide first:** read [TECH-72-use-pretext-decision-guide](references/TECH-72-use-pretext-decision-guide.md) — if CSS solves it (`line-clamp`, `text-overflow`, `text-wrap: balance`) there's no reason to add pretext.
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
2. **Pick the technique** from the decision tree above — one TECH file, not a monolithic dump. Use [_index](references/_index.md) for a flat lookup if you already know the slug.
3. **Follow the exact API path** documented in that TECH file. Do NOT improvise — pretext has sharp gotchas (lineHeight-in-px, font-string-parity, `system-ui` drift).
4. **Build the wrapper module first** ([TECH-64](references/TECH-64-wrapper-module.md)) — this catches the #1 integration bug (lineHeight multiplier vs pixels).
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
5. **Handle resize** ([TECH-66](references/TECH-66-resize-observer-pattern.md)) — re-layout never re-prepare.
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
6. **Validate against the font strategy** ([TECH-77](references/TECH-77-font-strategy.md)) — named fonts, `document.fonts.ready`, no `system-ui`.
  > What it does · When to use · How it works · Minimal example · Suggested font pairings by mood (source: pretext-frontend-motion-main/references/font-strategy.md) · Gotchas · Cross-references

## Prerequisites

- **Runtime (user installs — NOT auto-installed by the plugin):** `@chenglou/pretext` via npm / bun — adds ~15 KB to the user's bundle. Documented in each TECH file; not mandatory for every design task.
- **Optional runtime companions:** `opentype.js@1.3.4` (glyph paths), `flubber@0.4.2` (glyph morph), `canvas` (Node SSR). All loaded conditionally by the TECH that needs them.
- **Plugin-side:** none — this skill is pure documentation / routing.

## Examples

Each TECH file under `./references/` contains a "Minimal example" section with near-runnable code. Start with `TECH-72-use-pretext-decision-guide.md` to determine if pretext is needed, then read the matching TECH file for the specific technique.

**Concrete example — auto-height textarea:**

- **Input:** "make this textarea auto-height as the user types"
- **Routing:** Decision tree → "Workflow assembly" → [TECH-71](references/TECH-71-auto-height-textarea.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- **Output:** ~80 LOC component using `prepare()` once at mount, `layout()` per keystroke, `whiteSpace: pre-wrap` parity per [TECH-15](references/TECH-15-textarea-prewrap.md), wrapper module per [TECH-64](references/TECH-64-wrapper-module.md). Saved to the project's component folder (Vite → `./src/components/AutoTextarea.tsx`).
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references

**Concrete example — virtualized list with variable-height rows:**

- **Input:** "render a 10k-row chat log with smooth scrolling"
- **Routing:** Decision tree → "Workflow assembly" → [TECH-68](references/TECH-68-virtualized-list.md), companion measurement [TECH-14](references/TECH-14-dom-free-height.md) and [TECH-18](references/TECH-18-font-string-parity.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- **Output:** virtualized-list component that pre-measures every row height in a single `prepare()` pass, stores them in a binary index for O(log n) scroll-to-row, and layouts only the visible window. No row reflow on resize — call `clearCache()` and re-measure (TECH-66).

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| Measurement results differ from browser render | Font string mismatch between `prepare()` call and CSS/canvas renderer | Follow TECH-18: font-string parity — pass the exact same CSS font string to both. |
| Layout produces wrong line count after resize | `prepare()` called in the resize loop | `prepare()` must be called once at stable font load time; only call `layout()` on resize. See TECH-66. |
| Canvas text blurry on retina | Missing HiDPI backing-store scaling | Scale canvas by `devicePixelRatio` at setup. See TECH non-negotiables. |
| `@chenglou/pretext` not found | Library not installed in user's project | `npm install @chenglou/pretext` or `bun add @chenglou/pretext`. Not auto-installed by this plugin. |
| `system-ui` measurement drift across OS | Font resolved differently per OS | Use named, loaded fonts only. See TECH-77 (font strategy). |

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator; pretext must reuse the design-principles typography tokens, not introduce new fonts.
- [typography-system](../amw-design-principles/typography-system.md) — type scale + families pretext extends (never replaces).
  > I. Modular type scale · Default recommendation (Perfect Fourth, base = 16px) · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · Successful combinations · Failure modes · VI. Recommended font stacks (avoiding AI slop) · Latin · CJK / other scripts · Banned list (AI slop) · VII. Fallback-stack syntax
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — review every kinetic / calligram output against item 9 (over-cute effects).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
- [`../amw-design-principles/starter-components/animations.html`](../amw-design-principles/starter-components/animations.html) — Stage + Sprite timeline; pretext kinetic work composes with this, not with Framer Motion / GSAP (banned plugin-wide).
- [SKILL](../amw-mermaid-render/SKILL.md) — pretext is NOT a diagram skill. For diagrams, the plugin has dedicated ASCII / Mermaid / SVG paths.
- [_index](references/_index.md) — flat alphabetical/numeric catalog of every TECH-NN file with one-line descriptions.

## Non-negotiables

- Never activate on "make the type nice" / "pick a font" — those belong to [typography-system](../amw-design-principles/typography-system.md).
  > I. Modular type scale · Default recommendation (Perfect Fourth, base = 16px) · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · Successful combinations · Failure modes · VI. Recommended font stacks (avoiding AI slop) · Latin · CJK / other scripts · Banned list (AI slop) · VII. Fallback-stack syntax
- No Framer Motion, no GSAP — plugin-wide ban. Pretext's frame-by-frame Canvas / SVG approach IS the approved kinetic-text alternative.
- The font string passed to `prepare()` MUST be loaded and byte-identical to what the renderer uses.
- `prepare()` MUST live outside animation / render loops. `layout()` is the hot path.
- HiDPI: scale the canvas backing store by `devicePixelRatio` at setup.
- No pseudocode — every code snippet in a TECH file is runnable or near-runnable.
- Responses stay in the user's language.
