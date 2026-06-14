---
name: amw-pretext
description: Pretext-driven typography, text measurement, layout, virtualized tables, ASCII-on-canvas, calligrams, 3D/motion text. Triggers on "pretext", "@chenglou/pretext", "text-on-path", "balanced headline", "shrink-wrap text", "virtualized list", "kinetic typography", "auto-fit font". Does NOT claim generic design vocabulary — design-principles retains those. Use when applying pretext-based typography or layout. Trigger with "pretext".
version: 0.1.0
---

# Pretext

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). Do not activate for generic "make the type nice" requests — those stay in the base typography system. Activate only on the narrow triggers above.

## Overview

Precision text-layout engine for when CSS flow is insufficient. Wraps `@chenglou/pretext` — a headless, DOM-free text measurement library — across 81 technique files covering API functions, measurement prerequisites, layout patterns, obstacle-aware flow, kinetic typography, virtualized tables, 3D/motion text, integration patterns, workflow assemblies, and CJK typography. Routes each narrow trigger (shrink-wrap, text-on-path, balanced headline, virtualized list, etc.) to the matching TECH file. Output reuses existing project typography tokens; pretext never introduces new fonts or motion systems.

## Instructions

The decide → pick → follow → build wrapper → handle resize → validate workflow runs in six steps: walk the `## Technique selection` tree to pick the category, open ONLY the matching `references/TECH-NN-<slug>.md` (never the whole catalog), call `prepare()` once before any layout call, reuse the project's typography tokens (pretext exposes metrics, not typographic decisions), call `clearCache()` on the resize path, and validate font-string parity before shipping. The full step-by-step procedure — with the TECH routing links — lives in [_how-to-use](references/_how-to-use.md).
> [_how-to-use.md] Instructions · How to use this skill

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during **Phase B** when the approved design requires precision text layout beyond what CSS flow provides (virtualization, shrink-wrap, obstacle-aware flow, kinetic typography). Also callable directly when the user explicitly names `pretext` or its API.

This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT. Pretext is the precision text-layout engine the plugin reaches for when CSS flow is insufficient (variable-height virtualization, shrink-wrap bubbles, obstacle-aware editorial flow, kinetic typography, auto-fit font search). All pretext-powered output must reuse the project's existing typography tokens — pretext does NOT introduce new fonts or motion systems, it just exposes the per-line metrics.

## Technique selection

**Always start with the decision guide** — if CSS already solves the problem (`line-clamp`, `text-overflow`, `text-wrap: balance`), skip pretext entirely. See [TECH-72-use-pretext-decision-guide](references/TECH-72-use-pretext-decision-guide.md).
> [TECH-72-use-pretext-decision-guide.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references

Then route by category (every technique below is one TECH file in `references/`; full one-line descriptions at [_index](references/_index.md)):
> [_index.md] API functions (TECH-01 — TECH-13) · Measurement prerequisites (TECH-14 — TECH-18) · Layout patterns / obstacle routing (TECH-19 — TECH-31) · Typography techniques (TECH-32 — TECH-44) · Motion / interactive demos (TECH-45 — TECH-55) · Tables (TECH-56 — TECH-58) · Integration patterns (TECH-59 — TECH-66) · Workflow assemblies (TECH-67 — TECH-71) · Consult / decision-routing (TECH-72 — TECH-78) · Cross-references

| Category | Range | Coverage |
|---|---|---|
| API functions | TECH-01 — TECH-13 | `prepare()`, `layout()`, `walkLineRanges()`, `measureLineStats()`, `clearCache()`, `setLocale()`, `prepareRichInline()`, `profilePrepare()` |
| Measurement prerequisites | TECH-14 — TECH-18 | DOM-free paragraph height, textarea pre-wrap parity, CJK keep-all, font-loading sync, font-string parity |
| Layout / obstacle patterns | TECH-19 — TECH-31 | flow around shapes, fit into container, multi-column handoff, balanced headline, auto-fit font, line-clamp truncate, layout-shift prevention, overflow prediction |
| Typography techniques | TECH-32 — TECH-44 | multilingual/bidi/emoji, kinetic width, wavy baseline, text-on-path, generative poster, typographic ASCII, calligrams, glyph mask, illuminated manuscript, variable-font waves, glyph morphing, outline calligram |
| Motion / interactive demos | TECH-45 — TECH-55 | accordions, chat bubbles, editorial spreads, multi-column engines, justification, cycling auto-fit, CSS filters, glyph paths, Three.js, splat editor, variable ASCII canvas |
| Tables | TECH-56 — TECH-58 | virtualized + resizable + sticky-header grid tables |
| Integration patterns | TECH-59 — TECH-66 | React hooks, Svelte/Astro islands, vanilla TS, SSR/Node-canvas, progressive enhancement, wrapper module, single-file ESM, ResizeObserver |
| Workflow assemblies | TECH-67 — TECH-71 | Masonry, virtualized list, SmartPage A4 auto-fit, streaming AI chat, auto-height textarea |
| Consult / route / mobile | TECH-73 — TECH-78 | design-pipeline consult, dragon-text reflow, rich-note atomic pills, postext (RN), font strategy, style profiles |
| CJK typography (JA + ZH stub) | TECH-80 — TECH-81 | Japanese web typography (kinsoku, BudouX `<wbr>`, `word-break:auto-phrase` engine matrix, `text-align:justify` suppression on mobile cards, `font-feature-settings:"palt"`, quoted-phrase protection) + Chinese-typography placeholder |

## Output

1. **Artifacts** — HTML pages / JS modules using `@chenglou/pretext` (wrapper module, layout component, virtualized table, etc.). Path is inferred from the project (user path → framework convention → `./design/<subtype>/` → fallback `./design/mockups/`).
2. **Job-completion report** at `$MAIN_ROOT/reports/webdesigner/<ts±tz>_<title-slug>_<8-char-hash>.md` listing every artifact + the per-item checklist verdict.

Full output contract (artifact-path inference rules, report shape, mandatory checklist) lives in [TECH-79-output-contract](./references/TECH-79-output-contract.md). Before reporting complete: every checklist item there MUST be PASS or N/A. Any FAIL triggers a remediation loop.
> [TECH-79-output-contract.md] 1. Artifacts (work product) · 2. Job-completion report (mandatory) · Completion checklist (FAIL on any → remediation loop, do not deliver partial work)

## Prerequisites

- **Runtime (user installs — NOT auto-installed by the plugin):** `@chenglou/pretext` via npm / bun — adds ~15 KB to the user's bundle. Documented in each TECH file; not mandatory for every design task.
- **Optional runtime companions:** `opentype.js@1.3.4` (glyph paths), `flubber@0.4.2` (glyph morph), `canvas` (Node SSR). All loaded conditionally by the TECH that needs them.
- **Plugin-side:** none — this skill is pure documentation / routing.

## Examples

Each TECH file under `./references/` contains a "Minimal example" section with near-runnable code. Start with `TECH-72-use-pretext-decision-guide.md` to determine if pretext is needed, then read the matching TECH file for the specific technique.

**Concrete example — auto-height textarea:**

- **Input:** "make this textarea auto-height as the user types"
- **Routing:** Decision tree → "Workflow assembly" → [TECH-71](references/TECH-71-auto-height-textarea.md)
> [TECH-71-auto-height-textarea.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- **Output:** ~80 LOC component using `prepare()` once at mount, `layout()` per keystroke, `whiteSpace: pre-wrap` parity per [TECH-15](references/TECH-15-textarea-prewrap.md), wrapper module per [TECH-64](references/TECH-64-wrapper-module.md). Saved to the project's component folder (Vite layout → *src/components/AutoTextarea.tsx*).
> [TECH-64-wrapper-module.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-15-textarea-prewrap.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references

**Concrete example — virtualized list with variable-height rows:**

- **Input:** "render a 10k-row chat log with smooth scrolling"
- **Routing:** Decision tree → "Workflow assembly" → [TECH-68](references/TECH-68-virtualized-list.md), companion measurement [TECH-14](references/TECH-14-dom-free-height.md) and [TECH-18](references/TECH-18-font-string-parity.md)
> [TECH-18-font-string-parity.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-14-dom-free-height.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-68-virtualized-list.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
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
> [typography-system.md] I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax · VIII. Forbidden AI-giveaway fonts (T-043)
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — review every kinetic / calligram output against item 9 (over-cute effects).
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- [`../amw-design-principles/starter-components/animations.html`](../amw-design-principles/starter-components/animations.html) — Stage + Sprite timeline; pretext kinetic work composes with this, not with Framer Motion / GSAP (banned plugin-wide).
- [SKILL](../amw-mermaid-render/SKILL.md) — pretext is NOT a diagram skill. For diagrams, the plugin has dedicated ASCII / Mermaid / SVG paths.
- [_index](references/_index.md) — flat catalog of every TECH-NN file.

## Non-negotiables

- Never activate on "make the type nice" / "pick a font" — those belong to [typography-system](../amw-design-principles/typography-system.md).
> [typography-system.md] I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax · VIII. Forbidden AI-giveaway fonts (T-043)
- No Framer Motion, no GSAP — plugin-wide ban. Pretext's frame-by-frame Canvas / SVG approach IS the approved kinetic-text alternative.
- The font string passed to `prepare()` MUST be loaded and byte-identical to what the renderer uses.
- `prepare()` MUST live outside animation / render loops. `layout()` is the hot path.
- HiDPI: scale the canvas backing store by `devicePixelRatio` at setup.
- No pseudocode — every code snippet in a TECH file is runnable or near-runnable.
- Responses stay in the user's language.
