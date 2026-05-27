---
name: TECH-variant-hard-constraints
category: design-principles-process
source: Bexa design-principles cluster (direct port, batch9 Wave 2 Round 2, T-051)
license: MIT (Bexa upstream is MIT; plugin re-licenses under its own MIT — see ../../../LICENSE)
also-in: TECH-brand-color-by-product.md (the hue table that seeds variant primaries); TECH-tone-archetypes.md (the 11 visual archetypes that map to preset clusters); three-hard-rules.md (rule 2: always 3 variants)
---

# Variant hard constraints

## Table of Contents

- [What it does](#what-it-does)
- [The problem this solves](#the-problem-this-solves)
- [The three hard constraints](#the-three-hard-constraints)
  - [C1. Primary hue ≥60° apart](#c1-primary-hue-60-apart)
  - [C2. Display fonts in ≥2 font categories](#c2-display-fonts-in-2-font-categories)
  - [C3. Density ratio ≥1.5× between most and least dense variant](#c3-density-ratio-15-between-most-and-least-dense-variant)
- [How amw-ascii-sketch steers variant generation](#how-amw-ascii-sketch-steers-variant-generation)
- [The "fake variants" failure mode](#the-fake-variants-failure-mode)
- [Worked example: 3 variants for a fintech landing page](#worked-example-3-variants-for-a-fintech-landing-page)
- [Validation](#validation)
- [Cross-references](#cross-references)

## What it does

The three-hard-rules of `amw-design-principles` mandate "always produce at least three variants" (rule 2). This file makes that rule **verifiable** by defining three concrete, measurable constraints every variant trio must satisfy.

Without this file, "3 variants" can degenerate into 3-versions-of-the-same-design with tiny tweaks. With this file, each of the 3 variants is forced to occupy a measurably different region of the design space — the trio gives the user a genuine choice instead of three points clustered around one local optimum.

Consumed primarily by:
- `skills/amw-ascii-sketch/SKILL.md` — variant generator
- `agents/ai-maestro-webdesign-main-agent.md` — Phase A orchestrator that validates the 3 variants before showing them to the user
- `agents/amw-wireframe-builder-agent.md` — Phase B emitter that may carry the 3 variants forward into 3 HTML mockups

## The problem this solves

Default LLM behavior, when asked for "3 variants", is to produce one design and then tweak `--accent-hue` by 30° and `--padding-y` by 8px in the second and third. The user looking at the trio cannot tell them apart in 5 seconds; the variant exercise becomes theatre.

Genuine design exploration requires variants that are **categorically different** — different brand hue, different typographic register, different content density. A user looking at a true 3-variant trio in 5 seconds should be able to say "the first one is the cautious one, the second is the magazine-style one, the third is the playful one" — without reading any of the body copy.

The three constraints below operationalise that requirement.

## The three hard constraints

### C1. Primary hue ≥60° apart

**Rule.** Across the 3 variants, the primary brand accents must occupy hues that are at least **60 degrees apart** on the HSL color wheel.

**Why 60°.** Smaller hue gaps (≤30°) read as "the same color in three shades". 60° is the threshold where the eye registers two hues as *distinct colors*, not as adjacent variations. Three hues at 60°+ separation on a 360° wheel typically land in three different psychological color families (e.g., blue, green-yellow, magenta).

**How to satisfy.** Pick the seed hue from `TECH-brand-color-by-product.md`'s product-type table. Generate the other two variants at +120° and +240° around the wheel (or use any other rotation that lands in 3 different rows of the product-type table).

**Verification.**
```
abs(H1 - H2) >= 60 AND abs(H2 - H3) >= 60 AND abs(H1 - H3) >= 60
```
where hue subtraction is computed modulo 360 (the shortest arc).

**Exception.** Monochrome brand requirements (the brief mandates "must be black + white only"). In that case, C1 is satisfied by varying SATURATION (one variant fully grayscale, one with a single saturated accent at 5% coverage, one with a single saturated accent at 15% coverage) instead of hue.

### C2. Display fonts in ≥2 font categories

**Rule.** Across the 3 variants, the display typeface must span at least **2 of the 4 font categories**:

1. **Serif** (Old-style, Transitional, Modern/Didone, Slab)
2. **Sans-serif** (Geometric, Humanist, Neo-grotesque, Rounded)
3. **Mono** (Typewriter, Geometric mono, Slab mono)
4. **Display/Special** (Handwritten, Script, Display-only, Pixel-bitmap)

**Why ≥2 categories.** Picking all 3 display fonts from "sans-serif" (Inter, Geist, DM Sans, all Neo-grotesque or Humanist) produces 3 variants that read as typographically identical. Spanning 2+ categories forces a real typographic decision: at least one variant feels structurally different in its lettering.

**How to satisfy.** Two acceptable patterns:

- **2-1 split.** Two variants share one category (say sans-serif), the third variant uses a different category (say serif). Often the cleanest result — variants 1 and 2 are sibling explorations within sans, variant 3 is a serif outlier for contrast.
- **1-1-1 split.** Each variant uses a different category. Stronger differentiation but harder to maintain coherence — the user often picks one variant cleanly because the other two feel too far apart in register.

**Verification.** Track display-font category in the variant metadata. Reject any trio where `len(set(categories)) < 2`.

**Body fonts** are not constrained — they can share the same family across all 3 variants (commonly a Neo-grotesque like Inter or system stack) because body legibility constraints push every variant toward similar choices. The constraint is on **display fonts**, where personality lives.

### C3. Density ratio ≥1.5× between most and least dense variant

**Rule.** Compute information density per variant. The densest variant must be **at least 1.5× as dense** as the least dense variant.

**Why a density ratio.** Without this constraint, all 3 variants get the same component count, same spacing scale, same number of CTAs, same depth of nav. The result reads as 3 versions of one layout. Forcing a 1.5× ratio means one variant is "stripped down" (luxury / minimal) and one is "dense" (editorial / dashboard), with the third somewhere between — the user gets a meaningful density choice.

**How to measure density.** Two acceptable proxies:

- **Component count proxy.** Count distinct interactive components visible above-the-fold (buttons, cards, inputs, navigation items, tabs, badges, links-as-CTAs). Density ratio = `max(counts) / min(counts)`.
- **Token-spacing proxy.** Multiply (1 / spacing-unit-base) × (number-of-grid-columns). Higher = denser. Density ratio = `max / min`.

The component-count proxy is simpler and usually sufficient. If three variants score (above-the-fold component counts) of 8, 12, 18, the ratio is 18/8 = 2.25× ≥ 1.5 ✓.

**Verification.** Compute and log the density score for each variant; reject the trio if ratio < 1.5.

**Edge case.** Pages where density is intrinsically constrained (login form, error page, 404). The 1.5× rule still applies but the proxies are weakened — pick the closest-feasible density spread and document the constraint in the variant metadata.

## How amw-ascii-sketch steers variant generation

`skills/amw-ascii-sketch/SKILL.md` is the plan-phase variant generator. This file is one of its primary input constraints.

The generator workflow that satisfies all 3 constraints:

1. **Pull seed hue** from `TECH-brand-color-by-product.md` based on product type.
2. **Pick visual archetype** from `TECH-tone-archetypes.md` (one archetype gets 3 preset variants under it, or one archetype-pair is chosen so the trio spans two clusters).
3. **Assign per-variant hue offsets:**
   - Variant 1: seed hue
   - Variant 2: seed hue + 120° (mod 360)
   - Variant 3: seed hue + 240° (mod 360)
   then snap each to the closest hue allowed for the product type — if the offset lands in an out-of-range hue, pick the nearest in-range one within ±30°.
4. **Assign per-variant display-font categories:**
   - Variant 1: closest match to archetype preference
   - Variant 2: variant-1's category OR adjacent category
   - Variant 3: a different category from variants 1 and 2
5. **Assign per-variant density targets:**
   - Variant 1: archetype baseline density (medium)
   - Variant 2: archetype baseline × 0.7 (strip down)
   - Variant 3: archetype baseline × 1.5 (compress)
6. **Generate the 3 ASCII variants** with these constraints baked in.
7. **Self-validate** against C1, C2, C3 before showing the user. If any constraint fails, regenerate the failing variant.

## The "fake variants" failure mode

This file exists to block a specific failure: **three variants that all look like the same design with knobs tweaked**. Symptoms of fake variants:

- All 3 share the primary brand accent (only saturation or shade differs) → violates C1.
- All 3 use the same display font, just at different weights → violates C2.
- All 3 have the same component count and spacing → violates C3.

If the orchestrator catches any of these symptoms — either via the verifications above, or in a self-review pass — it regenerates the offending variant. The user must never see a fake-variant trio.

A symptom check the orchestrator runs:

```
fake_trio_score = 0
if not C1_satisfied: fake_trio_score += 1
if not C2_satisfied: fake_trio_score += 1
if not C3_satisfied: fake_trio_score += 1
if fake_trio_score > 0: regenerate
```

## Worked example: 3 variants for a fintech landing page

Product type: fintech (per `TECH-brand-color-by-product.md` row 5 — deep green hsl(155–165, 50–65%)).
Archetype: editorial-magazine (per `TECH-tone-archetypes.md` archetype 7).

Seed hue: hsl(160, 60%, 35%) — deep teal-green.

**Variant 1: Trust-conservative.**
- Primary: `hsl(160, 60%, 35%)` — the seed deep green.
- Display font: Inter Tight (sans-serif, Neo-grotesque).
- Density: 12 above-the-fold components (baseline).

**Variant 2: Magazine-bold.**
- Primary: `hsl(160 + 120 = 280, 55%, 40%)` — purple. Out of fintech range → snap to nearest in-range: hsl(220, 60%, 40%) deep blue (fintech-adjacent but distinct from variant 1). Hue gap from variant 1: 60°. ✓ (≥60°)
- Display font: GT Sectra (serif, Modern/Didone).
- Density: 18 components (compressed, magazine-style; 1.5× variant 1).

**Variant 3: Confident-minimal.**
- Primary: `hsl(160 + 240 = 40, 60%, 50%)` — orange. Out of fintech range → snap to in-range monochrome (no saturated accent at all). Use grayscale + tiny green from variant 1 at 3% coverage.
- Display font: JetBrains Mono (mono, Geometric mono).
- Density: 8 components (stripped; 0.66× variant 1).

Verification:
- C1: Hues are 160° green, 220° blue, 0° grayscale-with-touch-of-160. Gaps: 60°, 160°, 160°. ✓
- C2: Categories are sans-serif, serif, mono — 3 different categories. ✓
- C3: Counts are 12, 18, 8. Ratio = 18/8 = 2.25× ≥ 1.5. ✓

Trio passes. Shown to the user.

## Validation

When `amw-ascii-sketch` emits the 3-variant trio, it includes a metadata block at the top of each variant. Example:

```
# Variant 1: Trust-conservative
# - hue: hsl(160, 60%, 35%)
# - display-font-category: sans-serif
# - density: 12 (baseline)
# - archetype: editorial-magazine
```

The orchestrator parses these blocks and runs the C1/C2/C3 checks mechanically before showing the variants to the user. Failed checks trigger regeneration; passed checks proceed to the user-facing variant gallery.

Future hardening (Wave 3): add a `bin/amw-validate-variants.py` that takes 3 ASCII variant files and emits a PASS/FAIL with which constraint failed. Until then, the orchestrator runs the check in-prompt.

## Cross-references

- [three-hard-rules.md](./three-hard-rules.md) — Rule 2 mandates "always produce at least three variants"; this file makes the rule verifiable
- [TECH-brand-color-by-product.md](./TECH-brand-color-by-product.md) — supplies the seed hue and constrains C1's hue rotation
- [TECH-tone-archetypes.md](./TECH-tone-archetypes.md) — supplies the archetype + preset cluster that anchors all 3 variants
- [TECH-brand-voltage.md](./TECH-brand-voltage.md) — each variant's accent count must satisfy voltage independently
- [skills/amw-ascii-sketch/SKILL.md](../../amw-ascii-sketch/SKILL.md) — variant generator constrained by this file
- [skills/amw-design-system-presets/references/catalogue.md](../../amw-design-system-presets/references/catalogue.md) — 45 graphic presets from which variants draw
- [agents/ai-maestro-webdesign-main-agent.md](../../../agents/ai-maestro-webdesign-main-agent.md) — Phase A orchestrator that validates the trio before user delivery
- [agents/amw-wireframe-builder-agent.md](../../../agents/amw-wireframe-builder-agent.md) — Phase B emitter that may carry approved variants forward to HTML
- [skills/amw-design-principles/ai-slop-avoid.md](../ai-slop-avoid.md) — bans the "3 versions of the same design" pattern this file structurally prevents
- [skills/amw-design-principles/SKILL.md](../SKILL.md) — orchestrator
