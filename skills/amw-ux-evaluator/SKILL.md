---
name: amw-ux-evaluator
description: Systematic UX evaluation of a rendered UI via a 3-dimension framework (Position, Visual Weight, Spacing) cross-checked against Balsamiq, Nielsen, and Material conventions. Narrow triggers — "evaluate UX", "review this component", "review UX", "check button design", "evaluate layout", "score this layout", "UX feedback on", "evaluate this page against heuristics", "run UX audit". Does NOT trigger on generic design-intent vocabulary ("design a page", "build a landing page", "mockup", "prototype", "style my page") — those belong to the `design-principles` orchestrator. Use when systematically evaluating a rendered UI component or layout against heuristics. Trigger with /amw-eval or explicit "evaluate UX" / "run UX audit" phrasing.
version: 0.1.0
author: ai-maestro-webdesign
---

# UX Evaluator

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Triggers are evaluation-specific only — `design-principles` routes already-rendered HTML here when the workflow calls for scored feedback before ship.

## Overview

Systematic UX evaluation of rendered HTML or live URLs using a 3-dimension framework: Position (reading flow, adjacency conventions), Visual Weight (hierarchy, fill vs ghost vs icon-only), and Spacing (gaps, touch targets, rhythm). Each dimension scores Pass / Warn / Fail with concrete selector + computed-style evidence. Cross-checks against Balsamiq, Nielsen, and Material conventions. Produces a structured evaluation report with prioritized recommendations (P1 = UX-breaking, P2 = suboptimal, P3 = polish). Read-only — never modifies HTML.

## Instructions

1. Gather context: identify the component (hero, navbar, CTA stack, form, pricing card), the evaluation trigger, and the input source (local HTML → `Read`; live URL → `../amw-dev-browser/`).
2. Score the three dimensions — Position (reading flow, adjacency), Visual Weight (fill vs ghost vs icon-only, hierarchy), and Spacing (gaps, touch targets, rhythm) — using concrete selector + computed-style evidence; each dimension gets Pass / Warn / Fail.
3. Produce a structured Markdown evaluation report with every Fail/Warn citing the selector, computed-style value, and the convention violated; prioritize findings as P1 (UX-breaking), P2 (suboptimal), P3 (polish).

See `## Usage` below.

## Examples

See [TECH-uxeval-output-format](references/TECH-uxeval-output-format.md) for a complete evaluation report example ("Pricing Page CTA Evaluation").

## Activation

Callable directly via the `/amw-eval` command (user shortcut — fast path for UX evaluation of a specific HTML file). Also invoked by the `design-principles` orchestrator as a Phase B validation step after HTML is produced in Main-agent mode. In Main-agent mode the orchestrator may apply the full 3-dimension framework and heuristic checklist from this skill beyond what the `/amw-eval` command parameters expose.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**VALIDATION (Phase B).** Runs on finished HTML or already-rendered components (not sketches, not wireframes) to produce scored feedback against Balsamiq + Nielsen + Material conventions. Positioned **after** `../amw-ascii-to-html/` has produced an HTML variant and **before** the user accepts it as shippable. Never writes HTML — reads, scores, reports.

## Trigger conditions

Activate only on explicit evaluation intents: "evaluate the UX of this page", "review this component", "review UX", "score this layout", "check button design", "UX feedback on …", "evaluate this page against Nielsen heuristics", "run a UX audit on …", "is this button positioned correctly", "check the spacing / visual weight of …".

Do **not** activate on generic design intent ("design a landing page", "make it look nicer", "build the UI", "style my page"). Those are owned by `design-principles`, which routes here only once an HTML artifact exists. Skip when the user has already committed and just wants implementation.

## Prerequisites

- **runtime_binaries (system):** none beyond plugin baseline (`node ≥ 22`).
- **runtime_binaries (via /amw-init):** none unique. Live-URL inspection delegates DOM + computed-style capture to `../amw-dev-browser/`; static HTML is read from disk directly.
- **python_packages / npm_packages / mcp_servers:** none. The framework is fully prose-encoded.

## Usage

Invoked by `/amw-eval [file.html | url]` or directly on an evaluation trigger.

**Step 1 — Gather context.** Identify the component (hero, navbar, CTA stack, form, pricing card), the reason for evaluation (user concern, pre-ship check, cited standard), and the input source (local HTML → `Read`; live URL → `../amw-dev-browser/`). Classify the component's role (primary CTA, secondary action, utility control, navigation, form field).

**Step 2 — Score the 3 dimensions.** For every inspected component:

| Dimension | What to analyze | Key questions |
|---|---|---|
| **Position** | Location relative to other elements, reading flow, adjacency | Does position follow conventions (primary right, utility far right)? Discoverable? |
| **Visual Weight** | Fill vs ghost vs icon-only, color, shadow, size, font weight | Does it compete with the primary action? Is the hierarchy legible at a glance? |
| **Spacing** | Gaps from adjacent elements, touch target, rhythm | Adequate separation (≥ 8 px intra-group, ≥ 24 px between groups)? Touch targets ≥ 44 × 44 px on mobile? |

Each dimension gets one of: **Pass** (matches convention), **Warn** (acceptable but suboptimal — improvement attached), **Fail** (breaks convention or accessibility floor — recommendation is mandatory).

**Step 3 — Report.** Markdown output, every Fail / Warn citing concrete evidence (selector, computed-style value, DOM attribute, measured pixel distance). Prose-only verdicts are rejected.

```markdown
## [Component Name] Evaluation

### Current State
- **Position:** [selector + coordinates]
- **Visual Weight:** [selector + computed-style evidence]
- **Spacing:** [measured gaps + selector pairs]

### Analysis

| Dimension | Verdict | Evidence | Rationale |
|---|---|---|---|
| Position | Pass / Warn / Fail | `selector` + value | Why + cited convention |
| Visual Weight | Pass / Warn / Fail | `selector` + computed-style | Why + cited convention |
| Spacing | Pass / Warn / Fail | measured gap + selectors | Why + cited convention |

### Verdict: PASS / NEEDS CHANGES

### Recommendations
| Priority | Change | Evidence | Cited principle |
|---|---|---|---|
| P1 | [Specific change] | [selector / value] | [e.g. Balsamiq #4 — primary on right] |
| P2 | [Specific change] | [selector / value] | [e.g. Nielsen #4 — consistency] |
```

**Priority rubric:** **P1** breaks UX (wrong button order, inaccessible touch target, buried primary, contrast below AA). **P2** suboptimal but usable (tight spacing, non-standard utility placement, weak label). **P3** polish only (token drift, micro-alignment, aesthetic).

**Step 4 — Hand off.** All Pass → emit report and stop. Warnings only → report; user decides. Fails present → recommendations return to `design-principles`, which decides patch-in-place vs re-enter `../amw-ascii-sketch/`.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Is the user asking about this skill's domain?
  - For "3-dimension evaluation framework (Position, Visual Weight, Spacing)" -> [TECH-uxeval-3-dimension-framework](./references/TECH-uxeval-3-dimension-framework.md)
    > What it does · When to use · How it works · Verdict rubric per dimension · Evaluation workflow · Minimal example · Gotchas · Cross-references
  - For "Button conventions (position + visual weight + spacing + labels)" -> [TECH-uxeval-button-conventions](./references/TECH-uxeval-button-conventions.md)
  - For "Form conventions (labels / submit / errors / spacing)" -> [TECH-uxeval-form-conventions](./references/TECH-uxeval-form-conventions.md)
  - For "Navigation conventions (logo / primary / utilities)" -> [TECH-uxeval-navigation-conventions](./references/TECH-uxeval-navigation-conventions.md)
    > What it does · When to use · How it works · Position (top bar, LTR) · Theme toggle placement (industry cross-check) · Visual weight · Utility control visual weight · Spacing · Mobile patterns · Minimal example · Gotchas · Cross-references
  - For "Output format — structured evaluation report" -> [TECH-uxeval-output-format](./references/TECH-uxeval-output-format.md)
  - For "Priority rubric (P1 / P2 / P3)" -> [TECH-uxeval-priority-rubric](./references/TECH-uxeval-priority-rubric.md)
    > What it does · When to use · How it works · Assignment rule · Output structure · Minimal example · Gotchas · Cross-references

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-uxeval-3-dimension-framework.md](./references/TECH-uxeval-3-dimension-framework.md)**
  > What it does · When to use · How it works · Verdict rubric per dimension · Evaluation workflow · Minimal example · Gotchas · Cross-references
  - Description: 3-dimension evaluation framework (Position, Visual Weight, Spacing)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uxeval-button-conventions.md](./references/TECH-uxeval-button-conventions.md)**
  - Description: Button conventions (position + visual weight + spacing + labels)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uxeval-form-conventions.md](./references/TECH-uxeval-form-conventions.md)**
  - Description: Form conventions (labels / submit / errors / spacing)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uxeval-navigation-conventions.md](./references/TECH-uxeval-navigation-conventions.md)**
  > What it does · When to use · How it works · Position (top bar, LTR) · Theme toggle placement (industry cross-check) · Visual weight · Utility control visual weight · Spacing · Mobile patterns · Minimal example · Gotchas · Cross-references
  - Description: Navigation conventions (logo / primary / utilities)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uxeval-output-format.md](./references/TECH-uxeval-output-format.md)**
  - Description: Output format — structured evaluation report
  - TOC:
    - What it does
    - When to use
    - How it works
    - [Component Name] Evaluation
    - Minimal example
    - Pricing Page CTA Evaluation
    - Gotchas
    - Cross-references
- **[./references/TECH-uxeval-priority-rubric.md](./references/TECH-uxeval-priority-rubric.md)**
  > What it does · When to use · How it works · Assignment rule · Output structure · Minimal example · Gotchas · Cross-references
  - Description: Priority rubric (P1 / P2 / P3)
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
- At least one `TECH-*.md` file from `skills/amw-ux-evaluator/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. UX evaluation `.md` reports scoring Position / Visual Weight / Spacing). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/references/` or `./reports/webdesigner/` created fresh)
   - Last-resort scratch: `/tmp/amw-ux-evaluator-<slug>/`

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

## Quick-lookup conventions

Full reference in [balsamiq-button-principles](references/balsamiq-button-principles.md). Summary:

- **Buttons:** primary right + filled + brand color; secondary left + ghost/outline; utility far right, icon-only. ≥ 24 px between groups, 8–12 px intra-group, ≥ 44 × 44 px mobile touch. Labels: "Sign Up" not "Get Started"; "Delete Account" not "Proceed"; verb-first.
- **Navigation:** logo left, primary nav centre or after logo, utilities (search / auth / theme) right. Active state clearly distinguished; nav does not compete with content.
- **Forms:** labels above/left of inputs; submit bottom, right-aligned or full-width; errors adjacent; label-to-input 0.25–0.5 rem; field-to-field 1–1.5 rem.
- **Industry cross-check:** button order secondary LEFT, primary RIGHT (GitHub, Stripe, Google, Notion). Theme toggle far right after user menu or in settings (GitHub, VS Code Docs, Stripe Docs). Utility controls icon-only, subordinate to primary actions.

## Resources

- [SKILL](../amw-dev-browser/SKILL.md) — source of live-page DOM + computed-style capture when the input is a URL.
- [spacing-rhythm](../amw-design-principles/spacing-rhythm.md) — grid / alignment / whitespace rules the evaluator enforces.
  > I. 8pt grid system · Allowed spacing values · T-shirt naming (use tokens) · Forbidden · II. Fibonacci spacing rhythm (large-scale) · III. Vertical rhythm (baseline grid) · Core rule · Result · IV. Hit targets (tappable areas) · V. Alignment · Left vs centered vs justified · Forbidden · VI. Three principles of whitespace · The most important element gets the most whitespace around it · Related elements cluster, unrelated elements separate (Gestalt proximity) · Outer whitespace > inner whitespace · VII. Border radius · Rules · VIII. Shadow system · Rules · IX. Self-check
- [typography-system](../amw-design-principles/typography-system.md) — type-scale compliance check.
  > I. Modular type scale · Default recommendation (Perfect Fourth, base = 16px) · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · Successful combinations · Failure modes · VI. Recommended font stacks (avoiding AI slop) · Latin · CJK / other scripts · Banned list (AI slop) · VII. Fallback-stack syntax
- [color-system](../amw-design-principles/color-system.md) — oklch / contrast validation for state surfaces.
  > I. Always prefer oklch over rgb / hex / hsl · Why · Syntax · Comfort ranges · II. WCAG contrast — hard requirement · Checking tools · III. Palette structure (cap at 5–7 colors) · Standard 6-color framework · Rules · IV. Dark mode is not a simple inversion · Wrong approach · Right approach · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — final scan for AI-slop patterns before a Pass verdict.
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- [SKILL](../amw-ascii-to-html/SKILL.md) — upstream producer of the HTML this skill evaluates.
- [SKILL](../amw-ui-ux-reasoning/SKILL.md) — industry-specific anti-pattern taxonomy.
- [balsamiq-button-principles](references/balsamiq-button-principles.md) — full button-design reference corpus.
  > Core Principles · Use Conventional Labels · Say Exactly What Happens · Primary and Secondary Should Look Different · Primary Action on the Right · Use Adequate Spacing · Make Buttons Look Clickable · Size Appropriately · Use Icons Wisely · Consider Loading States · Error Prevention · Button Hierarchy Summary · Common Mistakes
- `/amw-eval` — user-facing slash command that runs this skill.

## Non-negotiables

- **Read-only.** Never modifies the HTML it evaluates. Fixes are proposed; applying them is routed by `design-principles`.
- **Every Fail or Warn cites concrete evidence** — selector, computed-style value, DOM attribute, or measured pixel distance. Prose-only verdicts are rejected.
- **All three dimensions, always.** Partial evaluations are a failure mode.
- **Cite authoritative conventions, not preference.** Balsamiq, Nielsen, Material, or observable industry pattern (GitHub, Stripe, Notion, VS Code Docs).
- **Does not substitute for Lighthouse or axe-core.** Scores design quality, not runtime perf, not programmatic a11y. Those run alongside, not inside.
- **Prioritization is mandatory.** Every recommendation carries P1 / P2 / P3.
- **Run the `ai-slop-avoid.md` scan before emitting a Pass.** A component can satisfy the 3 dimensions and still be AI-slop-shaped; the final check is non-skippable.

## Error Handling

| Symptom | Likely cause | Fix |
|---|---|---|
| Auth-walled URL → blank DOM | Login required | Ask the user for a session cookie or pull the authenticated page locally; don't score a login page as the target. |
| JS-heavy SPA → missing component | Client-side render not yet complete | `../amw-dev-browser/` with wait flag via `dev-browser-wrapper.sh pass-through`; don't score a skeleton state. |
| Viewport-dependent layout scored at wrong width | Desktop vs mobile conventions differ | Specify viewport in the request; evaluate both breakpoints separately if ambiguous. |
| Missing computed-style data | CSS-in-JS or shadow DOM not surfaced in DOM dump | Fall back to screenshot-based visual evaluation, flag missing evidence explicitly; never fabricate selectors. |
| Report emitted without evidence | Evaluator shortcut ("looks wrong") | Reject and re-run. Evidence is a hard requirement. |
| All Warnings downgraded to Pass | Over-accommodating the user | Warnings remain Warnings. The user, not the evaluator, decides whether to accept. |
| Activated on generic design intent | Wrong entry point | "Design a landing page" belongs to `design-principles`. Activate only when HTML exists and a score was requested. |
