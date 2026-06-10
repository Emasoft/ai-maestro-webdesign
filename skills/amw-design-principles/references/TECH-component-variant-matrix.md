# TECH — Component Variant Matrix

## Table of Contents

- [What is a variant matrix?](#what-is-a-variant-matrix)
- [Tokens](#tokens)
- [Wireframe-phase token swap (T-121)](#wireframe-phase-token-swap-t-121)
- [Authoring the matrix](#authoring-the-matrix)
- [Single-file multi-variant toggle output (T-120)](#single-file-multi-variant-toggle-output-t-120)
- Implementation spec sheet (T-122) — purpose, component tree, interaction state table, token swatches, responsive, edge cases
- [Style Dictionary integration](#style-dictionary-integration)
- [Figma Tokens (Tokens Studio) integration](#figma-tokens-tokens-studio-integration)
- [Cross-route component dedup (T-125)](#cross-route-component-dedup-t-125)
- [Vertical-specific mandatory elements (T-127)](#vertical-specific-mandatory-elements-t-127)
- [LLMO deliverable bundle (T-128)](#llmo-deliverable-bundle-t-128)
- [Agent-accessibility attributes (T-129)](#agent-accessibility-attributes-t-129)
- [Agentic UI affordances (T-130, EU EAA-required June 2025)](#agentic-ui-affordances-t-130-eu-eaa-required-june-2025)
- [/tmp standalone preview checkpoint (T-117)](#tmp-standalone-preview-checkpoint-t-117)
- [Component sourcing hierarchy (T-116)](#component-sourcing-hierarchy-t-116)
- [Breaks-if](#breaks-if)
- [Component examples](#component-examples)
- [Cross-references](#cross-references)

How to enumerate a component's variant axes, constrain orphan combinations, and feed the matrix into design-token export tools (Style Dictionary, Figma Tokens, the plugin's own `bin/amw-design-md-emit-companions.py`). Owned by `amw-component-library-architect-agent`; consumed by `amw-wireframe-builder-agent` for variant rendering and by `amw-form-designer-agent` for form-control variants.

Provenance: composed from `atelier` single-file multi-variant toggle (T-120, MIT direct-port), `design-with-claude-code` SPEC_GUIDE (T-122, MIT direct-port), wireframe-token-swap (T-121, MIT direct-port), per-project token-scale generation (T-126, clean-room), and clean-room writeups of T-125 (cross-route component dedup), T-127 (vertical-specific mandatory elements), T-128 (LLMO bundle), T-129 (data-ai-* attributes), T-130 (Agentic UI affordances).

---

## What is a variant matrix?

A component has N orthogonal axes. Each axis has a fixed enum of values. The full variant space is the cartesian product. Most combinations are valid; some are orphans (forbidden). The matrix is the explicit table of which combinations the design system supports.

The four canonical axes:

| Axis | Description | Example values |
|---|---|---|
| Size | Visual density / physical scale | `xs`, `sm`, `md`, `lg`, `xl` |
| State | Interaction state | `default`, `hover`, `active`, `focus`, `disabled`, `loading`, `error`, `success` |
| Intent | Semantic role / brand emphasis | `neutral`, `primary`, `secondary`, `danger`, `success`, `warning` |
| Density | Information packing per unit area | `compact`, `default`, `comfortable` |

A button might have `5 sizes × 8 states × 6 intents × 3 densities = 720 combinations`. Few of those are useful. The matrix is the document that says which subset ships.

---

## Tokens

```css
:root {
  /* Density token — the multiplier feeding all size-derived tokens */
  --density-compact: 0.8;
  --density-default: 1;
  --density-comfortable: 1.2;

  /* Size base — paired with the spacing scale from spacing-rhythm.md */
  --size-base: 16px;
  --size-xs: calc(var(--size-base) * 0.75);   /* 12 */
  --size-sm: calc(var(--size-base) * 0.875);  /* 14 */
  --size-md: var(--size-base);                /* 16 */
  --size-lg: calc(var(--size-base) * 1.125);  /* 18 */
  --size-xl: calc(var(--size-base) * 1.5);    /* 24 */

  /* Hit-target floor — the 44 px WCAG-AAA tap target survives at any size below this */
  --hit-target-min: 44px;

  /* Per-project token-scale (T-126) — derive secondary scales from a single base */
  --spacing-unit: 4px;
  --space-1: calc(var(--spacing-unit) * 1);   /* 4 */
  --space-2: calc(var(--spacing-unit) * 2);   /* 8 */
  --space-3: calc(var(--spacing-unit) * 3);   /* 12 */
  --space-4: calc(var(--spacing-unit) * 4);   /* 16 */
  --space-6: calc(var(--spacing-unit) * 6);   /* 24 */
  --space-8: calc(var(--spacing-unit) * 8);   /* 32 */
  --space-12: calc(var(--spacing-unit) * 12); /* 48 */
  --space-16: calc(var(--spacing-unit) * 16); /* 64 */
  --space-24: calc(var(--spacing-unit) * 24); /* 96 */
  --space-32: calc(var(--spacing-unit) * 32); /* 128 */

  --font-size-base: 16px;
  --font-size-sm: calc(var(--font-size-base) * 0.875);   /* 14 */
  --font-size-md: var(--font-size-base);                  /* 16 */
  --font-size-lg: calc(var(--font-size-base) * 1.125);    /* 18 */
  --font-size-xl: calc(var(--font-size-base) * 1.25);     /* 20 */
  --font-size-2xl: calc(var(--font-size-base) * 1.5);     /* 24 */
  --font-size-3xl: calc(var(--font-size-base) * 1.875);   /* 30 */
  --font-size-4xl: calc(var(--font-size-base) * 2.25);    /* 36 */
  --font-size-5xl: calc(var(--font-size-base) * 3);       /* 48 */
  --font-size-6xl: calc(var(--font-size-base) * 3.75);    /* 60 */

  --radius-base: 6px;
  --radius-sm: calc(var(--radius-base) * 0.5);  /* 3 */
  --radius-md: var(--radius-base);              /* 6 */
  --radius-lg: calc(var(--radius-base) * 2);    /* 12 */

  /* Transition tokens (T-126) — 3 named durations */
  --transition-fast: 150ms cubic-bezier(0.16, 1, 0.3, 1);
  --transition-base: 300ms cubic-bezier(0.65, 0, 0.35, 1);
  --transition-slow: 600ms cubic-bezier(0.16, 1, 0.3, 1);
}
```

**Hard invariants:**
1. One base token per scale (`--spacing-unit`, `--font-size-base`, `--radius-base`). Every derived token is a `calc()` of the base. Changing the base re-scales the entire system in one edit.
2. No magic numbers in component CSS. Every value reads from a token.
3. Hit targets ≥ 44 × 44 px on interactive elements (WCAG 2.5.5 AAA, recommended baseline). The `xs` size variant of a button still satisfies this — small text gets bigger padding to keep the tap target.

---

## Wireframe-phase token swap (T-121)

Optional intermediate: during the wireframe phase, swap brand tokens for a grayscale set so reviewers focus on layout, not color.

```css
:root {
  /* Brand tokens — applied at approval */
  --color-bg: oklch(99% 0 0);
  --color-surface: oklch(96% 0.01 250);
  --color-border: oklch(85% 0.02 250);
  --color-text: oklch(15% 0.02 250);
  --color-accent: oklch(58% 0.18 252);
}

[data-wireframe="true"] {
  /* Grayscale override — same lightness anchors, chroma stripped */
  --wf-bg: oklch(99% 0 0);
  --wf-surface: oklch(96% 0 0);
  --wf-border: oklch(85% 0 0);
  --wf-text: oklch(15% 0 0);
  --wf-accent: oklch(58% 0 0);

  --color-bg: var(--wf-bg);
  --color-surface: var(--wf-surface);
  --color-border: var(--wf-border);
  --color-text: var(--wf-text);
  --color-accent: var(--wf-accent);
}
```

Approval flow: `<html>` carries `data-wireframe="true"` during review. Removing the attribute is a one-line swap to the brand palette. No component CSS changes between wireframe and final.

---

## Authoring the matrix

The matrix lives in a single source-of-truth file: `design-tokens/variants.json` (canonical) or the `variants:` block of DESIGN.md (when DESIGN.md is the single source).

Skeleton:

```json
{
  "component": "Button",
  "axes": {
    "size": { "values": ["sm", "md", "lg"], "default": "md" },
    "intent": { "values": ["primary", "secondary", "danger", "ghost"], "default": "primary" },
    "state": { "values": ["default", "hover", "active", "focus", "disabled", "loading"], "default": "default" }
  },
  "supported_combinations": "all_except_orphans",
  "orphans": [
    { "axes": { "intent": "ghost", "state": "loading" }, "reason": "Ghost buttons have no visible background — the loading spinner has no container to anchor in" },
    { "axes": { "intent": "danger", "size": "sm" }, "reason": "Danger actions need physical prominence; sm size undermines the urgency signal" }
  ],
  "per_combination_overrides": [
    { "axes": { "intent": "primary", "state": "disabled" }, "tokens": { "background": "var(--color-muted)", "color": "var(--color-text-muted)" } }
  ]
}
```

Constraint rules:
1. **No orphan combinations ship.** The component code must refuse to render an orphan combo (throw at dev-time, silently fallback to nearest valid combo at runtime — pick one per project policy).
2. **Every axis has a documented default.** `<Button>` with no props gets the matrix-defined defaults.
3. **Per-combination overrides are explicit.** The disabled-primary combo deserves its own token mapping, not a CSS `:disabled` selector that silently overrides the primary token.

---

## Single-file multi-variant toggle output (T-120)

When delivering a variant-rich component to a reviewer, ship a single HTML file that renders every variant simultaneously with a toolbar to filter by axis. CSS custom properties + `data-variant` attribute carry the toggle state; no JS framework required.

Skeleton:

```html
<header class="vm-toolbar">
  <fieldset>
    <legend>Size</legend>
    <label><input type="checkbox" name="size" value="sm" checked> sm</label>
    <label><input type="checkbox" name="size" value="md" checked> md</label>
    <label><input type="checkbox" name="size" value="lg" checked> lg</label>
  </fieldset>
  <fieldset>
    <legend>Intent</legend>
    <label><input type="checkbox" name="intent" value="primary" checked> primary</label>
    <label><input type="checkbox" name="intent" value="secondary" checked> secondary</label>
    <label><input type="checkbox" name="intent" value="danger" checked> danger</label>
  </fieldset>
</header>
<main class="vm-grid" data-show-size="sm md lg" data-show-intent="primary secondary danger">
  <button data-size="sm" data-intent="primary">sm primary</button>
  <button data-size="sm" data-intent="secondary">sm secondary</button>
  <!-- ... full grid ... -->
</main>
<script>
  document.querySelectorAll('.vm-toolbar input').forEach(box => {
    box.addEventListener('change', () => {
      const axes = ['size', 'intent'];
      const grid = document.querySelector('.vm-grid');
      axes.forEach(axis => {
        const allowed = [...document.querySelectorAll(`input[name="${axis}"]:checked`)].map(b => b.value);
        grid.dataset[`show${axis[0].toUpperCase() + axis.slice(1)}`] = allowed.join(' ');
      });
    });
  });
</script>
<style>
  .vm-grid > * { display: none; }
  .vm-grid[data-show-size~="sm"] > [data-size="sm"]:where([data-intent]) { display: revert; }
  /* ... etc — generate one rule per axis × value via the build script ... */
</style>
```

Query-parameter persistence: extend the toolbar to write the active filter set into `?size=sm,md&intent=primary` so URLs are shareable to specific variant subsets. The agent's spec sheet (T-122) below references the exact URL form.

Compare(N) drawer pattern: a side panel pinning N variants side-by-side, each labeled with its axis values. Useful when a reviewer wants to compare `sm primary` vs `md primary` vs `lg primary` and lock the visual diff in their attention.

---

## Implementation spec sheet (T-122)

After variant matrix approval, emit a machine-readable spec the implementer consumes. Structure:

1. **Purpose / user story** — what does the component do, who uses it, why.
2. **Component tree** — inline-rendered tree of the component's structural composition.
3. **Interaction state table** — element × trigger × change × duration. Every interactive subelement gets a row.
4. **Token swatches** — every token the component reads, with its current resolved value.
5. **Responsive behavior per breakpoint** — what changes at sm / md / lg / xl viewport widths.
6. **Edge cases** — error / empty / loading / overflow states with explicit visual specs.

Skeleton (Markdown):

```markdown
# Component: Button

## 1. Purpose
Primary CTA for confirming a user action. Used in forms, modals, and content sections.
User story: "As a customer, I want a clear visible action to submit my order."

## 2. Component tree
- Button (root, `<button>` or `<a>` based on `as` prop)
  - LeadingIcon? (`<svg>`, decorative `aria-hidden`)
  - Label (`<span>`, required)
  - LoadingSpinner? (replaces Label when state=loading)
  - TrailingIcon? (`<svg>`, decorative `aria-hidden`)

## 3. Interaction state table
| Element | Trigger | Change | Duration |
|---|---|---|---|
| Root | :hover | translateY(-2px), shadow lift | --transition-fast |
| Root | :active | scale(0.97) | 100ms |
| Root | :focus-visible | outline appears | 0ms |
| Root | state=loading | label hidden, spinner shown | --transition-base |
| Root | state=success | success-pulse animation | --transition-slow |

## 4. Token swatches
- `--btn-bg-primary` = oklch(58% 0.18 252)
- `--btn-bg-primary-hover` = oklch(52% 0.20 252)
- `--btn-text-primary` = oklch(99% 0 0)
- `--btn-padding-md` = var(--space-3) var(--space-6)
- ... (one row per token the component reads)

## 5. Responsive
- sm viewport (< 640): button stretches to 100% width inside its container
- md viewport (640+): button is auto-width, content-fitted
- lg viewport (1024+): unchanged from md

## 6. Edge cases
- Empty label: rejected at the type level — the Label child is required
- Overflow: long labels get `text-overflow: ellipsis` + title attribute mirroring the label
- Loading > 5 seconds: button shows secondary "This is taking longer than usual" copy below
- Error from server: button reverts to default state; error toast surfaces outside the button
```

This spec is consumed by implementers in any framework. The token names match the JSON matrix; the component-tree matches the framework's component model.

---

## Style Dictionary integration

[Style Dictionary](https://styledictionary.com/) (Apache 2.0) consumes the token JSON and emits per-platform output (CSS variables, Sass, JS objects, iOS plist, Android XML).

Source layout:

```
design-tokens/
├── tokens/
│   ├── color.json
│   ├── size.json
│   ├── space.json
│   ├── radius.json
│   ├── motion.json
│   └── variants.json
├── config.js
└── build.sh
```

Each token file uses Style Dictionary's reference syntax:

```json
{
  "size": {
    "base": { "value": "16px" },
    "sm": { "value": "{size.base.value}", "transforms": ["multiply-0.875"] },
    "lg": { "value": "{size.base.value}", "transforms": ["multiply-1.125"] }
  }
}
```

`build.sh` runs `style-dictionary build` which emits `build/css/variables.css`, `build/js/tokens.js`, `build/scss/_variables.scss`. The plugin's `bin/amw-design-md-emit-companions.py` is the equivalent for DESIGN.md → tokens.css + tokens.json; for projects that want native Style Dictionary integration, use the upstream tool directly.

---

## Figma Tokens (Tokens Studio) integration

[Tokens Studio for Figma](https://tokens.studio/) (free tier + paid sync, MIT plugin) consumes JSON in the W3C Design Tokens Community Group format. The schema is similar but the `$value` / `$type` keys are mandatory:

```json
{
  "color": {
    "primary": {
      "$value": "oklch(58% 0.18 252)",
      "$type": "color"
    }
  },
  "size": {
    "base": { "$value": "16px", "$type": "dimension" },
    "sm": { "$value": "14px", "$type": "dimension" }
  }
}
```

Round-trip flow:
1. Designer edits tokens in Figma via Tokens Studio.
2. Tokens Studio syncs to a GitHub repo on save.
3. Style Dictionary in the repo's CI reads the synced JSON and emits per-platform CSS / JS / iOS / Android.
4. Developers pull the emitted files into the application.

The variant matrix lives outside Tokens Studio (it is structural, not a token). Tokens Studio holds the leaf values; the matrix holds the combinatorial space.

---

## Cross-route component dedup (T-125)

When generating multi-route projects, prevent component proliferation by recording every produced component in a manifest.

```json
// .planning/used-components.json
{
  "components": [
    { "name": "Button", "props": ["size", "intent"], "first_route": "/", "reused_in": ["/pricing", "/contact"] },
    { "name": "CardProduct", "props": ["image", "title", "price"], "first_route": "/shop", "reused_in": ["/shop/category"] }
  ]
}
```

Decision matrix when a new route needs a component:
1. Read `.planning/used-components.json`.
2. Search for a structurally-matching entry. If found, reuse — instantiate the existing component with new props.
3. If a match exists but props differ slightly, extend the existing component (add a new prop), do not create a sibling.
4. Only create a new component when no structural match exists.

This is the agent-level equivalent of DRY for design systems. The R3 build step appends the new component to the manifest; the next route generation reads it before authoring.

---

## Vertical-specific mandatory elements (T-127)

Different industry verticals require specific structural elements. The matrix carries a `vertical_requirements` block:

```json
{
  "verticals": {
    "restaurant": ["maps_iframe", "menu_pdf", "hours_block"],
    "saas": ["api_snippet_hero", "pricing_table", "trust_logos"],
    "medical": ["disclaimer_no_absolute_claims", "license_footer"],
    "legal": ["founding_year_footer", "attribution_attorney_advertising"],
    "real_estate": ["masonry_grid", "map_integration", "filter_sidebar"],
    "education": ["fundae_badge_eu", "course_catalog_table"],
    "ecommerce": ["cart_persistence", "trust_badges", "return_policy_link"],
    "fintech": ["regulatory_disclaimer", "rate_table", "trust_indicators"],
    "nonprofit": ["donation_cta", "impact_metrics", "transparency_report"]
  }
}
```

Each vertical also has a ranked list of visual directions (e.g., restaurant → 1: warm-photographic, 2: editorial-minimal, 3: artisanal-handcrafted). The orchestrator's intake step matches user-stated vertical to this table and surfaces the top three options.

---

## LLMO deliverable bundle (T-128)

Modern sites ship metadata for LLM crawlers alongside the standard SEO bundle. The matrix's project-level config includes:

```
public/
├── llms.txt           # Plain-text site summary for LLMs
├── llms-full.txt      # Full content index
├── identity.json      # Structured identity (org name, contact, purpose)
└── (existing) sitemap.xml, robots.txt
```

Each route emits JSON-LD structured data in the page `<head>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Co.",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png"
}
</script>
```

If the org has a physical address, the type becomes `LocalBusiness` with `address` and `geo` sub-objects. Copyright year is dynamic — `{new Date().getFullYear()}` in React / `<?php echo date('Y'); ?>` in PHP — never hardcoded.

---

## Agent-accessibility attributes (T-129)

For sites operated by AI agents (browser automation, assistive AI), stable locators help the agent reliably target elements:

```html
<button data-ai-action="submit-order">Place order</button>
<div data-ai-hidden="true"><!-- decorative element, AI should skip --></div>
```

The `.well-known/ai.json` manifest declares the site's agent-accessibility surface:

```json
{
  "$schema": "https://example.com/ai-manifest-v1.json",
  "actions": [
    { "id": "submit-order", "method": "POST", "endpoint": "/api/orders", "rate_limit": "1/sec" }
  ],
  "honeypot_fields": ["website_url", "phone_number_2"]
}
```

Honeypot + rate-limit replaces CAPTCHA on agent-facing flows. CAPTCHAs assume a human; an authorized agent should be able to operate without solving an image puzzle.

---

## Agentic UI affordances (T-130, EU EAA-required June 2025)

Sites that deploy AI assistance must surface three affordances:

1. **Intent Preview** — before the AI takes an action, show what it will do as a diff / before-after. The user approves or cancels.
2. **Action Audit** — every AI action is logged with a reversible undo. The user can review and revert.
3. **Escalation Pathway** — a visible "take over from AI" control. The user is never trapped in an AI flow.

Component matrix entry:

```json
{
  "component": "AIActionConfirm",
  "axes": {
    "action_type": ["create", "modify", "delete", "navigate"],
    "reversibility": ["instant", "delayed_24h", "irreversible"]
  },
  "orphans": [
    { "axes": { "action_type": "delete", "reversibility": "instant" }, "reason": "Delete with instant reversibility is misleading — actual deletion is queued for 30 days" }
  ]
}
```

EU EAA (European Accessibility Act) requires these affordances on consumer-facing services from June 2025. Sites without them face compliance risk for EU users.

---

## /tmp standalone preview checkpoint (T-117)

When iterating on a component, always write a `/tmp/<component>-preview.html` standalone file as the first artifact. Reasons:

1. Zero risk to the real project.
2. The reviewer opens one local file; no dev server, no build step.
3. The file embeds the toolbar (T-120 toggle), every variant grid cell, and the spec-sheet markdown rendered alongside.
4. If the reviewer requests changes, you regenerate `/tmp/<component>-preview.html` only.

When the reviewer types `ship it` / `approved`, the agent then writes to the real project files (token JSON, component source, story file). Until then, only `/tmp` is touched.

---

## Component sourcing hierarchy (T-116)

When you need an off-the-shelf component, follow this hierarchy in order:

1. `amw-shadcn-ui` (MIT, in this plugin) — the default.
2. MagicUI (MIT, externally hosted) — for richer animated primitives shadcn does not cover.
3. ReactBits (MIT) — niche reactive UI components.
4. 21st.dev (MIT) — extra catalog.
5. Aceternity (mixed license — verify per-component) or custom.

Pre-install checklist for any external component:
- URL exists (no inventing GitHub URLs).
- License is MIT / Apache / BSD / 0BSD / ISC / CC0. Reject GPL, abandoned > 12 months, webpack-only (incompatible with the plugin's Vite / Bun runtime).
- Dependency weight checked — a component bringing 200 KB of deps for one chip is rejected.
- Sandbox test: drop into a clean preview file, confirm it renders without errors.

Post-install hygiene:
- Replace any hardcoded color classes (`text-blue-500`, `bg-gray-100`) with token references (`text-[var(--color-primary)]`).
- Remove unused props the component exposes that the project will not use.
- Match the project's naming convention (kebab-case files vs PascalCase).

Component-reuse decision matrix: `Reuse > Extend props > Create new`. Creating a sibling is the last resort.

---

## Breaks-if

- The variant matrix lives only in the implementer's head, not in `variants.json`. The next developer recreates orphan combinations.
- Orphan combinations have no runtime guard. A consumer renders `Button intent="ghost" state="loading"` and gets a visually broken spinner-in-nothing.
- Token scale derivation is hand-typed (the `--space-1`..`--space-32` values are manually written as `4px`, `8px`, etc., not as `calc()` of the base). Changing the base requires editing 30 lines instead of 1.
- The wireframe-token swap is implemented as hardcoded grayscale values in component CSS (`color: #888`). At approval time, every component needs editing instead of one attribute removal.
- The spec sheet omits the edge-cases section. The implementer ships the happy-path component; error / empty / loading states are filled in ad-hoc, drift from the system.
- `data-ai-action` attributes drift from the actions documented in `.well-known/ai.json`. Agents fail to find expected actions; the manifest becomes a stale lie.
- Cross-route dedup manifest is not read before new component generation. Three routes ship three different `<Card>` components with overlapping props.
- Vertical mandatory elements are missing (e.g., a medical site missing the no-absolute-claims disclaimer). Regulatory exposure.
- Per-component overrides in the matrix conflict with the base token (e.g., `disabled-primary` override says `background: var(--color-muted)` but the component CSS later applies `:disabled { background: var(--color-bg-disabled) }`). Two sources of truth; one wins randomly.

---

## Component examples

### Example A — Button variant matrix → CSS

`variants.json` extract:

```json
{
  "component": "Button",
  "axes": {
    "size": ["sm", "md", "lg"],
    "intent": ["primary", "secondary", "danger"],
    "state": ["default", "hover", "active", "disabled", "loading"]
  }
}
```

Generated CSS (per intent × state cell, reading tokens for size):

```css
.btn { /* base */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  border: 0;
  border-radius: var(--radius-md);
  font-family: inherit;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-fast);
  min-height: var(--hit-target-min);
}
.btn[data-size="sm"] { padding: var(--space-2) var(--space-4); font-size: var(--font-size-sm); }
.btn[data-size="md"] { padding: var(--space-3) var(--space-6); font-size: var(--font-size-md); }
.btn[data-size="lg"] { padding: var(--space-4) var(--space-8); font-size: var(--font-size-lg); }
.btn[data-intent="primary"]   { background: var(--color-primary);   color: var(--color-on-primary); }
.btn[data-intent="secondary"] { background: var(--color-secondary); color: var(--color-on-secondary); }
.btn[data-intent="danger"]    { background: var(--color-danger);    color: var(--color-on-danger); }
.btn[data-state="disabled"] { background: var(--color-muted); color: var(--color-text-muted); cursor: not-allowed; }
.btn[data-state="loading"] { pointer-events: none; opacity: 0.7; }
```

### Example B — Card matrix with density axis

`variants.json`:

```json
{
  "component": "Card",
  "axes": {
    "density": ["compact", "default", "comfortable"],
    "elevation": ["flat", "raised", "floating"]
  }
}
```

```css
.card { background: var(--color-surface); border-radius: var(--radius-md); }
.card[data-density="compact"]     { padding: var(--space-3); gap: var(--space-2); }
.card[data-density="default"]     { padding: var(--space-6); gap: var(--space-4); }
.card[data-density="comfortable"] { padding: var(--space-8); gap: var(--space-6); }
.card[data-elevation="flat"]      { border: 1px solid var(--color-border); }
.card[data-elevation="raised"]    { box-shadow: 0 2px 8px rgb(0 0 0 / 0.08); }
.card[data-elevation="floating"]  { box-shadow: 0 12px 32px rgb(0 0 0 / 0.16); }
```

Three densities × three elevations = nine combinations, all valid, all derived from tokens. Changing `--spacing-unit` from 4 to 6 rescales every card density in one edit.

---

## Cross-references

- DESIGN.md authoring + lint: `skills/amw-design-md/SKILL.md` + `bin/amw-design-md-lint.sh`.
- DESIGN.md → tokens emission: `bin/amw-design-md-emit-companions.py`.
- WCAG contrast verification: `bin/amw-design-md-contrast.py`.
- Color token doctrine: `skills/amw-design-principles/color-system.md`.
- Spacing scale + hit-target floor: `skills/amw-design-principles/spacing-rhythm.md`.
- Typography scale: `skills/amw-design-principles/typography-system.md`.
- Microinteractions consumed by component variants: `TECH-microinteractions-catalog.md`.
- Component reuse manifest: lives in .planning/used-components.json per-project.
