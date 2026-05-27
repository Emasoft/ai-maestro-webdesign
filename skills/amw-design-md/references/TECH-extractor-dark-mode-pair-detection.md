<!--
Inspired by a GPL-licensed extractor (design-extractor-skill); the
pair-detection algorithm here is reimplemented clean-room from
documented `prefers-color-scheme` + computed-style behaviour.
No verbatim code carried over.
-->

# TECH: Dark-mode pair detection — pairing light/dark color tokens by role

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Why pairing is non-trivial](#why-pairing-is-non-trivial)
- [Algorithm](#algorithm)
  - [Step 1 — Dual-pass extraction with media emulation](#step-1--dual-pass-extraction-with-media-emulation)
  - [Step 2 — Build role maps for each scheme](#step-2--build-role-maps-for-each-scheme)
  - [Step 3 — Pair by on-page role + media-query context](#step-3--pair-by-on-page-role--media-query-context)
  - [Step 4 — Emit dual-scheme frontmatter](#step-4--emit-dual-scheme-frontmatter)
- [Pseudo-code](#pseudo-code)
- [The three pairing signals](#the-three-pairing-signals)
- [Output schema](#output-schema)
- [Worked example](#worked-example)
- [Breaks if](#breaks-if)
- [Cross-references](#cross-references)

## What it does

Documents how the URL-extraction pipeline produces a **pair-aware** color map when a site supports both `prefers-color-scheme: light` and `prefers-color-scheme: dark`. A naive single-pass extraction picks whichever scheme the user's OS or browser currently advertises — capturing only half the design system. A dual-pass extraction captures both palettes but leaves a harder problem: **which light color is the dark version of which?**

Pairing by raw color similarity is wrong — `#08090a` is not the dark version of `#ffffff` in any color space; they are functionally inverse, not perceptually adjacent. Pairing by **on-page role** is right: the color used as `body { background }` in light mode is the dark-mode partner of the color used as `body { background }` in dark mode, regardless of how dissimilar the hex values are.

The pairing pass runs after both extractions complete and emits a dual-scheme block consumed by the DESIGN.md frontmatter emitter. The output preserves the canonical Variant 1 role names and adds a parallel `light`/`dark` axis per role.

## When to use

- User says: "extract DESIGN.md with both light and dark modes"
- User says: "this site has a theme switcher — capture both"
- Brand-researcher: extracting from a site where the dark mode is an explicit brand signal (Linear, Vercel, Stripe Dashboard, GitHub)
- Resting-state extraction returns suspiciously high contrast ratios (often a signal that the page is in dark mode while the brand prefers light, or vice versa)

## When NOT to use

- The site has only a single color scheme (no `@media (prefers-color-scheme: dark)` rules, no `data-theme` attribute, no theme toggle) — emit single-scheme DESIGN.md
- The site has a "dim" or "high-contrast" third scheme — TECH-extractor-dark-mode-pair-detection handles a binary axis only; record `warnings: ["3+ schemes detected; extraction limited to light + dark"]`
- The dark and light modes share a single shared palette with minor tweaks (e.g., text becomes 8% lighter on dark) — pair detection is overkill; emit single-scheme + an `extensions.theme-overrides` block listing the tweaks

## Why pairing is non-trivial

A site declares its dark mode in any of four common ways, often combined:

| Mechanism | Detection signal | Switching method |
|---|---|---|
| `@media (prefers-color-scheme: dark)` queries | Stylesheet rules contain this @media | CDP `Emulation.setEmulatedMedia { features: [{name: "prefers-color-scheme", value: "dark"}] }` |
| `[data-theme="dark"]` attribute on `<html>` or `<body>` | DOM mutation observable | `document.documentElement.setAttribute("data-theme", "dark")` |
| `.dark` class on `<html>` (Tailwind v3 dark mode class) | Class presence check | `document.documentElement.classList.add("dark")` |
| Two stylesheets toggled by user JS | Inspect `<link>` tags with `media` or `disabled` attrs | Locate toggle, dispatch click |

The pair-detection pass must trigger each mechanism the site uses without relying on a user click — the cleanest approach is `Emulation.setEmulatedMedia` (works for the first mechanism universally and triggers most class/attribute toggles too because well-built theme JS listens to the `MediaQueryList.change` event).

The pairing-by-role idea is what makes the algorithm work despite the variance in mechanisms: regardless of HOW the site switches, the SAME button on the page is `colors.primary` in both schemes — extract its computed `backgroundColor` in light mode and in dark mode, you have a pair.

## Algorithm

### Step 1 — Dual-pass extraction with media emulation

```text
Pass 1: emulate prefers-color-scheme: light
  → run TECH-07 extractor → snapshot_light
Pass 2: emulate prefers-color-scheme: dark
  → run TECH-07 extractor → snapshot_dark
```

Between passes the page may need a forced reflow (`document.body.offsetHeight`) or a `setTimeout(0)` yield to let theme-listening JS apply class/attribute mutations.

If neither mechanism flips the theme (some hand-rolled toggles ignore the media query and listen only to a JS click event), fall back to:

- Searching the DOM for a button labeled "theme", "dark", "light", "appearance" — dispatch a synthetic click via CDP `Input.dispatchMouseEvent`.
- If no such button is found, record `warnings: ["dark mode toggle not auto-detectable; second pass skipped"]` and abort the dual-pass; emit single-scheme.

### Step 2 — Build role maps for each scheme

For each pass, run the standard color-role inference from [TECH-extractor-color-role-inference](./TECH-extractor-color-role-inference.md). The two passes produce two independent role maps:

```python
roles_light = {
  "background": "#ffffff",
  "surface":    "#f7f7f8",
  "on-surface": "#1a1d23",
  "primary":    "#5e6ad2",
  "secondary":  "#22c55e",
  ...
}
roles_dark = {
  "background": "#08090a",
  "surface":    "#1a1d23",
  "on-surface": "#fafafa",
  "primary":    "#7a85e6",
  "secondary":  "#34d399",
  ...
}
```

Note the role names are identical — both passes use the same inference algorithm on the same set of landmarks. This is what makes pairing trivial in Step 3.

### Step 3 — Pair by on-page role + media-query context

The pairing is now an inner-join on role name:

```python
paired_roles = {}
for role in roles_light.keys() & roles_dark.keys():
    paired_roles[role] = {
        "light": roles_light[role],
        "dark":  roles_dark[role],
    }
```

Roles present in one scheme but not the other (e.g., `error-light` appears only in light mode because the dark-mode error state was reassigned to `secondary`) get a `null` value on the missing side:

```python
for role in roles_light.keys() - roles_dark.keys():
    paired_roles[role] = {"light": roles_light[role], "dark": None}
for role in roles_dark.keys() - roles_light.keys():
    paired_roles[role] = {"light": None, "dark": roles_dark[role]}
```

The asymmetry is recorded in the DESIGN.md prose as a warning ("`tertiary` extracted only in light mode; the dark theme uses `secondary` for this slot").

### Step 4 — Emit dual-scheme frontmatter

Variant 1 DESIGN.md frontmatter is single-scheme by default. Dual-scheme output writes to the extension namespace `extensions.schemes` per [extension-sections-10-14](./extension-sections-10-14.md):

```yaml
colors:
  # Canonical single-scheme map — defaults to the light scheme
  # (the more universally readable default).
  primary: "#5e6ad2"
  background: "#ffffff"
  surface: "#f7f7f8"
  ...

extensions:
  schemes:
    light:
      colors:
        primary: "#5e6ad2"
        background: "#ffffff"
        surface: "#f7f7f8"
        on-surface: "#1a1d23"
    dark:
      colors:
        primary: "#7a85e6"
        background: "#08090a"
        surface: "#1a1d23"
        on-surface: "#fafafa"
```

The canonical `colors:` block at the top mirrors `extensions.schemes.light.colors` — consumers who don't process the extension still get a working single-scheme palette.

## Pseudo-code

```python
async def extract_dual_scheme(url, dev_browser):
    # Pass 1 — light
    await dev_browser.emulate_color_scheme("light")
    await dev_browser.goto(url)
    snapshot_light = await extract_tech07_snapshot(dev_browser)
    roles_light = assign_color_roles(snapshot_light.palette)

    # Pass 2 — dark
    await dev_browser.emulate_color_scheme("dark")
    await dev_browser.reload()  # cheap; cache is warm
    await dev_browser.evaluate("document.body.offsetHeight")  # force reflow
    snapshot_dark = await extract_tech07_snapshot(dev_browser)
    roles_dark = assign_color_roles(snapshot_dark.palette)

    # Sanity — did the second pass actually flip?
    background_delta = wcag_luminance_delta(
        roles_light["background"],
        roles_dark["background"],
    )
    if background_delta < 0.20:
        warn("dark-mode flip did not change background; emulation may have failed")
        return single_scheme_result(roles_light)

    # Pair by role
    paired_roles = {}
    all_roles = roles_light.keys() | roles_dark.keys()
    for role in all_roles:
        paired_roles[role] = {
            "light": roles_light.get(role),
            "dark":  roles_dark.get(role),
        }

    return {
        "default_scheme": "light",
        "canonical_colors": roles_light,
        "extensions": {"schemes": {
            "light": {"colors": roles_light},
            "dark":  {"colors": roles_dark},
        }},
        "paired_roles": paired_roles,
    }
```

## The three pairing signals

The algorithm intentionally pairs by ONLY role name. The bin script records three additional **signals** in the prose section but does NOT use them for pairing decisions:

| Signal | What it tells | Why not used for pairing |
|---|---|---|
| Hue similarity (Δhue in OKLCH) | Light `primary` and dark `primary` usually share hue | Some sites deliberately shift hue between modes (e.g., warmer accent in light, cooler in dark) — pairing on hue would split correct pairs |
| Selector overlap | Both schemes' role assignments came from the same DOM landmark | Already implicit in pairing by role; recording it is for prose ("primary observed on `<button class="btn-primary">` in both modes") |
| `@media (prefers-color-scheme: dark)` rule matching | The dark `primary` came from a rule guarded by the media query | Confirms the pair is theme-related, not from a per-component override; recorded as a `confidence: high/low` field |

The "what would look wrong?" prose technique from upstream design-extractor — explicitly ask "is this pair contradictory?" during emission — surfaces problems the algorithm cannot detect (e.g., a `primary` paired with a near-identical hue in both modes means the site has no real dark mode; flag it for user review).

## Output schema

```yaml
colors:
  primary: "#5e6ad2"
  background: "#ffffff"
  surface: "#f7f7f8"
  on-surface: "#1a1d23"
  border-subtle: "#e5e5e7"

extensions:
  schemes:
    default: "light"
    light:
      colors:
        primary: "#5e6ad2"
        background: "#ffffff"
        surface: "#f7f7f8"
        on-surface: "#1a1d23"
        border-subtle: "#e5e5e7"
      meta:
        observed_via: "prefers-color-scheme: light"
        contrast_aa_pairs: 12
    dark:
      colors:
        primary: "#7a85e6"
        background: "#08090a"
        surface: "#1a1d23"
        on-surface: "#fafafa"
        border-subtle: "#26282d"
      meta:
        observed_via: "prefers-color-scheme: dark"
        contrast_aa_pairs: 14
```

The `meta:` sub-block records per-scheme provenance (which mechanism triggered, how many WCAG-AA pairs passed) for downstream auditing.

## Worked example

Linear.app — extraction with dual-scheme.

Pass 1 (`prefers-color-scheme: light`):

| Role | Hex | Confidence |
|---|---|---|
| background | `#ffffff` | 0.95 |
| surface | `#f7f7f8` | 0.81 |
| on-surface | `#0c0e12` | 0.94 |
| primary | `#5e6ad2` | 0.84 |
| border-subtle | `#e8e9ec` | 0.79 |

Pass 2 (`prefers-color-scheme: dark`):

| Role | Hex | Confidence |
|---|---|---|
| background | `#08090a` | 0.92 |
| surface | `#1a1d23` | 0.81 |
| on-surface | `#ffffff` | 0.95 |
| primary | `#7a85e6` | 0.86 |
| border-subtle | `#26282d` | 0.79 |

Paired output:

```yaml
extensions:
  schemes:
    default: "light"
    light:
      colors:
        background: "#ffffff"
        surface: "#f7f7f8"
        on-surface: "#0c0e12"
        primary: "#5e6ad2"
        border-subtle: "#e8e9ec"
    dark:
      colors:
        background: "#08090a"
        surface: "#1a1d23"
        on-surface: "#ffffff"
        primary: "#7a85e6"
        border-subtle: "#26282d"
```

Prose note: "Dark-mode primary (`#7a85e6`) is a lightened variant of light-mode primary (`#5e6ad2`) — both have hue ≈ 245°, the dark version is +0.15 lightness for legibility on the near-black background."

## Breaks if

- **Site uses `prefers-color-scheme` only for the initial scheme, then locks via JS** — CDP `Emulation.setEmulatedMedia` switches the media query but the page-state machine ignores the change after first load. Detect by sampling `document.documentElement.dataset.theme` before AND after emulation; if unchanged, fall back to clicking a theme-toggle button by label.
- **The dark mode is themed per-component, not per-site** — some sites apply dark mode only to documentation but keep the marketing site light. The extracted dark snapshot will still contain the original landmark elements — pairing works but the resulting DESIGN.md misrepresents intent. Record `warnings: ["dark scheme observed but page chrome is light; partial dark mode site"]`.
- **Theme JS runs only on user-interaction** (not on `MediaQueryList.change`) — the emulation flips the media query but the page never re-applies the theme. Detect by sampling `:root` CSS variables before/after; if `--background` is unchanged, the emulation is being ignored. Click the toggle button instead.
- **The page has 3+ schemes** — "system / light / dark / high-contrast" or "auto / light / dim / dark" (GitHub). The pairing algorithm only handles a binary axis. Detect via the presence of multiple `@media (prefers-*)` queries OR a toggle button with 3+ options. Capture only `light` + `dark` and warn.
- **Pairing by role fails when role assignments differ between passes** — the color-role inference may assign `tertiary` in light mode and `accent` in dark mode for the same underlying brand color. Record both assignments and reconcile via prose ("this color appears as `tertiary` in light, `accent` in dark — likely the same role").
- **The cache holds the pre-emulation render** — reload between passes (`page.reload({waitUntil: "networkidle"})`). Without reload, the dark-mode pass renders cached light-mode CSS.

## Cross-references

- [TECH-extractor-color-role-inference](./TECH-extractor-color-role-inference.md) — algorithm run twice (one per scheme); produces the role maps this pass joins
- [TECH-07-url-extraction](./TECH-07-url-extraction.md) — base single-pass extraction flow this technique calls twice
- [TECH-extractor-pseudo-element-extraction](./TECH-extractor-pseudo-element-extraction.md) — interaction states are scheme-dependent too; can be combined for full coverage
- [TECH-02-color-tokens](./TECH-02-color-tokens.md) — see "Light + dark mode token pairs" — the authoring side of the same problem
- [extension-sections-10-14](./extension-sections-10-14.md) — where the `extensions.schemes` namespace lives in DESIGN.md
- `../../../bin/amw-design-md-from-url.sh` — bin script that hosts this pass
- `../../../bin/amw-dev-browser-wrapper.sh` — browser primitive used internally
- [amw-design-md-extractor-agent](../../../agents/amw-design-md-extractor-agent.md) — the agent that owns this flow
- Upstream reference: GPL-licensed `design-extractor-skill` (algorithm only; clean-room reimplementation)
