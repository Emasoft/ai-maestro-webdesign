---
name: TECH-layout-discipline
category: design-principles-reference
source: mechanical layout hard-rules + pre-flight count-checks reimplemented in this plugin's voice (stack-neutral) from taste-skill §4.7 "Layout Discipline" and §14 "Final Pre-Flight Check" (Leonxlnx, MIT) — no verbatim copy; thresholds are the source's, the phrasing and our-stack framing are amw-specific
license: this file = MIT (plugin license)
also-in: "amw-wireframe-builder-agent (enforces these at HTML-emit time); TECH-landing-anatomy.md (the scaffold these rules discipline); pre-output-checklist.md (the mechanical counts run as a gate); ai-slop-avoid.md Section X (the eyebrow / logo-wall / hero-decoration tells these rules operationalize)"
---

# LAYOUT DISCIPLINE — mechanical hard-rules that stop slop layouts

## Table of Contents

- [What this is](#what-this-is)
- [Hero discipline](#hero-discipline)
- [Navigation discipline](#navigation-discipline)
- [Section-layout discipline](#section-layout-discipline)
- [Bento / grid discipline](#bento--grid-discipline)
- [Logo wall discipline](#logo-wall-discipline)
- [List discipline](#list-discipline)
- [Mobile collapse](#mobile-collapse)
- [The mechanical pre-flight counts](#the-mechanical-pre-flight-counts)
- [Cross-references](#cross-references)

## What this is

[TECH-landing-anatomy](TECH-landing-anatomy.md) gives the 9-section scaffold and the copy formula. This file gives the **mechanical hard-rules** that keep that scaffold from collapsing into the templated AI-slop layout — the one where every section has an eyebrow, the hero overflows the fold, six identical zig-zag rows repeat, and a bento grid has an empty cell. Each rule below is a yes/no check with a number attached, so it can be enforced at HTML-emit time and re-checked in the pre-flight, not argued about. **Failing any of these is shipping broken work.**

These rules are gated by the dials (see [TECH-dial-configuration](TECH-dial-configuration.md)): a high `DATA_DENSITY` dashboard relaxes some hero/whitespace rules, but the hero-fit, nav, and bento-cell-count rules hold regardless.

## Hero discipline

- **The hero fits in the initial viewport.** Headline ≤ 2 lines on desktop; subtext ≤ 20 words AND ≤ 4 lines; the primary CTA is visible without scrolling. If the copy won't fit, cut copy or drop the font scale — never let the hero overflow so the CTA hides below the fold. If you can't state the value-prop in 20 words, the value-prop is unclear; that's not the rule being too tight.
- **Plan font scale and asset size together.** A 4-line hero headline is a font-size error, not a copy-length error. Sensible default range is `text-4xl md:text-5xl lg:text-6xl`; reach for `text-6xl md:text-7xl` only when the headline is 3–5 words and the hero asset is small.
- **Hero top padding cap: `pt-24` (≈6rem) max at desktop.** More than that floats the hero content halfway down the viewport and reads as a layout bug. Need more presence? Raise the font scale or asset size, not the top padding.
- **Hero stack: at most 4 text elements.** Allowed: (1) eyebrow OR brand strip OR neither — pick zero or one; (2) headline; (3) subtext; (4) CTAs (1 primary + at most 1 secondary). **Banned inside the hero:** a tiny tagline under the CTAs, a "trusted by" trust-strip, a pricing teaser, a feature-bullet list, a social-proof avatar row. All of those move to dedicated sections directly below the hero.

## Navigation discipline

- **Desktop nav renders on a single line.** If items don't fit at `lg` (1024px), condense labels, drop secondary items, or collapse to a menu. A two-line desktop nav is broken.
- **Nav height ≤ 80px at desktop** (default 64–72px). No oversized "agency" bars that eat 15% of the viewport.

## Section-layout discipline

- **Layout-family repetition ban.** Once a section uses a layout family (3-column cards, full-width quote, split text+image, …), that family appears **at most once** on the page. A landing page of 8 sections uses **at least 4 different layout families**. "Selected work" must not look identical to "What we do".
- **Zig-zag alternation cap: max 2 consecutive.** Alternating left-image/right-text then left-text/right-image is fine twice; a 3rd consecutive image+text split is a fail. Break it with a full-width section, a vertical stack, a bento grid, or a different family.
- **Eyebrow restraint: ≤ 1 eyebrow per 3 sections** (hero counts as 1). An eyebrow is the small uppercase wide-tracking label above a section headline (`text-[11px] uppercase tracking-[0.18em]`). Putting one above *every* header is the templated-AI rhythm. If section A has an eyebrow, the next two sections do not. What to do instead: drop it — the headline alone is enough; the section's position on the page already categorizes it. (This operationalizes the section-number-eyebrow tell in [ai-slop-avoid](../ai-slop-avoid.md) Section X.)
- **Split-header ban (default).** "Left big headline + right small explainer paragraph" as a section header is banned as a default. One focused message per section. If you genuinely need a headline plus an explainer, stack them vertically (headline, then body at ≤ 65ch). Use the split only when the right column carries a real visual/interactive element, not filler text.

## Bento / grid discipline

- **Exact cell count: N items → N cells.** A bento grid has exactly as many cells as you have content for. An empty cell in the middle or at the end means you planned the grid wrong — re-shape it (1+2, 2+1, hero+4, asymmetric trio); never paste a blank tile.
- **Rhythm, not one-sided repetition.** Don't stack six left-image/right-text rows. Alternate full-width feature rows, asymmetric tile sizes, and vertical breaks.
- **Background diversity.** A multi-cell grid can't be all white-on-white text cards. At least 2–3 cells need real visual variation: a real image, a brand-appropriate gradient (not AI-purple), a pattern, or a tinted background. Cream-on-cream typography-only bento reads as boring AI default even when the rest of the page is strong.

## Logo wall discipline

- **The "Used by / Trusted by" logo wall lives UNDER the hero, never inside it.** The hero is value-prop + primary CTA; the logo wall is a separate section directly below.
- **Use real logos, not text wordmarks.** Source real SVGs (Simple Icons: `https://cdn.simpleicons.org/{slug}/{color}`; devicon for tech-stack marks). For an invented brand, generate a simple SVG monogram matching the page style — a plain `<span>Acme Co</span>` row looks generic. Ensure logos render in both light and dark mode.
- **Logo-only rule.** A logo wall is logos and nothing else. Do NOT print an industry/category label under each logo (no `Stripe` + `payments`, no `Vercel` + `hosting`). The logo is the credibility; the label adds nothing. Brand name as `alt` for screen readers is fine.

## List discipline

- **Long lists use the right component.** A default `<ul>` with `divide-y` borders is fine up to ~5 items. Past that, reach for a real component (table with proper headers, a card grid, an accordion, a virtualized list) — a 20-row `border-t`/`border-b` divider list is a density tell (see [ai-slop-avoid](../ai-slop-avoid.md) Section X). Let `DATA_DENSITY` decide how much fits per section.

## Mobile collapse

- **Declare the `< 768px` fallback in the same component** for every multi-column layout (`w-full`, `px-4`, `max-w-7xl mx-auto`, the stack/carousel/collapse strategy). No "Tailwind handles it" assumptions — an implicit collapse is an untested collapse.

## The mechanical pre-flight counts

These are countable and belong in the pre-flight gate ([pre-output-checklist](pre-output-checklist.md)); `amw-wireframe-builder-agent` runs them before promoting an artifact:

| Check | Pass condition |
|---|---|
| Eyebrow count | `eyebrows ≤ ceil(sectionCount / 3)` (hero counts as 1) |
| Zig-zag run | no 3+ consecutive image+text-split sections |
| Layout-family diversity | `distinct layout families ≥ 4` for an 8-section page |
| Bento cells | `cells == items` (no empty cell anywhere) |
| Nav | single line at desktop AND height ≤ 80px |
| Hero lines | headline ≤ 2 lines, subtext ≤ 20 words AND ≤ 4 lines |
| Hero text elements | ≤ 4 (eyebrow/brand-strip, headline, subtext, CTAs) |
| Hero top padding | ≤ `pt-24` desktop |
| Marquee | ≤ 1 horizontal marquee per page |
| Duplicate CTA intent | no two CTAs with the same intent ("Get in touch" + "Let's talk" = fail) |
| Logo wall | under the hero, real SVG logos, no category labels |

## Cross-references

- [TECH-landing-anatomy](TECH-landing-anatomy.md) — the 9-section scaffold + hero copy formula these rules discipline.
- [ai-slop-avoid](../ai-slop-avoid.md) — Section X production-test tells (eyebrows, logo walls, hero decoration) that these rules turn into countable gates; § III Layout for the 3-equal-cards / alternating-bg bans.
- [TECH-variant-hard-constraints](TECH-variant-hard-constraints.md) — per-variant constraints that compose with these page-level rules.
- [TECH-pattern-vocabulary](TECH-pattern-vocabulary.md) — named layout patterns (Bento, Sticky-Stack) these rules constrain.
- [TECH-css-modern-syntax](TECH-css-modern-syntax.md) — `100dvh` viewport rule + Grid-over-flexbox for building these layouts.
- [TECH-dial-configuration](TECH-dial-configuration.md) — `DATA_DENSITY` / `VISUAL_COMPLEXITY` gate how strict the whitespace/density rules are.
- [pre-output-checklist](pre-output-checklist.md) — where the mechanical counts above run as a delivery gate.
