# Design DNA — non-negotiables derived from 175 real pieces

## Table of Contents

- [Density is the defining trait](#density-is-the-defining-trait)
- [Backgrounds are near-black](#backgrounds-are-near-black)
- [Palette is warm + cool together](#palette-is-warm--cool-together)
- [Display fonts are all-caps condensed](#display-fonts-are-all-caps-condensed)
- [Stacked Reference is the default composition](#stacked-reference-is-the-default-composition)
- [Section variety is mandatory](#section-variety-is-mandatory)
- [Arrows are load-bearing](#arrows-are-load-bearing)
- [Visible borders, not ghost borders](#visible-borders-not-ghost-borders)
- [Tight spacing inside sections](#tight-spacing-inside-sections)
- [Content format hierarchy](#content-format-hierarchy)
- [Cross-references](#cross-references)

The #1 failure mode is producing something that looks like a dark-mode SaaS landing page. Hold these rules:

## Density is the defining trait

Target 8–15 content blocks on portrait-medium (1080×1440). A "content block" is a table, chart, stat callout, bullet list, flow diagram, or callout box. Under 6 content blocks = too sparse.

## Backgrounds are near-black

Default range `#060606`–`#090909`. Lighter `#1a1a1a`–`#1d1d1d` is valid for strategy guides. Light mode is reserved for game-event / quest / bounty guides — never just because the piece is called "whitepaper".

## Palette is warm + cool together

75% of pieces use a warm + cool pairing. Defaults: amber `#E99A00` warm accent + teal `#00E88A` / blue `#29B7FF` cool complement.

## Display fonts are all-caps condensed

| Font | % of pieces | Notes |
|---|---|---|
| Bebas Neue | 43% | default |
| Teko | 13% | tokenomics, esports |
| Orbitron | 7% | tech / game |
| Press Start 2P | 5% | pixel only |
| Bungee | 3% | arcade / bold |

Body font: Montserrat. Inter as fallback.

## Stacked Reference is the default composition

70%+ of real pieces stack named sections top-to-bottom. Four other archetypes (Flow Poster, Hub & Spoke, Stat Poster, Cheat Sheet) are secondary.

## Section variety is mandatory

4+ sections must use at least 3 different component types. If 3 sections in a row are card grids, redesign one of them.

## Arrows are load-bearing

If content describes a process, economy, or flow — arrows are mandatory, always labeled (action, percentage, token name).

## Visible borders, not ghost borders

Minimum `rgba(primary, 0.25)`. `rgba(255,255,255,0.08)` is invisible and looks like a frontend component.

## Tight spacing inside sections

- Card padding 12–16px (NOT 24–32px).
- Body font 11–13px for dense content (intentional poster/print-scale exception to design-principles' 16px desktop floor — see [typography-system](../../amw-design-principles/typography-system.md) for the floor rule this skill carves out from).
- Gap 8–12px between items.
- Whitespace separates *sections* from each other, not content within a section.

## Content format hierarchy

Tables → bullet lists → flow diagrams → stat callouts → badges. Paragraphs are a last resort, reserved for 1–2 sentence hero intros.

## Cross-references

- [SKILL](../SKILL.md) — parent skill (amw-infographics)
- [style-details](../resources/style-details.md) — full design system with component CSS patterns, type playbooks, reduction-pass rules
- [layout-patterns](../resources/layout-patterns.md) — full layout and archetype scaffold library
