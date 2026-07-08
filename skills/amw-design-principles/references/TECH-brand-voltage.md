---
name: TECH-brand-voltage
category: design-principles-color
source: Bexa design-principles cluster (direct port, batch9 Wave 2 Round 2, T-047)
license: MIT (Bexa upstream is MIT; plugin re-licenses under its own MIT — see the plugin root LICENSE file)
also-in: TECH-brand-color-by-product.md (where the chromatic accent comes from); ai-slop-avoid.md (banned multi-accent "rainbow" patterns); bin/amw-ai-slop-check.py (mechanical enforcement — voltage-check rule is a known gap, see "Known gap" below)
---

# Brand voltage and scarcity rules

## Table of Contents

- [What it does](#what-it-does)
- [The voltage rule (one chromatic accent)](#the-voltage-rule-one-chromatic-accent)
- [Why scarcity beats abundance](#why-scarcity-beats-abundance)
- [Element caps per accent (the voltage table)](#element-caps-per-accent-the-voltage-table)
- [What counts as "an element using accent"](#what-counts-as-an-element-using-accent)
- [Authoring rule for variants](#authoring-rule-for-variants)
- [Known gap: voltage-check in amw-ai-slop-check.py](#known-gap-voltage-check-in-amw-ai-slop-checkpy)
- [Cross-references](#cross-references)

## What it does

Every brand identity in this plugin ships with **at most one chromatic accent**. The rest of the palette is neutral (greys, off-whites, near-blacks) or a tinted variant of the brand hue. Scarcity rules then cap how many on-screen elements may carry the accent at any one time, so the accent retains signal value across the whole product.

A page that lights up six surfaces with the brand accent reads as marketing-noise; a page that lights up two surfaces reads as intentional. The voltage rule operationalises this.

This file is consumed by:
- `agents/amw-wireframe-builder-agent.md` — Phase B HTML emission must count accent-using elements per screen
- `agents/amw-component-library-architect-agent.md` — when authoring tokens, only ONE color slot gets a saturated value; the rest are neutral or hue-shifted
- `agents/amw-brand-researcher-agent.md` — when extracting tokens from competitor URLs, the researcher annotates which hue is the brand voltage and ignores all secondary chromatic noise

## The voltage rule (one chromatic accent)

**Rule.** A brand identity defines exactly one accent hue with saturation > 50% (in HSL terms). Every other color in the brand is one of:

1. **Neutral** — greys with saturation < 10%. Always derived from the brand hue (slight tint), never pure RGB grey. See `TECH-brand-color-by-product.md` "One-brand-hue HSL arithmetic" for the construction recipe.
2. **Tinted neutral** — backgrounds, surfaces, borders, dividers carry 5–15% of the brand hue's saturation. Reads as "off-white that belongs to this brand" rather than generic grey.
3. **Semantic colors** — success / warning / error / info. These are NOT the brand accent. They are functional and may appear independently of the accent.

Anything that would introduce a second chromatic hue (sat > 50%) breaks voltage. Common offenders:

- Secondary CTA in a different accent. Wrong: primary blue + secondary orange. Right: primary blue + neutral secondary.
- "Hero gradient" stitching two saturated hues together. Wrong: blue→purple→pink gradient. Right: brand-hue-to-tinted-neutral gradient.
- Multi-color illustration imported from a stock library. Wrong: imported icon set with 8 chromatic colors. Right: re-color icons to brand accent + neutral.
- "Category color coding" with 6 saturated hues. Wrong: 6 product categories, each a different vibrant color. Right: 6 categories sharing the brand accent, distinguished by typography / iconography / number-prefix.

## Why scarcity beats abundance

Three reasons:

1. **Signal-to-noise.** If every interactive element is the accent, "click here" loses meaning. The accent works as a directional signal only when it's rare.
2. **Brand recognition.** A brand that owns one hue (Stripe's blurple, Linear's purple, Vercel's black) is recallable in five seconds. A brand with six hues is a logo, not an identity.
3. **Cross-cultural safety.** A single accent has one cultural reading to manage; six accents have six. Localisation cost scales with chromatic count.

## Element caps per accent (the voltage table)

Hard caps per single rendered screen (above-the-fold + immediately scrollable region). When the brand voltage is the listed hue, the page may have AT MOST `max-elements` simultaneously rendered components carrying that accent.

| Brand accent (HSL hue) | Common name | Max elements / screen | Notes |
|---|---|---|---|
| 0–15, 345–360 | Red | 2 | Reads as urgent; high voltage; cap aggressively. |
| 15–45 | Orange | 3 | Warm; energetic; tolerates slightly more density. |
| 45–60 | Yellow / Gold | 2 | Easily fatigues the eye; cap tight. |
| 60–90 | Lime / Yellow-Green | 2 | Rare brand voltage; treat as red. |
| 90–150 | Green | 3 | Calmer; tolerates more. |
| 150–195 | Teal / Cyan | 3 | Calm; medium voltage. |
| 195–245 | Blue | 4 | Calmest saturated hue; highest tolerable density. |
| 245–280 | Indigo / Violet | **2** | High visual voltage; cap aggressively. |
| 280–320 | Purple / Magenta | 2 | High voltage. |
| 320–345 | Pink / Rose | 3 | Reads warm; medium voltage. |

Reading the table: a Linear-style violet brand may use the accent on at most **2 elements per screen** at once. A Stripe-style blue brand may use the accent on at most **4 elements per screen**. Pages that exceed the cap read as "marketing landing pages from 2014" — too loud, too dense, too try-hard.

Below-the-fold content is governed independently — each scroll region is its own "screen" for the cap. A long landing page can have the accent on 2 elements per visible viewport without breaking voltage, even if the total document contains 12+ accent uses across the full scroll.

## What counts as "an element using accent"

For the cap to be enforceable, "element using accent" must be defined unambiguously.

Counts:
- Buttons whose `background` is the accent (filled CTA).
- Buttons whose `color` is the accent (text-only CTA on neutral background).
- Links rendered in the accent color (in body copy: count ONE link, not each individual `<a>`, if multiple share the same paragraph).
- Icons whose `fill` or `stroke` is the accent.
- Borders rendered in the accent (focus ring, active tab indicator).
- Headings whose `color` is the accent (rare; usually neutral).
- Background blocks or pills whose background is the accent (badge, tag, status pill).
- Charts where the primary series is in the accent (count 1 chart, not N data points).

Does NOT count:
- Hover states. The accent appearing on hover is reactive, not ambient — does not count toward the screen cap. (A link that is neutral at rest and accent on hover counts as **zero** elements at rest.)
- Focus rings on currently-unfocused elements. Only the actually-focused element counts.
- Brand logo in the header. The logo is allowed to use the accent regardless of cap; it's identity, not signal.
- Decorative chrome — a single accent stripe at top of page, a single accent underline under section headings — counts as ONE element total (not one per occurrence) because it's repeated branding chrome.

## Authoring rule for variants

When `amw-ascii-sketch` generates the 3 mandatory variants (per `three-hard-rules.md`), each variant gets its own voltage budget — they may use DIFFERENT accent hues, but EACH variant individually must obey its hue's cap.

This produces a useful contrast across variants without breaking voltage in any one:

- Variant 1 (baseline) — blue accent, 4 uses per screen.
- Variant 2 (advanced) — green accent, 3 uses per screen.
- Variant 3 (experimental) — violet accent, 2 uses per screen.

The variant with the smaller cap is not "less designed" — it's a deliberate scarcity choice that may read as more sophisticated.

## Known gap: voltage-check in amw-ai-slop-check.py

**Status:** Not yet implemented. Tracked here so future agents (and `amw-slop-verifier-agent`) know it's pending.

What's needed: extend `bin/amw-ai-slop-check.py` with a rule that counts on-screen accent uses by:

1. Reading the brand voltage from the design tokens (DESIGN.md or tokens.json — the `--primary` or `--brand-accent` slot).
2. Computing the HSL hue of that slot.
3. Mapping the hue to the voltage table's `max-elements` cap.
4. Walking the rendered HTML (or the ASCII wireframe spec, in plan-phase) to count elements whose computed color matches the accent within ΔE < 5.
5. Failing the check if the count > cap, with an actionable list of which elements exceeded the budget.

Until that lands, the voltage rule is enforced by sub-agent self-audit during Phase B emission and by `amw-slop-verifier-agent` reading this file as part of its checklist. The follow-up to wire this into `amw-ai-slop-check.py` is **Wave 3** (post-Bexa-cluster) — author `bin/` first, then update this section to remove "Known gap".

## Cross-references

- [TECH-brand-color-by-product.md](./TECH-brand-color-by-product.md) — how the one accent hue is chosen per product type
- [TECH-tone-archetypes.md](./TECH-tone-archetypes.md) — the visual archetype that determines whether voltage runs hot or cold
- [TECH-variant-hard-constraints.md](./TECH-variant-hard-constraints.md) — the variant-generation constraints that demand 3 distinct hues
- [skills/amw-design-principles/ai-slop-avoid.md](../ai-slop-avoid.md) — the rainbow-gradient / multi-accent patterns banned by the same principle
- [bin/amw-ai-slop-check.py](../../../bin/amw-ai-slop-check.py) — mechanical enforcement (voltage-check pending; see "Known gap" above)
- [agents/amw-wireframe-builder-agent.md](../../../agents/amw-wireframe-builder-agent.md) — Phase B emitter that must obey the cap
- [agents/amw-component-library-architect-agent.md](../../../agents/amw-component-library-architect-agent.md) — token-authoring step where the one accent is enshrined
- [agents/amw-brand-researcher-agent.md](../../../agents/amw-brand-researcher-agent.md) — competitor-token extractor that annotates which hue is the brand voltage
- [agents/amw-slop-verifier-agent.md](../../../agents/amw-slop-verifier-agent.md) — manual gate that reads this file pre-delivery
- [skills/amw-design-principles/SKILL.md](../SKILL.md) — orchestrator
