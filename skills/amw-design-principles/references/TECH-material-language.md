---
name: TECH-material-language
category: design-principles-philosophy
source: clean-room reimplementation (T-055 batch9 Wave 2; the principle that material effects need physical justification is common knowledge in motion/visual-design pedagogy — e.g. Apple HIG materials, Material 3 elevation, Refactoring UI)
license: this file = MIT (plugin license); NO verbatim copy from any GPL-2.0 source — written fresh in plugin idiom
also-in: "`amw-design-principles/SKILL.md` (rule 3 cites this for AI-slop rejection); `amw-wireframe-builder-agent` (enforces 1–2 material moments per page at HTML emit time); `references/component-taste.md` (per-component surface treatments)"
---

# Material language — physical origin, restraint, and information rhythm

## Table of Contents

- [What this is](#what-this-is)
- [The physical-origin rule](#the-physical-origin-rule)
- [The five material primitives](#the-five-material-primitives)
- [Material as focus — the 1–2 rule](#material-as-focus--the-12-rule)
- [Information rhythm — the four beats](#information-rhythm--the-four-beats)
- [Anti-patterns the language rejects](#anti-patterns-the-language-rejects)
- [Cross-references](#cross-references)

## What this is

A design-language doctrine that constrains how surface treatments (glass, gradient, texture, shadow, glow, frosted blur) and "material moments" are used across a page. Without this constraint, modern web design slides into one of two failure modes: **slop maximalism** (every section is a different material — glass card, then noise texture, then gradient mesh, then frosted nav, then bevel button) or **anemic flatness** (no material anywhere, the page reads as a 2016 medium.com post).

The doctrine answers two questions:

1. **When is a material effect legitimate?** When it has a physical origin (see below). Never as decoration alone.
2. **How much material is too much?** Maximum 1–2 material moments per page. The rest is calm.

This doctrine is what makes Stripe, Linear, Vercel, and Apple-style pages look "premium" — they use one or two strong material moments and let the rest of the page breathe. Sites that try to be premium with 6+ material moments read as AI-slop.

## The physical-origin rule

Every material effect on a page must trace back to one of **five physical sources**:

1. **Surface** — what the element is made of (paper, glass, brushed metal, frosted plastic, etc.)
2. **Light** — how light hits the surface (specular highlight, soft shadow, rim light, ambient occlusion)
3. **Texture** — micro-detail on the surface (paper grain, fabric weave, noise, scanlines)
4. **Depth** — z-axis offset (elevation, parallax, layering, focus blur)
5. **Feedback** — response to interaction (press depression, hover lift, ripple, glow on focus)

If a material effect on the page does NOT trace to one of these five, it is decoration without origin and must be removed.

**Examples of legitimate effects:**

| Effect | Physical origin |
|---|---|
| Frosted glass nav bar with backdrop-blur | Surface (frosted plastic) + Depth (nav is z-elevated above content) |
| Soft shadow under a card | Light (overhead light on elevated surface) + Depth (card sits above page) |
| Subtle noise texture on a hero background | Texture (matte paper grain) — must be ≤ 6% opacity or it reads as JPEG compression |
| Button depresses on click (translateY 1 px + darker color) | Feedback (physical press) |
| Specular highlight on a glossy pricing-tier card | Light (overhead specular on glossy surface) — only on the highlighted tier, not all tiers |

**Examples that fail the rule:**

| Effect | Why it fails |
|---|---|
| Gradient on every section background | No source — gradients with no light cue are just "colors that fade" |
| Glow around random text | Glow implies emission; text doesn't emit. Reserve for active states, neon brand identity, or status indicators |
| Bevel on every button | Bevel implies hardware; software buttons don't have hardware bevels. Use 1× on a single hero "physical" CTA at most |
| Multiple drop shadows at different angles | Multiple light sources contradicting each other reads as broken physics |
| Frosted blur on a non-z-elevated element | Frost implies "I'm in front of something" — if nothing is behind it, the blur is decoration |

## The five material primitives

The plugin's surface treatments collapse to five primitives. Each has a physical origin and a budget per page.

| Primitive | Origin | Default budget per page |
|---|---|---|
| **Glass** (frosted backdrop-blur card or nav) | Surface (glass) + Depth | 1 instance max |
| **Textured surface** (noise, paper grain, scanline) | Texture | 1 instance max — typically the hero background |
| **Elevated card** (shadow-elevated surface) | Light + Depth | up to 3 elevation tiers (sm/md/lg), but use sparingly — most cards should be hairline-bordered, not shadow-elevated |
| **Glow** (color-shifted radial emission) | Light (emissive) | 1 active/focus state per page + brand identity glow if applicable |
| **Press / hover feedback** (translateY + opacity / color) | Feedback | required on every interactive — these are not "moments," they're table-stakes |

The first four are "material moments." The fifth (feedback) is universal — it's not counted toward the 1–2 budget below.

## Material as focus — the 1–2 rule

**Hard rule: maximum 1–2 material moments per page.**

A "material moment" is one of the first four primitives (Glass, Textured surface, Elevated card, Glow). The exception is *Press / hover feedback*, which is required everywhere and is not counted.

| Page has | Verdict |
|---|---|
| 0 material moments | Anemic. Add 1. Hero usually wants the moment. |
| 1 material moment | Premium-default. Most pages should ship here. |
| 2 material moments | Allowed only when the moments serve different jobs (e.g., glass nav + textured hero bg — nav is "I float above," hero is "I have substance"). |
| 3+ material moments | Slop. Remove until ≤ 2. |

**The pick rule when you have to choose ONE:**

- If the brand is **kinetic / editorial** → the moment goes in the Hero (textured surface OR glass card with the headline).
- If the brand is **SaaS / dashboard** → the moment goes on the active interactive (the highlighted pricing tier, the live demo card, the elevated CTA).
- If the brand is **content / docs** → no material moment. Calm is correct.

**The pick rule when you have TWO:**

- One Glass + one Textured surface — nav is glass, hero is textured. Never both on the same z-plane.
- One Elevated card + one Glow — the pricing "most popular" tier is elevated, the CTA on it glows. Same job, two reinforcing primitives — this counts as one moment, not two. Don't add a third elsewhere.

The 1–2 rule applies per page. A site with 5 pages can have up to 10 material moments total — but never 3+ on one page.

## Information rhythm — the four beats

A page's content is sequenced in **four beats**. Each beat has a different visual weight, a different material treatment, and a different conversion job.

| Beat | Job | Visual weight | Material treatment |
|---|---|---|---|
| **Intro beat** | Set the frame, name the audience | Maximum (Hero, full viewport) | Material moment 1 lives here for most brands |
| **Claim beat** | State the unique value | High — but lower than intro | Hairline borders + 1 brand-color highlight; no new material |
| **Proof beat** | Show evidence (logos, screenshots, quotes, data) | Mid — restraint reads as confidence | Calm. No material. Let the proof speak. |
| **Action beat** | Ask for the click | High — focused, single CTA | Material moment 2 may live here (elevated CTA + glow on hover) |

A well-paced page has exactly **one** intro beat, one claim beat, one proof beat, and one action beat. Multi-section pages repeat the claim → proof → action cycle. The intro beat is one-shot.

**The rhythm hard rules:**

- Never put two intro beats on a page (no "double Hero"). If a page needs two Heroes, it's actually two pages.
- Never skip the proof beat. Without proof, the action beat reads as "trust me." Visitors don't.
- Never let the action beat live in the same section as the intro beat — separate them by at least the claim + proof cycle.
- The proof beat is calm by design. Do not make it ornamental. Calm proof reads as confident; ornamental proof reads as overcompensating.

## Anti-patterns the language rejects

The following surface-treatment patterns are forbidden — every one violates either the physical-origin rule or the 1–2 budget. `amw-wireframe-builder-agent` MUST reject them at HTML emit time:

| Pattern | Violation |
|---|---|
| Every section a different gradient background | No physical origin; visual cacophony |
| Glassmorphism on every card | Frosted blur implies depth; >1 instance kills the depth signal |
| Noise texture on every section | Texture is one moment; tiling it everywhere is JPEG compression |
| Glow on text bodies | Text doesn't emit; reserve glow for active/focus states |
| Multiple drop-shadow directions on the same page | Contradicts physics (multiple sun positions) |
| Bevel + emboss on buttons | Software UI; bevel is from skeuomorphism era; use flat + feedback instead |
| "Glassmorphic" cards with no background image | Glass without something to be in front of is just translucent paint |
| Color gradients on text | Sometimes legitimate as brand-identity Hero treatment; never on body copy, never on every H2 |
| Shadow on top of shadow on top of shadow | "Floating" stack — one elevation tier reads as floating; three reads as a Mac OS dock from 2007 |
| Backdrop-blur on a fully-opaque element | Frost without translucency is just compute waste |

## Cross-references

- `skills/amw-design-principles/SKILL.md` — rule 3 (Reject AI-slop) cites this doctrine as the enforcement source for surface-treatment slop.
- `skills/amw-design-principles/ai-slop-avoid.md` — anti-pattern list overlaps with the table above; this file gives the *why* (physical origin), that file gives the bare *what*.
- `agents/amw-wireframe-builder-agent.md` — enforces the 1–2 material moment budget at HTML emit time; counts moments per page before delivery.
- `agents/amw-slop-verifier-agent.md` — verifies the four-beat rhythm and the 1–2 material rule as part of pre-delivery slop check.
- `component-taste.md` — per-component surface treatments; defers to this file for the *which primitive when* decision.
- `TECH-motion-density.md` — companion ruleset; motion has the same restraint principle (per-tier caps).
- `TECH-dial-configuration.md` — VISUAL_COMPLEXITY dial caps material-moment count; VISUAL_COMPLEXITY=1 forces 0 moments, VISUAL_COMPLEXITY=10 allows 2.
