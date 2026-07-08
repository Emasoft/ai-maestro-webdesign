---
name: amw-design-remix
description: >-
  Reskin an extracted design in a named graphic vocabulary (from the
  amw-design-system-presets catalogue) OR rotate OKLCH hue around a new brand
  primary while preserving chroma/lightness ramps. Activates on narrow remix triggers — "remix this in
  <style>", "reskin in brutalist", "rotate hue to <new primary>", "convert
  palette to OKLCH around <color>", "swap theme to swiss", "art-deco variant
  of this site". Does NOT activate on broad design vocabulary ("design a
  page", "build a UI") — those route to amw-design-principles.
author: ai-maestro-webdesign (clean-room)
---

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Triggers are remix-specific only — `amw-design-principles` routes here when the user has an existing design (tokens, DESIGN.md, or extracted bundle) and wants to see it in a different visual vocabulary. For initial design from scratch use `amw-design-principles` + `amw-design-system-presets`. For audit see `amw-design-grade`.

## Overview

`amw-design-remix` takes an existing design's tokens and produces a NEW token bundle in a target visual vocabulary, plus a render-test page showing the result. Two remix modes are supported:

1. **Named-vocabulary remix.** The user picks a style from the `amw-design-system-presets` catalogue (Swiss, Brutalist, Art Deco, Cyberpunk, Soft UI, Editorial, etc.). The skill swaps in that preset's token block while preserving the artifact's CONTENT structure (sections, copy, component instances).
2. **OKLCH hue rotation.** The user supplies a new brand primary colour and the skill rotates the entire palette around the new hue while preserving chroma and lightness ramp structure. This is the lightweight remix path — same vocabulary, new identity.

Both modes preserve the original artifact's structural content (HTML/wireframe). They differ only in WHAT they swap (named vocabulary swaps tokens AND structural defaults like radius/shadow/motion; hue rotation swaps only colour tokens).

## Inputs

EXACTLY ONE source design + ONE remix target.

**Source design** can be:

- An existing `DESIGN.md` (canonical or community variant)
- A `designlang` extraction JSON from `amw-design-extract`
- A live URL (fetched via `amw-dev-browser`; tokens derived from computed styles)
- A local HTML file with token-driven CSS

**Remix target** is ONE of:

- A named style ID from `amw-design-system-presets` (e.g. `S-001 Swiss`, `S-002 Brutalism`, `S-028 Art Deco`)
- A named style description string ("brutalist", "swiss", "art deco", "cyberpunk", "soft-ui", "editorial") — the skill resolves to the catalogue entry
- A new OKLCH primary colour (e.g. `oklch(60% 0.15 240)` or the hex `#3b82f6`)

When the user supplies BOTH a named style AND a new primary colour, both are applied: named style sets structural tokens (radius, shadow, motion, type) AND a palette skeleton; the user-supplied primary then drives the hue rotation atop the preset's chroma/lightness structure.

## The two remix modes

The detailed technical contract for both modes lives in [TECH-theme-swap](references/TECH-theme-swap.md). Load that file before any remix. Summary here:
> [TECH-theme-swap.md] Mode 1 — Named-vocabulary remix · Mode 2 — OKLCH hue rotation · Combined Mode 1 + Mode 2 · Render-test contract · Anti-patterns (do not do) · Versioning

### Mode 1 — Named-vocabulary remix

1. **Identify the target style.** Read [catalogue](../amw-design-system-presets/references/catalogue.md) to confirm the style ID. If the user supplied a description only (e.g. "make it brutalist"), match to the closest catalogue entry and confirm with the user before continuing.
2. **Load the preset's token block.** Read the full `S-NNN-<slug>.md` file. The Token Block section is the authoritative source for the new bundle.
3. **Identify which source tokens to preserve.** The source design's BRAND identity (logo wordmark colour, brand name typography if it is part of the wordmark, registered colour like Coca-Cola red) overrides the preset. Other source tokens (component colours, body text, accents) are REPLACED by the preset's tokens.
4. **Emit the merged bundle.** Output is a complete token set: preset tokens + preserved brand tokens, with conflicts resolved in favour of brand tokens per `amw-design-system-presets/SKILL.md` non-negotiable §5.
5. **Verify the preset's "breaks-if" invariants.** Each preset has invariants (e.g. Swiss "breaks if border-radius exceeds 4px"). Scan the merged bundle and flag any preserved brand tokens that violate them. Warn the user explicitly.
6. **Render the test page.** Inject the merged bundle into `amw-design-system-presets/references/_test-skeleton.html` and emit the result.

### Mode 2 — OKLCH hue rotation

1. **Parse the source palette into OKLCH.** Convert every colour token (`--color-primary`, `--color-accent`, all ramp steps, semantic colours) into OKLCH triples (lightness, chroma, hue). The skill MUST parse hex, rgb, hsl, and OKLCH input.
2. **Detect the source primary hue.** Either the user names which token is "primary" or the skill picks the highest-chroma chromatic token as the primary.
3. **Compute hue delta.** `delta = target_primary_hue - source_primary_hue`. This is the rotation amount in degrees.
4. **Rotate every chromatic token by delta.** For each colour token, add `delta` to its hue (mod 360). Preserve lightness and chroma exactly. Neutral tokens (low-chroma greys, pure white, pure black) are NOT rotated — they stay neutral.
5. **Re-clamp into the in-gamut OKLCH space.** Some rotations push a colour out of the displayable sRGB or P3 gamut. Re-clamp by reducing chroma incrementally (1% steps) until the colour is in-gamut. Record any clamping in the report.
6. **Emit the rotated bundle + render-test page.**

The hue-rotation mode preserves the source design's structural identity (typography, spacing, motion, radius, shadow) entirely — only colour changes.

## Workflow

1. **Determine remix mode.** If the user named a style (catalogue entry), Mode 1. If the user supplied a colour, Mode 2. If both, Mode 1 with the user's colour driving the palette swap atop the preset's structure.
2. **Load source tokens.** Parse the source artifact (DESIGN.md, JSON, URL, or HTML) into a canonical internal token shape.
3. **Run the remix algorithm** (Mode 1 or 2 per above, fully specified in [TECH-theme-swap](references/TECH-theme-swap.md)).
4. **Verify invariants** (Mode 1: the preset's "breaks-if" rules; Mode 2: WCAG-AA contrast on the rotated palette).
5. **Emit deliverables.**

## Output shape

Four files written to the user's working directory (or a path the user specifies):

- `remix-tokens.css` — the new bundle as CSS custom properties (drop-in replacement for the source `--color-*`, `--font-*`, `--spacing-*` etc.)
- `remix-tokens.json` — same bundle as JSON for programmatic consumption (matches the shape produced by `amw-design-extract`)
- `remix-render-test.html` — the test skeleton populated with the new bundle (visual proof the remix renders coherently)
- `remix-report.md` — what was swapped, what was preserved, any clamping, any invariant warnings

The `remix-tokens.json` shape:

```json
{
  "remix_mode": "named-vocabulary | hue-rotation",
  "source": {
    "type": "design.md | extract | url | html",
    "ref": "<source>",
    "primary_hue_oklch": 264.0
  },
  "target": {
    "style_id": "S-001",        // when Mode 1
    "style_name": "Swiss",       // when Mode 1
    "primary_hex": "#3b82f6",    // when Mode 2
    "primary_hue_oklch": 240.0   // when Mode 2
  },
  "delta_degrees": -24.0,        // when Mode 2
  "preserved_brand_tokens": [    // when Mode 1
    { "token": "--brand-logo-color", "value": "#ff0000", "reason": "registered brand colour" }
  ],
  "invariant_warnings": [        // when Mode 1
    "Swiss preset breaks if border-radius exceeds 4px; preserved brand --radius-card=8px violates this. Recommend resolving."
  ],
  "clamped_tokens": [            // when Mode 2
    { "token": "--color-accent-12", "original_oklch": "65% 0.32 30", "clamped_oklch": "65% 0.24 30", "reason": "out of sRGB gamut" }
  ],
  "tokens": {
    "--color-bg": "...",
    "--color-text": "...",
    /* full token set */
  },
  "files": {
    "css": "<path>",
    "json": "<path>",
    "html": "<path>",
    "md": "<path>"
  }
}
```

## Non-negotiables

1. **The catalogue is canonical for Mode 1.** Read [catalogue](../amw-design-system-presets/references/catalogue.md) to resolve the target style. Do NOT remix into an unnamed "brutalist-like" thing from memory — pick the catalogue entry.
2. **Brand tokens override preset tokens** (Mode 1). The source design's wordmark colour, brand-name font, and other identity-defining tokens are PRESERVED. The preset fills the structural slots (radius, shadow, motion, scale).
3. **OKLCH preservation in Mode 2.** Lightness and chroma are preserved per-token; only hue rotates. Neutrals stay neutral.
4. **Gamut clamping is required, not optional.** If any rotated colour exits sRGB or P3, clamp chroma down. Record the clamp.
5. **WCAG-AA after rotation.** After Mode 2, re-check body/UI text contrast on the rotated backgrounds. If contrast drops below 4.5:1 anywhere, REPORT it explicitly and recommend lightness adjustments. Do NOT silently emit a palette that breaks AA.
6. **Invariant warnings are explicit.** Mode 1 must scan against the preset's "breaks if" list. Each violation is a warning in the report; do NOT suppress them.
7. **Render-test before delivery.** Every remix MUST produce the test-skeleton render. The user inspects it; if the visual doesn't match the target vocabulary, the remix is rejected and the user iterates.
8. **No re-implementation of catalogue logic.** All structural defaults (radius, shadow, motion, type scale) come from the named preset's S-NNN file. Do NOT invent values not in the catalogue.

## When to recommend a different skill

- **No source design yet, want to design from scratch** → `amw-design-principles` + `amw-design-system-presets`
- **Audit the existing design first** → `amw-design-grade`
- **Compare two designs head-to-head** → `amw-design-battle`
- **Just want to extract tokens from a URL** → `amw-design-extract`
- **Want to lint a DESIGN.md** → `amw-design-md`

## Resources

- [TECH-theme-swap](references/TECH-theme-swap.md) — full Mode 1 and Mode 2 algorithms, OKLCH math, gamut clamping, brand-token preservation rules
> [TECH-theme-swap.md] Mode 1 — Named-vocabulary remix · Mode 2 — OKLCH hue rotation · Combined Mode 1 + Mode 2 · Render-test contract · Anti-patterns (do not do) · Versioning
- The named-vocabulary catalogue: [catalogue](../amw-design-system-presets/references/catalogue.md)
> [catalogue.md] How the author-agent uses this · Index — 45 styles across 8 aesthetic positions · Selecting styles — quick decision rules · Wave 2 — Round 4 additions (S-010b, S-046..S-083)
- The render-test scaffold: [`amw-design-system-presets/references/_test-skeleton.html`](../amw-design-system-presets/references/_test-skeleton.html)
- Input pipelines: [`amw-design-extract`](../amw-design-extract/SKILL.md), [`amw-design-md`](../amw-design-md/SKILL.md), [`amw-dev-browser`](../amw-dev-browser/SKILL.md)
- Companion remix-adjacent skills: [`amw-design-grade`](../amw-design-grade/SKILL.md), [`amw-design-battle`](../amw-design-battle/SKILL.md)
