---
name: TECH-brand-color-by-product
category: design-principles-color
source: Bexa design-principles cluster (direct port, batch9 Wave 2 Round 2, T-048)
license: MIT (Bexa upstream is MIT; plugin re-licenses under its own MIT — see the plugin root LICENSE file)
also-in: TECH-brand-voltage.md (the scarcity rule applied to the accent chosen here); skills/amw-design-principles/color-system.md (general palette guidance)
---

# Brand color by product type

## Table of Contents

- [What it does](#what-it-does)
- [Product-type → brand HSL ranges](#product-type--brand-hsl-ranges)
- [How to read the table](#how-to-read-the-table)
- [One-brand-hue HSL arithmetic (construction recipe)](#one-brand-hue-hsl-arithmetic-construction-recipe)
- [Tinting neutrals with the brand hue](#tinting-neutrals-with-the-brand-hue)
- [Worked example: B2B SaaS at hsl(220, 65%, 50%)](#worked-example-b2b-saas-at-hsl220-65-50)
- [When the product type doesn't match the table](#when-the-product-type-doesnt-match-the-table)
- [Cross-references](#cross-references)

## What it does

When the brand brief is silent on a specific brand color (which is most of the time — the user says "B2B SaaS for compliance teams" and stops), this table gives the brand-researcher and component-library-architect agents a deterministic starting hue. The chosen hue is then frozen as the **one chromatic accent** (per `TECH-brand-voltage.md`) and the rest of the palette is constructed by HSL arithmetic — light, dim, border, semantic, neutrals — all derived from that single hue.

The table encodes recognisable conventions, not arbitrary preferences. B2B SaaS that ships with a cool blue accent feels like B2B SaaS; B2B SaaS that ships with a saturated red accent reads as wrong. Convention is signal; novelty for its own sake is noise.

## Product-type → brand HSL ranges

| Product type | HSL hue range | HSL saturation range | HSL lightness (light theme primary) | HSL lightness (dark theme primary) | Common reading |
|---|---|---|---|---|---|
| B2B SaaS | 215–225 | 60–70% | 50–55% | 60–65% | Cool, professional, "trust the platform" |
| Dev tools / Engineering | 220–230 | 30–50% | 40–55% | 55–70% | Near-neutral; restrained; lets the code stand out |
| Consumer DTC (lifestyle) | 15–45, 340–355 | 65–80% | 50–60% | 55–65% | Warm; inviting; "the brand likes you" |
| Consumer DTC (tech) | 195–215 | 55–70% | 45–55% | 55–65% | Cool but friendlier than B2B; "approachable tech" |
| Fintech | 155–165 | 50–65% | 30–40% | 45–55% | Deep green; signals stability and money |
| Crypto / Web3 | 245–280 | 60–80% | 55–65% | 65–75% | Indigo / violet; high voltage; "new financial primitive" |
| Healthcare / Telehealth | 175–195, 150–170 | 40–55% | 40–50% | 50–60% | Teal or muted green; calming; clinical |
| Education / Learning | 25–45, 200–220 | 55–70% | 55–65% | 60–70% | Warm orange OR friendly blue; choose by audience age |
| Government / Civic | 215–230 | 30–45% | 30–40% | 45–55% | Restrained blue; conservative; "we are not flashy" |
| Luxury (any) | 0–30 (deep red), 25–45 (gold) | 15–30% | 20–35% | 30–45% | Desaturated; expensive looks quiet, not loud |
| Travel / Hospitality | 195–215, 25–45 | 60–75% | 50–60% | 55–65% | Sky-blue OR sunset orange |
| Food / Drink | 0–25, 90–130 | 65–80% | 45–55% | 55–65% | Warm red OR fresh green; tied to the product |
| Gaming / Entertainment | 270–320, 0–15 | 70–90% | 50–65% | 55–70% | Magenta, hot pink, hot red; high voltage |
| Charity / Non-profit | 95–125, 195–215 | 45–60% | 35–45% | 45–55% | Green of growth OR blue of trust |
| News / Editorial | 0–15 (masthead red), 215–230 (link blue) | 50–70% | 35–45% | 50–60% | Newspaper conventions; red masthead OR blue link |

## How to read the table

The agent picks **one row** from the product type and **one hue** from the range. The output is a single `hsl(H, S%, L%)` triple — not a range — that becomes the brand voltage.

Example: brief says "B2B SaaS for compliance teams". Agent picks row 1. Agent chooses H=220, S=65%, L=50% — a single specific blue. That triple is now frozen for the whole project.

If two product types overlap (e.g., "fintech for developers"), the agent picks the dominant frame from the brief — "fintech" wins over "for developers" because fintech is the primary value proposition. When in doubt, the agent asks one Phase A question: "Does this product read more as fintech (deep green) or as dev tooling (near-neutral)?" — and freezes the chosen hue based on the answer.

## One-brand-hue HSL arithmetic (construction recipe)

Once the brand hue is fixed at `hsl(H, S%, L%)`, the entire palette is constructed deterministically by arithmetic on that one hue. This is the **single-source-of-truth** principle (`amw-design-principles/SKILL.md` Rule 1) applied to color.

Formulas — `H`, `S`, `L` are the brand hue values:

| Token | Light theme | Dark theme |
|---|---|---|
| `--primary` | `hsl(H, S, L)` | `hsl(H, S, L+10)` |
| `--primary-hover` | `hsl(H, S, L-7)` | `hsl(H, S, L+3)` |
| `--primary-active` | `hsl(H, S, L-12)` | `hsl(H, S, L-3)` |
| `--primary-foreground` | `hsl(H, max(S-20, 0), L+45)` then clamp ≤ 98 | `hsl(H, max(S-20, 0), L+30)` then clamp ≤ 95 |
| `--primary-light` (tint backgrounds) | `hsl(H+5, max(S-30, 5), L+40)` clamp ≤ 96 | `hsl(H-5, max(S-30, 5), L-30)` clamp ≥ 12 |
| `--primary-dim` (muted accent) | `hsl(H, S-20, L+15)` | `hsl(H, S-20, L+5)` |
| `--primary-border` | `hsl(H+10, max(S-15, 10), L+25)` clamp ≤ 88 | `hsl(H-10, max(S-15, 10), L-20)` clamp ≥ 25 |
| `--ring` (focus) | `hsl(H, S, L)` (same as primary) | `hsl(H, S, L+10)` (same as primary dark) |

The hue-shift `±5–15°` between related tokens (light, dim, border) is what makes a single-brand palette feel **cohesive** rather than mechanical. A pure-grayscale dim is correct mathematically and feels wrong visually; a hue-shifted dim feels like it belongs to the brand.

## Tinting neutrals with the brand hue

Neutrals (greys, off-whites, near-blacks) are NOT pure RGB. They carry 5–15% of the brand hue's saturation so the whole product feels tonally unified.

| Token | Light theme | Dark theme |
|---|---|---|
| `--background` | `hsl(H, 8%, 98%)` | `hsl(H, 12%, 8%)` |
| `--surface` (cards) | `hsl(H, 5%, 100%)` | `hsl(H, 10%, 12%)` |
| `--surface-elevated` (popovers, modals) | `hsl(H, 4%, 100%)` with shadow | `hsl(H, 12%, 16%)` |
| `--muted` | `hsl(H, 8%, 95%)` | `hsl(H, 10%, 18%)` |
| `--muted-foreground` | `hsl(H, 8%, 45%)` | `hsl(H, 10%, 65%)` |
| `--border` | `hsl(H, 8%, 88%)` | `hsl(H, 10%, 22%)` |
| `--input` | `hsl(H, 8%, 92%)` | `hsl(H, 10%, 20%)` |
| `--foreground` | `hsl(H, 15%, 12%)` | `hsl(H, 10%, 95%)` |

Saturation under 10% reads as neutral but tonally connected — the eye doesn't perceive the hue explicitly, but the whole interface feels "blue" or "green" in aggregate.

## Worked example: B2B SaaS at hsl(220, 65%, 50%)

Brand voltage: `hsl(220, 65%, 50%)` (a saturated cool blue).

Applied to the formulas, light theme:

- `--primary: hsl(220, 65%, 50%)` — the brand blue
- `--primary-hover: hsl(220, 65%, 43%)` — 7% darker on hover
- `--primary-active: hsl(220, 65%, 38%)` — 12% darker when pressed
- `--primary-foreground: hsl(220, 45%, 95%)` — almost white but with the brand hue
- `--primary-light: hsl(225, 35%, 90%)` — tinted background for hover surfaces
- `--primary-dim: hsl(220, 45%, 65%)` — muted accent for secondary surfaces
- `--primary-border: hsl(230, 50%, 75%)` — accent border for selected states
- `--background: hsl(220, 8%, 98%)` — almost-white with a whisper of blue
- `--surface: hsl(220, 5%, 100%)` — pure-ish white for cards
- `--muted-foreground: hsl(220, 8%, 45%)` — body-secondary text, blue-tinted grey
- `--border: hsl(220, 8%, 88%)` — neutral border, blue-tinted

The whole palette is mathematically derived from one number. The component-library-architect agent emits this as `tokens.css` + `tokens.json` automatically — no human choice for any of the secondary slots.

## When the product type doesn't match the table

When the brief describes a product type not in the table (e.g., "B2B2C marketplace for industrial supply"), the agent:

1. **Decomposes** the brief into the table's closest two product types ("B2B SaaS" + "Consumer DTC tech") and picks the dominant one.
2. **Asks** one Phase A question if the decomposition is ambiguous.
3. **Documents** the choice in the DESIGN.md as "Brand hue chosen by product-type analogy: closest match is B2B SaaS based on the audience being procurement teams."

The table is a starting point, not a constraint. A user who knows their brand should override; a user who doesn't is well-served by the convention.

## Cross-references

- [TECH-brand-voltage.md](./TECH-brand-voltage.md) — the scarcity rule applied to the accent chosen here
- [TECH-tone-archetypes.md](./TECH-tone-archetypes.md) — visual archetype that may modulate the saturation choice
- [TECH-variant-hard-constraints.md](./TECH-variant-hard-constraints.md) — when 3 variants must each pick a different hue, this table seeds the choices
- [skills/amw-design-principles/color-system.md](../color-system.md) — general color-system rules (contrast, semantic colors, hover/active states)
- [skills/amw-design-principles/ai-slop-avoid.md](../ai-slop-avoid.md) — the multi-color anti-patterns this file routes around
- [agents/amw-brand-researcher-agent.md](../../../agents/amw-brand-researcher-agent.md) — agent that consults this table for unbranded briefs
- [agents/amw-component-library-architect-agent.md](../../../agents/amw-component-library-architect-agent.md) — agent that applies the HSL arithmetic to emit tokens
- [agents/amw-design-md-author-agent.md](../../../agents/amw-design-md-author-agent.md) — author flow that asks the brand-hue question during the 5-Q interview
- [skills/amw-design-principles/SKILL.md](../SKILL.md) — orchestrator
