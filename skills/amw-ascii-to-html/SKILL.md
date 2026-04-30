---
name: amw-ascii-to-html
description: Convert a validated ASCII wireframe into responsive, accessible, Tweaks-compatible HTML. Triggers on narrow technical intents only — "convert this ASCII to HTML", "render this wireframe as HTML", "ascii-to-html", "turn my ASCII mockup into a webpage", "/amw-ascii-to-html". Does NOT trigger on generic "design a landing page" — that belongs to design-principles. Upstream consumer: user's `/amw-sketch` → approved variant. Orchestrated by design-principles.
version: 0.2.0
---

# ASCII → HTML converter

> Orchestrated by `../amw-design-principles/SKILL.md`. Terminal step of the `/amw-sketch` plan-phase loop. Do not run without explicit user approval of the ASCII (see Satisfaction Gate).

This skill is a SYNTHESIS — it composes techniques from 9 sources (starter-components, AI-slop rules, ui-ux-pro-max, ux-designer+a11y, create-infographics, diagram-design-editorial, ascii-creator catalog, CHI'24 ASCII classics, and the in-repo `ascii-parse.py`). Every design decision below cites a `TECH-NN` from `references/techniques.md`.

## Activation

Callable directly via the `/amw-ascii-to-html` command (user shortcut — fast path for users who already have an approved ASCII), or invoked by the `design-principles` orchestrator as the Phase B terminal step after Phase A approval in Main-agent mode. In Main-agent mode the orchestrator may apply rendering and token-application techniques from this skill beyond what the `/amw-ascii-to-html` command parameters expose.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT (terminal — Phase B). Converts an already-validated, already-approved ASCII wireframe into a single-file responsive HTML page. Upstream sources of acceptable input:

- `../amw-ascii-sketch/SKILL.md` — the plan-phase loop — approved variant at `/tmp/amw-sketch-<slug>-final.txt`.
- `../amw-ascii-creator/SKILL.md` — Mode B freeform wireframe, validator-PASS.
- User-supplied ASCII pasted into `$ARGUMENTS` (direct mode — flag to the user that the iteration loop was skipped).

All three producers guarantee the ASCII has already passed `bin/amw-validate-ascii.pl`. This skill does NOT re-validate by default; it gates on validator-PASS (TECH-99).

## Trigger conditions

Narrow. This skill does NOT own generic design vocabulary.

- "convert this ASCII to HTML"
- "render this wireframe as HTML"
- "turn my ASCII mockup into a webpage"
- "build the HTML from the approved sketch"
- "/amw-ascii-to-html <path>"

Anything matching "design a landing page" / "make a mockup" / "build a dashboard" routes to `../amw-design-principles/SKILL.md` first — that skill decides whether this one gets invoked.

## Preconditions (all three must hold)

1. **Validator-PASS.** Input ASCII passed `bin/amw-validate-ascii.pl`. If the upstream producer skipped validation, re-run it; hard-stop on FAIL (TECH-99).
2. **Explicit approval.** User said exactly one of `yes`, `ship it`, `convert it`, `that's the one`, `perfect`, `done`. Silence, "looks good", "sure", "ok", "fine" do NOT count — STOP and ask once: *"To confirm — convert this ASCII to HTML now?"*
3. **Tokens on file.** Design tokens exist from a prior `/amw-extract-style` run OR the user supplied an inline palette OR the user explicitly opted into starter-components defaults. NEVER invent tokens (TECH-63, TECH-24).

## Component detection table (synthesis evidence)

Every row maps an ASCII pattern → HTML element → which starter-component is the canonical source → which CSS tokens drive it. Parser functions from `bin/amw-ascii-parse.py` are named in parens.

| ASCII pattern | HTML element | Starter-component source | Key CSS tokens | Tech |
|---|---|---|---|---|
| Outer `╭─╮ / │..│ / ╰─╯` frame | `<div class="frame">` with `max-width` + `margin: 0 auto` | `browser-window.html` `.browser` | `--radius`, `--bg` | TECH-69, TECH-08 |
| 3-line rounded button `╭──╮ / │ L │ / ╰──╯` | `<button type="button">L</button>` min-h 44px | `animations.html` primary-btn | `--primary`, `--radius` | TECH-70, TECH-16, TECH-37 |
| Box with `▾` inside | `<button aria-haspopup="listbox" aria-expanded="false">L <span aria-hidden="true">▾</span></button>` | — | `--primary`, `--text` | TECH-74 |
| Titled card `│ Title │ / │ ──── │ / │ body │` | `<article class="card"><header class="card-title">` + bottom-border | — | `--bg`, `--text`, `--radius` | TECH-71, TECH-57 |
| 3 peer cards side-by-side | `<div class="row-3"><div class="card">...</div>×3</div>` CSS `grid-cols-3` | — | `--space-*`, gap | TECH-73, TECH-72 |
| Pipe-table w/ `----\|----` rule | `<table><thead><th scope="col">` | create-infographics table primacy | `--text`, `--bg` | TECH-82, TECH-54, TECH-49 |
| `[!]` / `[*]` prefix inside card | `<article role="alert" aria-live="polite" class="alert alert-warn">` | — | `--danger`, `--primary` | TECH-75, TECH-47 |
| `(@name)` attribution tag | `<span class="owner">@name</span>` with `aria-label` | — | `--text-muted` | TECH-76 |
| `→ action` inline route line | `<ul class="route-list"><li>` with `::before { content:"→ "; }` | — | `--text`, `--primary` | TECH-80 |
| `[ Text ]` / `[__ placeholder __]` | `<button>` / `<input>` with `<label for>` | form patterns | `--primary`, `--bg` | TECH-95, TECH-50 |
| `[x] Text` / `[ ] Text` / `(o)` `( )` | `<input type="checkbox">` / `<input type="radio">` | form patterns | focus-ring | TECH-95, TECH-44 |
| Sidebar + main `+---+------+` | CSS `grid-template-columns: 260px 1fr` | `macos-window.html` | layout | TECH-81, TECH-11 |
| T-junction `┬ / ┴` multi-col | CSS `grid-template-columns: repeat(N, 1fr)` | — | gap | TECH-72 |
| Nav tabs bar (3-line buttons in a row) | `<nav role="tablist"><button role="tab" aria-selected="true">` | `browser-window.html` tab chrome | `--primary`, `--radius` | TECH-08, TECH-43 |
| Numbered `1. STAGE` / `2. STAGE` | `<ol class="stages">` | — | `--text` | TECH-79 |
| Sparkline axis row `│────────│` inside a KPI card | inline `<svg viewBox>`+`<polyline>` placeholder | diagram-design-editorial | `--primary` | TECH-66, TECH-78 |
| `+---+|   |+---+` classic mode (detect_format = ascii) | `<pre class="classic-ascii">` preserving chars | — | mono font | TECH-88, TECH-94 |
| Empty row `│                │` inside box | extra `padding-top` on next child (not `<br>`) | — | `--space-*` | TECH-100 |

## Conversion pipeline

1. **Validate** with `bin/amw-validate-ascii.pl --in <source>`. FAIL → stop and return the validator report verbatim. (TECH-99)
2. **Parse** with `bin/amw-ascii-parse.py --in <source> --mode wireframe --out /tmp/amw-ascii-html-<slug>-layout.json`. This runs `detect_format`, `to_grid`, `find_boxes`, `find_arrows`, `find_wireframe_components`. (TECH-91..TECH-97)
3. **Pattern-match** each box/line against the component detection table above. Unknown shapes become literal text inside a `<div>` with a comment listing the glyphs that did not match — so the user can extend the parser if needed.
4. **Emit** semantic HTML:
   - `<header>` for the outer title row (if the wireframe has one — breadcrumbs, app name, date chip).
   - `<nav role="tablist">` for the tab row; each tab is `<button role="tab" aria-selected="<bool>" aria-controls="panel-N">`.
   - `<main>` for the viewport interior; use CSS grid with column count matching T-junctions.
   - `<section>` per horizontal-rule-delimited band (`├──┤` rows separate sections).
   - `<article>` for each card; `<article role="alert">` when the card has `[!]` / `[*]`.
   - `<table>` for any pipe-table region. `<thead>`, `<tbody>`, `<th scope="col">`.
   - `<footer>` only when the wireframe has one.
5. **Apply design tokens** from `/amw-extract-style` or user-supplied palette. Map to `:root { --primary; --text; --bg; --radius; --font-size; --space-1..--space-6; }` (TECH-07). Never invent values.
6. **Insert Tweaks block** (optional — only if the user requested live-editable tuning). Preserve the three invariants verbatim:
   - Listener registered BEFORE `__edit_mode_available` is posted (TECH-05).
   - `__edit_mode_set_keys` carries partial updates only (TECH-06).
   - `/*EDITMODE-BEGIN*/.../*EDITMODE-END*/` stays valid JSON with double-quoted keys AND values (TECH-04).
7. **React/Babel pins** — if and ONLY if the wireframe requires React (live state, interactive charts). Use the exact CDN URLs + integrity hashes in `starter-components/react-babel-pins.md` (TECH-01). Name every styles object with a component prefix (TECH-02).
8. **AI-slop gate** — mentally walk `ai-slop-avoid.md` top to bottom. Self-check every rule 1..26 and the density principle. Any FAIL → revise the section and re-check. Record PASS per rule in the file header comment. (TECH-19..TECH-30)
9. **Smoke test** — optionally load in `dev-browser` and check console for zero errors. Do NOT run this inside the plan phase if the user just asked for a static file.
10. **Save** to `<cwd>/<Descriptive Filename>.html` (Title-Case, no `v2`/`v3`). Return the file path + AI-slop checklist + a one-line summary.

## AI-slop avoidance gate (checklist, in order)

Run these before saving. Each is pulled from `ai-slop-avoid.md`:

- (1) No `linear-gradient(135deg, #667eea, #764ba2)` or similar purple-blue gradient. (TECH-19)
- (2) No `border-left: 4px solid <color>` on cards. (TECH-20)
- (3) No AI-drawn SVG illustrations (use sized gray placeholder with dimension label). (TECH-21)
- (4) No emoji carpet-bombing in headings or icons. (TECH-22)
- (5) No default Inter/Roboto/Arial/system-ui/Fraunces/Poppins for body. (TECH-24)
- (6) Max 3 font weights on one page. (TECH-25)
- (7) No alternating white / pale-gray / white mechanical bands. (TECH-26)
- (8) No "3 features in a row, icon each" stamped hero. (TECH-27)
- (9) No fabricated testimonials ("Sarah J., CEO at TechCorp"). (TECH-28)
- (10) No `element.scrollIntoView({behavior:'smooth'})` anywhere. (TECH-29)
- (11) Borders ≥ `rgba(primary, 0.3)` or solid — no ghost borders. (TECH-52)
- (12) Every element earns its place — delete decorative fillers. (TECH-30)

## Starter-component cross-reference

- `../amw-design-principles/starter-components/browser-window.html` — default desktop chrome (TECH-08).
- `../amw-design-principles/starter-components/ios-frame.html` — mobile-forced viewport (TECH-09).
- `../amw-design-principles/starter-components/macos-window.html` — sidebar + main desktop app shell (TECH-11).
- `../amw-design-principles/starter-components/deck-stage.html` — multi-screen deck with `data-screen-label` (TECH-10).
- `../amw-design-principles/starter-components/android-frame.html` — mobile Android device frame.
- `../amw-design-principles/starter-components/design-canvas.html` — free-standing canvas wrapper.
- `../amw-design-principles/starter-components/animations.html` — timeline core (~50 LOC) — use FIRST before Popmotion (TECH-12).
- `../amw-design-principles/starter-components/tweaks-block.html` — live-edit protocol (TECH-04, TECH-05, TECH-06, TECH-13).
- `../amw-design-principles/starter-components/react-babel-pins.md` — version lock spec (TECH-01, TECH-02, TECH-03).

## Dependencies

```yaml
runtime_binaries:
  - python3   # runs bin/amw-ascii-parse.py
  - perl      # runs bin/amw-validate-ascii.pl

python_packages: []   # ascii-parse.py is stdlib-only

npm: []              # no build; emitted HTML uses UMD CDN for React only

external_services:
  - none   # offline-capable
```

## Non-negotiables

- Approval gate is non-skippable. Ambiguous acknowledgement is NOT approval. (TECH rule from upstream design-principles)
- Single source file by default. Split only if > 1000 lines. (TECH-61)
- React/Babel pinned to exact versions with integrity hashes. No `react@18` shorthand. No `type="module"`. (TECH-01)
- Three Tweaks protocol invariants preserved verbatim when Tweaks block is included. (TECH-04, TECH-05, TECH-06)
- `scrollIntoView` is banned everywhere. (TECH-29)
- No Framer Motion, no GSAP. Timeline core first, Popmotion as physics fallback. (TECH-12)
- Inherits the three hard rules from `../amw-design-principles/SKILL.md` — context gathered, variants offered upstream, AI-slop refused.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Validator FAIL on input | Upstream producer skipped validation or user hand-edited ASCII | Stop. Return the validator FIX hints verbatim. Do not attempt to guess-repair. |
| Parser returns empty `boxes` | Input exceeds `MAX_GRID_DIM` and got truncated | Ask the user to split into multiple frames. (TECH-96) |
| Unknown glyphs in wireframe | ASCII uses custom symbols not in the parser's classifier | Parse what's parseable; list unknown glyphs in the emitted file's header comment; ask whether to extend the parser. |
| No prior `/amw-sketch` run but user pasted ASCII | Direct mode | Flag it: *"Skipping iteration loop. If you want to iterate in ASCII first, run /amw-sketch."* Proceed only on explicit confirm. |
| User approval is ambiguous ("looks good", "sure") | Not a satisfaction token | STOP. Ask once: *"To confirm — convert this ASCII to HTML now?"* |
| Slop-gate FAIL (rule 1..26) | Default tokens leaked, emoji in header, purple gradient, etc. | Revise the affected section once and re-check. Record the rule that triggered. |
| React pin mismatch | User upgraded `react@18` → UMD integrity hash mismatch | Re-pin to `react@18.3.1` exactly; restore the three CDN lines from `react-babel-pins.md`. |

## Cross-references

- `../amw-design-principles/SKILL.md` — orchestrator (ALWAYS activate this first when user says "design").
- `../amw-ascii-sketch/SKILL.md` — upstream producer of the approved ASCII.
- `../amw-ascii-creator/SKILL.md` — upstream single-artifact authoring skill.
- `../amw-ascii-validator/SKILL.md` — the mandatory validation gate (wraps `bin/amw-validate-ascii.pl` + `bin/amw-ascii-render.py`).
- `../amw-design-principles/starter-components/` — canonical chrome + tweaks protocol.
- `../amw-design-principles/ai-slop-avoid.md` — output-ban list (final gate).
- `../amw-design-principles/color-system.md` — oklch tokens.
- `../amw-design-principles/typography-system.md` — type scale + fallback stacks.
- `../amw-design-principles/spacing-rhythm.md` — 8pt grid + radius + shadow tokens.
- `../../bin/amw-ascii-parse.py` — parser.
- `../../bin/amw-validate-ascii.pl` — validator.
- `../amw-dev-browser/SKILL.md` — preview pipeline (optional).
- `/amw-ascii-to-html` — user-facing slash command.
- `/amw-preview` — automatic next step when requested.

### Technique catalog

Full catalog with source citations: `references/techniques.md` (100 techniques, 9 sources).

Representative techniques per conversion step:

- Step 1 (validate): TECH-99 (validate-alignment-pre-parse), TECH-94 (detect_format-choose-mode).
- Step 2 (parse): TECH-91 (find_boxes), TECH-92 (find_arrows), TECH-95 (find_wireframe_components).
- Step 3 (pattern-match): TECH-69 (outer-frame), TECH-70 (3-line button), TECH-82 (pipe-table), TECH-75 ([!] alert), TECH-73 (3-peer-row).
- Step 4 (semantic HTML): TECH-42 (semantic tags), TECH-47 (role=alert), TECH-49 (th scope), TECH-50 (label for).
- Step 5 (tokens): TECH-07 (css-var-root), TECH-17 (border-radius-scale), TECH-46 (contrast 4.5:1).
- Step 6 (tweaks): TECH-04 (EDITMODE block), TECH-05 (listener-before-announce), TECH-06 (partial updates).
- Step 7 (React pins): TECH-01 (integrity hashes), TECH-02 (styles prefix), TECH-03 (window export).
- Step 8 (slop gate): TECH-19 (no purple gradient), TECH-20 (no left-accent), TECH-24 (no Inter default), TECH-29 (no scrollIntoView), TECH-52 (visible borders).
- Step 9 (smoke-test): TECH-44 (focus ring), TECH-45 (prefers-reduced-motion).
- Step 10 (save): TECH-61 (single-file no-build), TECH-30 (every element earns place).
