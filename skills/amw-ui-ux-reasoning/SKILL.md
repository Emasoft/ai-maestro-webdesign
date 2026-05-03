---
name: amw-ui-ux-reasoning
description: LAST-RESORT fallback library — 161 reasoning rules, 67 UI styles, 161 color palettes, 57 font pairings, 24 landing-page patterns — consulted ONLY when no design system, brand tokens, or reference exists. Triggers on "pick a style for me", "I have no design system", "choose a palette", "suggest a font pairing", "what UI style should I use". Does NOT trigger on generic design intent. Use when no design system is available. Trigger with "pick a style for me".
version: 0.1.0
author: ai-maestro-webdesign
---

# UI/UX Reasoning (Last-Resort Library)

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Only run this skill when design-principles has determined that Rule 1 context-gathering has no anchor — no UI kit, no brand tokens, no reference URL, no existing components, and the user cannot name a style. If any anchor exists, skip this skill entirely.

## Overview

Last-resort fallback library consulted only when design-principles has exhausted Rule 1 context-gathering with no result. Collapses an infinite-choice space into a confirmable shortlist: 3 style + 3 palette + 3 font DNA candidates drawn from 67 UI styles, 161 color palettes, and 57 font pairings — all pre-filtered against [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md). Produces named anchors only; the user picks, then `amw-ascii-sketch` resumes with those anchors.

## Instructions

1. Confirm the activation condition: only proceed if design-principles has already attempted Rule 1 context-gathering and found no anchors (no UI kit, no brand tokens, no reference URL, no existing components); if any anchor exists, stop and route back to `../amw-design-principles/`.
2. Acknowledge the fallback in one sentence: "No anchors found — presenting three visual-DNA candidates from 67 styles / 161 palettes / 57 font pairings, filtered against ai-slop."
3. Present three style candidates (name, 3-5 keywords, best-for, one-sentence feel), pre-filtered against [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
4. Present three palette candidates (mood tag, primary/secondary/CTA/background/text, one-sentence industry fit) and three font-pair candidates (heading + body, pairing rationale, tone).
5. Ask the user to pick one from each column (or mix); do not emit HTML, ASCII wireframes, or CSS here — those belong to `../amw-ascii-sketch/`.

See `## Usage` below.

## Prerequisites

- **runtime_binaries:** none — the reasoning library is inlined in companion reference files.
- **npm_packages (optional):** `uipro-cli` (`npm install -g uipro-cli`) exposes the same taxonomy as a CLI. Not wired into the orchestrator; the skill works identically without it.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during Phase A as a fallback library when Rule 1 context-gathering finds no anchor. The orchestrator may consult any reasoning rule, palette, font pairing, or landing-page pattern from this skill without command-layer restriction.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

PLAN phase (Phase A fallback sub-branch). Normal plan-phase routing goes through `../amw-ascii-sketch/` for variant exploration. This skill is consulted only when ASCII sketching has nothing to anchor on.

```
design-principles
    ├─ Rule 1 context found?  YES → ../amw-ascii-sketch/ (normal path)
    └─ Rule 1 context EMPTY → ui-ux-reasoning (this skill)
                                 │ 3 style + 3 palette + 3 font DNA candidates
                                 ▼
                              user picks
                                 ▼
                              ../amw-ascii-sketch/ resumes with anchors
```

Output is a set of named visual-DNA anchors, not HTML. The user picks; `ascii-sketch` produces the three plan-phase variants required by Rule 2.

## Trigger conditions

Activate ONLY when the user's message contains an explicit "no context" signal AND design-principles has already asked and failed to gather anchors. Valid phrases:

- "pick a style for me"
- "I don't have a design system"
- "no preference — just make it professional"
- "choose a palette for me"
- "suggest a font pairing"
- "what UI style should I use"
- "surprise me" (after orchestrator confirmed no anchor)

Do NOT trigger on: "design a landing page", "make a nice site", "build a dashboard", "I want something modern". Those go through the orchestrator's normal context-gathering path.

## Library inventory

| Dimension | Count | Purpose |
|---|---|---|
| Reasoning rules | 161 | Industry / product-type decisions — layout archetype, style priority, color mood, anti-patterns |
| UI styles | 67 | Named visual languages (Glassmorphism, Brutalism, Editorial, Soft UI, Bento Grid, Claymorphism, Data-Dense, ...) with keywords + best-for |
| Color palettes | 161 | Industry-matched, slotted into primary / secondary / CTA / background / text with mood tags |
| Font pairings | 57 | Heading + body combos with Google Fonts URLs; pre-filtered to exclude ai-slop defaults |
| Landing-page patterns | 24 | Conversion-optimized section structures, CTA placement, social-proof cadence |

All outputs are descriptive anchors, not production tokens. Any palette chosen here must be re-expressed in oklch form via [color-system](../amw-design-principles/color-system.md) before the output phase.

## Dependencies

- **None required.** The reasoning library is inlined in this skill's companion files.
- **Optional:** the upstream `uipro-cli` npm package (`npm install -g uipro-cli`) exposes the same taxonomy as a CLI for shell scripting. Not wired into the orchestrator; the skill works identically without it.

## Usage

When design-principles routes here, emit exactly one response:

1. **Acknowledge the fallback.** One sentence: *"No anchors found. Three visual-DNA candidates drawn from 67 styles / 161 palettes / 57 font pairings, filtered against ai-slop."*
2. **Three style candidates** — each: name, 3-5 keywords, best-for, one-sentence feel.
3. **Three palette candidates** — each: mood tag, primary / secondary / CTA / background / text, one-sentence industry fit.
4. **Three font-pair candidates** — each: heading + body, why the pair works, tone.
5. **Ask the user to pick one from each column, or mix across columns.**

Do not generate HTML, ASCII wireframes, or CSS here. Those belong to `ascii-sketch` and `ascii-to-html`. This skill's only job is to collapse an infinite-choice space into a confirmable shortlist.

## Non-negotiables

- **Never runs on the happy path.** If any anchor exists (reference URL, brand doc, existing component, screenshot), skip this skill entirely.
- **Every candidate is screened against [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) BEFORE emission.** Inter, Roboto, Arial, system-default stacks are never proposed. Purple-blue linear gradients, rounded-card + 4px accent bar, AI-illustrated mascots — all filtered out at source.
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- **At least three candidates per dimension.** Never a single recommendation — matches design-principles Rule 2.
- **Palettes must be oklch-convertible.** See [color-system](../amw-design-principles/color-system.md). If a palette can't be cleanly re-expressed in oklch, drop it.
  > I. Always prefer oklch over rgb / hex / hsl · Why · Syntax · Comfort ranges · II. WCAG contrast — hard requirement · Checking tools · III. Palette structure (cap at 5–7 colors) · Standard 6-color framework · Rules · IV. Dark mode is not a simple inversion · Wrong approach · Right approach · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- **Font pairings must satisfy [typography-system](../amw-design-principles/typography-system.md)** — two-family limit, full weight coverage, Google-Fonts-available.
  > I. Modular type scale · Default recommendation (Perfect Fourth, base = 16px) · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · Successful combinations · Failure modes · VI. Recommended font stacks (avoiding AI slop) · Latin · CJK / other scripts · Banned list (AI slop) · VII. Fallback-stack syntax
- **Does not emit HTML or code.** Output is named anchors. Handoff to `../amw-ascii-sketch/` is mandatory.
- **Industry anti-patterns travel with every candidate.** If the reasoning rule for "finance" says avoid playful fonts and neon colors, the fallback output must annotate that constraint on fintech-leaning candidates.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `ui-ux-reasoning` is the user asking about?
  - **uiux** (12 techniques)
    - [TECH-uiux-design-system-generator](./references/TECH-uiux-design-system-generator.md) — Design System Generator (end-to-end composition)
    - [TECH-uiux-font-pairings-catalog](./references/TECH-uiux-font-pairings-catalog.md) — Font-pairings catalog (57 heading+body combos)
    - [TECH-uiux-lp-patterns-catalog](./references/TECH-uiux-lp-patterns-catalog.md) — Landing-page patterns catalog (24 conversion-optimized structures)
    - [TECH-uiux-palettes-catalog](./references/TECH-uiux-palettes-catalog.md) — Color-palette catalog (161 industry-matched palettes)
    - [TECH-uiux-pre-delivery-checklist](./references/TECH-uiux-pre-delivery-checklist.md) — Universal pre-delivery checklist
      > What it does · When to use · How it works · Accessibility · Responsive · Performance · Interaction · Minimal example · Gotchas · Cross-references
    - [TECH-uiux-rule-fintech](./references/TECH-uiux-rule-fintech.md) — Reasoning rule — Fintech / Crypto / Banking
    - (see `## References` for the remaining 6 in this group)

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-uiux-design-system-generator.md](./references/TECH-uiux-design-system-generator.md)**
  - Description: Design System Generator (end-to-end composition)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uiux-font-pairings-catalog.md](./references/TECH-uiux-font-pairings-catalog.md)**
  - Description: Font-pairings catalog (57 heading+body combos)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uiux-lp-patterns-catalog.md](./references/TECH-uiux-lp-patterns-catalog.md)**
  - Description: Landing-page patterns catalog (24 conversion-optimized structures)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uiux-palettes-catalog.md](./references/TECH-uiux-palettes-catalog.md)**
  - Description: Color-palette catalog (161 industry-matched palettes)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uiux-pre-delivery-checklist.md](./references/TECH-uiux-pre-delivery-checklist.md)**
  > What it does · When to use · How it works · Accessibility · Responsive · Performance · Interaction · Minimal example · Gotchas · Cross-references
  - Description: Universal pre-delivery checklist
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uiux-rule-fintech.md](./references/TECH-uiux-rule-fintech.md)**
  - Description: Reasoning rule — Fintech / Crypto / Banking
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uiux-rule-food-restaurant.md](./references/TECH-uiux-rule-food-restaurant.md)**
  - Description: Reasoning rule — Food / Restaurant / Hospitality
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uiux-rule-healthcare.md](./references/TECH-uiux-rule-healthcare.md)**
  - Description: Reasoning rule — Healthcare / Medical
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uiux-rule-luxury-ecommerce.md](./references/TECH-uiux-rule-luxury-ecommerce.md)**
  - Description: Reasoning rule — Luxury E-commerce
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uiux-rule-saas-dashboard.md](./references/TECH-uiux-rule-saas-dashboard.md)**
  - Description: Reasoning rule — SaaS Dashboard / B2B Analytics
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-uiux-rules-catalog.md](./references/TECH-uiux-rules-catalog.md)**
  - Description: Reasoning-rules catalog (161 rules)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Top 10 distinctive rules — broken out as individual TECH files
    - Cross-references
- **[./references/TECH-uiux-styles-catalog.md](./references/TECH-uiux-styles-catalog.md)**
  - Description: UI-styles catalog (67 named visual languages)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Representative styles (partial list — full 67 are in the upstream corpus)
    - Minimal example
    - Gotchas
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-ui-ux-reasoning/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. UI/UX reasoning notes (picked rules, palette, font pairing, pattern) as `.md`). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/references/` created fresh)
   - Last-resort scratch: `/tmp/amw-ui-ux-reasoning-<slug>/`

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

## Examples

Example 1 — fallback activation:
- **Input**: User says "I don't have a design system, pick a style for me" after `amw-design-principles` exhausted Rule 1 (no design-system docs, no brand tokens, no reference URL).
- **Output**: Three contrasting style anchors (e.g., Glassmorphism / Brutalist / Refined-modern) with ascii-friendly palette + font-pairing summaries. User picks one; orchestrator passes the chosen anchors to `amw-ascii-sketch` for Rule-2 plan-phase variants.

Example 2 — industry-aware guardrails:
- **Input**: Fallback activation for a "finance dashboard" use case.
- **Output**: Three anchors filtered against finance industry anti-patterns — playful fonts and neon palettes are excluded a priori. The user receives only style candidates that survive both the raw taxonomy AND the industry-specific reasoning rules.

Example 3 — ai-slop filter applied before emission:
- **Input**: Raw taxonomy match returns Inter/Roboto pairing and a purple-blue gradient.
- **Output**: Pairing rejected by `ai-slop-avoid` filter; substituted with a non-trope alternative (e.g., Söhne / IBM Plex Sans + a flat oklch palette). User sees only post-filter candidates.

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator that routes here as a fallback
- [SKILL](../amw-ascii-sketch/SKILL.md) — resumes variant exploration once anchors are picked
- [color-system](../amw-design-principles/color-system.md) — oklch structure the palettes must conform to
  > I. Always prefer oklch over rgb / hex / hsl · Why · Syntax · Comfort ranges · II. WCAG contrast — hard requirement · Checking tools · III. Palette structure (cap at 5–7 colors) · Standard 6-color framework · Rules · IV. Dark mode is not a simple inversion · Wrong approach · Right approach · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [typography-system](../amw-design-principles/typography-system.md) — font-pairing compatibility rules
  > I. Modular type scale · Default recommendation (Perfect Fourth, base = 16px) · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · Successful combinations · Failure modes · VI. Recommended font stacks (avoiding AI slop) · Latin · CJK / other scripts · Banned list (AI slop) · VII. Fallback-stack syntax
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — mandatory filter applied BEFORE emission
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- [question-templates](../amw-design-principles/question-templates.md) — the upstream checklist used to confirm no anchor exists
  > Universal must-ask (every design task) · Context & starting point · Task & goal · Variant dimensions · Tweaks · Hard constraints · Task-specific additions · Landing page / Website · Slides / Deck · App / Prototype · Poster / Single image · Infographic / Data viz · Brand collateral (business cards / invitations / emblems) · Questions NOT to ask · Suggested format · Tip

## Error Handling

- **Activating too eagerly.** Triggering on "design a landing page" instead of "pick a style for me". Orchestrator must have exhausted Rule 1 first.
- **Single-option output.** Emitting "I suggest Glassmorphism" instead of three candidates. Violates Rule 2.
- **Skipping the ai-slop filter.** Proposing Inter/Roboto pairings, purple-blue gradients, or the 4px accent bar because they appear in the raw library. The filter runs BEFORE emission — always.
- **Emitting HTML or CSS.** This skill produces anchors only. HTML belongs to `ascii-to-html` after plan-phase closure.
- **Forgetting the handoff.** After the user picks, routing must return to `../amw-ascii-sketch/` with the chosen anchors as visual DNA — not straight to `ascii-to-html`, because Rule 2 still needs three plan-phase variants.
- **Ignoring industry anti-patterns.** Proposing a playful-font / neon-palette combo for a finance product because the raw taxonomy allowed it — the reasoning rules for that industry forbid it.
