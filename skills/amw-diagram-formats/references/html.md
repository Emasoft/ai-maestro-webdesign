## Table of Contents

- [1. Format definition](#1-format-definition)
- [2. Starter-components mapping](#2-starter-components-mapping)
- [3. Tweaks protocol invariants (HARD RULES)](#3-tweaks-protocol-invariants-hard-rules)
- [4. React / Babel pin rules](#4-react-babel-pin-rules)
- [5. AI-slop-avoid gate (12-item checklist)](#5-ai-slop-avoid-gate-12-item-checklist)
- [6. ARIA / keyboard / a11y patterns](#6-aria-keyboard-a11y-patterns)
- [7. CSS custom properties (Tweaks-compatible)](#7-css-custom-properties-tweaks-compatible)
- [8. Per-source breakdown of the technique catalog](#8-per-source-breakdown-of-the-technique-catalog)
- [9. Technique catalog](#9-technique-catalog)
- [10. Migration note (2026-04-22)](#10-migration-note-2026-04-22)

## Overview — canonical format reference

This file is the single authoritative spec for HTML diagrams and HTML pages emitted by the `ai-maestro-webdesign` plugin. Every skill that creates, modifies, validates, or converts HTML pulls from this file. Semantic HTML patterns, starter-components mapping, AI-slop-avoid gate, Tweaks invariants, React/Babel pins, ARIA/a11y rules, CSS custom properties, and the full technique catalog (100 techniques, migrated from `ascii-to-html/` into this canonical home) are all below.

**Consumers (cross-references):**
- [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) — the output-ban gate run as final check
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- `../../amw-design-principles/starter-components/*` — all 9 canonical chrome components
- [color-system](../../amw-design-principles/color-system.md) — oklch palette
  > I. Always prefer oklch over rgb / hex / hsl · Why · Syntax · Comfort ranges · II. WCAG contrast — hard requirement · Checking tools · III. Palette structure (cap at 5–7 colors) · Standard 6-color framework · Rules · IV. Dark mode is not a simple inversion · Wrong approach · Right approach · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [typography-system](../../amw-design-principles/typography-system.md) — type scale
  > I. Modular type scale · Default recommendation (Perfect Fourth, base = 16px) · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · Successful combinations · Failure modes · VI. Recommended font stacks (avoiding AI slop) · Latin · CJK / other scripts · Banned list (AI slop) · VII. Fallback-stack syntax
- [SKILL](../../amw-ascii-to-html/SKILL.md) — ASCII → HTML parse/map/emit pipeline
- [SKILL](../../amw-diagram-editorial/SKILL.md) — 13-archetype editorial HTML+SVG producer
- [SKILL](../../amw-infographics/SKILL.md) — dense HTML/PNG/PDF producer
- [SKILL](../../amw-shadcn-ui/SKILL.md) — component reference
- [SKILL](../../amw-tailwind-4/SKILL.md) — utility reference
- `../../bin/amw-html-export.py` — HTML → PNG/PDF rasterizer (Playwright)
- `../../bin/amw-ascii-parse.py` — ASCII → layout JSON consumed by HTML emitter
- [ir-schema](./ir-schema.md) — when HTML is a source of the diagram IR
  > Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Minimal flowchart (3 nodes, 2 edges) · Sequence (two actors, one message + note) · Architecture (3 layers) · Raw-source stub (MVP HTML → IR) · Validation · Consumers
- [conversion-matrix](./conversion-matrix.md) — HTML → {ASCII, SVG, Mermaid, PNG} cells
  > Full N×N table · Cell semantics · PNG-as-source refusal (mandatory) · PNG-as-target pipelines (all supported) · Dispatch algorithm · Per-cell implementation notes · Tools index (required backends) · Related references · ascii · html · svg · mermaid · png
- [modify-flow](./modify-flow.md) — edit flow for existing `.html` artifacts
  > The pipeline · Create vs modify dispatch · Step-by-step detail · Step 1 — Detect · Step 2 — Parse to IR · Step 3 — Patch · Step 4 — (loop point) · Step 5 — Emit · Step 6 — Re-validate · Work directory and file naming · Per-format guidance · 1 ASCII modify (MVP structural) · 2 HTML modify (MVP raw-source; Phase 1 structural) · 3 SVG modify (MVP raw-source; Phase 1 structural) · 4 Mermaid modify (MVP raw-source; Phase 1 structural) · Conversion is a modify-flow variant · Composition with round-trip skills · 1 `diagram-webpage-sync` (`/amw-modify-webpage-from-diagram`) · 2 `webpage-to-diagram` (`/amw-modify-diagram-of-webpage`) · Related references · `/amw-create-or-modify-ascii-diagram` → backed by `ascii-creator` · `/amw-create-or-modify-html-diagram` → backed by `html-diagram` · `/amw-create-or-modify-svg-diagram` → backed by `svg-diagram` · `/amw-create-or-modify-mermaid-diagram` → backed by `mermaid-diagram` · `diagram-webpage-sync` / `/amw-modify-webpage-from-diagram` · `webpage-to-diagram` / `/amw-modify-diagram-of-webpage`
- [validation-dispatcher](./validation-dispatcher.md) — unified validator output contract (HTML branch = `xmllint --html` or `tidy`)
  > Unified output contract · Dispatch algorithm · PNG refusal message (fixed) · Per-format validator specs · 1 ASCII — `bin/amw-validate-ascii.py` (primary) and `bin/amw-validate-ascii.py` (fallback) · 2 SVG — `bin/amw-validate-svg-diagram.sh` · 3 HTML — `bin/amw-validate-html-diagram.sh` · 4 Mermaid — `bin/amw-mermaid-lint.sh` · Caller integration patterns · 1 Post-create gate · 2 Post-convert gate · 3 Modify-flow loop · 4 Multi-format mode (ascii-validator) · Known limitations (Phase 0) · Related references

---

## 1. Format definition

HTML emissions in this plugin are **single-file, self-contained `.html` artifacts** with:
- Inline CSS in `<style>` — no external stylesheets
- Inline SVG where diagrams are needed — no `<img src>` to remote assets
- React / Babel via pinned UMD CDN URLs (with integrity hashes) — only when the artifact is interactive
- Static HTML otherwise

No build step. No `npm install`. No bundler. A cold clone of the plugin opens the emitted file directly in a browser and it renders.

### 1.1 File structure (baseline)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Descriptive Title</title>
  <style>
    :root { /* CSS custom properties — Tweaks-compatible */ }
    /* inline CSS — no @import of external sheets */
  </style>
</head>
<body>
  <header><nav></nav></header>
  <main>
    <section></section>
    <article></article>
  </main>
  <footer></footer>
  <!-- Optional: tweaks-block.html contents -->
</body>
</html>
```

### 1.2 Semantic-HTML requirements

- **Top-level landmarks**: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>` — NEVER `<div role="...">` override (TECH-42)
- **One `<h1>` per page**, heading hierarchy without skips
- **Lists**: `<ul>` / `<ol>` / `<dl>` based on semantic — numbered stages = `<ol>` (TECH-79), glossary = `<dl>` (TECH-83), nav = `<ul>`
- **Tables**: `<table><thead><tbody>`, every `<th>` has `scope="col"` or `scope="row"` (TECH-49)
- **Forms**: every `<input>` has `<label for="id">` or `aria-label` (TECH-50)
- **Code**: `<pre><code>`, monospace stack (TECH-67)

---

## 2. Starter-components mapping

The plugin ships 9 canonical chrome components under `skills/amw-design-principles/starter-components/`. Every HTML emitter references one of these as shell; the content sits inside.

| Component | Path | Used for | Key technique(s) |
|---|---|---|---|
| `browser-window.html` | starter-components/browser-window.html | Desktop laptop mockup | TECH-08 (chrome), TECH-14 (3-layer shadow), TECH-15 (inline SVG), TECH-16 (hit targets) |
| `ios-frame.html` | starter-components/ios-frame.html | Mobile mockup (390×844) | TECH-09 (mobile-force) |
| `android-frame.html` | starter-components/android-frame.html | Android mockup | Same family as iOS |
| `macos-window.html` | starter-components/macos-window.html | Desktop app with sidebar | TECH-11 (grid 260px 1fr) |
| `deck-stage.html` | starter-components/deck-stage.html | Multi-screen slide deck | TECH-10 (`data-screen-label`) |
| `design-canvas.html` | starter-components/design-canvas.html | Freeform canvas for poster / editorial | TECH-82 (small caps), TECH-83 (3-col editorial) |
| `animations.html` | starter-components/animations.html | ~50-LOC timeline core | TECH-12 (animations) |
| `tweaks-block.html` | starter-components/tweaks-block.html | Runtime-editable JSON config | TECH-04, TECH-05, TECH-06, TECH-13 |
| `react-babel-pins.md` | starter-components/react-babel-pins.md | Exact React/Babel UMD pins | TECH-01, TECH-02, TECH-03 |

---

## 3. Tweaks protocol invariants (HARD RULES)

The `tweaks-block.html` component implements a two-way postMessage protocol with a host page. Three invariants a future Claude MUST NOT break:

### 3.1 Listener-before-announce

```javascript
// ✅ CORRECT ORDER
window.addEventListener('message', handler);          // 1. Register first
window.parent.postMessage({type: '__edit_mode_available'}, '*');  // 2. Announce second

// ❌ WRONG — host's activate message races ahead of listener
window.parent.postMessage({type: '__edit_mode_available'}, '*');  // announces first
window.addEventListener('message', handler);          // registers too late
```

### 3.2 Partial-keys only

`__edit_mode_set_keys` carries **only changed keys**, never the full config:

```javascript
// ✅ CORRECT
postMessage({type: '__edit_mode_set_keys', edits: {primary: '#ff0000'}});

// ❌ WRONG — sending full config overwrites keys the host didn't touch
postMessage({type: '__edit_mode_set_keys', edits: entireConfig});
```

### 3.3 Valid JSON EDITMODE block

The `/*EDITMODE-BEGIN*/ … /*EDITMODE-END*/` block stays valid JSON with **double-quoted keys AND string values**. The host parses it and writes back to disk; a syntax slip bricks persistence.

```javascript
/*EDITMODE-BEGIN*/
{
  "primary": "#0066cc",
  "radius": "8px",
  "fontSize": "16px"
}
/*EDITMODE-END*/
```

---

## 4. React / Babel pin rules

Exact versions, exact integrity hashes, NEVER `react@18` shorthand, NEVER `type="module"`.

```html
<script crossorigin
  src="https://unpkg.com/react@18.3.1/umd/react.development.js"
  integrity="sha384-..."></script>
<script crossorigin
  src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"
  integrity="sha384-..."></script>
<script
  src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js"
  integrity="sha384-..."></script>
```

**Rules:**
- Drop nothing from the `integrity` attributes — browsers refuse to load without them
- `react@18.3.1` exact — no `react@18`
- No `type="module"` — UMD path only
- Multi-file Babel pages use `const terminalStyles = {...}` pattern; NEVER `const styles = {...}` (globals collide across Babel blocks, TECH-02)
- Share components between Babel blocks via `Object.assign(window, {Foo, Bar})` at the end of each file (TECH-03)

---

## 5. AI-slop-avoid gate (12-item checklist)

Every HTML emission passes this gate BEFORE save. Full list in [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) — this is the short version run as a grep:
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)

1. **No purple-blue gradient** on hero bg (TECH-19)
2. **No `border-left: 4px solid`** card accents (TECH-20)
3. **No AI-drawn SVG illustrations** (TECH-21) — gray placeholder box instead
4. **No emoji carpet** (🚀 ✨ 📊) in headings (TECH-22)
5. **No blanket glassmorphism** `backdrop-filter: blur(20px)` (TECH-23)
6. **No default-font trap** (Inter / Roboto / Arial / Fraunces / Poppins as primary body) (TECH-24)
7. **Max 3 weights** on one page (TECH-25)
8. **No alternating bands** white / pale-gray / white (TECH-26)
9. **No icon-per-feature** (3 features in a row, icon each) (TECH-27)
10. **No fake testimonials** ("Sarah J., CEO at TechCorp") (TECH-28)
11. **No `scrollIntoView`** — use manual offset + `window.scrollTo` (TECH-29)
12. **Content density** — every element earns its place (TECH-30)

Final grep before save:

```bash
grep -E "linear-gradient|border-radius.*border-left|Inter|Roboto|🚀|✨|scrollIntoView" <file>
```

---

## 6. ARIA / keyboard / a11y patterns

Rule priority: **User-Needs → Accessibility → Usability → Visual Hierarchy → Consistency** (TECH-41). A11y sits ABOVE visual in the trade-off stack.

- **Focus ring**: `:focus-visible { outline: 2px solid var(--primary); outline-offset: 2px; }` — never `outline: none` without replacement (TECH-44)
- **Reduced motion**: wrap animations in `@media (prefers-reduced-motion: no-preference)` (TECH-45)
- **Color contrast**: body text ≥ 4.5:1, UI elements ≥ 3:1 (TECH-46)
- **Tablist** for tabbed panels: `role="tablist"` / `role="tab"` / `role="tabpanel"` + arrow-key navigation
- **Alert**: `role="alert"` + `aria-live="polite"` (not assertive unless life-critical) (TECH-47)
- **Icon button**: every icon-only `<button>` gets `aria-label="<action>"` (TECH-43)
- **Tab order**: DOM order must match visual — no `tabindex > 0` (TECH-48)
- **Hit target**: min 44×44px for primary interactive; 28×28 OK for nav chrome (TECH-16)

---

## 7. CSS custom properties (Tweaks-compatible)

Tokens exposed at `:root` drive both the page and the Tweaks protocol:

```css
:root {
  --primary: #0066cc;
  --text: #0f172a;
  --bg: #ffffff;
  --surface: #f8fafc;
  --border: #e2e8f0;
  --radius: 8px;
  --font-size: 16px;
  --font-sans: ui-sans-serif, system-ui, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, monospace;
}
```

Tweaks edits: `document.documentElement.style.setProperty('--foo', value)` — no DOM reflow, no re-render (TECH-07).

---

## 8. Per-source breakdown of the technique catalog

| Src | Source material | TECH range | Focus |
|---|---|---|---|
| S1 | `skills/amw-design-principles/starter-components/*` (9 components, in-repo) | TECH-01 .. TECH-18 | Canonical chrome, Tweaks protocol, React pins, tokens, animations |
| S2 | `skills/amw-design-principles/ai-slop-avoid.md` (26 rules + density principle) | TECH-19 .. TECH-30 | Output-ban checklist (executed as final gate) |
| S3 | `SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/` | TECH-31 .. TECH-40 | Component patterns, industry-specific layouts, conversion-optimized structures |
| S4 | `SKILLS-TO-INTEGRATE/web-design/ux-designer/` + `rules/accessibility.md` | TECH-41 .. TECH-50 | A11y, WCAG, semantic HTML, focus order, ARIA |
| S5 | `SKILLS-TO-INTEGRATE/image-generation/create-infographics/SKILL.md` | TECH-51 .. TECH-60 | Dense editorial HTML, bold borders, section separators, table primacy |
| S6 | `SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md` | TECH-61 .. TECH-68 | Self-contained HTML+SVG, 13 diagram archetypes, no-build layout |
| S7 | `skills/amw-ascii-creator/references/techniques.md` (ASCII-parse source) | TECH-69 .. TECH-80 | ASCII-pattern recognition primitives (mirrors of ascii-creator authoring catalog) |
| S8 | `SKILLS-TO-INTEGRATE/diagrams-skills/ascii-diagrams-skill-main/references/` (CHI'24 classics) | TECH-81 .. TECH-90 | Classic `+-\|` HTML-table equivalents, UI-mockup sidebar grid → CSS grid |
| S9 | `bin/amw-ascii-parse.py` (in-repo tokenizer) | TECH-91 .. TECH-100 | find_boxes / find_arrows / classify → HTML-emission hooks |

Total: **100 techniques**, 9 sources.

---

## 9. Technique catalog

Format: `TECH-NN <name>: <description> | source: <path>:<section> | applies-to: <ASCII-pattern-or-HTML-concern>`

### S1 — design-principles starter-components (canonical chrome)

TECH-01 react-babel-pin: include `react@18.3.1` UMD + `react-dom@18.3.1` UMD + `@babel/standalone@7.29.0` with `integrity` hashes; never `react@18`, never `type="module"` | source: starter-components/react-babel-pins.md:7-11 | applies-to: any emitted HTML containing React
TECH-02 styles-object-prefix: `const terminalStyles = {...}`, never `const styles = {...}` (globals collide across Babel blocks) | source: starter-components/react-babel-pins.md:22-34 | applies-to: JSX-emitting pages with multiple Babel files
TECH-03 window-export-share: `Object.assign(window, {Terminal, Line, ...})` at end of a babel file to share components between `<script type="text/babel">` blocks | source: starter-components/react-babel-pins.md:38-48 | applies-to: multi-component React pages
TECH-04 tweaks-editmode-block: delimit runtime-tunable JSON in `/*EDITMODE-BEGIN*/{...}/*EDITMODE-END*/` with double-quoted keys AND string values (host parses as JSON) | source: starter-components/tweaks-block.html:52-57 | applies-to: every page that wants host-writable live config
TECH-05 tweaks-listener-before-announce: `window.addEventListener('message', ...)` MUST register BEFORE `postMessage({type:'__edit_mode_available'})` or the toggle silently fails | source: starter-components/tweaks-block.html:64-73 | applies-to: ALL tweaks-enabled HTML output
TECH-06 tweaks-partial-update: `postMessage({type:'__edit_mode_set_keys', edits:{[key]:value}})` carries ONE changed key — never the full config | source: starter-components/tweaks-block.html:102-111 | applies-to: tweaks round-trip back to host
TECH-07 css-var-token-root: `:root { --primary; --text; --bg; --radius; --font-size; }` — Tweaks edits `document.documentElement.style.setProperty('--foo', v)` | source: starter-components/tweaks-block.html:7-13 | applies-to: all tokenized chrome pages
TECH-08 browser-window-chrome: pre-built traffic-lights + addr-bar + tab-bar; `.viewport { background: var(--bg); padding: 48px; }` — slot content inside `.viewport` | source: starter-components/browser-window.html:19-113 | applies-to: laptop/desktop mockup wrappers
TECH-09 ios-frame-mobile-force: ios-frame.html forces 390×844 viewport — emit mobile-first layout inside | source: starter-components/ios-frame.html (referenced) | applies-to: mobile wireframe → HTML conversion
TECH-10 deck-stage-screen-label: `<section data-screen-label="01 Title">` 1-indexed label persists to localStorage; multi-screen deck navigator reads it | source: starter-components/deck-stage.html (referenced) | applies-to: multi-screen wireframes (sequence of frames in one file)
TECH-11 macos-window-two-col: sidebar + main-content split; use CSS grid `grid-template-columns: 260px 1fr` | source: starter-components/macos-window.html (referenced) | applies-to: desktop app wireframes with sidebar
TECH-12 animations-timeline-core: use `starter-components/animations.html` ~50-LOC timeline first; fall back to Popmotion for physics; NEVER Framer/GSAP | source: starter-components/animations.html (referenced) | applies-to: any scroll reveal / stagger / CTA pulse
TECH-13 keyboard-t-toggle-tweaks: `keydown 't'` toggles tweaks-panel for standalone preview | source: starter-components/tweaks-block.html:127-131 | applies-to: every tweaks-enabled page (user can preview without a host)
TECH-14 box-shadow-token-stack: layered `0 0 0 1px rgba + 0 30px 60px -20px rgba + 0 20px 40px -15px rgba` for depth (3-layer realistic shadow) | source: starter-components/browser-window.html:26-31 | applies-to: cards, hero, chrome elements
TECH-15 inline-svg-nav-button: 14×14 `viewBox="0 0 24 24"` stroke-width 2, `fill:none; stroke: currentColor` — inline per button, no icon library | source: starter-components/browser-window.html:127-140 | applies-to: back/forward/reload/share/menu, every glyph button
TECH-16 hit-target-min: desktop nav `width: 28px; height: 28px` OK for chrome; all primary interactive `min-height: 44px` (touch) | source: starter-components/browser-window.html:56-60 + CLAUDE.md dimensional-hard-limits | applies-to: every `<button>` outside chrome
TECH-17 border-radius-scale: 12px window, 8px cards, 6px small buttons — matches design-principles 8pt grid | source: starter-components/browser-window.html:25,101 | applies-to: every rounded element
TECH-18 font-stack-ui-sans: `font-family: ui-sans-serif, system-ui` default fallback; replace when design-extract tokens override | source: starter-components/browser-window.html:19 | applies-to: body font base

### S2 — ai-slop-avoid (output-ban gate)

TECH-19 no-purple-gradient: reject `linear-gradient(135deg, #667eea, #764ba2)` on hero bg | source: ai-slop-avoid.md:12-14 | applies-to: every hero / full-width section bg emitted
TECH-20 no-left-accent-card: reject `border-left: 4px solid <color>` on cards; prefer background shift / hairline rule | source: ai-slop-avoid.md:17-20 | applies-to: every card / alert / callout emitted
TECH-21 no-ai-svg-illustrations: refuse inline SVG painting people/landscapes; use sized gray placeholder | source: ai-slop-avoid.md:23-26 | applies-to: hero / feature / testimonial illustrations
TECH-22 no-emoji-carpet: strip `🚀 ✨ 📊` from headings/icons; keep only if brand explicitly uses | source: ai-slop-avoid.md:29-32 | applies-to: headings, feature icons, CTAs
TECH-23 no-glassmorphism-default: reject blanket `backdrop-filter: blur(20px) + translucent white` | source: ai-slop-avoid.md:35-38 | applies-to: cards, nav bar, modal overlays
TECH-24 no-inter-roboto-default: reject Inter/Roboto/Arial/system-ui/Fraunces/Poppins as primary body font when no token supplied; pick a typeface with identity | source: ai-slop-avoid.md:52-58 | applies-to: body and display fonts
TECH-25 no-weight-soup: max 3 weights on one page (typically Regular + Bold, Medium optional) | source: ai-slop-avoid.md:60-63 | applies-to: type scale CSS
TECH-26 no-alternating-bands: reject mechanical white / pale-gray / white bg alternation | source: ai-slop-avoid.md:81-85 | applies-to: full-width section backgrounds
TECH-27 no-icon-per-feature: reject "3 features in a row, icon each"; text-only unless icon carries real differentiation | source: ai-slop-avoid.md:88-91 | applies-to: feature rows, value props, capability grids
TECH-28 no-fake-testimonials: reject "Sarah J., CEO at TechCorp" + stars; use whitespace or `[customer testimonial TK]` | source: ai-slop-avoid.md:110-113 | applies-to: social proof sections
TECH-29 no-scrollIntoView: BAN `element.scrollIntoView({behavior:'smooth'})`; use `window.scrollTo({top, behavior:'smooth'})` with manual offset | source: ai-slop-avoid.md:182-185 | applies-to: every scroll-anchor / nav click / CTA smooth-scroll
TECH-30 content-density-earn: every element must answer "what task does this perform?"; delete if decorative | source: ai-slop-avoid.md:205-217 | applies-to: final pass before save

### S3 — ui-ux-pro-max-skill (industry patterns)

TECH-31 landing-pattern-per-industry: select from 24 landing-page patterns matched to industry (luxury spa ≠ SaaS ≠ fintech) — do NOT default to "hero → 3 columns → CTA → footer" | source: ui-ux-pro-max-skill/SKILL.md:72 | applies-to: landing-page archetype selection
TECH-32 palette-per-industry: match color palette to industry context from 161-palette library (not hardcoded primary) | source: ui-ux-pro-max-skill/SKILL.md:72 | applies-to: token selection when user has no brand
TECH-33 font-pairing-57: pair display + body from curated 57-combo list; preserve Google Fonts URL when chosen | source: ui-ux-pro-max-skill/SKILL.md:72 | applies-to: typography layer when design-extract missed
TECH-34 pre-delivery-checklist: A11y + UX gates run BEFORE save (contrast, focus, hit-target, semantic) | source: ui-ux-pro-max-skill/SKILL.md:82 | applies-to: conversion pipeline step 8
TECH-35 anti-pattern-per-industry: each industry has its own anti-pattern list (luxury ≠ fintech; follow both the global slop list and the per-industry one) | source: ui-ux-pro-max-skill/SKILL.md:82 | applies-to: slop-check gate
TECH-36 style-keyword-declaration: declare visual language at top of the emitted file as a comment (Glassmorphism? Brutalism? Editorial? Swiss?) for future iteration | source: ui-ux-pro-max-skill/SKILL.md:79 | applies-to: file-header comment in emitted HTML
TECH-37 primary-cta-distinct: ONE primary CTA color per screen — secondary CTAs use outline/ghost variants | source: ui-ux-pro-max-skill/SKILL.md + design-principles | applies-to: button emission from `[ Label ]` pattern
TECH-38 hero-density-editorial: hero carries one big line + short supporting sentence; no filler paragraph | source: ui-ux-pro-max-skill/SKILL.md:82 + ai-slop-avoid.md:125 | applies-to: hero region emission
TECH-39 stack-multi-framework: same skill emits React, NextJS, Astro, Vue, raw HTML — parse tokens once, emit via template literal | source: ui-ux-pro-max-skill/SKILL.md:99-101 | applies-to: stack parameter handling
TECH-40 cta-placement-pattern: follows the industry pattern (above-the-fold for SaaS, bottom-of-page for luxury) | source: ui-ux-pro-max-skill/SKILL.md:76 | applies-to: CTA placement from ASCII position

### S4 — ux-designer + accessibility

TECH-41 priority-order-a11y: rule priority User-Needs → **Accessibility** → Usability → Visual Hierarchy → Consistency (A11y is above visual) | source: ux-designer/SKILL.md:39 | applies-to: trade-off resolution in emission
TECH-42 semantic-nav-header-main: use `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>` — NOT `<div>` with aria-role override | source: ux-designer/rules/accessibility.md | applies-to: frame → semantic skeleton
TECH-43 aria-label-on-icon-button: every icon button gets `aria-label="<action>"` (e.g. "Back", "Close", "Next") | source: starter-components/browser-window.html:128 + ux-designer | applies-to: icon-only buttons from ASCII `[ ▾ ]` / `[ ✕ ]`
TECH-44 focus-ring-visible: `:focus-visible { outline: 2px solid var(--primary); outline-offset: 2px; }` — never `outline: none` without replacement | source: ux-designer/rules/accessibility.md | applies-to: every interactive element
TECH-45 reduced-motion-query: wrap animations in `@media (prefers-reduced-motion: no-preference)` | source: ux-designer/rules/accessibility.md + ai-slop-avoid.md:144 | applies-to: any CSS animation / transform
TECH-46 color-contrast-4-5-1: body text ≥ 4.5:1 contrast, UI elements ≥ 3:1 — verify with oklch chroma bounds | source: ux-designer/rules/accessibility.md + design-principles/color-system.md | applies-to: text on bg for every surface emitted
TECH-47 role-alert-live-polite: alert cards get `role="alert" aria-live="polite"` (not "assertive" unless life-critical) | source: ux-designer/rules/accessibility.md | applies-to: `[!]`-prefixed boxes in ASCII → alert card HTML
TECH-48 keyboard-tab-order-dom: DOM order must match visual order (no `tabindex > 0`) — rely on document flow | source: ux-designer/rules/accessibility.md | applies-to: CSS-grid/flex reordering hazard check
TECH-49 th-scope-row-col: every `<th>` gets `scope="col"` or `scope="row"` | source: ux-designer/rules/accessibility.md | applies-to: pipe-table → `<table>` conversion
TECH-50 label-input-for: every `<input>` has an associated `<label for="id">` (or `aria-label`) | source: ux-designer/rules/accessibility.md | applies-to: `[__ placeholder __]` → `<input>` conversion

### S5 — create-infographics (editorial density)

TECH-51 density-target-8-to-15: 8–15 content blocks per 1080×1440 canvas — fewer than 6 is "too sparse" | source: create-infographics/SKILL.md:99 | applies-to: long-form vertical wireframes
TECH-52 bold-visible-borders: borders ≥ `rgba(primary, 0.3)`; `rgba(255,255,255,0.08)` is ghost-border — BAN | source: create-infographics/SKILL.md:44 | applies-to: card/section borders
TECH-53 section-separator-band: full-width solid-dark strip containing the section label in all-caps — not just a text header | source: create-infographics/SKILL.md:69 | applies-to: section dividers between major blocks
TECH-54 table-primacy: any comparison/spec/tier/rate/requirement goes in `<table>` not cards | source: create-infographics/SKILL.md:43 | applies-to: pipe-table pattern detection
TECH-55 variety-mandatory: 3+ same-type sections (e.g. all "feature cards") forbidden; replace at least one with table/flow/bullets | source: create-infographics/SKILL.md:42 | applies-to: section emission when wireframe repeats
TECH-56 arrows-connect-sections: use arrows/flow-lines between major sections to show how A's output feeds B | source: create-infographics/SKILL.md:41 | applies-to: multi-step wireframes where flow is implicit
TECH-57 bullets-not-paragraphs: body text inside components is bullets one-line-per-fact — only hero may carry a 1-2-sentence intro | source: create-infographics/SKILL.md:40 | applies-to: card body emission from ASCII lines
TECH-58 header-all-caps-bold: section headers ALWAYS all-caps when editorial (dense-reference context); never all-caps for generic SaaS landing | source: create-infographics/SKILL.md:64 | applies-to: header case decision per wireframe type
TECH-59 outer-canvas-border: 1-2px solid accent-colored `body { outline: 2px solid var(--primary); }` — signature move | source: create-infographics/SKILL.md:86 | applies-to: poster/dashboard-style pages only
TECH-60 neon-glow-on-accent: `box-shadow: 0 0 20px rgba(primary, 0.4)` on accent elements — 57% of editorial pieces | source: create-infographics/SKILL.md:84 | applies-to: CTA / badge / key-metric emission

### S6 — diagram-design-editorial (self-contained HTML+SVG)

TECH-61 no-build-no-external: emit single-file HTML with inline CSS+SVG, no `<link>` to CDN CSS, no npm dependency | source: diagram-design-editorial/SKILL.md:18 | applies-to: every ASCII→HTML output (single-file rule)
TECH-62 no-mermaid-no-shadow: reject Mermaid renders, reject shadow-heavy styling — clean line-art aesthetic | source: diagram-design-editorial/SKILL.md:18 | applies-to: when wireframe has a diagram region
TECH-63 brand-matched-60s: scrape user's site in 60s to derive tokens (equivalent to `/amw-extract-style`) | source: diagram-design-editorial/SKILL.md:19 | applies-to: token-acquisition step when user names a URL
TECH-64 13-archetype-selection: Architecture, Flowchart, Sequence, StateMachine, ER, Timeline, Swimlane, Quadrant, Nested, Tree, Layer-stack, Venn, Pyramid — pick the one the wireframe implies | source: diagram-design-editorial/SKILL.md:45-60 | applies-to: wireframe regions that draw a diagram
TECH-65 reader-value-test: "would a reader learn more from this than a well-written paragraph?" — if no, delete | source: diagram-design-editorial/SKILL.md:63 | applies-to: decorative diagram removal
TECH-66 inline-svg-for-sparkline: sparkline/chart regions render as inline `<svg>` polyline, not `<canvas>`, not chart.js | source: diagram-design-editorial/SKILL.md (pattern) | applies-to: KPI-card sparkline wireframe regions
TECH-67 monospace-for-code-blocks: any `<pre><code>` block uses `ui-monospace, SFMono-Regular, Menlo, monospace` | source: starter-components/tweaks-block.html:22 + diagram-design-editorial | applies-to: terminal/code-preview wireframes
TECH-68 minimal-color-palette: 2–3 colors per diagram (accent + neutral + 1 semantic max) | source: diagram-design-editorial/SKILL.md + ai-slop-avoid.md:170-172 | applies-to: diagram-region coloring

### S7 — ascii-creator mirror (pattern recognition)

TECH-69 rounded-frame-to-container: `╭─╮ / │..│ / ╰─╯` outer → `<div class="container" style="max-width:1200px; margin: 0 auto">` | source: ascii-creator/references/techniques.md:TECH-01 | applies-to: outer frame detection
TECH-70 3-line-button-to-button: `╭──╮ / │ label │ / ╰──╯` → `<button type="button">label</button>` with min-height 44px | source: ascii-creator/references/techniques.md:TECH-02 | applies-to: every CTA button
TECH-71 separator-row-to-hr: internal `│ ──── │` → visual separator (bottom-border on title, not `<hr>` inside card) | source: ascii-creator/references/techniques.md:TECH-04 | applies-to: titled-card headers
TECH-72 T-junction-to-grid: `┬/┴` columns → CSS `grid-template-columns: repeat(N, 1fr); gap: 1rem;` | source: ascii-creator/references/techniques.md:TECH-05 | applies-to: multi-column dashboard rows
TECH-73 three-peer-row-to-grid-3: 3 same-width cards side-by-side 3 spaces apart → `grid-template-columns: repeat(3, 1fr)` | source: ascii-creator/references/techniques.md:TECH-14 | applies-to: KPI triplet, feature triplet
TECH-74 dropdown-glyph-to-select: `▾` inside button frame → `<select>` OR `<button aria-haspopup="listbox" aria-expanded="false">` | source: ascii-creator/references/techniques.md + ascii-parse.py:classify | applies-to: "you ▾" / "Week ▾" patterns
TECH-75 bracket-marker-alert: `[!]` / `[*]` inline marker → `role="alert"` card with semantic severity icon | source: ascii-creator/references/techniques.md:TECH-38 | applies-to: alert cards with `[!]` prefix
TECH-76 owner-tag-parens: `(@sre-oncall)` → `<span class="owner" aria-label="Assigned to SRE on-call">@sre-oncall</span>` | source: ascii-creator/references/techniques.md:TECH-39 | applies-to: attribution labels
TECH-77 metric-delta-sign: `+12% DAU` / `-4% churn` sign-prefixed → `<span class="delta delta-positive">` or `delta-negative` | source: ascii-creator/references/techniques.md:TECH-40 | applies-to: KPI delta rows
TECH-78 sparkline-axis-to-svg: `│ ────────── │` axis-like row → inline `<svg>` polyline (placeholder when no real data) | source: ascii-creator/references/techniques.md | applies-to: KPI card axis row
TECH-79 numbered-stage-to-ol: `1. ALERT` / `2. TRIAGE` → `<ol>` with `<li>` — never `<ul>` | source: ascii-creator/references/techniques.md:TECH-11 | applies-to: numbered stage lists
TECH-80 inline-route-arrow-list: `→ check wal sender queue` → `<li>` with `::before { content: "→ "; }` | source: ascii-creator/references/techniques.md:TECH-12 | applies-to: sub-action lists inside alert cards

### S8 — CHI'24 ASCII classics (mockup → HTML skeleton)

TECH-81 ui-mockup-sidebar-grid: `+---+------+` sidebar + main → `grid-template-columns: 260px 1fr` | source: graphs-annotations.md:77-90 | applies-to: dashboard wireframes with nav sidebar
TECH-82 pipe-table-to-table: `Path | Req | p99` with `-----|-----|----` rule below → `<table><thead><th scope="col">` | source: sequences-tables.md:31-36 | applies-to: data tables inside a frame
TECH-83 compact-status-key-to-dl: 2-col enum `Status | Meaning` → `<dl><dt><dd>` definition list | source: sequences-tables.md:40-47 | applies-to: legend / status key / glossary
TECH-84 sequence-lifeline-to-list: `|` columns + `-->` messages → `<ol class="sequence"><li class="msg" data-from="A" data-to="B">` | source: sequences-tables.md:9-16 | applies-to: OAuth / request-response wireframes
TECH-85 tree-branch-to-nested-ul: `+-- src/` / `|   +-- utils/` → nested `<ul>` (tree semantics) | source: trees.md:6-23 | applies-to: file trees, nav trees
TECH-86 decision-diamond-to-form: `yes|no` diamond → two `<button type="submit" name="choice" value="yes|no">` or `<fieldset><legend>` | source: flowcharts.md:15-20 | applies-to: decision-gate wireframes
TECH-87 timeline-tick-to-ordered-list: `t=0  t=100ms` tick row → `<ol class="timeline"><li data-t="0">` | source: sequences-tables.md:19-23 | applies-to: roadmap / release-timeline regions
TECH-88 classic-plus-ascii-passthrough: `+---+|   |+---+` present (user chose classic mode) → emit `<pre><code>` preserving exact chars | source: flowcharts.md:7-9 + ascii-parse.py:detect_format | applies-to: when wireframe uses classic mode (no Unicode)
TECH-89 namespace-container-to-fieldset: outer `+-- NS0 namespace --+` → `<fieldset><legend>NS0 namespace</legend>` | source: network-topology.md:67-72 | applies-to: grouped regions with a border-label
TECH-90 stack-top-bottom-to-semantic: `TOP --> +-----+` → `<aside data-stack-end="top">` with order CSS | source: data-structures.md:28-34 | applies-to: rare — stack/queue wireframes

### S9 — ascii-parse.py (in-repo tokenizer hooks)

TECH-91 find_boxes-to-bounding: `find_boxes()` returns `{x, y, w, h, text}` — this is the component's bounding box in char-cells; convert 1 char ≈ 12px width, 1 row ≈ 20px height (rough-scale, actual tokens override) | source: bin/amw-ascii-parse.py:131 (find_boxes) | applies-to: box → HTML region mapping
TECH-92 find_arrows-to-flow: `find_arrows()` returns `{row, col, symbol, direction}` — emit inline SVG `<polyline>` overlay OR `::after` arrow glyph | source: bin/amw-ascii-parse.py:200 (find_arrows) | applies-to: arrow → visual flow in final HTML
TECH-93 classify-to-role: `classify()` returns token class per char (box-corner, horiz-rule, vert-rule, arrow, text) — drives component-type decision | source: bin/amw-ascii-parse.py:62 (classify) | applies-to: per-char parse pass
TECH-94 detect_format-choose-mode: `unicode` vs `ascii` vs `mixed` → Unicode mode emits CSS-grid HTML; ASCII-only mode emits `<pre>`-preserved classic ASCII inside a light shell | source: bin/amw-ascii-parse.py:87 (detect_format) | applies-to: pipeline step 2 format branch
TECH-95 find_wireframe_components-to-fields: `find_wireframe_components()` extracts `[ Text ]` / `[ ]` / `[x]` / `[__ placeholder __]` / `(o)` / `( )` / `▾` / image-tokens | source: bin/amw-ascii-parse.py:257 (find_wireframe_components) | applies-to: form / button / radio / checkbox emission
TECH-96 MAX_GRID_DIM-guard: `to_grid()` caps at `MAX_GRID_DIM` — oversized wireframes get truncated with a warning; never silently fail | source: bin/amw-ascii-parse.py:106 (to_grid) | applies-to: oversize-input failure mode
TECH-97 layout-json-intermediate: pipeline emits `/tmp/amw-ascii-html-<slug>-layout.json` from parser — HTML templater reads this, never the raw ASCII | source: ascii-to-html/SKILL.md:47 (existing) | applies-to: stage separation (parse vs render)
TECH-98 safe-arrowhead-glyph-preserve: `▾ ▴ ▸ ◂` (1-col) preserved in emitted HTML text nodes (do NOT replace with `▼ ▲`) | source: ascii-creator/references/techniques.md:TECH-07 + ascii-parse.py:find_arrows | applies-to: dropdown glyph / arrow-in-text rendering
TECH-99 validate-alignment-pre-parse: run `bin/amw-validate-ascii.py` BEFORE parse; hard-stop on FAIL (misaligned ASCII → broken HTML grid) | source: ascii-validator/SKILL.md + bin/amw-validate-ascii.py | applies-to: pipeline step 1 gate
TECH-100 empty-line-in-box-to-padding: `│                 │` all-space row → extra `padding-top` on the next block, not `<br>`, not empty `<p>` | source: ascii-creator/references/techniques.md:TECH-13 | applies-to: breathing-room rows inside cards

---

## 10. Migration note (2026-04-22)

This file is the **canonical home** for the HTML technique catalog. It supersedes:
- `skills/amw-ascii-to-html/references/techniques.md` (100 techniques, moved here in full)

The original file is preserved at `docs_dev/backups/<timestamp>-phase0-refs/` and now carries a 3-line pointer referencing this file. Future edits to HTML techniques go here, not in per-skill references.
