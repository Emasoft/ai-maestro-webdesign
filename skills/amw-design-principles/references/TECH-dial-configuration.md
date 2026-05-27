---
name: TECH-dial-configuration
category: design-principles-workflow
source: clean-room reimplementation (T-053 batch9 Wave 2; the 1-10 dial idea derives from open knobs/sliders patterns common in image-gen prompting and parametric design — common-knowledge concept, no verbatim copy)
license: this file = MIT (plugin license); NO verbatim copy from any GPL-2.0 source — designed fresh for amw-design-principles
also-in: `amw-ascii-sketch` (reads dials to steer Variant 1/2/3 spread); `amw-wireframe-builder-agent` (reads dials at HTML emit time); `amw-motion-designer-agent` (reads MOTION_DRAMA); `agents/ai-maestro-webdesign-main-agent.md` (writes dial values during Phase A interview)
---

# DIAL CONFIGURATION — six numeric knobs that steer every variant

## Table of Contents

- [What this is](#what-this-is)
- [Why dials, not adjectives](#why-dials-not-adjectives)
- [The six dials](#the-six-dials)
- [Natural-language → dial mapping](#natural-language--dial-mapping)
- [Variant spread rule](#variant-spread-rule)
- [Dial conflicts](#dial-conflicts)
- [Default dial bundles by archetype](#default-dial-bundles-by-archetype)
- [Cross-references](#cross-references)

## What this is

Six numeric dials, each ranging 1–10, that steer downstream sub-agents (`amw-ascii-sketch`, `amw-wireframe-builder-agent`, `amw-motion-designer-agent`, `amw-asset-generator-agent`) toward concrete decisions. The orchestrator (`ai-maestro-webdesign-main-agent`) sets the dials during the Phase A interview and writes them into the frozen DESIGN.md so every Phase B agent reads the same numbers.

Dials replace vague adjectives ("make it premium," "more modern," "less corporate") with values both the human and the model can reason about and adjust by integers.

## Why dials, not adjectives

Adjectives drift. "Premium" means hairline borders + serifs to one designer and frosted-glass + Inter to another. "Modern" means flat in 2019 and gradient-on-blur in 2025. By the time three agents downstream interpret "premium," the brand has drifted three different directions.

Numbers don't drift. `BRAND_INTENSITY=8` reads the same to every agent: high-saturation primary, large brand-color surface area, bold logotype, brand color in the CTAs. `BRAND_INTENSITY=2` reads the same: neutral grays dominate, brand color appears only in the CTA, logotype is small.

The dials also make iteration cheap. "Turn MOTION_DRAMA from 7 to 4" is a one-edit instruction that propagates through every sub-agent. "Less dramatic motion" requires every sub-agent to re-interview.

## The six dials

Each dial is a 1–10 integer. 1 = minimum; 10 = maximum. Default for any unset dial is **5**.

### 1. VISUAL_COMPLEXITY (1–10)

How busy the page is. Counts surface decoration, number of colors visible at once, layering depth, and ornamentation.

| Value | Effect |
|---|---|
| 1 | One surface color, one accent, sans-serif only, no decorations, no shadows, no gradients |
| 5 | 2–3 surface tones, 1 accent, hairline borders allowed, single shadow elevation, neutral-modern default |
| 10 | 4+ surface tones, multiple accents, layered cards, multiple shadow elevations, hand-drawn or photographic embellishment, ornamented typography |

### 2. MOTION_DRAMA (1–10)

The amplitude and personality of motion across the page. Composes with the tier from `references/TECH-motion-density.md` — Minimal tier caps motion count, MOTION_DRAMA caps each motion's amplitude.

| Value | Effect |
|---|---|
| 1 | No entrance animations, no scroll reveals, no hover beyond color shift, no transitions over 150 ms |
| 5 | Subtle fade-in on scroll, hover-lift on cards (translateY 2 px), button micro-feedback ≤ 200 ms, page-transition wrapper ≤ 250 ms |
| 10 | SplitText hero entrance, asymmetric scroll reveals, ambient bg, marquee, page-transition up to 700 ms, elastic ease curves, parallax allowed |

### 3. CONVERSION_FOCUS (1–10)

How aggressively the page pushes the visitor toward a single CTA. Higher = fewer paths, shorter Hero, repeated CTAs.

| Value | Effect |
|---|---|
| 1 | No primary CTA emphasis, multiple equally-weighted links, long-form editorial reading |
| 5 | One primary CTA in Hero + one in Final CTA, secondary CTA in Hero is allowed |
| 10 | One CTA repeated 4+ times down the page, no secondary CTAs anywhere, Hero is ≤ 3 lines, sticky CTA bar on scroll |

### 4. DATA_DENSITY (1–10)

Information per square pixel. Drives whether sections are airy/marketing or dense/dashboard.

| Value | Effect |
|---|---|
| 1 | Hero takes 1 full viewport; sections separated by 200+ px; max 1 idea per section; large typography (H1 ≥ 80px) |
| 5 | Hero ≈ 1 viewport; sections separated by 80–120 px; Features section is 3-up; H1 ≈ 48–64 px |
| 10 | Multiple data tables, dashboards, comparison grids 4-wide, dense pricing tables, H1 ≈ 32–40 px, sections packed tight |

### 5. BRAND_INTENSITY (1–10)

How much the brand color and logotype dominate the visual field.

| Value | Effect |
|---|---|
| 1 | Brand color appears only in the CTA; everything else is neutral; logo is small (24–32 px) |
| 5 | Brand color used for CTA + section accents + active states; logo is mid-size (32–40 px) |
| 10 | Brand color used as a full Hero background or wraps multiple sections; logo is hero-size; logotype is reused as a graphic device (large pre-text in section dividers) |

### 6. INTERACTION_DEPTH (1–10)

How much state the page exposes to interaction. From a static brochure to an in-page playground.

| Value | Effect |
|---|---|
| 1 | Static. No JS state changes. Hover is the only interaction |
| 5 | One interactive element (pricing toggle monthly/yearly, FAQ accordion, demo carousel) |
| 10 | Live calculator, embedded sandbox, interactive feature explorer, in-page configurator, mid-page interactive demo |

## Natural-language → dial mapping

When the user speaks in adjectives, the orchestrator translates to dial deltas before writing them into DESIGN.md. Some canonical translations:

| User says | Dial change |
|---|---|
| "Turn up the drama" | MOTION_DRAMA → 9 |
| "Tone down the drama" | MOTION_DRAMA → 3 |
| "More data-dense" | DATA_DENSITY → 9 |
| "More airy / breathe more" | DATA_DENSITY → 3, VISUAL_COMPLEXITY → 3 |
| "More premium" | VISUAL_COMPLEXITY → 6, BRAND_INTENSITY → 3, DATA_DENSITY → 4 (premium reads as restraint, not loud) |
| "More punchy / more saas" | BRAND_INTENSITY → 8, CONVERSION_FOCUS → 8 |
| "Less corporate" | VISUAL_COMPLEXITY → 4, BRAND_INTENSITY → 4, MOTION_DRAMA → 6 |
| "More minimal" | VISUAL_COMPLEXITY → 2, MOTION_DRAMA → 3, BRAND_INTENSITY → 3 |
| "More editorial" | VISUAL_COMPLEXITY → 7, DATA_DENSITY → 3, BRAND_INTENSITY → 6 |
| "More playful" | MOTION_DRAMA → 7, VISUAL_COMPLEXITY → 6, BRAND_INTENSITY → 7 |
| "More serious / more trust" | MOTION_DRAMA → 3, VISUAL_COMPLEXITY → 4, BRAND_INTENSITY → 4 |
| "More interactive" | INTERACTION_DEPTH → 8 |
| "Sell harder" | CONVERSION_FOCUS → 9 |
| "Be subtler about selling" | CONVERSION_FOCUS → 3 |

The orchestrator MUST surface the dial change in the response when interpreting an adjective. Example: *"Setting MOTION_DRAMA → 9 (turn up the drama). Keeping the other five dials unchanged."* This makes the translation visible and the user can correct it before Phase A iteration burns tokens.

## Variant spread rule

When `amw-ascii-sketch` produces the mandatory 3 variants (`amw-design-principles` rule 2), the variants vary dials by a controlled spread, not by random mutation:

- **Variant 1 (baseline):** all dials at the user-set values.
- **Variant 2 (advanced):** pick ONE dial and shift by +2. Choose the dial that most defines the brand. Example: a SaaS pricing page → CONVERSION_FOCUS +2.
- **Variant 3 (experimental):** pick a DIFFERENT dial and shift by +3 OR shift TWO dials by +2. Example: editorial brand → VISUAL_COMPLEXITY +3, OR MOTION_DRAMA +2 and BRAND_INTENSITY +2.

This produces three variants that are visibly different but on the same brand axis — not "three random aesthetics." The user picking variant 3 then tells the orchestrator which axis to push further.

## Dial conflicts

Some dial combinations produce visual contradictions. The orchestrator flags these in the Phase A response and asks for clarification:

| Combination | Conflict | Resolution |
|---|---|---|
| `VISUAL_COMPLEXITY=2` + `BRAND_INTENSITY=10` | Minimal layout but max brand → looks like a billboard, not a product | Lower BRAND_INTENSITY to ≤ 6 OR raise VISUAL_COMPLEXITY to ≥ 6 |
| `MOTION_DRAMA=9` + `DATA_DENSITY=9` | Dense data + loud motion → motion sickness, illegibility | Pick one: dramatic motion for marketing pages, OR dense data for dashboards. Not both. |
| `CONVERSION_FOCUS=10` + `DATA_DENSITY=9` | Aggressive single-CTA + lots of competing data → CTA disappears in the noise | Lower DATA_DENSITY to ≤ 5, keep CONVERSION_FOCUS=10 |
| `INTERACTION_DEPTH=10` + `MOTION_DRAMA=1` | Live interactive product but no motion feedback → feels broken when the user interacts | Raise MOTION_DRAMA to ≥ 4 to give interactive feedback |

## Default dial bundles by archetype

When the user hasn't expressed strong preferences, the orchestrator may pick a default bundle from the brand archetype.

| Archetype | VC | MD | CF | DD | BI | ID |
|---|---|---|---|---|---|---|
| **SaaS dashboard** | 5 | 4 | 6 | 7 | 5 | 7 |
| **SaaS marketing** | 5 | 6 | 8 | 4 | 6 | 4 |
| **E-commerce product** | 6 | 5 | 9 | 6 | 5 | 5 |
| **Editorial / magazine** | 8 | 7 | 3 | 4 | 7 | 3 |
| **Fintech / serious** | 4 | 3 | 7 | 6 | 4 | 4 |
| **Healthcare / clinical** | 3 | 2 | 5 | 5 | 3 | 3 |
| **Agency / portfolio** | 7 | 8 | 5 | 3 | 7 | 5 |
| **Developer tool** | 5 | 4 | 7 | 7 | 5 | 8 |
| **Internal tool** | 3 | 2 | 4 | 8 | 3 | 5 |
| **Luxury brand** | 6 | 5 | 4 | 3 | 6 | 3 |
| **Playful consumer** | 7 | 8 | 7 | 5 | 8 | 6 |

Legend: VC=VISUAL_COMPLEXITY, MD=MOTION_DRAMA, CF=CONVERSION_FOCUS, DD=DATA_DENSITY, BI=BRAND_INTENSITY, ID=INTERACTION_DEPTH.

The bundles are starting points, not requirements. The user can override any dial after the orchestrator surfaces the proposed bundle.

## Cross-references

- `agents/ai-maestro-webdesign-main-agent.md` — sets dials during the Phase A interview; writes them to DESIGN.md; surfaces dial changes when interpreting adjectives.
- `skills/amw-ascii-sketch/SKILL.md` — reads dials to drive variant spread and section weighting in the ASCII scaffold.
- `agents/amw-wireframe-builder-agent.md` — reads dials at HTML emit time to pick component variants, surface treatments, and spacing rhythms.
- `agents/amw-motion-designer-agent.md` — reads MOTION_DRAMA + INTERACTION_DEPTH to pick timing curves, amplitudes, and which interactions get motion feedback.
- `agents/amw-asset-generator-agent.md` — reads VISUAL_COMPLEXITY + BRAND_INTENSITY to decide ornamentation, icon weight, and pretext typography intensity.
- `references/TECH-motion-density.md` — companion ruleset; MOTION_DRAMA caps amplitude, the density tier caps motion count.
- `references/TECH-landing-anatomy.md` — variant spread rule applies to the 9 canonical sections.
