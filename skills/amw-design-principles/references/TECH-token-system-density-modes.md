<!--
Sources: Material 3 density (Apache-2.0, https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes) — direct-port of compact/comfortable/spacious naming; Carbon Design density tokens (Apache-2.0, IBM) — direct-port of multiplier-over-baseline approach.
Synthesis novel to this plugin: 3-mode multiplier table over the plugin's 10-step spacing scale, breakpoint-driven vs user-toggle decision tree, density's interaction with type-scale, breaks-if invariants. Clean-room beyond the cited sources.
-->

---
name: TECH-token-system-density-modes
category: design-principles-tokens
source: Material 3 + Carbon density direct-port of mode naming; clean-room synthesis of the multiplier table + breakpoint vs toggle decision (batch9 Wave 2 Round 3, T-082/T-083)
license: this file = MIT (plugin license); Material 3 + Carbon are Apache-2.0 with attribution preserved in the HTML-comment header above
also-in: TECH-token-system-spacing-and-grid.md (the 10-step spacing scale this density multiplies); TECH-motion-density.md (motion-density 3-tier system is the kinetic twin of this static-density system); TECH-dial-configuration.md (VISUAL_COMPLEXITY dial may co-vary with density mode)
---

# Token system — compact / comfortable / spacious density modes

## Table of Contents

- [What this is](#what-this-is)
- [The three density modes](#the-three-density-modes)
- [The multiplier table — how density scales each token family](#the-multiplier-table--how-density-scales-each-token-family)
- [Density and type-scale interaction](#density-and-type-scale-interaction)
- [Responsive density vs user-toggle density](#responsive-density-vs-user-toggle-density)
- [Token block — canonical declaration](#token-block--canonical-declaration)
- [Breaks if](#breaks-if)
- [Component example A — data table at three densities](#component-example-a--data-table-at-three-densities)
- [Component example B — responsive density on a sidebar](#component-example-b--responsive-density-on-a-sidebar)
- [Cross-references](#cross-references)

## What this is

A single page can serve different audiences and different viewports without forking the markup. Density modes encode "how tightly should content pack" as a global multiplier over the 10-step spacing scale (from `TECH-token-system-spacing-and-grid.md`). Three named modes — **compact**, **comfortable**, **spacious** — cover 90% of real product needs. Comfortable is the baseline; compact tightens for data-heavy contexts; spacious loosens for editorial / marketing / accessibility-first contexts.

Crucially, density is a **multiplier over spacing only**. Radii, elevations, type sizes, and color roles do NOT change with density mode. A button is still `--radius-2` in compact and in spacious — only the padding around it shifts. This keeps the visual identity stable across densities.

This file gives the three modes, the multiplier table, the responsive vs user-toggle decision, the canonical token block, and the breaks-if invariants.

## The three density modes

| Mode | Spacing multiplier | Typical use |
|---|---|---|
| **Compact**     | ×0.75 | Data tables, dashboards with many rows, design-tool UIs (Figma sidebars), admin consoles, spreadsheets |
| **Comfortable** | ×1.00 (baseline) | Default web product; landing pages; consumer apps; documentation; the value the 10-step scale was designed for |
| **Spacious**    | ×1.25 | Editorial long-form, marketing hero sections, accessibility-first UIs (large-touch targets), kiosk / TV screens |

**Pick by content type, not by personal preference.**

- A pricing table with 10 rows of comparison data → compact.
- A pricing table with 3 tiers of marketing-pitched plans → comfortable.
- A hero landing page → comfortable (NOT spacious — spacious is for the body content only if the brand voice is editorial; hero blocks pick their own padding from steps 7–10).
- A dashboard data grid → compact.
- A long-form article body → comfortable.
- A "we care about accessibility / large fonts" config → spacious.

**There is no "extra compact" or "extra spacious."** Stretching the multiplier beyond ×0.75 / ×1.25 breaks the type-scale relationship (see below). Products that legitimately need denser-than-compact (Bloomberg terminal, trading screens) are a specialist tier and not in the standard density set.

## The multiplier table — how density scales each token family

Density acts on the 10-step spacing scale by **multiplying each step's value**. Every step is multiplied by the same factor; the scale stays internally proportional. The resulting spacing values are still on the 4pt grid because each step's baseline value is a multiple of 4 and the multipliers 0.75 / 1.0 / 1.25 keep things 4pt-aligned for most steps (1px sub-grid drift is tolerated for the smallest tokens).

| Token family | Compact (×0.75) | Comfortable (×1.00) | Spacious (×1.25) |
|---|---|---|---|
| **Spacing scale** `--space-1` … `--space-10` | multiplied per the table below | unchanged | multiplied per the table below |
| **Grid gutter** `--grid-gutter` | derived from spacing; auto-shifts | unchanged | derived from spacing; auto-shifts |
| **Component padding** (button/card/input internal) | shifts via spacing | baseline | shifts via spacing |
| **Section margins** (between landing-page sections) | shifts via spacing | baseline | shifts via spacing |
| **Type scale** `--text-*` | **unchanged** | unchanged | **unchanged** |
| **Radius scale** `--radius-*` | **unchanged** | unchanged | **unchanged** |
| **Elevation scale** `--elevation-*` | **unchanged** | unchanged | **unchanged** |
| **Color roles** `--color-*` | **unchanged** | unchanged | **unchanged** |
| **z-index layers** `--z-*` | **unchanged** | unchanged | **unchanged** |
| **Line-height multipliers** | **unchanged** | unchanged | **unchanged** |

**Explicit per-step spacing values:**

| Step | Compact (px) | Comfortable (px) | Spacious (px) |
|---|---|---|---|
| `--space-1` | 4* | 4 | 4* |
| `--space-2` | 6 | 8 | 10 |
| `--space-3` | 8 | 12 | 16 |
| `--space-4` | 12 | 16 | 20 |
| `--space-5` | 16 | 24 | 32 |
| `--space-6` | 24 | 32 | 40 |
| `--space-7` | 32 | 48 | 64 |
| `--space-8` | 48 | 64 | 80 |
| `--space-9` | 72 | 96 | 120 |
| `--space-10` | 96 | 128 | 160 |

*`--space-1` floors at 4 px in every mode — it would round below the 4pt grid at ×0.75 (3 px) and look out of grid; same logic applies in reverse if 5 px came up at ×1.25, so 4 stays 4 in both directions. This floor is intentional — the smallest spacing step is the "we can't shrink any further" floor.

## Density and type-scale interaction

Type does NOT scale with density. This is the most counter-intuitive rule of the density system and the most important.

**Why type stays fixed.** Reducing font sizes in compact mode makes text unreadable; increasing them in spacious mode makes layouts blow out. The 10-step type scale (from `typography-system.md`) is engineered to be readable at 1× without scaling. If a product genuinely needs smaller text (data terminal) or larger text (kiosk), it picks a different *type scale*, not a different *density*.

**What changes around the fixed type.** Padding around text changes. Line-spacing (block-level) between paragraphs changes. The distance from the baseline of one line to the top of the next paragraph follows the spacing scale and thus follows the density mode. But the line-height multiplier within a paragraph stays constant — line-height is a typographic property, not a spacing property.

**Concrete example.** A 16 px body paragraph with `line-height: 1.6` renders at 25.6 px between baselines in every density mode. What changes:
- Compact: 12 px space between paragraphs (was `--space-3`=12 — no, that's comfortable; compact = 8 px).
- Comfortable: 12 px space between paragraphs (`--space-3`).
- Spacious: 16 px space between paragraphs (×1.25 of comfortable's 12).

Same line-height, different inter-paragraph space.

## Responsive density vs user-toggle density

Density mode can be set in two ways. They are not exclusive — products can use both, with the user-toggle overriding the responsive default.

### Mode 1 — Responsive (breakpoint-driven, automatic)

The page picks a density mode based on viewport width.

| Viewport | Default density | Why |
|---|---|---|
| `<= --bp-sm` (mobile) | Compact | Small viewport → tight packing maximizes visible content. Spacious on mobile wastes the precious vertical space. |
| `--bp-sm` to `--bp-xl` (tablet/desktop) | Comfortable | The mode the spacing scale is engineered for. |
| `>= --bp-2xl` (large desktop / TV) | Spacious | Big viewport → more space available; tighter spacing leaves a sea of unused canvas. |

This is the default for marketing / landing / consumer pages. The user doesn't think about it; the page adapts.

### Mode 2 — User-toggle (preference, persisted)

The user picks compact / comfortable / spacious in a settings UI. Persists in `localStorage` or a user account.

When to expose this:
- **Productivity tools** — data tables, dashboards, IDEs, design tools. Power users will want compact; casual users will want comfortable; some accessibility users will want spacious. Always expose the toggle.
- **Reading apps** — articles, docs, blogs. Expose comfortable / spacious only; compact rarely makes sense for long-form reading.
- **Marketing / landing / consumer single-purpose pages** — do NOT expose. The brand picks the density.

When user-toggle is active, it overrides the responsive default. A user who picked "spacious" on their phone gets spacious on their phone, not the responsive compact. Implementation:

```css
:root[data-density="compact"]     { /* compact tokens */ }
:root[data-density="comfortable"] { /* comfortable tokens (baseline) */ }
:root[data-density="spacious"]    { /* spacious tokens */ }

/* Responsive default — applies only if data-density is unset */
@media (max-width: 40rem) {
  :root:not([data-density]) { /* compact tokens */ }
}
@media (min-width: 96rem) {
  :root:not([data-density]) { /* spacious tokens */ }
}
```

The selector `:root:not([data-density])` is the key: the responsive default applies only when the user hasn't picked a mode.

### Decision matrix — pick the right mode

| Page type | Responsive? | User-toggle? |
|---|---|---|
| Marketing landing page | yes | no |
| Consumer mobile app | yes | no |
| Productivity SaaS (dashboards, tools) | yes | yes — expose in settings |
| Data terminal / Bloomberg-like | no (always compact) | no |
| Long-form article / docs | yes (light) | yes — comfortable/spacious only |
| Kiosk / TV display | no (always spacious) | no |
| Accessibility-first product | optional | yes — required |

## Token block — canonical declaration

The plugin uses a single CSS file that defines all three density modes; the active one is selected via `data-density` on `:root` (or via media query when no override is set).

```css
/* === Compact mode === */
:root[data-density="compact"] {
  --space-1:  0.25rem;    /* 4 (floor) */
  --space-2:  0.375rem;   /* 6 */
  --space-3:  0.5rem;     /* 8 */
  --space-4:  0.75rem;    /* 12 */
  --space-5:  1rem;       /* 16 */
  --space-6:  1.5rem;     /* 24 */
  --space-7:  2rem;       /* 32 */
  --space-8:  3rem;       /* 48 */
  --space-9:  4.5rem;     /* 72 */
  --space-10: 6rem;       /* 96 */

  --grid-gutter: var(--space-4);
}

/* === Comfortable mode (BASELINE — identical to spacing scale defaults) === */
:root,
:root[data-density="comfortable"] {
  --space-1:  0.25rem;    /* 4 */
  --space-2:  0.5rem;     /* 8 */
  --space-3:  0.75rem;    /* 12 */
  --space-4:  1rem;       /* 16 */
  --space-5:  1.5rem;     /* 24 */
  --space-6:  2rem;       /* 32 */
  --space-7:  3rem;       /* 48 */
  --space-8:  4rem;       /* 64 */
  --space-9:  6rem;       /* 96 */
  --space-10: 8rem;       /* 128 */

  --grid-gutter: var(--space-5);
}

/* === Spacious mode === */
:root[data-density="spacious"] {
  --space-1:  0.25rem;    /* 4 (floor) */
  --space-2:  0.625rem;   /* 10 */
  --space-3:  1rem;       /* 16 */
  --space-4:  1.25rem;    /* 20 */
  --space-5:  2rem;       /* 32 */
  --space-6:  2.5rem;     /* 40 */
  --space-7:  4rem;       /* 64 */
  --space-8:  5rem;       /* 80 */
  --space-9:  7.5rem;     /* 120 */
  --space-10: 10rem;      /* 160 */

  --grid-gutter: var(--space-6);
}

/* === Responsive default (applies only when user hasn't set data-density) === */
@media (max-width: 40rem) {
  :root:not([data-density]) {
    --space-1:  0.25rem; --space-2:  0.375rem; --space-3:  0.5rem;
    --space-4:  0.75rem; --space-5:  1rem;     --space-6:  1.5rem;
    --space-7:  2rem;    --space-8:  3rem;     --space-9:  4.5rem;
    --space-10: 6rem;    --grid-gutter: var(--space-4);
  }
}
@media (min-width: 96rem) {
  :root:not([data-density]) {
    --space-1:  0.25rem; --space-2:  0.625rem; --space-3:  1rem;
    --space-4:  1.25rem; --space-5:  2rem;     --space-6:  2.5rem;
    --space-7:  4rem;    --space-8:  5rem;     --space-9:  7.5rem;
    --space-10: 10rem;   --grid-gutter: var(--space-6);
  }
}
```

Type, radius, elevation, color, z-index are NOT in this file — they're in their own token blocks and unaffected by density.

## Breaks if

The auditor and wireframe builder reject the density block when any of the following holds:

- A density mode redefines `--text-*`, `--radius-*`, `--elevation-*`, `--color-*`, `--z-*`, or any non-spacing token. Density is spacing-only.
- A density mode's multiplier deviates from {0.75, 1.0, 1.25} — invented multipliers (×0.5, ×1.5, ×2.0) break the scale's proportional integrity.
- The `--space-1` value goes below 4 px in any mode. The 4 px floor is hard.
- A spacing value used in markup is hard-coded for a specific density mode (e.g., `padding: 12px` when the comfortable token resolves to 12 — defeats the density system). All spacing in markup uses `var(--space-N)`.
- A page declares a user-toggle density UI but the JavaScript doesn't persist the choice — the toggle becomes meaningless on reload.
- A media-query density default is set without the `:not([data-density])` guard, so a user-toggled preference gets overridden by the viewport.
- The user-toggle exposes a 4th mode (e.g., "extra compact"). Stick to the three named modes.
- Compact density is used on a long-form reading page (cramming body text harms readability).
- Spacious density is used on a data table (wastes vertical real estate).
- Density mode changes mid-scroll (a single page can have only ONE density mode active at a time across its body; transient density shifts on scroll break visual stability).

## Component example A — data table at three densities

The same table renders at three densities by switching `data-density` on the root. Markup is identical; only the spacing tokens resolve differently.

```html
<table class="data-table">
  <thead>
    <tr>
      <th>Customer</th>
      <th>Plan</th>
      <th>MRR</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Acme Corp</td>
      <td>Pro</td>
      <td>$249</td>
      <td><span class="badge">Active</span></td>
    </tr>
    <!-- ... 50 more rows ... -->
  </tbody>
</table>

<style>
  .data-table th,
  .data-table td {
    padding-block: var(--space-3);              /* compact: 8 | comfy: 12 | spacious: 16 */
    padding-inline: var(--space-4);             /* compact: 12 | comfy: 16 | spacious: 20 */
    border-bottom: 1px solid var(--color-outline);
  }

  .data-table th {
    background: var(--color-surface-variant);
    color: var(--color-on-surface-variant);
    font-weight: 600;
  }

  .badge {
    padding-block: var(--space-1);              /* 4 in all modes (floor) */
    padding-inline: var(--space-2);             /* compact: 6 | comfy: 8 | spacious: 10 */
    border-radius: var(--radius-1);              /* 4 — unchanged across densities */
    background: var(--color-primary-container);
    color: var(--color-on-primary-container);
  }
</style>
```

A data-dense admin console picks `<html data-density="compact">`; the same markup in a marketing-style "see your customers" page picks `<html data-density="comfortable">`; an accessibility-first product picks `<html data-density="spacious">`. The badge radius stays 4 px in all three.

## Component example B — responsive density on a sidebar

A sidebar that auto-densifies on mobile (more content visible) and auto-spacifies on huge desktops (more breathing room):

```html
<html><!-- no data-density attribute — responsive defaults apply -->
<body>
  <nav class="sidebar">
    <a href="/" class="sidebar-link">Home</a>
    <a href="/projects" class="sidebar-link">Projects</a>
    <a href="/clients" class="sidebar-link">Clients</a>
    <a href="/billing" class="sidebar-link">Billing</a>
    <a href="/settings" class="sidebar-link">Settings</a>
  </nav>
</body>
</html>

<style>
  .sidebar {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);                        /* mobile: 6 | desktop: 8 | TV: 10 */
    padding: var(--space-4);                    /* mobile: 12 | desktop: 16 | TV: 20 */
    background: var(--color-surface);
  }

  .sidebar-link {
    padding-block: var(--space-3);              /* mobile: 8 | desktop: 12 | TV: 16 */
    padding-inline: var(--space-4);             /* mobile: 12 | desktop: 16 | TV: 20 */
    border-radius: var(--radius-2);              /* 8 — unchanged */
    color: var(--color-on-surface);
  }
</style>
```

On a phone, the sidebar packs into a compact list — five links fit in the viewport. On a default desktop, comfortable spacing reads as standard navigation. On a large desktop, spacious padding lets each link breathe — appropriate for a "premium app" feel.

If the product exposes a user-toggle, adding `<html data-density="comfortable">` would override the viewport-driven density across all three viewports — the user's preference always wins.

## Cross-references

- `TECH-token-system-spacing-and-grid.md` — the 10-step spacing scale this density multiplies; density does NOT change the step *names*, only the *values*.
- `TECH-token-system-color-roles.md` — color roles are NOT density-scoped; same hex values across all densities.
- `TECH-token-system-elevation-and-radius.md` — elevation + radius scales are NOT density-scoped; same values across all densities.
- `TECH-motion-density.md` — the **kinetic** density companion: 3-tier motion density (subtle / moderate / lively) is the motion-system twin of this static-spacing density. Pair them when authoring (e.g., a "compact + subtle" dashboard vs a "spacious + moderate" landing page).
- `TECH-dial-configuration.md` — VISUAL_COMPLEXITY dial may co-vary with density (a complexity-1 page tends toward spacious; complexity-10 tends toward compact), but the two are independent and can be set separately.
- `../typography-system.md` — type scale is unaffected by density; never scale fonts to match density mode.
- `skills/amw-design-md/SKILL.md` — DESIGN.md declares the active density mode via `density: comfortable | compact | spacious` in frontmatter; the wireframe builder reads this.
- `skills/amw-design-system-presets/SKILL.md` — each preset picks its default density (e.g., the linear preset defaults to comfortable, the design-tool preset defaults to compact); users can still toggle at runtime.
- `bin/amw-design-md-validate.py` — checks that the density mode (if specified in DESIGN.md) is one of {compact, comfortable, spacious}.
- `agents/amw-wireframe-builder-agent.md` — Phase B HTML emission selects the density-mode CSS block based on DESIGN.md frontmatter; emits the `data-density` attribute when user-toggle is required.
- `agents/amw-component-library-architect-agent.md` — authors the density block; decides whether user-toggle is exposed.
