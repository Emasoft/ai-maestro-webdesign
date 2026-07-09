---
name: TECH-brand-researcher-playbook
category: agent-playbook
source: design-forge-main/references/research-playbook.md (MIT) + ux-designer-skill-main brand-positioning notes (T-157/T-158 synthesis)
also-in:
---

## Table of Contents

- [What this is](#what-this-is)
- [Step 1 — Identify top-N competitors](#step-1--identify-top-n-competitors)
- [Step 2 — Extract design tokens per site](#step-2--extract-design-tokens-per-site)
- [Step 3 — Cluster aesthetic positions](#step-3--cluster-aesthetic-positions)
- [Step 4 — Produce DESIGN.md exemplars](#step-4--produce-designmd-exemplars)
- [Step 5 — Recommend 1–3 directions](#step-5--recommend-13-directions)
- [Search query templates](#search-query-templates)
- [Source list — GREEN vs REJECT](#source-list--green-vs-reject)
- [Traffic-light scoring](#traffic-light-scoring)
- [Anti-reference board (T-158)](#anti-reference-board-t-158)
- [Cross-references](#cross-references)

# Brand-researcher playbook — competitor analysis to DESIGN.md exemplars

## What this is

The mechanical recipe `amw-brand-researcher-agent` executes when the user provides reference URLs or asks for competitive brand analysis. Five steps from "I want to understand the visual landscape" to "here are 1–3 specific directions for Phase A ASCII iteration".

This playbook is consumed by `amw-brand-researcher-agent.md` (the judgment-layer agent file). The agent reads this file to learn the recipe; the agent applies judgment when the recipe doesn't fit cleanly.

## Step 1 — Identify top-N competitors

Goal: produce a list of 5–8 reference URLs that span the competitive landscape.

If the user provides URLs, use those. Otherwise:

1. **Categorize the project.** Industry, target audience, primary archetype (luxury / kinetic / Bauhaus / playful / editorial / SaaS-clean / fintech-trust / etc.). The archetype drives search queries.
2. **Compose search queries** from `archetype + density + primary asset`. Pin year range (`2024..2026`) to avoid aged references. Use the templates below.
3. **Always include a reference mix:**
   - 2 direct competitors (industry convention)
   - 1 indirect competitor (same UX pattern, different industry — breaks monotony)
   - 1 aspirational benchmark (award-winning, ceiling-setter)
4. **Never** all 4 competitors. **Never** all 4 aspirational. The mix forces grounded creativity.

When the user provides URLs that are all from the same brand family, this becomes a brand-consistency audit, NOT a competitive analysis. Note this in the report — the playbook still runs, but step 3 produces "internal consistency observations" instead of "positioning whitespace".

## Step 2 — Extract design tokens per site

Goal: per-URL design tokens normalized to the design-principles schema.

For each URL:

1. **Run `bin/amw-designlang-wrapper.sh <url>`** to extract tokens via designlang.
2. **If coverage < 60% after ~20s,** fall back to `bin/amw-dev-browser-wrapper.sh screenshot <url>` and analyze visually.
3. **Normalize to schema:**
   - `primary` (dominant brand color)
   - `secondary` / `accent` (highlight, used sparingly)
   - `surface` / `background` (canvas color)
   - `text` (body color)
   - `border` (hairline color)
   - `body-font` family + weight + size + tracking
   - `display-font` family + weight + size + tracking
   - `radius` style (sharp 0–2px / subtle 4–8px / rounded 12–16px / pill 20+px)
   - `spacing-unit` (base spacing — 8px / 12px / 16px)
   - `component-patterns` (hero archetype, card style, button style)
4. **Run WCAG AA contrast check** on the primary text/background pair. Report the ratio.
5. **Classify** color (warm / cool / neutral), typography (serif / sans, geometric / humanist), spacing (tight / standard / airy), radius (sharp / subtle / rounded / pill).

Each site's tokens become a row in the cross-site summary.

## Step 3 — Cluster aesthetic positions

Goal: map the competitive landscape across token dimensions; identify density (commoditized ground) and gaps (positioning whitespace).

For each token dimension, plot where the competitor set clusters:

| Dimension | Cluster examples | Whitespace examples |
|---|---|---|
| Color warmth | "5 of 7 warm neutral" → commoditized | "0 of 7 cool / dark jewel" → whitespace |
| Typography | "6 of 7 serif display" → commoditized | "1 of 7 geometric sans" → whitespace |
| Spacing | "all airy" → commoditized | "no one tight + dense" → whitespace |
| Radius | "all 4–8px subtle" → commoditized | "no one sharp 0px" → whitespace |
| Component archetype | "6 of 7 full-bleed hero" → commoditized | "split-screen, asymmetric grid, no-hero" → whitespace |

**Commoditized ground** = where every competitor already lives. A design matching this looks like a competitor, not a differentiator.

**Differentiated territory** = unclaimed gaps. A design occupying whitespace stands out — for better or worse, depending on whether the brand brief calls for differentiation or fit-in.

When the user's stated direction matches the commoditized ground, flag the collision. Three resolutions exist: (a) proceed and differentiate on execution (copy, imagery, interaction), (b) adjust the direction toward whitespace, (c) accept fitting in.

## Step 4 — Produce DESIGN.md exemplars

Goal: turn extracted tokens into a Variant 1 DESIGN.md file the wireframe-builder can consume directly.

When the main-agent requests `output_format=design.md`:

1. **Pick the most representative direction(s)** — typically 1 (commoditized baseline) + 1 (whitespace direction).
2. **Emit DESIGN.md per direction** using `bin/amw-design-md-from-url.sh` for direct extraction, or hand-author from the normalized tokens.
3. **Validate** with `bin/amw-design-md-lint.sh`.
4. **Run WCAG contrast pre-flight** with `bin/amw-design-md-contrast.py` — flag any pair-level failures.
5. **Output paths** land in `${CLAUDE_PROJECT_DIR}/reports/webdesigner/<ts>-brand-direction-<slug>.design.md`.

The DESIGN.md becomes the canonical hand-off artifact for `amw-wireframe-builder-agent` and `amw-component-library-architect-agent`. Free-form positioning prose stays in the agent's report; the DESIGN.md is the machine-parseable token bundle.

## Step 5 — Recommend 1–3 directions

Goal: present the user with 1–3 actionable directions for Phase A ASCII variant exploration. Never more than 3 — the orchestrator's three-variant rule.

Each direction is a one-paragraph synthesis:

1. **Baseline (align with commoditized ground, differentiate on execution).** Match the dominant competitive pattern. Differentiate via copy, imagery, interaction craft. Safe; relies on non-visual differentiation.
2. **Advanced (partial whitespace).** Pick one differentiating dimension (e.g., type treatment, color temperature, layout archetype) while keeping the rest familiar. Stands out without alienating audience expectations.
3. **Experimental (full whitespace).** Pick multiple differentiating dimensions. Strong differentiator; higher risk because it departs from audience expectation. Recommend when brand intent is clearly "distinct" or "challenger".

When the brand brief is missing or contradicts the references, present the directions as options, not prescriptions. Main-agent surfaces to the user.

## Search query templates

Compose from `archetype + density + primary asset`, not product category:

| Archetype | Base queries |
|---|---|
| Luxury | `"editorial" dark site:awwwards.com`, `fintech serif landing`, `private banking homepage 2025` |
| Kinetic / Motion | `scroll-driven hero awwwards`, `gsap ScrollTrigger case study 2024..2026`, `cinematic landing site:godly.website` |
| Bauhaus | `grid poster web`, `swiss typography landing site:siteinspire.com`, `geometric primary colors homepage` |
| Luxury + product | `premium product hero dark site:awwwards.com`, `boutique hardware landing` |
| Hand-drawn | `illustrated portfolio site:awwwards.com`, `hand drawn landing page` |
| Playful | `colorful SaaS landing 2025`, `friendly onboarding illustration landing` |
| System-first | `design system marketing site`, `documentation homepage` |
| Editorial | `editorial magazine web 2025`, `long-form longread homepage` |
| Retro / Y2K | `y2k brutalist landing 2024..2026`, `pixel ui revival` |

Always pin the year range (`2024..2026`) to avoid aged references. Always include the source filter when targeting curated lists.

## Source list — GREEN vs REJECT

**GREEN (curated, by default trust):**
- Awwwards — `awwwards.com/sites/`
- SiteInspire — `siteinspire.com`
- Godly — `godly.website`
- One Page Love — `onepagelove.com`
- Muzli — `muz.li`
- Httpster — `httpster.net`
- Typewolf — `typewolf.com/site-of-the-day`
- Land-book — `land-book.com`
- SaaSLandingPage — `saaslandingpage.com`
- Refero — `refero.design`

**REJECT (never use for production reference):**
- Dribbble hero-only shots (no system, no context)
- Pinterest boards (collage, no source)
- Template marketplaces (ThemeForest, TemplateMonster, Elementor)
- Generic portfolio grids (Behance unless live + verified)
- Rendered-in-Figma mockups shown as live sites
- Anything > 3 years old without classic-rationale

## Traffic-light scoring

For each reference, score 5 dimensions:

| Dimension | GREEN | YELLOW | RED |
|---|---|---|---|
| Layout | Unique + works | Solid but common | Generic or broken |
| Color | Intentional palette with rationale | Fine, forgettable | Harmful or off-brand |
| Typography | Award-grade pairing & scale | Competent | System / default |
| Motion | Meaningful, performant | Present, unremarkable | Broken or gratuitous |
| Performance | LCP < 2.5s, CLS < 0.1 | 2.5–4s | > 4s or layout shift |

Only extract directives from GREEN rows. YELLOW provides context. RED is excluded — even a popular site with poor scores does not get its patterns recommended.

## Anti-reference board (T-158)

Beyond identifying what TO match, identify what to AVOID:

1. **Name 3–5 specific sites the design should NOT resemble.** Not categories ("avoid corporate") — specific URLs ("don't look like Notion, Linear, Stripe — they all share an over-saturated category aesthetic").
2. **Per anti-reference, document the specific off-brand signal:** "Notion's mint-green is too playful for a financial product"; "Linear's gradient hero is over-used in 2025 SaaS landing pages"; "Stripe's purple-pink gradient is the prototypical AI-slop pattern".
3. **Blur test at 20% visibility.** Apply CSS `filter: blur(40px) opacity(0.2)` to the proposed design and to each anti-reference. The silhouettes must differ — color block placement, hero treatment, density. If the blurred outline matches an anti-reference, the design has not differentiated.
4. **Add a "What This Brand Fights" field to DESIGN.md.** A one-paragraph statement: "We are NOT [list of anti-references]. We avoid [list of patterns]. We choose [list of contrarian moves]." This field constrains the wireframe-builder downstream.

The anti-reference board is as important as the reference board. Many designs fail not because they lack good references but because they accidentally land on a saturated pattern.

## Cross-references

- `agents/amw-brand-researcher-agent.md` — judgment-layer agent that runs this playbook
- `../color-system.md` — palette classification, WCAG contrast rules
- `../typography-system.md` — type pairing, font-stack rules
- `../spacing-rhythm.md` — spacing classification (tight / standard / airy)
- `../ai-slop-avoid.md` — anti-patterns to flag during scoring
- `authority-hierarchy.md` — brand-researcher's (non-veto) visual-direction authority
- `skills/amw-design-extract/SKILL.md` — token extraction skill
- `skills/amw-dev-browser/SKILL.md` — only browser primitive
- `skills/amw-design-md/SKILL.md` — DESIGN.md authoring / lint / contrast / convert
- `skills/amw-design-md-spec/references/canonical-spec-google-alpha.md` — Variant 1 DESIGN.md schema
