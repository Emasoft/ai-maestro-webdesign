# TECH — CSS-Variable Discipline (colors via tokens, never raw Tailwind classes)

**License:** Apache-2.0 direct-port (adapted from upstream design-token-discipline guidance).
**Audience:** `amw-wireframe-builder-agent` (primary), `amw-infographic-builder-agent`, `amw-email-designer-agent`, `amw-component-library-architect-agent`, `amw-design-md-author-agent`.
**Purpose:** Every HTML artifact the plugin emits uses CSS custom properties (CSS variables) for ALL color values, sourced from the project's DESIGN.md token block. Raw Tailwind color utilities (`bg-blue-500`, `text-purple-600`, `border-zinc-300`, etc.) are NOT allowed. This makes every artifact theme-portable, brand-agnostic, and re-skinnable without touching markup.

Tailwind is still used — for layout, spacing, typography utilities — but its color utilities are off-limits. The discipline is: **Tailwind for geometry, CSS variables for chroma.**

---

## The rule (mechanical)

A generated HTML artifact passes the discipline check if and only if:

1. No `class="..."` attribute contains a Tailwind color utility matching the regex `\b(bg|text|border|ring|divide|outline|fill|stroke|from|via|to|placeholder|caret|accent|decoration|shadow)-(slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-(50|100|200|300|400|500|600|700|800|900|950)\b`.
2. No `class="..."` attribute contains `bg-white`, `bg-black`, `text-white`, `text-black`, or any other shortcut alias to a non-token color.
3. Every color used in markup or `<style>` is either (a) `var(--token-name)` referencing a DESIGN.md token, or (b) a literal hex/rgb explicitly justified in the `data-amw-color-source` attribute on the element (rare — see "Justified literals" below).

`bin/amw-ai-slop-check.py` runs this check; the check is also surfaced as `[RULE-CSS-VARS]` in `TECH-override-policy.md`.

---

## Why this rule exists (the four arguments)

### Argument 1 — Theme portability

A page built with `bg-blue-500` is hard-coded to one palette. A page built with `bg-[var(--primary)]` is themable by changing 4 lines of CSS in `:root`. Themes are the single most-requested customization after a page ships; the time saved by token-discipline at authoring pays for itself within a week.

### Argument 2 — Brand-agnosticism

The plugin produces output for many users with many brands. Tailwind's `blue-500` is a specific blue with specific corporate associations (some users will recognize it as a Twitter / Telegram blue). Token names like `--primary` carry no such association — they let the brand assert itself instead of borrowing Tailwind's defaults.

### Argument 3 — Slop-detection avoidance

Tailwind's default palette is the single most-recognized "I didn't customize this" signal on the modern web. The combination `bg-blue-500 + bg-purple-600 + text-zinc-300` is the canonical AI-slop palette. Raw Tailwind color classes are the visible fingerprint of "auto-generated landing page". Token discipline removes the fingerprint.

### Argument 4 — DESIGN.md round-trip

The DESIGN.md → tokens.css → markup pipeline (see `bin/amw-design-md-emit-companions.py`) only works if the markup is the LAST hop. If the markup hard-codes Tailwind colors, the DESIGN.md tokens are not the source of truth — the markup is. This breaks every downstream extractor (`amw-design-md-extractor-agent`), every audit pass (`amw-design-md-auditor-agent`), and every regeneration of the artifact.

---

## Before / after (the canonical example)

### BEFORE — slop

```html
<section class="bg-blue-500 text-white p-8 rounded-lg shadow-lg">
  <h2 class="text-2xl font-bold mb-4">Welcome</h2>
  <p class="text-blue-100 mb-6">Track your sleep score this week.</p>
  <button class="bg-white text-blue-700 px-6 py-3 rounded-md hover:bg-blue-50">
    Get started
  </button>
</section>
```

Every color is a Tailwind utility. The page reads as default-blue-Tailwind to any experienced eye.

### AFTER — token-disciplined

```html
<section
  class="p-8 rounded-lg shadow-lg"
  style="background: var(--primary); color: var(--ink-on-primary);"
>
  <h2 class="text-2xl font-bold mb-4">Welcome</h2>
  <p class="mb-6" style="color: var(--ink-on-primary-soft);">
    Track your sleep score this week.
  </p>
  <button
    class="px-6 py-3 rounded-md transition-colors"
    style="background: var(--surface-1); color: var(--primary-strong);"
    onmouseover="this.style.background='var(--surface-2)'"
    onmouseout="this.style.background='var(--surface-1)'"
  >
    Get started
  </button>
</section>
```

Layout, spacing, radius, shadow, typography size + weight = Tailwind utilities (`p-8 rounded-lg shadow-lg text-2xl font-bold mb-4 px-6 py-3 rounded-md`). Every color = a CSS variable.

### The companion `:root` block

The variables resolve in `:root` (or `[data-theme="..."]` for multi-theme support):

```css
:root {
  --primary:             #2d4a7c;
  --primary-strong:      #1f3458;
  --surface-1:           #faf7f2;
  --surface-2:           #f0ebe1;
  --ink-on-primary:      #faf7f2;
  --ink-on-primary-soft: rgba(250, 247, 242, 0.78);
}

[data-theme="dark"] {
  --primary:             #5e7fb8;
  --primary-strong:      #87a3d6;
  --surface-1:           #1a1c20;
  --surface-2:           #23262c;
  --ink-on-primary:      #1a1c20;
  --ink-on-primary-soft: rgba(26, 28, 32, 0.78);
}
```

Switching theme = changing `data-theme` on `<html>`. Zero markup edits.

---

## What Tailwind IS still used for

Token discipline applies to color utilities ONLY. The rest of Tailwind stays useful:

| Use Tailwind for | Examples |
|---|---|
| Layout | `flex`, `grid`, `grid-cols-12`, `gap-4`, `items-center`, `justify-between` |
| Spacing | `p-8`, `m-4`, `px-6`, `py-3`, `space-y-4` |
| Sizing | `w-full`, `max-w-7xl`, `min-h-screen`, `aspect-square` |
| Typography (non-color) | `text-2xl`, `font-bold`, `leading-tight`, `tracking-tight` |
| Radius / shadow shape | `rounded-md`, `rounded-lg`, `shadow-sm`, `shadow-lg` (but the shadow COLOR comes from a token via `[box-shadow]` inline if tinted — see `TECH-named-color-shadow-techniques.md` §1) |
| Position | `relative`, `absolute`, `top-0`, `inset-x-0` |
| Responsive prefixes | `md:grid-cols-3`, `lg:p-12` |
| State prefixes | `hover:scale-x-100`, `focus-visible:ring-2` |
| Animation utilities | `transition-colors`, `duration-200`, `ease-out` |

This is roughly 80% of Tailwind. The 20% that's banned is exactly the color-utility palette.

---

## The 5 Tailwind utilities that are STILL fine despite the regex

A small set of color-adjacent utilities pass the discipline check because they don't reference the palette:

- `bg-transparent` — semantic, not a color.
- `bg-current` — inherits from `color`, which is itself token-bound.
- `bg-inherit` — semantic.
- `text-transparent` — used for gradient text effects with `bg-clip-text`.
- `text-inherit` / `text-current` — semantic.

These are allowed. Everything else in the palette regex is not.

---

## Justified literals (the rare escape hatch)

Sometimes a literal color is genuinely correct — usually for third-party brand marks (a `#1877F2` Facebook button) or for precise control of a one-off illustration. The escape hatch is:

```html
<button
  class="px-4 py-2 rounded-md"
  style="background: #1877F2;"
  data-amw-color-source="facebook-brand-blue-2018-spec"
>
  Continue with Facebook
</button>
```

The `data-amw-color-source` attribute documents WHY the literal is there. The discipline checker allows literals only when the attribute is present and non-empty.

Allowed `data-amw-color-source` values:
- `facebook-brand-blue-2018-spec`, `google-brand-blue-spec`, `apple-button-black`, etc. — third-party brand specs.
- `chart-categorical-1` through `chart-categorical-N` — data-viz color scales (palette tokens exist but the chart owns the scale).
- `decorative-mesh-layer-N` — radial-gradient mesh stops (see `TECH-named-color-shadow-techniques.md` §3).
- `print-only` — colors used only in PDF/print exports.

Any other value triggers the slop check.

---

## How the discipline interacts with shadcn/ui

shadcn components ship CSS variables already (`--background`, `--foreground`, `--primary`, `--primary-foreground`, etc.). The plugin's discipline is COMPATIBLE with shadcn: use shadcn's variable names when working in a shadcn-based project, OR map DESIGN.md tokens to shadcn names via the companion CSS:

```css
:root {
  /* DESIGN.md tokens */
  --primary:             #2d4a7c;
  --surface-1:           #faf7f2;
  --ink-strong:          #1a1c20;

  /* shadcn aliases (so shadcn components inherit our tokens) */
  --background:          var(--surface-1);
  --foreground:          var(--ink-strong);
  --primary:             var(--primary);                   /* shadcn name == ours */
  --primary-foreground:  var(--ink-on-primary);
}
```

shadcn-aware artifacts re-use the shadcn variable names directly. DESIGN.md-from-scratch artifacts use the broader DESIGN.md naming. Either is acceptable; mixing is not.

---

## How `amw-wireframe-builder-agent` enforces this

The wireframe-builder-agent's step 6 (final HTML emission) MUST:

1. Reject any class attribute matching the Tailwind color regex (above) BEFORE writing the file.
2. Resolve every color to either a `var(--token)` reference or a justified literal with `data-amw-color-source`.
3. Emit a `:root` companion CSS block at the top of `<style>` containing every variable referenced in markup.
4. Verify variable-completeness: every `var(--X)` reference in markup MUST have a matching definition in `:root`. The build fails otherwise.
5. Run `bin/amw-ai-slop-check.py` and fix any flagged literals.

Cross-reference: `agents/amw-wireframe-builder-agent.md` step 6 — final HTML emission — invokes this discipline as a hard gate before file write.

---

## Common mistakes (and the fix)

| Mistake | Fix |
|---|---|
| `class="bg-blue-500"` | `style="background: var(--primary)"` + define `--primary` in `:root` |
| `class="text-zinc-700"` | `style="color: var(--ink-strong)"` |
| `class="border-gray-200"` | `style="border-color: var(--border-soft)"` |
| `class="hover:bg-blue-600"` | inline JS `onmouseover` / `onmouseout` with `var(--primary-strong)`, OR a `<style>` block with `:hover` rules using the token |
| `class="bg-white text-black"` | `style="background: var(--surface-1); color: var(--ink-strong)"` (DESIGN.md tokens, not literal `#fff`/`#000`) |
| `class="shadow-lg"` (with default black) | `class="shadow-lg" style="--tw-shadow-color: var(--shadow-tint-primary)"` OR replace `shadow-lg` with a custom `box-shadow` using a tinted token |
| Hex literal in `<style>` (no `data-amw-color-source`) | Add the token to `:root`, replace literal with `var(--token)`, OR add `data-amw-color-source` if genuinely a one-off |
| `<svg fill="#3b82f6">` | `<svg fill="var(--primary)">` (CSS variables work in SVG `fill`/`stroke` since ~2018) |

---

## Anti-patterns (do NOT do)

- Defining tokens but still using Tailwind color classes in 50% of the markup. The discipline is binary — either ALL colors are tokens, or none are. Mixed mode produces the worst of both.
- Inventing token names ad-hoc per-page (`--my-blue`, `--my-purple`). Token names come from DESIGN.md's vocabulary. Inventing local names defeats portability.
- Using `data-amw-color-source` as a blanket bypass. The attribute is for genuinely-third-party or genuinely-decorative literals. Using it on every literal to skip the rule = silent slop.
- Putting `:root` variables in an external CSS file the user has to manually load. For single-file artifacts (the canonical plugin output), the `:root` block lives in an inline `<style>` at the top of the file.

---

## Cross-references

- `agents/amw-wireframe-builder-agent.md` — step 6 enforces this discipline.
- `TECH-override-policy.md` — `[RULE-CSS-VARS]` is the numbered MUST rule.
- `TECH-named-color-shadow-techniques.md` — the techniques that consume these tokens.
- `bin/amw-design-md-emit-companions.py` — generates `:root` tokens.css from DESIGN.md.
- `bin/amw-ai-slop-check.py` — mechanical enforcement check.
- `skills/amw-design-md/` — the source of truth for the token vocabulary.
- `skills/amw-design-principles/ai-slop-avoid.md` — broader slop catalog.
